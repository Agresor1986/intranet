from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, PrivateConversation, PrivateMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from notifications.models import Notification
import re
import bleach

def convert_urls_to_links(text):
    if not text:
        return ""
    text = bleach.clean(text)
    url_pattern = r'(https?://[^\s]+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)

def create_notification(user, message, url=None):
    Notification.objects.create(user=user, message=message, url=url)

@login_required
def chat(request):
    messages = Message.objects.all().order_by("timestamp")
    users = User.objects.exclude(username=request.user.username)
    Notification.objects.filter(user=request.user, url="/chat/").delete()

    for message in messages:
        message.content = convert_urls_to_links(message.content)

    if request.method == "POST":
        content = request.POST.get("content")
        file = request.FILES.get("file")

        if not content and not file:
            return redirect("chat")

        Message.objects.create(user=request.user, content=content, file=file)

        for user in users:
            create_notification(user=user, message=f"💬 <strong>{request.user.username}</strong> poslal správu do skupinového chatu.", url="/chat/")

        return redirect("chat")

    return render(request, "chat.html", {"messages": messages, "chat_type": "group", "users": users})

@login_required
def private_chat(request, username):
    user2 = get_object_or_404(User, username=username)
    conversation = PrivateConversation.get_conversation(request.user, user2)

    if not conversation:
        conversation = PrivateConversation.objects.create(user1=min(request.user, user2, key=lambda x: x.pk), 
                                                          user2=max(request.user, user2, key=lambda x: x.pk))

    Notification.objects.filter(user=request.user, url=f"/chat/private/{username}/").delete()

    messages = PrivateMessage.objects.filter(conversation=conversation).order_by("timestamp")
    users = User.objects.exclude(username=request.user.username)

    for message in messages:
        message.content = convert_urls_to_links(message.content)

    if request.method == "POST":
        content = request.POST.get("content")
        file = request.FILES.get("file")

        if not content and not file:
            return redirect("private_chat", username=username)

        PrivateMessage.objects.create(conversation=conversation, sender=request.user, content=content, file=file)

        create_notification(user=user2, message=f"💬 <strong>{request.user.username}</strong> Vám poslal správu.", url=f"/chat/private/{request.user.username}/")

        return redirect("private_chat", username=username)

    return render(request, "chat.html", {"messages": messages, "chat_type": "private", "other_user": user2, "users": users})
