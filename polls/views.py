from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Poll, Choice, Vote  # Zmenené z forum.models na PollApp.models
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
import threading
import time
import bleach
from django.utils.safestring import mark_safe

def create_notification(user, message, url=None):
    allowed_tags = ['strong']
    clean_message = bleach.clean(message, tags=allowed_tags, strip=True)
    safe_message = mark_safe(clean_message)
    if not Notification.objects.filter(user=user, message=safe_message, url=url).exists():
        Notification.objects.create(user=user, message=safe_message, url=url)

def check_and_send_notifications():
    while True:
        polls = Poll.objects.all()
        now = timezone.now()

        for poll in polls:
            if not poll.is_active() and not poll.notified_closed:
                users = User.objects.all()
                for user in users:
                    create_notification(
                        user,
                        f'📊 Hlasovanie v ankete <strong>"{poll.name}"</strong> bolo ukončené.',
                        url=reverse('PollApp:poll', args=[poll.id])
                    )
                poll.notified_closed = True
                poll.save(update_fields=['notified_closed'])

            if poll.is_active() and poll.end_date and (poll.end_date - now).total_seconds() <= 300:
                users = User.objects.all()
                for user in users:
                    if not Notification.objects.filter(
                        user=user,
                        message=f'📊 Hlasovanie v ankete <strong>"{poll.name}"</strong> skončí o 5 minút.',
                        url=reverse('PollApp:poll', args=[poll.id])
                    ).exists():
                        create_notification(
                            user,
                            f'📊 Hlasovanie v ankete <strong>"{poll.name}"</strong> skončí o 5 minút.',
                            url=reverse('PollApp:poll', args=[poll.id])
                        )
        
        time.sleep(60)

def start_notification_checker():
    thread = threading.Thread(target=check_and_send_notifications)
    thread.daemon = True
    thread.start()

start_notification_checker()

class HomeView(View):
    def get(self, request):
        polls = Poll.objects.prefetch_related('choices').order_by('-timestamp')

        for poll in polls:
            total_votes = sum(choice.votes.count() for choice in poll.choices.all())
            poll.total_votes = total_votes

        return render(request, "polls.html", {"polls": polls})

class PollView(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        user_vote = None

        if request.user.is_authenticated:
            user_vote = Vote.objects.filter(poll=poll, user=request.user).first()
            Notification.objects.filter(
                user=request.user,
                url=reverse('PollApp:poll', args=[poll.id])
            ).delete()

        poll_results = [[choice.name, choice.votes.count()] for choice in poll.choices.all()]

        return render(request, "poll.html", {
            "poll": poll,
            "user_vote": user_vote,
            "poll_results": poll_results,
            "is_active": poll.is_active()
        })

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)

        if not poll.is_active():
            poll_results = [[choice.name, choice.votes.count()] for choice in poll.choices.all()]
            return render(request, "poll.html", {
                "poll": poll,
                "error_message": "Hlasovanie bolo ukončené.",
                "poll_results": poll_results
            })

        choice_id = request.POST.get('choice_id')

        if not choice_id:
            poll_results = [[choice.name, choice.votes.count()] for choice in poll.choices.all()]
            return render(request, "poll.html", {
                "poll": poll,
                "error_message": "Musíte vybrať možnosť, aby ste mohli hlasovať.",
                "poll_results": poll_results,
                "is_active": poll.is_active()
            })

        if not request.user.is_authenticated:
            return render(request, "poll.html", {
                "poll": poll,
                "error_message": "Musíte byť prihlásený, aby ste mohli hlasovať."
            })

        choice = get_object_or_404(Choice, id=choice_id)
        existing_vote = Vote.objects.filter(poll=poll, user=request.user).first()

        if existing_vote:
            existing_vote.choice = choice
            existing_vote.save()
            success_message = "Váš hlas bol aktualizovaný."
        else:
            Vote.objects.create(poll=poll, choice=choice, user=request.user)
            success_message = "Váš hlas bol zaznamenaný."

        poll_results = [[choice.name, choice.votes.count()] for choice in poll.choices.all()]

        return render(request, "poll.html", {
            "poll": poll,
            "success_message": success_message,
            "poll_results": poll_results,
            "is_active": poll.is_active()
        })

@method_decorator(login_required, name='dispatch')
class CreatePollView(View):
    def get(self, request):
        if not request.user.is_superuser and not request.user.groups.filter(name='manazer').exists():
            return render(request, "polls.html", {"error_message": "Nemáte oprávnenie na vytváranie ankiet."})
        
        return render(request, "create_polls.html")

    def post(self, request):
        if not request.user.is_superuser and not request.user.groups.filter(name='manazer').exists():
            return render(request, "polls.html", {"error_message": "Nemáte oprávnenie na vytváranie ankiet."})

        poll_name = request.POST.get("poll_name")
        poll_description = request.POST.get("poll_description")
        choice_names = request.POST.getlist("choices")
        end_date = request.POST.get("end_date")

        if end_date:
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
            
            if end_date <= timezone.now():
                return render(request, "create_polls.html", {
                    "error_message": "Dátum ukončenia musí byť v budúcnosti.",
                    "poll_name": poll_name,
                    "poll_description": poll_description,
                    "choices": choice_names,
                })

        choice_names = list(filter(None, map(str.strip, choice_names)))

        if len(choice_names) < 2:
            return render(request, "create_polls.html", {
                "error_message": "Musíte zadať aspoň dve možnosti!",
                "poll_name": poll_name,
                "poll_description": poll_description,
                "choices": choice_names,
            })

        poll = Poll.objects.create(
            name=poll_name,
            description=poll_description,
            end_date=end_date,
            created_by=request.user
        )

        choices = [Choice.objects.create(name=name) for name in choice_names]
        poll.choices.set(choices)

        users = User.objects.exclude(id=request.user.id)
        for user in users:
            create_notification(
                user,
                f'📊 Bola vytvorená nová anketa: <strong>"{poll_name}"</strong>',
                url=reverse('PollApp:poll', args=[poll.id])
            )

        return render(request, "create_polls.html", {
            "poll": poll,
            "success_message": "Anketa bola vytvorená!",
        })
