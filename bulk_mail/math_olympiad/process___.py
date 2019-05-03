import pandas as pd
import sendgrid
from sendgrid.helpers.mail import *
import codecs
from bs4 import BeautifulSoup

API_KEY = ''


school_code = 0000
college_code = 0000


def get_scode():
    if len(str(school_code)) == 1:
        return 's_00' + str(school_code)
    elif len(str(school_code)) == 2:
        return 's_0' + str(school_code)
    elif len(str(school_code)) == 3:
        return 's_' + str(school_code)


def get_ccode():
    if len(str(college_code)) == 1:
        return 'c_00' + str(college_code)
    elif len(str(college_code)) == 2:
        return 'c_0' + str(college_code)
    elif len(str(college_code)) == 3:
        return 'c_' + str(college_code)


def send_mail(msg, _email):
    # print(msg)
    # print(email)
    sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
    from_email = Email("math_olympiad@csefest2019.com")
    to_email = Email(_email)
    subject = "Confirmation for Math Olympiad"

    content = Content("text/html", msg)

    mail = Mail(from_email, subject, to_email, content)

    # print(mail.get())
    response = sg.client.mail.send.post(request_body=mail.get())

    # print(response.status_code)
    # print(response.body)
    # print(response.headers)


def main():
    df = pd.read_excel('Copy_of_Math_Olympiad_Registration_(Responses).xlsx').sample(frac=1).reset_index(drop=True)

    print(df)

    # print(df['Category'][0])

    # print(df.shape[0])

    s_name = []
    s_institute = []
    s_email = []
    s_category = []
    s_code = []

    c_name = []
    c_institute = []
    c_email = []
    c_category = []
    c_code = []

    for i in range(df.shape[0]):
        if df['Category'][i] == "School":
            code = get_scode()
            global school_code
            school_code = school_code + 1

            f = codecs.open("confirm.html", 'r', 'utf-8', )
            document = BeautifulSoup(f.read(), "html.parser")

            print(df['Name'][i])
            # o = document.new_string("Dear {}".format(df['name'][i]))

            # o = document.replace_with()
            # o = Tag(document, )

            yoo = document.find('p', {"class": "name"})
            yoo.clear()
            yoo.append("Dear ")
            yoo.append("{}".format(df['Name'][i]))

            _code_ = document.find('p', {"class": "code"})
            _code_.clear()
            _code_.append("{}".format(code))

            send_mail(str(document), df['Email ID'][i])

            s_name.append(df['Name'][i])
            s_category.append(df['Category'][i])
            s_email.append(df['Email ID'][i])
            s_institute.append(df['Institution'][i])
            s_code.append(code)
        else:
            code = get_ccode()
            global college_code
            college_code += 1

            f = codecs.open("confirm.html", 'r', 'utf-8')
            document = BeautifulSoup(f.read(), "html.parser")
            # print(document)
            print(df['Name'][i])

            yoo = document.find('p', {"class": "name"})
            yoo.clear()

            yoo.append("Dear ")
            yoo.append("{}".format(df['Name'][i]))

            _code_ = document.find('p', {"class": "code"})
            _code_.clear()
            _code_.append("{}".format(code))

            send_mail(str(document), df['Email ID'][i])

            c_name.append(df['Name'][i])
            c_category.append(df['Category'][i])
            c_email.append(df['Email ID'][i])
            c_institute.append(df['Institution'][i])
            c_code.append(code)

    s_frame = {
        'name': s_name,
        'institute': s_institute,
        'email': s_email,
        'category': s_category,
        'secret_code': s_code,
    }

    log_s = pd.DataFrame(data=s_frame)

    writer = pd.ExcelWriter('school_secret_code.xlsx')
    log_s.to_excel(writer, 'Sheet1', index=False)
    writer.save()

    c_frame = {
        'name': c_name,
        'institute': c_institute,
        'email': c_email,
        'category': c_category,
        'secret_code': c_code,
    }

    log_c = pd.DataFrame(data=c_frame)

    writer = pd.ExcelWriter('college_secret_code.xlsx')
    log_c.to_excel(writer, 'Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    main()
