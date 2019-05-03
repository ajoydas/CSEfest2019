from django import forms
from django.db.models import Q
from django.utils.safestring import mark_safe

from quiz.models import Submission


class SetForm(forms.Form):
    def gen_field(self, question, answer=""):
        # print(question)
        # print(question.type)

        return forms.CharField(
            widget=forms.Textarea(attrs={
                'class': "form-control",
                'rows': 10,
                'style': 'height: 10em;'
            }),
            label=mark_safe(question.description),
            max_length=800,
            required=False,
            initial=answer
        )


    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        user = kwargs.pop('user', None)

        super(SetForm, self).__init__(*args, **kwargs)

        if user is None:
            for index in range(len(questions)):
                self.fields['question_{index}'.format(index=index)] = \
                    self.gen_field(questions[index])
        else:
            user_subs = Submission.objects.filter(Q(user=user))
            for index in range(len(questions)):
                submitted = user_subs.filter(Q(question=questions[index].id))
                if submitted.count() != 0:
                    self.fields['question_{index}'.format(index=index)] = \
                        self.gen_field(questions[index], submitted.get().answer)
                else:
                    self.fields['question_{index}'.format(index=index)] = \
                        self.gen_field(questions[index])

        return



class MarksForm(forms.Form):
    def marks_field(self, marks):
        return forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': "form-control",
            }),
            label="Marks",
            initial=marks,
            required=False,
        )

    def submission_field(self, question, answer=""):
        # print(question)
        # print(question.type)

        return forms.CharField(
            widget=forms.Textarea(attrs={
                'class': "form-control",
                'rows': 10,
                'style': 'height: 10em;'
            }),
            label=mark_safe(question.description),
            max_length=800,
            required=False,
            initial=answer
        )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MarksForm, self).__init__(*args, **kwargs)

        user_subs = Submission.objects.filter(Q(user=user)).order_by("question")
        for index in range(len(user_subs)):
            question = user_subs[index].question
            self.fields['question_{index}'.format(index=index)] = \
                self.submission_field(question, user_subs[index].answer)
            self.fields['question_{index}_marks'.format(index=index)] = \
                self.marks_field(user_subs[index].marks)

















