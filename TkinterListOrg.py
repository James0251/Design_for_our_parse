import tkinter as tk
from tkinter import ttk    #Для добавления элементов в приложение(текстовые надписи, кнопки)
import requests
from bs4 import BeautifulSoup

#В переменную app будет помещен весь необходимый функционал для работы с приложением
app = tk.Tk()
app.title('Парсер list-org.com')

#Добавим текстовую надпись
search_label = ttk.Label(app, text='Введите ID компании или ссылку на неё: ')
search_label.grid(row =0, column=0)

#Создадим текстовое поле для ввода информации
text_field = ttk.Entry(app, width=70)
text_field.grid(row=0, column=1)

def search():
    if text_field.get().strip() !="":
        company_id = text_field.get()
        try:
            test_for_int = int(company_id)
            url = 'https://www.list-org.com/company/'+str(company_id)
        except:
            url = company_id

        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0', 'referer':'https://list-org.com'}
        session = requests.session()
        company_page = session.get(url, headers = user_agent)

        soup = BeautifulSoup(company_page.text, 'lxml')
        legal_name = soup.find('a', class_='upper').text
        director = soup.find_all('a', class_='upper')[1].text
        registration_date = soup.find('table', class_='tt').find_all('td')[-3].text
        status = soup.find('table', class_='tt').find_all('td')[-1].text
        inn = soup.find('table', class_='tt').find_all('td')[3].text.split('/')[0].strip()
        kpp = soup.find('table', class_='tt').find_all('td')[3].text.split('/')[1].strip()
        ogrn = soup.find_all('div', class_='c2m')[2].find_all('p')[3].text.split(':')[1].strip()

        data = {'legal_name':legal_name,
                'director':director,
                'registration_date':registration_date,
                'status':status,
                'inn':inn,
                'kpp':kpp,
                'ogrn':ogrn}

        file = open('company.csv','a')
        file.write(data['legal_name'] + ';')
        file.write(data['director'] + ';')
        file.write(data['registration_date'] + ';')
        file.write(data['status'] + ';')
        file.write(data['inn'] + ';')
        file.write(data['kpp'] + ';')
        file.write(data['ogrn'] +'\n')
        file.close()


#Создадим нажатие на кнопку "Найти"
def enterBtn(event):
    search()

#Создадим клик по кнопке "Найти"
def searchBtn():
    search()

#Создадим кнопку "Найти"
btn_search = ttk.Button(app, text="Найти", width= 10, command=searchBtn)
btn_search.grid(row=0, column=2)

text_field.bind('<Return>', enterBtn)

#Сделаем нашу строку поиска всегда на переднем плане
app.wm_attributes('-topmost', True)

app.mainloop()
