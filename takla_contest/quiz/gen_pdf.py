# using emojione to display unicode emoji in picture form
import os

from django.contrib.auth.models import User
from django.db.models import Q
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from emojipy import Emoji
import re

# Pdf doesn't need any unicode inside <image>'s alt attribute
from quiz.models import Submission, Question, QuestionSet

# Emoji.unicode_alt = False
from quiz_contest.settings import STATIC_ROOT, MEDIA_ROOT


def replace_with_emoji_pdf(text, size):
    """
    Reportlab's Paragraph doesn't accept normal html <image> tag's attributes
    like 'class', 'alt'. Its a little hack to remove those attrbs
    """

    text = Emoji.to_image(text)
    print(text)
    text = text.replace('class="emojione "', 'height=%s width=%s' %
                        (size, size))
    text = text.replace('style=""', '')
    return re.sub('alt="'+Emoji.shortcode_regexp+'"', '', text)

# Register font 'font_file' is location of symbola.ttf file

# font_file = 'Symbola/Symbola_hint.ttf'
# symbola_font = TTFont('Symbola', font_file)
# pdfmetrics.registerFont(symbola_font)
#
# width, height = defaultPageSize
# pdf_content = "It's emoji time \u263A \U0001F61C. Let's add some cool emotions \U0001F48F \u270C. And some more \u2764 \U0001F436"
#
# styles = getSampleStyleSheet()
# styles["Title"].fontName = 'Symbola'
# style = styles["Title"]
# content = replace_with_emoji_pdf(Emoji.to_image(pdf_content), style.fontSize)
#
# print(content)
#
# para = Paragraph(content, style)
# canv = canvas.Canvas('emoji.pdf')
#
# para.wrap(width, height)
# para.drawOn(canv, 0, height/2)
#
# canv.save()


def generate():


    Emoji.unicode_alt = False
    font_file = 'fonts/Siyamrupali.ttf'
    print(os.path.join(STATIC_ROOT,font_file))
    font = TTFont('bangla', os.path.join(STATIC_ROOT,font_file))
    pdfmetrics.registerFont(font)
    width, height = defaultPageSize

    from reportlab import rl_config
    rl_config._SAVED['canvas_basefontname'] = 'bangla'
    rl_config._startUp()

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = 'bangla'
    style = styles["Normal"]

    # get all non admin user and questions
    users = User.objects.filter(is_superuser=False)
    question_sets = QuestionSet.objects.all()

    for user in users:
        # create new pdf for user
        pdf_url = os.path.join(MEDIA_ROOT, "pdf/"+str(user.id)+"_"+user.username+'.pdf')
        print(pdf_url)
        # canv = canvas.Canvas(pdf_url)

        doc = SimpleDocTemplate(pdf_url, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        Story = []
        # get user's submissions
        for set in question_sets:
            questions = Question.objects.filter(question_set=set)
            for question in questions:
                submission = Submission.objects.filter(Q(user=user) & Q(question=question))
                # write submission to pdf
                if submission.count() == 0:
                    continue
                submission = submission.get()

                pdf_content = question.description + "\n"
                pdf_content += submission.answer

                # content = replace_with_emoji_pdf(Emoji.to_image(pdf_content), style.fontSize)
                # print(content)

                # attach on a place on the page of the pdf
                para = Paragraph(pdf_content, style)
                # para.wrap(width, height)
                # para.drawOn(canv, 0, height / 2)
                Story.append(para)
                Story.append(Spacer(1, 12))

        # save the pdf
        # canv.save()
        doc.build(Story)



























