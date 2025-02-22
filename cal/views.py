from datetime import datetime, timedelta
import calendar
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from .forms import EventForm
from .models import Event
from .utils import Calendar
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.models import Notification
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db.models import Q
from mail.models import SentEmail
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_queryset(self):
        check_event_start_notifications()
        return Event.objects.filter(Q(user=self.request.user) | Q(is_global=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, user=self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    return f'month={prev_month.year}-{prev_month.month}'

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    return f'month={next_month.year}-{next_month.month}'

@login_required
def event(request, event_id=None):
    instance = get_object_or_404(Event, pk=event_id) if event_id else Event(user=request.user)
    view_only = instance.is_global and not request.user.is_staff

    if event_id:
        event_url = reverse('cal:event_edit', kwargs={'event_id': event_id})
        Notification.objects.filter(user=request.user, url=event_url).delete()

    if request.POST and not view_only:
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_staff and 'is_global' in request.POST:
                event.is_global = True

            if event.start_time >= event.end_time:
                messages.error(request, "Začiatok udalosti musí byť skôr ako koniec.")
                return render(request, 'event.html', {'form': form, 'view_only': view_only})

            event.user = request.user
            event.save()

            # 🔹 Klasické intranetové notifikácie – presne ako boli predtým
            if request.user.is_staff and event.is_global:
                event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})
                for user in User.objects.exclude(id=request.user.id):
                    Notification.objects.create(
                        user=user,
                        message=f'📅 Nová udalosť <strong>"{event.title}"</strong> bola pridaná!',
                        url=event_url
                    )

            return HttpResponseRedirect(reverse('cal:calendar'))
    else:
        form = EventForm(instance=instance)

    return render(request, 'event.html', {'form': form, 'view_only': view_only})

def send_event_reminder(event, reminder_type):
    subject = f"Pripomienka: {event.title}"
    
    if reminder_type == "today":
        message = f"""
Pripomienka: Dnes sa koná udalosť!

🗓 Názov: {event.title}
📅 Dátum: {event.start_time.strftime('%d.%m.%Y')}
🕒 Čas: {event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}
📖 Popis: {event.description}

Nezabudnite na ňu!
"""
    elif reminder_type == "five_minutes":
        message = f"""
Udalosť začne o 5 minút!

🗓 Názov: {event.title}
📅 Dátum: {event.start_time.strftime('%d.%m.%Y')}
🕒 Čas: {event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}
📖 Popis: {event.description}

Buďte pripravení!
"""
    else:
        return  

    recipient_list = []
    if event.is_global:
        recipient_list = User.objects.values_list('email', flat=True).exclude(email="")
    else:
        recipient_list = [event.user.email] if event.user.email else []

    for recipient in recipient_list:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
        SentEmail.objects.create(sender=event.user, recipient=recipient, subject=subject, message=message)

def check_event_start_notifications():
    now_time = now()

    # 🔹 Klasická notifikácia: Keď udalosť práve začína
    events_starting_now = Event.objects.filter(
        start_time__lte=now_time, 
        start_time__gt=now_time - timedelta(minutes=1),  # Udalosti, ktoré začali pred max 1 min
        notification_sent_today=False
    )
    for event in events_starting_now:
        event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})
        if event.is_global:
            for user in User.objects.all():
                Notification.objects.create(
                    user=user,
                    message=f'⏰ Udalosť <strong>"{event.title}"</strong> práve začína!',
                    url=event_url
                )
        else:
            Notification.objects.create(
                user=event.user,
                message=f'⏰ Vaša udalosť <strong>"{event.title}"</strong> práve začína!',
                url=event_url
            )
        event.notification_sent_today = True
        event.save()

    # 🔹 Notifikácia + e-mail: Keď udalosť začína dnes
    events_starting_today = Event.objects.filter(
        start_time__date=now_time.date(), 
        notification_sent_today=False
    )
    for event in events_starting_today:
        event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})
        Notification.objects.create(
            user=event.user,
            message=f'📅 Vaša udalosť <strong>"{event.title}"</strong> dnes začína!',
            url=event_url
        )
        send_event_reminder(event, "today")
        event.notification_sent_today = True
        event.save()

    # 🔹 E-mailová notifikácia: 5 minút pred začiatkom (opravené)
    five_minutes_from_now = now_time + timedelta(minutes=5)
    events_starting_in_five_minutes = Event.objects.filter(
        start_time__gte=five_minutes_from_now - timedelta(seconds=30),  # Presne 5 min pred štartom ±30 sekúnd
        start_time__lte=five_minutes_from_now + timedelta(seconds=30),
        notification_sent_five_minutes=False
    )
    for event in events_starting_in_five_minutes:
        send_event_reminder(event, "five_minutes")
        event.notification_sent_five_minutes = True
        event.save()

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.user != request.user:
        messages.error(request, "Nemáte oprávnenie na odstránenie tejto udalosti.")
        return HttpResponseRedirect(reverse('cal:calendar'))
    event.delete()
    return HttpResponseRedirect(reverse('cal:calendar'))
