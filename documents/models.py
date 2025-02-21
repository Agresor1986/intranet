import os  # Modul na prácu so súbormi a cestami v operačnom systéme
from django.db import models  # Importuje Django ORM na definovanie databázových modelov
from django.contrib.auth.models import User  # Importuje zabudovaný model používateľa
# Definuje model Document, ktorý predstavuje dokumenty nahrané používateľmi
class Document(models.Model):
    # Reťazcové pole s maximálnou dĺžkou 200 znakov, slúži ako názov dokumentu
    title = models.CharField(max_length=200)
    # Pole na nahrávanie súborov, súbory sa ukladajú do priečinka 'files/'
    file = models.FileField(upload_to='files/')
    # Automaticky nastaví dátum a čas nahrania pri vytvorení záznamu
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Vytvára vzťah k modelu User; ak sa používateľ vymaže, vymažú sa aj jeho dokumenty
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    # Metóda na odstránenie dokumentu aj so súborom zo servera
    def delete(self, *args, **kwargs):
        if self.file:  # Overí, či model obsahuje súbor
            if os.path.isfile(self.file.path):  # Skontroluje, či súbor existuje v systéme
                os.remove(self.file.path)  # Odstráni fyzický súbor z disku
        super().delete(*args, **kwargs)  # Zavolá pôvodnú metódu delete, ktorá odstráni objekt z databázy
    # Metóda, ktorá určuje, ako sa objekt bude zobrazovať ako textová reprezentácia
    def __str__(self):
        return self.title  # Vracia názov dokumentu ako textovú reprezentáciu objektu



