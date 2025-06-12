from django.shortcuts import render, redirect, get_object_or_404 
from .models import Notification  
from django.contrib.auth.decorators import login_required

@login_required  
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')
    return render(request, 'home.html', {"notifications": notifications})

@login_required  
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True 
    notification.save() 
    return redirect('notifications')
    
@login_required  
def mark_all_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications')


