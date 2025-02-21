from datetime import datetime, timedelta, date  # Import potrebných modulov pre prácu s dátumom a časom
from calendar import HTMLCalendar  # Import triedy HTMLCalendar pre generovanie kalendára
from .models import Event  # Import modelu Event z aktuálnej aplikácie
from django.utils.timezone import now, localtime  # Import funkcií pre prácu s časovými pásmami
from django.db.models import Q  # Import pre OR filtrovanie v Django querysetoch
# Definícia vlastného kalendára dedičného od HTMLCalendar
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year  # Nastavenie roku pre kalendár
        self.month = month  # Nastavenie mesiaca pre kalendár
        self.user = user  # Pridanie používateľa pre filtrovanie udalostí
        super(Calendar, self).__init__()  # Volanie konštruktora rodičovskej triedy
    # Metóda na formátovanie dňa ako bunky tabuľky (td)
    def formatday(self, day, events):
        # Filtrovanie udalostí pre daný deň: udalosti používateľa + globálne udalosti
        events_per_day = events.filter(
            start_time__day__lte=day,  # Udalosti, ktoré začali pred alebo v daný deň
            end_time__day__gte=day  # Udalosti, ktoré skončili po alebo v daný deň
        ).filter(Q(user=self.user) | Q(is_global=True))  # Filtrovanie podľa používateľa alebo globálnych udalostí
        d = ''  # Inicializácia reťazca pre zoznam udalostí
        for event in events_per_day:
            now_local = localtime(now()).timestamp()  # Aktuálny čas v lokálnom časovom pásme
            event_end_timestamp = event.end_time.timestamp()  # Čas ukončenia udalosti
            if event_end_timestamp < now_local:
                # Ak udalosť už skončila, zobrazí sa s čiernym pozadím
                d += f'<li style="background-color: black; ' \
                     f'width: 90%; padding: 4px; border-radius: 5px; ' \
                     f'margin-left: 3px; margin-top: 2px; text-align: center;">' \
                     f'<a>{event.get_html_url}</a></li>'
            else:
                # Ak udalosť ešte neskončila, zobrazí sa s farbou udalosti
                d += f'<li style="background-color: {event.color}; ' \
                     f'width: 90%; padding: 4px; border-radius: 5px; ' \
                     f'margin-left: 3px; margin-top: 2px; text-align: center;">' \
                     f'<a>{event.get_html_url}</a></li>'
        today = date.today()  # Získanie dnešného dátumu
        # Kontrola, či je daný deň dnešný deň
        is_today = day == today.day and self.month == today.month and self.year == today.year
        # Zvýraznenie dnešného dňa v kalendári
        highlight = 'style="background-color: #ccd0d9; color: #000; font-weight: bold;"' if is_today else ''
        if day != 0:
            # Ak deň nie je 0 (prázdny deň), vráti sa bunka s dátumom a udalosťami
            return f"<td {highlight}><span class='date'>{day}</span>{d}</td>"
        return '<td></td>'  # Vráti prázdnu bunku pre neexistujúce dni
    # Metóda na formátovanie týždňa ako riadku tabuľky (tr)
    def formatweek(self, theweek, events):
        week = ''  # Inicializácia reťazca pre týždeň
        for d, weekday in theweek:
            week += self.formatday(d, events)  # Pridanie formátovaného dňa do týždňa
        return f'<tr> {week} </tr>'  # Vrátenie formátovaného týždňa
    # Metóda na formátovanie celého mesiaca ako tabuľky
    def formatmonth(self, withyear=True):
        # Filtrovanie udalostí pre daný mesiac: vlastné udalosti + globálne udalosti
        events = Event.objects.filter(
            start_time__year=self.year,  # Udalosti, ktoré začali v danom roku
            start_time__month=self.month  # Udalosti, ktoré začali v danom mesiaci
        ).filter(Q(user=self.user) | Q(is_global=True)) | Event.objects.filter(
            end_time__year=self.year,  # Udalosti, ktoré skončili v danom roku
            end_time__month=self.month  # Udalosti, ktoré skončili v danom mesiaci
        ).filter(Q(user=self.user) | Q(is_global=True))
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">'  # Začiatok tabuľky kalendára
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}'  # Pridanie názvu mesiaca
        cal += f'{self.formatweekheader()}'  # Pridanie hlavičky týždňa
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}'  # Pridanie formátovaných týždňov do kalendára
        return cal  # Vrátenie kompletného kalendára
