from django.db import models  
from django.contrib.auth.models import User  
# Definícia modelu Forum (fórum)
class Forum(models.Model):
    topic = models.CharField(max_length=300)  # Téma fóra, maximálne 300 znakov
    description = models.CharField(max_length=1000, blank=True)  # Voliteľný popis, maximálne 1000 znakov
    link = models.CharField(max_length=100, blank=True, null=True)  # Voliteľný odkaz, maximálne 100 znakov
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Prepojenie na užívateľa, ktorý vytvoril fórum
    created_at = models.DateTimeField(auto_now_add=True)  # Automatické nastavenie časového údaja pri vytvorení
    file = models.FileField(upload_to='files/', blank=True, null=True)  # Voliteľné pole pre nahrávanie súborov
    class Meta:
        verbose_name = "Diskusné fórum"  # Názov modelu v jednotnom čísle
        verbose_name_plural = "Diskusné fóra"  # Názov modelu v množnom čísle
    def __str__(self):
        return self.topic  # Vráti tému fóra ako reťazec
    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None  # Vráti názov súboru, ak existuje
# Definícia modelu Discussion (diskusia)
class Discussion(models.Model):
    forum = models.ForeignKey(Forum, null=True, blank=True, on_delete=models.CASCADE)  # Prepojenie na fórum, voliteľné
    discuss = models.CharField(max_length=1000, blank=True, null=True)  # Text diskusie
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Prepojenie na užívateľa, ktorý vytvoril diskusiu
    created_at = models.DateTimeField(auto_now_add=True)  # Automatické nastavenie časového údaja pri vytvorení
    link = models.CharField(max_length=100, blank=True, null=True)  # Voliteľný odkaz, maximálne 100 znakov
    file = models.FileField(upload_to='files/', blank=True, null=True)  # Voliteľné pole pre nahrávanie súborov
    class Meta:
        verbose_name = "Diskusia"  # Názov modelu v jednotnom čísle
        verbose_name_plural = "Diskusie"  # Názov modelu v množnom čísle
    def __str__(self):
        return f"Diskusia v {self.forum.topic} od {self.author.username}"  # Vráti reťazec reprezentujúci diskusiu
    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None  # Vráti názov súboru, ak existuje


