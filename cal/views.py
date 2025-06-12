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
from django.utils.timezone import now, localtime
from django.db.models import Q
from django.contrib.auth import get_user_model
import threading
import time
import bleach
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

def create_notification(user, message, url=None):
    allowed_tags = ['strong']
    clean_message = bleach.clean(message, tags=allowed_tags, strip=True)
    safe_message = mark_safe(clean_message)
    if not Notification.objects.filter(user=user, message=safe_message, url=url).exists():
        Notification.objects.create(user=user, message=safe_message, url=url)

def send_email_notification(user, subject, message):
    """Funkcia na posielanie e-mailových upozornení."""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  
        [user.email],  
        fail_silently=False,
        html_message=message,  
    )

def check_and_send_notifications():
    while True:
        events = Event.objects.all()
        now_time = now()

        for event in events:
            if event.start_time.date() == now_time.date() and not event.notification_sent_today:
                users = User.objects.all() if event.is_global else [event.user]
                for user in users:
                    message = f'📅 {"Vaša udalosť" if user == event.user else "Udalosť"} <strong>"{event.title}"</strong> dnes začína!'
                    create_notification(user, message, url=reverse('cal:event_edit', args=[event.id]))

                if event.is_global:
                    for user in User.objects.all():
                        local_start_time = localtime(event.start_time).strftime("%H:%M")
                        email_subject = f'Udalosť "{event.title}" začína dnes'
                        email_message = f'''
                            <h2>Udalosť "{event.title}" začína dnes!</h2>
                            <p><strong>Čas začiatku:</strong> {local_start_time}</p>
                            <p><strong>Popis udalosti:</strong> {event.description}</p>
                            <p>Pre viac informácií navštívte <a href="{settings.BASE_URL}{reverse('cal:event_edit', args=[event.id])}">tento odkaz</a>.</p>
                        '''
                        send_email_notification(user, email_subject, email_message)

                event.notification_sent_today = True
                event.save()

            if event.start_time <= now_time and not event.notification_sent_now:
                users = User.objects.all() if event.is_global else [event.user]
                for user in users:
                    message = f'📅 {"Vaša udalosť" if user == event.user else "Udalosť"} <strong>"{event.title}"</strong> teraz začína!'
                    create_notification(user, message, url=reverse('cal:event_edit', args=[event.id]))

                if event.is_global:
                    for user in User.objects.all():
                        local_start_time = localtime(event.start_time).strftime("%H:%M")
                        email_subject = f'Udalosť "{event.title}" teraz začína'
                        email_message = f'''
                            <h2>Udalosť "{event.title}" teraz začína!</h2>
                            <p><strong>Čas začiatku:</strong> {local_start_time}</p>
                            <p><strong>Popis udalosti:</strong> {event.description}</p>
                            <p>Pre viac informácií navštívte <a href="{settings.BASE_URL}{reverse('cal:event_edit', args=[event.id])}">tento odkaz</a>.</p>
                        '''
                        send_email_notification(user, email_subject, email_message)

                event.notification_sent_now = True
                event.save()

            if event.start_time - now_time <= timedelta(minutes=5) and not event.notification_sent_5_min:
                if event.is_global:
                    for user in User.objects.all():
                        local_start_time = localtime(event.start_time).strftime("%H:%M")
                        email_subject = f'Udalosť "{event.title}" začína o 5 minút'
                        email_message = f'''
                            <h2>Udalosť "{event.title}" začína o 5 minút!</h2>
                            <p><strong>Čas začiatku:</strong> {local_start_time}</p>
                            <p><strong>Popis udalosti:</strong> {event.description}</p>
                            <p>Pre viac informácií navštívte <a href="{settings.BASE_URL}{reverse('cal:event_edit', args=[event.id])}">tento odkaz</a>.</p>
                        '''
                        send_email_notification(user, email_subject, email_message)

                    event.notification_sent_5_min = True
                    event.save()

        time.sleep(30)  

def start_notification_checker():
    thread = threading.Thread(target=check_and_send_notifications)
    thread.daemon = True
    thread.start()

start_notification_checker()

class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_queryset(self):
        return Event.objects.filter(Q(user=self.request.user) | Q(is_global=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, user=self.request.user)
        context['calendar'] = mark_safe(cal.formatmonth(withyear=True))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime(year, month, 1)
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

    event_url = reverse('cal:event_edit', kwargs={'event_id': instance.id}) if instance.id else None

    if event_id:
        Notification.objects.filter(user=request.user, url=event_url).delete()

    if request.POST and not view_only:
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_staff and 'is_global' in request.POST:
                event.is_global = True

            if event.start_time >= event.end_time:
                messages.error(request, "Začiatok udalosti musí byť skorej ako koniec.")
                return render(request, 'event.html', {'form': form, 'view_only': view_only})
            
            event.user = request.user
            event.save()

            event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})

            if request.user.is_staff and event.is_global:
                for user in User.objects.exclude(id=request.user.id):
                    create_notification(
                        user,
                        f'📅 Bola vytvorená nová udalosť: <strong>"{event.title}"</strong>',
                        url=event_url
                    )
                event.notification_sent_created = True
                event.save()
            elif not event.is_global:
                event.notification_sent_created = True
                event.save()

            return HttpResponseRedirect(reverse('cal:calendar'))
    else:
        form = EventForm(instance=instance)

    return render(request, 'event.html', {'form': form, 'view_only': view_only})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.user != request.user:
        messages.error(request, "Nemáte oprávnenie na odstránenie tejto udalosti.")
        return HttpResponseRedirect(reverse('cal:calendar'))
    event.delete()
    return HttpResponseRedirect(reverse('cal:calendar'))
