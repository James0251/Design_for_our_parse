import tkinter as tk
from tkinter import ttk 
import requests
from bs4 import BeautifulSoup

app = tk.Tk()
app.title('Парсер habr.com')

search_label = ttk.Label(app, text='Введите количество постов: ')
search_label.grid(row =0, column=0)

text_field = ttk.Entry(app, width=70)
text_field.grid(row=1, column=0)

def search():
    if text_field.get().strip() !="":
        count = int(text_field.get())
        parse_page = ''

        if count % 20 == 0:
            pages_to_parse = count//20
        else:
            pages_to_parse = count//20 + 1

        for i in range (1, pages_to_parse+1):
            url = 'https://habr.com/ru/top/yearly/page' + str(i)
            r = requests.get(url)
            parse_page += r.text.replace('</html>', '')

        soup = BeautifulSoup(parse_page, 'lxml')

        for i in range (0, count):
            post_title = soup.find_all('a', class_='post__title_link')[i].text
            post_text = BeautifulSoup(str(soup.find_all('div', class_='post__text')[i]).replace('<br/>','').replace('\r\n',' ').replace('\n',' '),'lxml').text
            post_date = soup.find_all('span', class_='post__time')[i].text
            post_author = soup.find_all('span', class_='user-info__nickname')[i].text

            file = open('habr.csv', 'a')
            file.write(post_title + ';')
            file.write(post_text + ';')
            file.write(post_date + ';')
            file.write(post_author + '\n')
            file.close()

def enterBtn(event):
    search()

def searchBtn():
    search()

btn_search = ttk.Button(app, text="Найти", width= 10, command=searchBtn)
btn_search.grid(row=1, column=1)

text_field.bind('<Return>', enterBtn)

app.wm_attributes('-topmost', True)

app.mainloop()
