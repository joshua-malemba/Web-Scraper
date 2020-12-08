import requests
from tkinter import *
import smtplib
from bs4 import BeautifulSoup
import sqlite3
import os
# helps parse the HTML data and retrieve/pull out specific data.

master = Tk()

def scrape():
    # define base price ----> check if price changed
    headers = {'User Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    URL = 'https://www.amazon.co.uk/RockJam-Portable-Digital-Keyboard-Stickers/dp/B07F8KF4LC?ref_=s9_apbd_otopr_hd_bw_bRVqkp&pf_rd_r=RKCQTS6RCMTWQ6EZHHYF&pf_rd_p=ff1cb8e3-2a28-5cfc-8dba-de49f07c6333&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&pf_rd_i=406552031%27'
    
    page = requests.get(URL, headers=headers).text

    soup = BeautifulSoup(page, 'lxml')

    #we'll inspect and draw the class which the text is held in, to scrape the data!

    title = soup.find('span', {'class': 'a-size-large product-title-word-break'})

    ### stores the entire div of the span id within the variable 'title' then
    ### returns the text
    
    price = soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockBuyingPriceString'})
    ### initialize database ### store scraped information ###
    database = 'amazondata.db'
    
    if os.path.exists(database) == True:
        db = sqlite3.connect(database)
        cursor = db.cursor()

        cursor.execute('UPDATE amazon SET Price', price.text)

        db.commit()
    elif os.path.exists(database) == False:
        db = sqlite3.connect(database)
        
        cursor = db.cursor()

        # create tuple which will hold price and product title
        #data = [(e1.get, t.get('1.0', END)),]
        data = [(price.text, title.text),]
        cursor.execute('CREATE TABLE amazon(Product text, Price text)')
        cursor.executemany('insert into amazon values(?,?)', data)

        db.commit()

    
t = Text(master, font='Calibri 8', height=5.5, width=20)
t.grid(row=3, column=1)

l = Label(master, text='Product Title: ')
l.grid(row=3, column=0)

p = Label(master, text='Current Price: ')
p.grid(row=2, column=0)

b = Button(master, text='SCRAPE', command=scrape)
b.grid(row=2, column=2)

e1 = Entry(master)
e1.grid(row=2, column=1)

master.geometry('300x250')


mainloop()
