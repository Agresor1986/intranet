from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Forum, Discussion
from .forms import CreateInForum, CreateInDiscussion
from notifications.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def create_notification(user, message, url=None):
    Notification.objects.create(user=user, message=message, url=url)

@login_required
def forums(request):
    forums = Forum.objects.prefetch_related('discussion_set').order_by('-created_at')
    show_all_forum_id = request.GET.get('show_all_forum_id', None)
    count = forums.count()
    forum_data = []

    for forum_instance in forums:
        forum_discussions = forum_instance.discussion_set.select_related('author').order_by('-created_at')
        if not (show_all_forum_id and str(forum_instance.id) == show_all_forum_id):
            forum_discussions = forum_discussions[:3]

        forum_data.append({
            'forum': forum_instance,
            'discussions': forum_discussions,
            'show_all': show_all_forum_id and str(forum_instance.id) == show_all_forum_id
        })

    Notification.objects.filter(user=request.user, url=reverse('forum')).delete()

    return render(request, 'forum.html', {'forum_data': forum_data, 'count': count})

@login_required
def addInForum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST, request.FILES)
        if form.is_valid():
            forum_instance = form.save(commit=False)
            forum_instance.author = request.user
            forum_instance.save()

            for user in User.objects.exclude(id=request.user.id):
                create_notification(
                    user, 
                    f'📝 Bolo vytvorené nové diskusné fórum: <strong>"{forum_instance.topic}"</strong>', 
                    url=reverse('forum')
                )

            return redirect('forum')

    return render(request, 'addInForum.html', {'form': form})

@login_required
def addInDiscussion(request, forum_id):
    forum_instance = get_object_or_404(Forum, id=forum_id)
    Notification.objects.filter(user=request.user, url=reverse('forum')).delete()

    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST, request.FILES)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.forum = forum_instance
            discussion.author = request.user
            discussion.save()

            for user in User.objects.exclude(id=request.user.id):
                create_notification(
                    user, 
                    f'📝 Bol pridaný nový komentár do fóra: <strong>"{forum_instance.topic}"</strong>', 
                    url=reverse('forum')
                )

            return redirect('forum')

    return render(request, 'addInDiscussion.html', {'form': form, 'forum': forum_instance})
