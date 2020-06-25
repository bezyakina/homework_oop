import datetime as dt

NOW = dt.datetime.now().date()
WEEK_AGO = (dt.datetime.now() - dt.timedelta(days=7)).date()


class Calculator:
    """Класс Calculator используется для хранения и записи трат или \n
    килокалорий, получения их суммарных значений за текущий день или за \n
    прошедшие 7 дней.

    Attributes
    ----------
    records: list
        Cписок для хранения записей.
    limit: int
        Дневной лимит трат или килокалорий.
    """

    def __init__(
        self, limit,
    ):
        """Создает объект класса Calculator.
        """
        self.records = []
        self.limit = limit

    def add_record(
        self, record,
    ):
        """Добавляет новую запись об объекте класса Record в список.
        """
        self.records.append(record)

    def get_today_stats(self,):
        """Возвращает сумму трат или килокалорий за сегодня.
        """
        spent_amount = 0
        for record in self.records:
            if record.date == NOW:
                spent_amount += record.amount
        return spent_amount

    def get_week_stats(self,):
        """Возвращает сумму трат или килокалорий за неделю.
        """
        spent_amount = 0
        for record in self.records:
            if WEEK_AGO <= record.date <= NOW:
                spent_amount += record.amount
        return spent_amount


class Record:
    """Класс Record используется для создания записи трат или килокалорий.

    Attributes
    ----------
    amount: int
        Денежная сумма или количество килокалорий.
    comment: str
        Комментарий, поясняющий, на что потрачены деньги
        или откуда взялись килокалории.
    date: date
        Дата создания записи.
    """

    def __init__(
        self, amount, comment, date=NOW,
    ):
        """Создает объект класса Record.
        """
        self.amount = amount
        self.comment = comment
        if type(date) == str:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y",).date()
        else:
            self.date = date


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator используется определения
       дневного остатка килокалорий.

    Attributes
    ----------
    Calculator: class
        Родительский класс.
    """

    def get_calories_remained(self,):
        """Возвращает ответ, можно ли есть и сколько съесть килокалорий \n
        сегодня.
        """
        calories_eaten = self.get_today_stats()
        remainder = self.limit - calories_eaten

        if calories_eaten < self.limit:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей \
            калорийностью не более {remainder} кКал"
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    """Класс CashCalculator используется определения дневного остатка денег \n
    в рублях, долларах или евро.

    Attributes
    ----------
    Calculator: class
        Родительский класс.
    """

    # Курсы валют USD и EURO
    USD_RATE = 69.45
    EURO_RATE = 77.76

    def get_today_cash_remained(
        self, currency,
    ):
        """Возвращает ответ, можно ли и сколько денег потратить сегодня
           в рублях, долларах или евро.
        """

        # Словарь для хранения соответствия выбранного currency и строки для
        # его вывода
        currency_dict = {
            "rub": "руб",
            "usd": "USD",
            "eur": "Euro",
        }
        # Сумма потраченных денег сегодня
        spent_amount = self.get_today_stats()
        # Остаток денег по модулю
        remainder = abs(self.limit - spent_amount)

        # Перевод остатка из рублей в выбранную валюту
        if currency == "usd":
            remainder /= self.USD_RATE
        elif currency == "eur":
            remainder /= self.EURO_RATE

        if spent_amount < self.limit:
            return "На сегодня осталось {:.2f} {}".format(
                remainder, currency_dict[currency],
            )
        elif spent_amount > self.limit:
            return "Денег нет, держись: твой долг - {:.2f} {}".format(
                remainder, currency_dict[currency],
            )
        else:
            return "Денег нет, держись"


# Пример сценария использования для проверки работы классов
if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="кофе",))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед",))
    cash_calculator.add_record(
        Record(amount=3000, comment="бар в Танин др", date="08.11.2019",)
    )
    print(cash_calculator.get_today_cash_remained("rub"))
