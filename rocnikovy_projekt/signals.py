from django.contrib.auth.signals import user_login_failed
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib import messages
from django.conf import settings

@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    if request is None:
        return 

    username = credentials.get("username", "Neznámy používateľ")

    failed_attempts = request.session.get("failed_attempts", 0)
    failed_attempts += 1
    request.session["failed_attempts"] = failed_attempts


    if failed_attempts >= 3:
        messages.error(request, "Veľa nesprávnych pokusov. Admin bol kontaktovaný.")

        
        send_mail(
            "Pokus o prihlásenie",
            f"Používateľ  '{username}' sa pokúšal neúspešne prihlásiť.",
            settings.DEFAULT_FROM_EMAIL,  
            [settings.DEFAULT_FROM_EMAIL],  
            fail_silently=False,
        )

        
        request.session["failed_attempts"] = 0
    else:
       
        messages.error(request, "Nesprávne používateľské meno alebo heslo.")
