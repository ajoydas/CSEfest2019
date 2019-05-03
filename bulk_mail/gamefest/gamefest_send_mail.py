import pandas as pd
import sendgrid
from sendgrid.helpers.mail import *
import codecs
from bs4 import BeautifulSoup

API_KEY = ''

df = pd.read_excel('pubg-mail.xlsx')

sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

f = codecs.open("confirm.html", 'r', 'utf-8')
document = BeautifulSoup(f.read(), "html.parser")

from_email = Email("gamefest@mail.csefest2019.com")

subject = "PUBG Mobile Final Round Password"

slot = 0
room_id = "54531"
passw = "final"
for i in range(0, 84):
    print(i)
    if i%4 == 0:
        slot += 1

    _code_ = document.find('p', {"class": "slot"})
    _code_.clear()
    _code_.append(str(slot))

    _room_id = document.find('p', {"class": "room_id"})
    _room_id.clear()
    _room_id.append(str(room_id))
    
    _passw = document.find('p', {"class": "passw"})
    _passw.clear()
    _passw.append(str(passw))
    
    content = Content("text/html", str(document))

    to_email = Email(df['Email'][i])
    # print(to_email)

    # print(document)
    try:

        _mail = Mail(from_email, subject, to_email, content)
    
        # print(_mail.get())
        response = sg.client.mail.send.post(request_body=_mail.get())
    
        print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except:
        pass
