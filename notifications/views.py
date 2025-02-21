from django.shortcuts import render, redirect, get_object_or_404 
from .models import Notification  # Importovanie modelu Notification 
from django.contrib.auth.decorators import login_required
# Funkcia na zobrazenie notifikácií, ktoré používateľ ešte neprečítal
@login_required  
def view_notifications(request):
    # Získanie všetkých neprečítaných notifikácií pre prihláseného používateľa, zoradených podľa času (od najnovších)
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')
    # Vykreslenie šablóny 'home.html' a odoslanie notifikácií do kontextu šablóny
    return render(request, 'home.html', {"notifications": notifications})
# Funkcia na označenie konkrétnej notifikácie ako prečítanej
@login_required  
def mark_as_read(request, notification_id):
    # Získanie konkrétnej notifikácie podľa ID, ktorá patrí prihlásenému používateľovi
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True # Zmena stavu notifikácie na prečítanú
    notification.save() # Uloženie zmien do databázy
    return redirect('notifications') # Presmerovanie používateľa späť na stránku s notifikáciami
# Funkcia na označenie všetkých neprečítaných notifikácií ako prečítaných
@login_required  
def mark_all_as_read(request):
    # Aktualizácia všetkých neprečítaných notifikácií pre prihláseného používateľa na prečítané
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications') # Presmerovanie používateľa späť na stránku s notifikáciami


