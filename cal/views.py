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
from django.db.models import Q
from django.contrib.auth import get_user_model
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
        context['calendar'] = mark_safe(cal.formatmonth(withyear=True))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

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
                messages.error(request, "Začiatok udalosti musí byť skorej ako koniec.")
                return render(request, 'event.html', {'form': form, 'view_only': view_only})
            event.user = request.user
            event.save()

            if request.user.is_staff and event.is_global:
                event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})
                for user in User.objects.exclude(id=request.user.id):
                    Notification.objects.create(
                        user=user,
                        message=f'Nová udalosť <strong>"{event.title}"</strong> bola pridaná!',
                        url=event_url
                    )

            return HttpResponseRedirect(reverse('cal:calendar'))
    else:
        form = EventForm(instance=instance)

    return render(request, 'event.html', {'form': form, 'view_only': view_only})

def check_event_start_notifications():
    now_time = now()
    
    # Notifikácia pre udalosti začínajúce dnes
    events_starting_today = Event.objects.filter(
        start_time__date=now_time.date()
    )
    for event in events_starting_today:
        event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})
        message = f'Dôležitá udalosť "{event.title}" dnes začína!'
        if event.is_global:
            users = User.objects.all()
        else:
            users = [event.user]
        for user in users:
            Notification.objects.create(user=user, message=message, url=event_url)
            send_mail(
                subject='Pripomienka: Udalosť dnes začína',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
    
    # Notifikácia 5 minút pred začiatkom udalosti
    events_starting_soon = Event.objects.filter(
        start_time__lte=now_time + timedelta(minutes=5),
        start_time__gte=now_time
    )
    for event in events_starting_soon:
        event_url = reverse('cal:event_edit', kwargs={'event_id': event.id})
        message = f'Dôležitá udalosť "{event.title}" začne o 5 minút!'
        if event.is_global:
            users = User.objects.all()
        else:
            users = [event.user]
        for user in users:
            Notification.objects.create(user=user, message=message, url=event_url)
            send_mail(
                subject='Udalosť začne o 5 minút',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.user != request.user:
        messages.error(request, "You are not authorized to delete this event.")
        return HttpResponseRedirect(reverse('cal:calendar'))
    event.delete()
    return HttpResponseRedirect(reverse('cal:calendar'))

