from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote
from notifications.models import Notification  # Import modelu Notification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self, request):
        polls = Poll.objects.prefetch_related('choices').order_by('-timestamp')

        # Pridanie počtu hlasov pre každú možnosť a celkového počtu hlasov pre anketu
        for poll in polls:
            total_votes = 0
            for choice in poll.choices.all():
                choice.vote_count = Vote.objects.filter(choice=choice).count()
                total_votes += choice.vote_count
            poll.total_votes = total_votes  # Celkový počet hlasov

        return render(request, "polls.html", {"polls": polls})

class PollView(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        user_vote = None

        # Skontrolujte, či už užívateľ hlasoval
        if request.user.is_authenticated:
            user_vote = Vote.objects.filter(poll=poll, user=request.user).first()

            # Vymaž notifikáciu pre túto anketu
            Notification.objects.filter(
                user=request.user, 
                url=f"/polls/poll/{poll.id}/"
            ).delete()

        return render(
            request,
            template_name="poll.html",
            context={"poll": poll, "user_vote": user_vote}
        )

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        choice_id = request.POST.get('choice_id')

        if not request.user.is_authenticated:
            return render(
                request,
                template_name="poll.html",
                context={"poll": poll, "error_message": "You must be logged in to vote."}
            )

        # Nájdite zvolenú odpoveď
        choice = get_object_or_404(Choice, id=choice_id)

        # Skontrolujte, či už užívateľ hlasoval
        existing_vote = Vote.objects.filter(poll=poll, user=request.user).first()

        if existing_vote:
            # Aktualizácia hlasu
            existing_vote.choice = choice
            existing_vote.save()
            success_message = "Váš hlas bol pridaný."
        else:
            # Vytvorenie nového hlasu
            Vote.objects.create(poll=poll, choice=choice, user=request.user)
            success_message = "Váš hlas bol zaznamenaný."

        # Získajte výsledky ankety
        poll_results = [
            [choice.name, Vote.objects.filter(poll=poll, choice=choice).count()]
            for choice in poll.choices.all()
        ]

        return render(
            request,
            template_name="poll.html",
            context={
                "poll": poll,
                "success_message": success_message,
                "poll_results": poll_results
            }
        )

@method_decorator(login_required, name='dispatch')
class CreatePollView(View):
    def get(self, request):
        # Skontrolujeme, či užívateľ patrí do skupiny 'manazer' alebo je superuser
        if not request.user.is_superuser and not request.user.groups.filter(name='manazer').exists():
            return render(request, "polls.html", {"error_message": "Nemáte oprávnenie na vytváranie ankiet."})
        
        return render(request, "create_polls.html")

    def post(self, request):
        # Overenie oprávnenia ako pri GET
        if not request.user.is_superuser and not request.user.groups.filter(name='manazer').exists():
            return render(request, "polls.html", {"error_message": "Nemáte oprávnenie na vytváranie ankiet."})
        
        # Získanie údajov z formulára
        poll_name = request.POST.get('poll_name')
        poll_description = request.POST.get('poll_description')
        choice_names = request.POST.getlist('choices')  # Predpokladáme, že tu sa zbierajú názvy možností

        # Vytvorenie ankety
        poll = Poll.objects.create(name=poll_name, description=poll_description)

        # Pridanie možností k ankete
        for choice_name in choice_names:
            choice = Choice.objects.create(name=choice_name)
            poll.choices.add(choice)

        # Vytvorenie notifikácií pre všetkých používateľov okrem autora ankety
        users = User.objects.exclude(id=request.user.id)  # Vylúčenie autora ankety
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"Nová anketa {poll.name} bola vytvorená!",
                url=f"/polls/poll/{poll.id}/",
                is_read=False
            )

        return render(request, "create_polls.html", {"poll": poll, "success_message": "Anketa bola vytvorená!"})
