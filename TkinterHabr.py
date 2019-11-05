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
        url = 'https://habr.com/ru/top/yearly/page' + '1'
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'lxml')
        pages = soup.find('ul', attrs={'id': 'nav-pagess'}).find_all('li')[-1].find('a')['href'].split('/')[-2].replace('page', '')
        post_count = len(soup.find_all('a', class_='post__title_link'))
        if count % 20 == 0:
            pages_to_parse = count//20
        else:
            pages_to_parse = count//20 + 1
            last_page_post_count = count % 20

        for i in range (1, pages_to_parse+1):
            url = 'https://habr.com/ru/top/yearly/page' + str(i)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            if i==pages_to_parse:
                last_j = last_page_post_count
            else:
                last_j = 20
            for j in range (0, last_j):
                post_title = soup.find_all('a', class_='post__title_link')[j].text
                post_text = BeautifulSoup(str(soup.find_all('div', class_='post__text')[j]).replace('<br/>','').replace('\r\n',' ').replace('\n',' '),'lxml').text
                post_date = soup.find_all('span', class_='post__time')[j].text
                post_author = soup.find_all('span', class_='user-info__nickname')[j].text

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
