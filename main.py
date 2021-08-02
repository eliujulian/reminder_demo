import datetime
import calendar

INTERVAL = ((1, 'täglich'), (2, 'wöchentlich'), (3, 'monatlich'))

DAYS = (
    (1, 'Montag'),
    (2, 'Dienstag'),
    (3, 'Mittwoch'),
    (4, 'Donnerstag'),
    (5, 'Freitag'),
    (6, 'Samstag'),
    (7, 'Sonntag')
)

DAY_OF_MONTH = (
    (1, '1.'), (2, '2.'), (3, '3.'), (4, '4.'), (5, '5.'), (6, '6.'), (7, '7.'), (8, '8.'), (9, '9.'), (10, '10.'),
    (11, '11.'), (12, '12.'), (13, '13.'), (14, '14.'), (15, '15.'), (16, '16.'), (17, '17.'), (18, '18.'),
    (19, '19.'), (20, '20.'), (21, '21.'), (22, '22.'), (23, '23.'), (24, '24.'), (25, '25.'), (26, '26.'),
    (27, '27.'), (28, '28.'), (29, '29.'), (30, '30.'), (31, '31.'),

    (40, '1. Montag im Monat'),
    (41, '1. Dienstag im Monat'),
    (42, '1. Mittwoch im Monat'),
    (43, '1. Donnerstag im Monat'),
    (44, '1. Freitag im Monat'),
    (45, '1. Samstag im Monat'),
    (46, '1. Sonntag im Monat'),

    (50, '1. Werktag im Monat'),
    (51, '2. Werktag im Monat'),
    (52, '3. Werktag im Monat'),

    (60, 'Letzter Tag im Monat'),
    (61, 'Vorletzter Tag im Monat'),
    (62, 'Drittletzter Tag im Monat'),

    (70, 'Letzter Werktag im Monat'),
    (71, 'Vorletzter Werktag im Monat'),
    (72, 'Drittletzter Werktag im Monat'),
)


class Reminder:

    def __init__(self,
                 title: str,
                 recipient: str,
                 subject: str,
                 message: str,
                 interval: int,
                 skip_weekend: bool,
                 skip_weeksdays: bool,
                 day_of_week: int,
                 day_of_month: int,
                 time: datetime.time,
                 paused: bool,
                 last_email_send: datetime.date):
        if interval not in [1, 2, 3]:
            raise Exception("Interval value not correct.")

        self.title = title
        self.recipient = recipient
        self.subject = subject
        self.message = message
        self.interval = interval
        self.skip_weekend = skip_weekend
        self.skip_weekdays = skip_weeksdays
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.time = time
        self.paused = paused
        self.last_email_sent = last_email_send

    def _check_remind(self, date: datetime.date, time: datetime.time):
        if self.paused:
            return False

        if self.last_email_sent:
            if self.last_email_sent == date:  # Schon erledigt
                return False

        if self.time > time:  # Heute noch nicht zu prüfen
            return False

        if self.interval == 1:
            if self.skip_weekend and date.weekday() >= 5:
                return False
            if self.skip_weekdays and date.weekday() <= 4:
                return False
            return True

        if self.interval == 2:
            if self.day_of_week == date.weekday() + 1:
                return True
            else:
                return False

        if self.interval == 3:
            if self.day_of_month <= 31 and self.day_of_month == date.day:
                return True
            if self.day_of_month == 40 and date.day < 8 and date.weekday() == 0:
                return True
            if self.day_of_month == 41 and date.day < 8 and date.weekday() == 1:
                return True
            if self.day_of_month == 42 and date.day < 8 and date.weekday() == 2:
                return True
            if self.day_of_month == 43 and date.day < 8 and date.weekday() == 3:
                return True
            if self.day_of_month == 44 and date.day < 8 and date.weekday() == 4:
                return True
            if self.day_of_month == 45 and date.day < 8 and date.weekday() == 5:
                return True
            if self.day_of_month == 46 and date.day < 8 and date.weekday() == 6:
                return True
            if self.day_of_month == 50 and date.day == 1 and date.weekday() <= 4:
                return True
            if self.day_of_month == 51 and date.day == 2 and 1 <= date.weekday() <= 4:
                return True
            if self.day_of_month == 51 and date.day == 3 and 2 <= date.weekday() <= 4:
                return True
            if self.day_of_month == 51 and date.day == 4 and 3 <= date.weekday() <= 4:
                return True
            if self.day_of_month == 52 and date.day == 3 and 2 <= date.weekday() <= 4:
                return True
            if self.day_of_month == 52 and date.day == 4 and date.weekday() == 2:
                return True
            if self.day_of_month == 52 and date.day == 5 and date.weekday() <= 2:
                return True
            if self.day_of_month >= 60:
                last_day = calendar.monthrange(date.year, date.month)[1]
                if self.day_of_month == 60 and date.day == last_day:
                    return True
                if self.day_of_month == 61 and date.day == last_day - 1:
                    return True
                if self.day_of_month == 62 and date.day == last_day - 2:
                    return True

                if self.day_of_month == 70 and date.day == last_day and date.weekday() <= 4:
                    return True
                if self.day_of_month == 70 and date.day == last_day - 1 and date.weekday() == 4:
                    return True
                if self.day_of_month == 70 and date.day == last_day - 2 and date.weekday() == 4:
                    return True

                if self.day_of_month == 71 and date.day == last_day - 1 and date.weekday() <= 3:
                    return True
                if self.day_of_month == 71 and date.day == last_day - 2 and date.weekday() == 3:
                    return True
                if self.day_of_month == 71 and date.day == last_day - 3 and 3 <= date.weekday() <= 4:
                    return True

                if self.day_of_month == 72 and date.day == last_day - 2 and date.weekday() <= 2:
                    return True
                if self.day_of_month == 72 and date.day == last_day - 3 and date.weekday() == 2:
                    return True
                if self.day_of_month == 72 and date.day == last_day - 4 and 2 <= date.weekday() == 4:
                    return True
            return False
        print("nothing catched, fallback")
        return False

    def remind(self):
        today = datetime.datetime.now()
        date = today.date()
        time = today.time()
        check = self._check_remind(date, time)

        if check:
            return self.send_mail()
        else:
            return 0

    def send_mail(self):
        # Dummy function where sending E-Mail would have to be implemented.
        # function should return the number of e-mails send (0 or 1)
        print(f"Sending Reminder-E-Mail to: {self.recipient}")
        print(f"Reminder: {self}")
        print(f"E-Mail: {self.subject}")
        print(f"{self.message}")
        return None

    def __str__(self):
        return self.title


if __name__ == '__main__':
    print("-- start ---")
    r = Reminder(
        "Inbox Zero",
        "test@dummy.de",
        "Inbox-Zero: Alle E-Mails bearbeitet?",
        "Sind alle E-Mails beantwortet, bearbeitet, gelöscht, etc.",
        1,
        True,
        False,
        1,
        1,
        datetime.time(hour=16),
        False,
        datetime.date.today() - datetime.timedelta(days=1)
    )
    r.remind()
    print("-- end --")
