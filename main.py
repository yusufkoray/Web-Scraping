import selectorlib
import requests
import smtplib, ssl
import os
import sqlite3
import time

connection=sqlite3.connect("data.db")

PASSWORD=os.getenv("SAKINIM")
URL="http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response=requests.get(url,headers=HEADERS)
    source=response.text
    return source

def extract(source):
    extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)["tours"]
    #If you want to find selector easily, then copy, copy selector at the elemets console(when you inspect the selected thing at website.)
    return value
def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "ykcspor@gmail.com"
    password = PASSWORD

    receiver = "ykcspor@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted):
    # with open("data.txt",'a') as file: #a for append new
    #     file.write(extracted+'\n')
    cursor = connection.cursor()
    row = extracted.split(",")
    row = [item.strip() for item in row]

    cursor.execute("INSERT INTO events VALUES(?,?,?)",row)
    connection.commit()



def read_data(extracted):
    # with open("data.txt",'r') as file:
    #     data=file.read()
    # return  data
    cursor=connection.cursor()
    row=extracted.split(",")
    row=[item.strip() for item in row]
    band, city, date = row
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(band,city,date))
    rows=cursor.fetchall()
    return rows

if __name__=="__main__":
    while True:
    # print(source_)
    # print(extract(source_))
    # with open("text.txt","w") as file:
    #     file.write(scrape(URL))


        scraped = scrape(URL)

        extracted = extract(scraped)

        print(extracted)

        if extracted != "No upcoming tours":
            row = read_data(extracted)
            if not row: #row empty ise calisir.
                store(extracted)
                send_email("Hey, new event!")
        time.sleep(2)

#Calisma mantigi su sekilde. Cektigimiz bir liste database'de var mı. Var, o zaman liste boş değil ve ekleme yapmaz.
#List boşsa yani ilk defa internetten çekip database'e yazıyorsak, o zaman ekleme yapar.










#When you're scraping data from websites, headers play an important role because they help make your request look like
# it’s coming from a real web browser. This is important because when you ask a website for information, it checks these
# headers to decide how to respond.

# For example, the website might look at which browser is making the request, what type of content it expects, and other
# details. This way, the website can give you the right content.
#
# In Python, we can use the requests library to send a request to a webpage. One of the cool things about it is that we
# can set custom headers to control how the website sees our request.
# For example, we can set the User-Agent, which tells the website which browser we're using.
#
# Here’s a simple example to show how you can set headers:
#
# import requests
#
# url = 'https://example.com'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }
#
# response = requests.get(url, headers=headers)
# In this code, we are setting the User-Agent to make it look like we’re using a popular web browser. This helps in getting the data you need because some websites only allow certain browsers to access their content.