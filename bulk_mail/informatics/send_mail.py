# -*- coding: utf-8 -*-
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import *
import codecs
from bs4 import BeautifulSoup

API_KEY = ''

df = pd.read_excel('infor_list.xlsx')

sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

f = codecs.open("confirm.html", 'r', 'utf-8')
document = BeautifulSoup(f.read(), "html.parser")

from_email = Email("olympiad@mail.csefest2019.com")

subject = "Informatics Olympiad Confirmation Mail"

for i in range(df.shape[0]):
    print(i)

    yoo = document.find('p', {"class": "name"})
    yoo.clear()
    yoo.append("{}".format(df['Name'][i]))

    _code_ = document.find('p', {"class": "ins_name"})
    _code_.clear()
    _code_.append("{}".format(df['Institution'][i]))

    content = Content("text/html", str(document))

    to_email = Email(df['Email'][i])

    _mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=_mail.get())

    print(response.status_code)
    # print(response.body)
    # print(response.headers)
