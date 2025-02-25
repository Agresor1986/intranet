from django.contrib.auth.signals import user_login_failed
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib import messages

@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    if request is None:
        return  # Ak nie je request dostupný, ignoruj (napr. API requesty)

    username = credentials.get("username", "Neznámy používateľ")

    # Inicializácia počítadla pokusov v session
    failed_attempts = request.session.get("failed_attempts", 0)
    failed_attempts += 1
    request.session["failed_attempts"] = failed_attempts

    # Pridanie chybovej správy pre používateľa
    messages.error(request, "Nesprávne používateľské meno alebo heslo.")

    # Ak používateľ prekročí 3 neúspešné pokusy
    if failed_attempts >= 3:
        messages.error(request, "Veľa nesprávnych pokusov. Admin bol kontaktovaný.")

        # Poslanie e-mailu adminovi
        send_mail(
            "Pokus o prihlásenie",
            f"Používateľ  '{username}' sa pokúšal neúspešne prihlásiť.",
            "stredak.michael@gmail.com",  # Nastav odosielateľa
            ["stredak.michael@gmail.com"],  # E-mail admina
            fail_silently=False,
        )

        # Resetovanie pokusov po odoslaní e-mailu
        request.session["failed_attempts"] = 0
