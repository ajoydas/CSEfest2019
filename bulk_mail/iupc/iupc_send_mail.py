import pandas as pd
import sendgrid
from sendgrid.helpers.mail import *
import codecs
from bs4 import BeautifulSoup

# API_KEY = ''
API_KEY = ''


def main():
    df = pd.read_excel('Email_List.xlsx')

    sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

    f = codecs.open("confirm.html", 'r', 'utf-8')
    document = BeautifulSoup(f.read(), "html.parser")

    from_email = Email("buet_iupc@mail.csefest2019.com")

    subject = "Confirmation mail for Buet IUPC"

    for i in range(df.shape[0]):
        # to_email = Email('example@gmail.com')

        yoo = document.find('p', {"class": "name"})
        yoo.clear()
        yoo.append("{}".format(df['Team Name'][i]))

        _code_ = document.find('p', {"class": "uni_name"})
        _code_.clear()
        _code_.append("{}".format(df['Institution'][i]))

        content = Content("text/html", str(document))

        for j in range(1, 5):
            _mail = "Email_"+str(j)
            print(df[_mail][i])

            to_email = Email(df[_mail][i])
            # print(to_email)

            # print(document)

            _mail = Mail(from_email, subject, to_email, content)

            # print(_mail.get())
            response = sg.client.mail.send.post(request_body=_mail.get())

            print(response.status_code)
            # print(response.body)
            # print(response.headers)


if __name__ == '__main__':
    main()
