import datetime
import time
from requests_html import HTMLSession
import mysql.connector

day = []
month = []
year = []
title = []
location = []
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="nabv_crawler"
)


def generate_session(url_session):
    site = session.get(url_session)
    dayElements = site.html.find(".listItemEvent .dateDay")
    monthElements = site.html.find(".listItemEvent .dateMonthYear")
    titleElements = site.html.find(".listItemEvent .sfitemTitle")
    # todo: met requests-html de search methode gebruiken om de waarde bij "Plaats:"
    locationElements = site.html.find(".listItemEvent .eventLocation")
    retrieve_days(dayElements)
    retrieve_months(monthElements)
    retrieve_titles(titleElements)
    retrieve_locations(locationElements)


def get_event(array_index):
    event = []
    event.append(day[array_index])
    event.append(month[array_index])
    event.append(year[array_index])
    event.append(title[array_index])
    event.append(location[array_index])
    return event


def print_all():
    print(day)
    print(month)
    print(year)
    print(title)
    print(location)


def retrieve_days(elements):
    for element in elements:
        day.append(element.text)


def retrieve_months(elements):
    for element in elements:
        monthString = ""
        yearString = ""
        for x in element.text:
            if not represent_int(x):
                monthString += x
            else:
                yearString += x
        month.append(monthString)
        year.append(yearString)


def retrieve_titles(elements):
    for element in elements:
        title.append(element.text)


def retrieve_locations(elements):
    for element in elements:
        value = element.text
        if value == "Plaats:" or not value:
            location.append("Geen opgegeven plaats")
        else:
            location.append(value)


def retrieve_links(elements):
    for element in elements:
        value = element.text
        if value == "Plaats:" or not value:
            location.append("Geen opgegeven plaats")
        else:
            location.append(value)


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def trunicate_table():
    mycursor = db.cursor()
    sql = "TRUNCATE TABLE events"
    mycursor.execute(sql)
    db.commit()
    print("tabel geleegd")


def insert_row(values_array):
    print(values_array)
    dayRow = values_array[0]
    monthRow = values_array[1]
    yearRow = values_array[2]
    titleRow = values_array[3]
    locationRow = values_array[4]
    # linkRow = values_array[5]
    ts = time.time()
    mycursor = db.cursor()
    sql = "INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (None, dayRow, monthRow, yearRow, titleRow, locationRow, datetime.date.today())
    mycursor.execute(sql, val)
    db.commit()


trunicate_table()
session = HTMLSession()
urlPrefix = "https://www.nabv.nl/evenementen/page/"

generate_session(urlPrefix + "3")
insert_row(get_event(1))

# Voer code uit voor de 10 pagina's
exit()
for x in range(1, 11):
    generate_session(urlPrefix + str(x))
for x in range(len(day)):
    insert_row(get_event(x))
