import requests

class Connection:
    url = None
    connectURL = None
    connectAnswer = None
    connectDate = None

    def __init__(self, url):
        self.url = url

    def conn_request(self):
        try:
            print('log -----> conn_request - OK')
            return requests.get(self.url)
        except Exception as e:
            print(f'log -----> Error conn_request: {e}')
            return None

    def save_conn_request(self):
        self.connectURL = self.conn_request()
        print('log -----> save_conn_request - OK')

    def conn_request_status(self):
        self.save_conn_request()
        if 200 <= self.connectURL.status_code <= 299:
            print('log -----> conn_request_status - OK')
            return self.connectURL.status_code
        else:
            print('log -----> conn_request_status - FALSE: ', self.connectURL.status_code)
            return False

    def conn_request_answer(self):
        self.connectAnswer = self.connectURL.json()
        self.connectDate = self.connectURL.headers['Date']
        print('log -----> conn_request_answer - OK')
        return self.connectAnswer

    def save_answer_txt(self):
        counter = 1
        file = open('bank.txt', 'w')
        file.write(f'Date: {self.connectDate}\n')
        for item in self.connectAnswer:
            file.write(f'{counter}. {item.setdefault("txt")} к Украинской гривне: {item.setdefault("rate")}\n')
            counter += 1
        counter = 1
        file.close()

    def print_answer_user(self):
        if not self.connectAnswer:
            print('log -----> Server returned an empty array.')
            return None
        elif self.connectAnswer[0].setdefault("message"):
            print(f'log -----> Server answer {self.connectAnswer[0].setdefault("message")}')
        else:
            name = self.connectAnswer[0].setdefault("txt")
            rate = self.connectAnswer[0].setdefault("rate")
            ex_date = self.connectAnswer[0].setdefault("exchangedate")
            print(f'Курс {name} відносно Української гривні {rate} на {ex_date}')
            return name, rate, ex_date


# TASK 1
inputUserURL_One = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

connectUserURL_One = Connection(inputUserURL_One)

connectUserURL_One.conn_request_status()
connectUserURL_One.conn_request_answer()
connectUserURL_One.save_answer_txt()

# TASK 2
code = input('Введіть міжнародний код валюти: ').upper()
date = input('Введіть дату конвертації (Формат: РРРРММДД): ')
inputUserURL_Two = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={code}&date={date}&json'

connectUserURL_Two = Connection(inputUserURL_Two)

connectUserURL_Two.conn_request_status()
connectUserURL_Two.conn_request_answer()
connectUserURL_Two.print_answer_user()