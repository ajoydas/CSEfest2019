import pandas as pd
import sendgrid
from sendgrid.helpers.mail import *
import codecs
from bs4 import BeautifulSoup


API_KEY = ''


def main():
    df = pd.read_excel('web_sec.xlsx')

    sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

    f = codecs.open("confirm.html", 'r', 'utf-8')
    document = BeautifulSoup(f.read(), "html.parser")

    from_email = Email("hackathon@mail.csefest2019.com")

    subject = "Problem set for Web security and Block chain"

    for i in range(0, 1):
       
        for j in range(1, 4):
            """
                Name
            """
            _name = "Name_" + str(j)

            participant_name = document.find('p', {"class": "participant_name"})
            participant_name.clear()
            participant_name.append("{}".format(df[_name][i]))

            """
                Team Name
            """

            team_name = document.find('p', {"class": "team_name"})
            team_name.clear()
            team_name.append("{}".format(df['Team_Name'][i]))

            content = Content("text/html", str(document))

            """
                Email
            """

            to_email = Email("example@gmail.com")

            _mail = Mail(from_email, subject, to_email, content)

            # print(_mail.get())
            response = sg.client.mail.send.post(request_body=_mail.get())

            print(response.status_code)
            # print(response.body)
            # print(response.headers)


if __name__ == '__main__':
    main()
