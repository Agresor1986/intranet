from .models import Notification 

def create_notification(user, message, url=None):
    Notification.objects.create(user=user, message=message, url=url)


