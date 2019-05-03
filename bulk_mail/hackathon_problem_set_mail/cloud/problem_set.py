import pandas as pd
import sendgrid
from sendgrid.helpers.mail import *
import codecs
from bs4 import BeautifulSoup


API_KEY = ''


def main():
    df = pd.read_excel('cloud.xlsx')

    sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

    f = codecs.open("confirm.html", 'r', 'utf-8')
    document = BeautifulSoup(f.read(), "html.parser")

    from_email = Email("hackathon@mail.csefest2019.com")

    subject = "Problem set for Cloud computing"

    for i in range(df.shape[0]):
     
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
            # change the below

            _mail = "Email_"+str(j)
            print(df[_mail][i])

            to_email = Email(df[_mail][i])
            # print(to_email)


            _mail = Mail(from_email, subject, to_email, content)

            # print(_mail.get())
            response = sg.client.mail.send.post(request_body=_mail.get())

            print(response.status_code)
            # print(response.body)
            # print(response.headers)


if __name__ == '__main__':
    main()
