import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


# Create your views here.
# from quiz.models import Comment

# from django.views.generic import ListView
# from .models import Comment
#
#
# class CommentsView(ListView):
#     model = Comment
#     context_object_name = 'comments'

#
# from .forms import CommentForm
#
# def comment(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = CommentForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             print(form)
#             comm = Comment(text=form.cleaned_data.get('text'), author=form.cleaned_data.get('author'))
#             comm.save()
#
#             return render(request, 'comments/comments.html', {'form': form})
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         comm = Comment.objects.get(id=1)
#         print(comm)
#
#         form = CommentForm(data={
#             'text': comm.text,
#             'author': comm.author
#         })
#
#     return render(request, 'comments/comments.html', {'form': form})
#
#
# def comments(request):
#     comms = Comment.objects.all()
#     return render(request, 'comments/comment_list.html', {'comments':comms})
from core.models import Profile
from quiz.forms import SetForm, MarksForm
from quiz.gen_pdf import generate
from quiz.models import QuestionSet, Question, Submission


def send(request, title, form, pk, set_count, end_time):
    return render(
        request, "quiz_front_end/questions.html",
        {
            'title': title,
            'form': form,
            'current_question': pk,
            'question_count': range(set_count),
            'end_time': end_time
        })


def questions(request, pk, pk2=None):
    user = request.user
    # redirect unauthenticated users
    if user.is_authenticated is False:
        return redirect('core:login_user')

    # redirect if contest not started
    if settings.START_TIME > datetime.datetime.now():
        start_time = str(settings.START_TIME)
        print(start_time)
        return render(request, "quiz_front_end/wait.html", {"start_time": start_time})

    # redirect if contest finished
    end_time = str(settings.END_TIME)
    print(end_time)

    if (request.method == "POST" and settings.END_TIME < datetime.datetime.now()- datetime.timedelta(minutes=1)) \
            or settings.END_TIME < datetime.datetime.now()\
            or user.profile.submitted:
        return render(request, "quiz_front_end/end.html")

    # check the requested question exist
    question_set = get_object_or_404(QuestionSet, pk=pk)
    title = question_set.description
    set_count = QuestionSet.objects.count()
    question_list = Question.objects.filter(question_set=question_set)

    if request.method == "POST":
        print(pk2)
        redirect_set = get_object_or_404(QuestionSet, pk=pk)

        form = SetForm(request.POST, questions=question_list)
        # print(form)

        if form.is_valid():
            for index in range(question_list.count()):
                answer = form.cleaned_data.get('question_{index}'.format(index=index))
                # print(answer)
                # update or save submission
                submitted = Submission.objects.filter(Q(user=user) & Q(question = question_list[index].id))
                if submitted.count() == 0:
                    submitted = Submission(user=user, question = question_list[index])
                else:
                    submitted = submitted.get()
                # save updated answer
                submitted.answer = answer
                submitted.save()

            return redirect("quiz:question", pk2)

        # send error message & don't change page
        msg = "Please fill up the answer correctly!"
        messages.add_message(request, messages.ERROR, msg)
        return send(request, title, form, pk, set_count, end_time)

    # get request, send the form
    # check if previous submission exists

    # value_dict = {}
    # user_subs = Submission.objects.filter(Q(user=user))
    # for index in range(question_list.count()):
    #     submitted = user_subs.filter(Q(question=question_list[index].id))
    #     if submitted.count() != 0:
    #         value_dict =
    #
    # form = SetForm(initial={
    #     'company_name': user.client.company_name,
    #     'registration_info': user.client.registration_info,
    #     'website': user.client.website,
    #     'additional_info': user.client.additional_info,
    # })

    form = SetForm(questions=question_list, user=user)
    return send(request, title, form, pk, set_count, end_time)


@login_required()
def ended(request, pk):
    user = request.user

    # finished user's contest
    user.profile.submitted = True
    user.profile.submission_time = datetime.datetime.now()
    user.save()

    # recheck for ending
    if (request.method == "POST" and settings.END_TIME < datetime.datetime.now()- datetime.timedelta(minutes=1)) \
            or settings.END_TIME < datetime.datetime.now()\
            or user.profile.submitted:
        return render(request, "quiz_front_end/end.html")

    if request.method == "POST":
        question_set = get_object_or_404(QuestionSet, pk=pk)
        question_list = Question.objects.filter(question_set=question_set)

        form = SetForm(request.POST, questions=question_list)
        # print(form)

        if form.is_valid():
            for index in range(question_list.count()):
                answer = form.cleaned_data.get('question_{index}'.format(index=index))
                # print(answer)
                # update or save submission
                submitted = Submission.objects.filter(Q(user=user) & Q(question = question_list[index].id))
                if submitted.count() == 0:
                    submitted = Submission(user=user, question = question_list[index].id)
                else:
                    submitted = submitted.get()
                # save updated answer
                submitted.answer = answer
                submitted.save()

            # send error message

    return render(request, "quiz_front_end/end.html")


@user_passes_test(lambda u: u.is_superuser)
def gen_pdf(request):
    content = "Success."
    # try:
    #     generate()
    # except Exception as e:
    #     content = str(e)

    generate()

    return HttpResponse(content, content_type='text/plain')


@user_passes_test(lambda u: u.is_superuser)
def submissions(request):
    page_length = 10

    user_list = Profile.objects.filter(user__is_superuser=False)

    # user_list = Profile.objects.order_by('-level_completed')
    paginator = Paginator(user_list, page_length)  # Show 25 contacts per page

    page = request.GET.get('page')
    if page is None:
        page = 1

    users = paginator.get_page(page)

    return render(request, 'quiz_front_end/submissions.html', {
        'users': users,
    })


@user_passes_test(lambda u: u.is_superuser)
def submission(request, pk):
    # get all non admin user and questions
    user = User.objects.filter(Q(is_superuser=False) & Q(pk = pk)).get()

    if request.method == "POST":
        form = MarksForm(request.POST, user=user)
        # print(form)

        sum = 0
        if form.is_valid():
            user_subs = Submission.objects.filter(Q(user=user)).order_by("question")
            for index in range(len(user_subs)):
                sub = user_subs[index]
                marks = form.cleaned_data.get('question_{index}_marks'.format(index=index))
                try:
                    sub.marks = int(marks)
                    sub.save()
                    sum += marks
                except Exception as e:
                    print(e)
                    pass

        user.profile.marks = sum
        user.save()

        return redirect('quiz:submissions')

    form = MarksForm(user=user)
    return render(
        request, "quiz_front_end/submission.html",
        {
            'form': form,
            'user': user,
        })
