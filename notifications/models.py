from django.db import models # Importovanie potrebných modulov pre model
from django.contrib.auth.models import User  # Importovanie základného modelu pre používateľov
# Definícia modelu Notification, ktorý reprezentuje notifikácie (oznámenia)
class Notification(models.Model):
    # Cudzí kľúč na používateľa (každá notifikácia patrí konkrétnemu používateľovi)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField() # Textová správa, ktorá sa zobrazí v notifikácii
    # Odkaz na akciu, ktorá bude vykonaná po kliknutí na notifikáciu (môže byť prázdny)
    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False) # Pole určujúce, či bola notifikácia už prečítaná
    timestamp = models.DateTimeField(auto_now_add=True) # Čas vytvorenia notifikácie


