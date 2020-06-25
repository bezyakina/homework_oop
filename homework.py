import datetime as dt

NOW = dt.datetime.now().date()
WEEK_AGO = (dt.datetime.now() - dt.timedelta(days=7)).date()


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        spent_amount = 0
        for record in self.records:
            if record.date == NOW:
                spent_amount += record.amount
        return spent_amount

    def get_week_stats(self):
        spent_amount = 0
        for record in self.records:
            if WEEK_AGO <= record.date <= NOW:
                spent_amount += record.amount
        return spent_amount


class Record:
    def __init__(self, amount, comment, date=NOW):
        self.amount = amount
        self.comment = comment
        if type(date) == str:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        else:
            self.date = date


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):

        calories_eaten = self.get_today_stats()
        remainder = self.limit - calories_eaten

        if calories_eaten < self.limit:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remainder} кКал"
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):

    USD_RATE = 69.45
    EURO_RATE = 77.76

    def get_today_cash_remained(self, currency):
        currency_dict = {"rub": "руб", "usd": "USD", "eur": "Euro"}
        spent_amount = self.get_today_stats()
        remainder = abs(self.limit - spent_amount)

        if currency == "usd":
            remainder /= self.USD_RATE
        elif currency == "eur":
            remainder /= self.EURO_RATE

        if spent_amount < self.limit:
            return "На сегодня осталось {:.2f} {}".format(
                remainder, currency_dict[currency]
            )
        elif spent_amount > self.limit:
            return "Денег нет, держись: твой долг - {:.2f} {}".format(
                remainder, currency_dict[currency]
            )
        else:
            return "Денег нет, держись"
