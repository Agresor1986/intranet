from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from .models import Event
from django.utils.timezone import now, localtime
from django.db.models import Q

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def formatweekheader(self):
        days = ['Po', 'Ut', 'St', 'Št', 'Pi', 'So', 'Ne']
        return '<tr> ' + ''.join(['<th class="%s">%s</th>' % (self.cssclasses[i], day) for i, day in enumerate(days)]) + ' </tr>'

    def formatmonthname(self, theyear, themonth, withyear=True):
        months = [
            'Január', 'Február', 'Marec', 'Apríl', 'Máj', 'Jún',
            'Júl', 'August', 'September', 'Október', 'November', 'December'
        ]
        s = '%s %s' % (months[themonth - 1], theyear)
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def formatday(self, day, events):
        events_per_day = events.filter(
            start_time__day__lte=day,
            end_time__day__gte=day
        ).filter(Q(user=self.user) | Q(is_global=True))
        d = ''
        for event in events_per_day:
            now_local = localtime(now()).timestamp()
            event_end_timestamp = event.end_time.timestamp()
            if event_end_timestamp < now_local:
                d += f'<li style="background-color: black; ' \
                     f'width: 90%; padding: 4px; border-radius: 5px; ' \
                     f'margin-left: 3px; margin-top: 2px; text-align: center;">' \
                     f'<a>{event.get_html_url}</a></li>'
            else:
                d += f'<li style="background-color: {event.color}; ' \
                     f'width: 90%; padding: 4px; border-radius: 5px; ' \
                     f'margin-left: 3px; margin-top: 2px; text-align: center;">' \
                     f'<a>{event.get_html_url}</a></li>'
        today = date.today()
        is_today = day == today.day and self.month == today.month and self.year == today.year
        highlight = 'style="background-color: #ccd0d9; color: #000; font-weight: bold;"' if is_today else ''
        if day != 0:
            return f"<td {highlight}><span class='date'>{day}</span>{d}</td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(
            start_time__year=self.year,
            start_time__month=self.month
        ).filter(Q(user=self.user) | Q(is_global=True)) | Event.objects.filter(
            end_time__year=self.year,
            end_time__month=self.month
        ).filter(Q(user=self.user) | Q(is_global=True))
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}'
        cal += f'{self.formatweekheader()}'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}'
        return cal
