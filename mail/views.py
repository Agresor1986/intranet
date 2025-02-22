from django.core.mail import EmailMessage
from django.shortcuts import render
from .models import SentEmail

def send_mail_page(request):
    result = None  # Výsledok operácie
    if request.method == 'POST':
        address = request.POST.get('address')  # Príjemca
        subject = request.POST.get('subject', '').strip()  # Predmet
        message = request.POST.get('message')  # Správa
        file = request.FILES.get('file')  # Súbor (ak je pripojený)

        if address and message:  # Predmet už nemusí byť kontrolovaný
            try:
                user_email = request.user.email  # Používateľský e-mail
                if not subject:  # Ak je predmet prázdny, nastaví sa predvolená hodnota
                    subject = f"Od: {user_email}"

                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email='stredak.michael@gmail.com',
                    to=[address],
                    reply_to=[user_email],
                )

                if file:
                    email.attach(file.name, file.read(), file.content_type)

                email.send(fail_silently=False)

                SentEmail.objects.create(
                    sender=request.user,
                    recipient=address,
                    subject=subject,
                    message=message,
                    file=file if file else None,  # Uloženie súboru iba ak existuje
                )
                result = 'Email bol poslaný!'
            except Exception as e:
                result = f'Chyba pri posielaní mailu: {e}'
        else:
            result = 'Všetky polia sú povinné.'

    return render(request, "mail.html", {'result': result})

