from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self, request):
        polls = Poll.objects.prefetch_related('choices').order_by('-timestamp')

        for poll in polls:
            total_votes = 0
            for choice in poll.choices.all():
                choice.vote_count = Vote.objects.filter(choice=choice).count()
                total_votes += choice.vote_count
            poll.total_votes = total_votes

        return render(request, "polls.html", {"polls": polls})

class PollView(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        user_vote = None

        if request.user.is_authenticated:
            user_vote = Vote.objects.filter(poll=poll, user=request.user).first()
            Notification.objects.filter(user=request.user, url=f"/polls/poll/{poll.id}/").delete()

        return render(request, "poll.html", {"poll": poll, "user_vote": user_vote})

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        choice_id = request.POST.get('choice_id')

        if not request.user.is_authenticated:
            return render(request, "poll.html", {"poll": poll, "error_message": "You must be logged in to vote."})

        choice = get_object_or_404(Choice, id=choice_id)
        existing_vote = Vote.objects.filter(poll=poll, user=request.user).first()

        if existing_vote:
            existing_vote.choice = choice
            existing_vote.save()
            success_message = "Váš hlas bol pridaný."
        else:
            Vote.objects.create(poll=poll, choice=choice, user=request.user)
            success_message = "Váš hlas bol zaznamenaný."

        poll_results = [[choice.name, Vote.objects.filter(poll=poll, choice=choice).count()] for choice in poll.choices.all()]

        return render(request, "poll.html", {"poll": poll, "success_message": success_message, "poll_results": poll_results})

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

        # Odstránenie prázdnych hodnôt
        choice_names = list(filter(None, map(str.strip, choice_names)))

        # Debugging - pozrieme sa, čo sa skutočne spracováva
        print("Filtered choices:", choice_names)

        # Kontrola, či sú aspoň dve možnosti
        if len(choice_names) < 2:
            return render(request, "create_polls.html", {"error_message": "Musíte zadať aspoň dve možnosti!"})

        # Vytvorenie ankety
        poll = Poll.objects.create(name=poll_name, description=poll_description)

        # Vytvorenie a pridanie možností
        choices = [Choice.objects.create(name=name) for name in choice_names]
        poll.choices.set(choices)

        return render(request, "create_polls.html", {"poll": poll, "success_message": "Anketa bola vytvorená!"})
