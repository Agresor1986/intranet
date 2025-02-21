from .models import Notification # Importovanie modelu Notification
# Funkcia na vytvorenie novej notifikácie
def create_notification(user, message, url=None):
    # Vytvorenie novej notifikácie v databáze pre konkrétneho používateľa
    Notification.objects.create(user=user, message=message, url=url)


