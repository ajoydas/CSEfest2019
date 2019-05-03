import datetime
import random
from math import ceil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Puzzle, Submission, Meme, Music, Submitted
from core.models import Profile
from django.http import HttpResponse
import json
import random



# generate meme
# def gen_meme(submission, profile):
#     # for code writing
#     ###### must comment ######
#     submission = Submission.objects.get(id = 1)
#     profile = Profile.objects.get(user = 1)
#
#     # for failure
#     # showing on every {frequency} no of image once and
#     # random freq before {threshold} no of tries for a single image is {random_freq_before}
#     # random freq after {threshold} no of tries for a single image is {random_freq_after}
#
#     if submission.accepted is False:
#         type = 0
#         frequency = 5
#         threshold = 10
#         random_freq_before = 1/10
#         random_freq_after = 1/5
#         puzzle_threshold = 1/frequency
#
#         # meme already showed for current section
#         if profile.showed_meme:
#             return None
#
#         rand = random.uniform(0, 1)
#         if rand < puzzle_threshold:
#             return None
#
#         if submission.tried < threshold:
#             rand = random.uniform(0, 1)
#             if rand > random_freq_before:
#                 return None
#
#             return get_meme(type, profile.account_type)
#
#         rand = random.uniform(0, 1)
#         if rand < random_freq_after:
#             return get_meme(type, profile.account_type)
#
#         return None
#
#     # for success
#     # must show image if got success on {must_threshold} of tries
#     # must show image if got success on {max_threshold} of tries
#     # random freq before {random_threshold} no of tries for a single image is {random_freq}
#     # random freq after {random_threshold} no of tries for a single image is 0
#
#     type = 1
#     must_threshold = 2
#     max_threshold = 30
#     random_threshold = 10
#     random_freq = 1/5
#
#     # must show the meme case
#     if submission.tried < must_threshold or submission.tried>max_threshold:
#         return get_meme(type, profile.account_type)
#
#     if submission.tried < random_threshold:
#         rand = random.uniform(0,1)
#         if rand < random_freq:
#             return get_meme(type, profile.account_type)
#
#     return None

# get random meme based on meme type and account type
def get_meme(type, account_type):
    # print(type)
    # print(account_type)
    # memes = Meme.objects.filter(Q(type=type) & Q(account_type=account_type))
    memes = Meme.objects.filter(type=type)
    if memes.count() == 0:
        return None

    rand = random.randint(0, memes.count()-1)
    return memes[rand]


def gen_meme(submission, profile):
    # for code writing
    ###### must comment ######
    # submission = Submission.objects.get(id = 1)
    # profile = Profile.objects.get(user = 1)

    # for failure
    # showing on every {frequency} no of image once and
    # random freq before {threshold} no of tries for a single image is {random_freq_before}
    # random freq after {threshold} no of tries for a single image is {random_freq_after}

    if submission.accepted is False:
        # threshold_lower = 2
        # threshold_upper = 6
        # random_freq_lower = 1/3
        # random_freq_upper = 1/2
        type = 0
        threshold_lower = settings.THRESHOLD_LOWER
        threshold_upper = settings.THRESHOLD_UPPER
        random_freq_lower = settings.RANDOM_FREQ_LOWER
        random_freq_upper = settings.RANDOM_FREQ_UPPER

        # meme already showed for current section
        if submission.showed_meme:
            return None

        if submission.tried > threshold_upper:
            rand = random.uniform(0, 1)
            if rand > random_freq_upper:
                return None

            submission.showed_meme = True
            submission.save()
            return get_meme(type, profile.account_type)

        if submission.tried > threshold_lower:
            rand = random.uniform(0, 1)
            if rand > random_freq_lower:
                return None

            submission.showed_meme = True
            submission.save()
            return get_meme(type, profile.account_type)

        return None

    # for success
    # must show image if got success on {must_threshold} of tries
    # must show image if got success on {max_threshold} of tries
    # random freq before {random_threshold} no of tries for a single image is {random_freq}
    # random freq after {random_threshold} no of tries for a single image is 0

    # must_threshold = 5
    # max_threshold = 8
    # random_threshold = 5
    # random_freq = 1 / 2

    type = 1
    must_threshold = settings.MUST_THRESHOLD
    max_threshold = settings.MAX_THRESHOLD
    random_threshold = settings.RANDOM_THRESHOLD
    random_freq = settings.RANDOM_FREQ

    # must show the meme case
    if submission.tried <= must_threshold or submission.tried > max_threshold:
        return get_meme(type, profile.account_type)

    if submission.tried < random_threshold:
        rand = random.uniform(0,1)
        if rand < random_freq:
            return get_meme(type, profile.account_type)

    return None


def puzzle(request, pk):
    if request.user.is_authenticated is False:
        return redirect('core:login_user')

    if request.method == 'GET':
        if request.user.profile.level_completed == pk - 1:
            puzzle = Puzzle.objects.filter(Q(pk=pk) & Q(visible=True))

            if puzzle is None or puzzle.count() !=1:
                # if contest has ended
                if settings.ENDED_CONTEST:
                    return render(request, 'puzzle_front_end/end.html')
                else:
                    return render(request, 'puzzle_front_end/wait.html')

            puzzle = puzzle.get()
            pk = puzzle.id
            img_url = puzzle.get_image()

            # add title
            if puzzle.title is None or puzzle.title == '':
                title = 'none'
            else:
                title = puzzle.title

            # ADD FEATURE: BACK MUSIC
            music = "none"
            if settings.BACK_MUSIC:
                musics = Music.objects.all()
                if musics.count() != 0:
                    rand = random.randint(0, musics.count()-1)
                    music = musics[rand].music.url

            # ADD FEATURE: FUN FACT
            if settings.SHOW_FUN_FACT is False or puzzle.fact is None or puzzle.fact == '':
                fun_fact = "none"
            else:
                fun_fact = puzzle.fact

            return render(request, 'puzzle_front_end/puzzle.html', {
                'pk': pk,
                'img_url': img_url,
                'title': title,
                'music': music,
                'fun_fact': fun_fact
            })

        elif request.user.profile.level_completed > pk - 1:
            return redirect('puzzle:show_puzzle', request.user.profile.level_completed+1)
        else:
            return redirect('puzzle:hacker_man')



def add_meme(response_data, submission, user):
    if settings.SHOW_MEME:
        meme = gen_meme(submission, user)
    else:
        meme = None

    # send meme as json data
    if meme is None:
        response_data['meme'] = 'false'
    else:
        response_data['meme'] = 'true'
        if bool(meme.image) == False:
            response_data['meme_text'] = 'none'
            response_data['meme_image'] = 'none'
        else:
            response_data['meme_text'] = meme.text
            response_data['meme_image'] = meme.image.url

        # ADD FEATURE: MEME MUSIC
        if settings.MEME_MUSIC is False or bool(meme.sound) == False:
            response_data['meme_sound'] = 'none'
        else:
            response_data['meme_sound'] = meme.sound.url

    return response_data


@login_required
def submit_puzzle(request, pk):
    user = request.user
    profile = request.user.profile
    # print(user)

    if request.method != 'POST':
        return redirect('puzzle:hacker_man')

    if profile.level_completed != pk - 1:
        return redirect('puzzle:hacker_man')

    response_data = {}
    answer = request.POST.get('answer', '')
    # if submission error happens
    if answer == '':
        response_data['result'] = 'error'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    answer = answer.strip().lower()
    # print(answer)

    puzzles = Puzzle.objects.filter(Q(pk=pk) & Q(visible=True))
    if puzzles is None or puzzles.count() != 1:
        return redirect('puzzle:hacker_man')

    puzzle = puzzles[0]
    # save this try to submitted
    submitted = Submitted(user=user, puzzle=puzzle, text=answer)
    submitted.save()

    # get submission or create new submission
    submissions = Submission.objects.filter(Q(user=user) & Q(puzzle= puzzle))
    if submissions is None or submissions.count() != 1:
        submission = Submission(user=user, puzzle=puzzle, tried=1)
    else:
        submission = submissions[0]
        submission.user = user
        submission.puzzle = puzzle
        submission.tried += 1

    puzzle_ans = puzzle.ans.strip().lower()
    # answer matched, successful submissions
    if answer == puzzle_ans:
        profile.level_completed += 1
        profile.last_sub = datetime.datetime.now()
        user.save()

        # save submission
        submission.accepted = True
        submission.save()

        # make result as success
        response_data['result'] = 'success'

        # ADD FEATURE: MEME
        response_data = add_meme(response_data, submission, profile)

        # ADD FEATURE: INFO
        response_data['show_info'] = 'no'
        if settings.SHOW_INFO:
            if puzzle.info is not None:
                response_data['show_info'] = 'yes'
                response_data['info'] = puzzle.info
            else:
                response_data['info'] = 'none'

            if puzzle.info_link is not None:
                response_data['show_info'] = 'yes'
                response_data['info_link'] = puzzle.info_link
            else:
                response_data['info_link'] = 'none'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    # answer did not match, wrong submission
    else:
        submission.accepted = False
        submission.save()

        response_data['result'] = 'error'
        # ADD FEATURE: MEME
        response_data = add_meme(response_data, submission, profile)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def leader_board(request):
    page_length = 10

    user_list = Profile.objects.filter(user__is_superuser = False).order_by('-level_completed','last_sub')

    # user_list = Profile.objects.order_by('-level_completed')
    paginator = Paginator(user_list, page_length)  # Show 25 contacts per page

    page = request.GET.get('page')
    if page is None:
        page = 1
        if request.user.is_authenticated:
            user_id = request.user.id
            for i in range(user_list.count()):
                if user_list[i].id == user_id:
                    page = ceil((i+1)/page_length)
                    break

    try:
        rank = page_length * (int(page)-1)
        users = paginator.get_page(page)
    except:
        return redirect('puzzle:hacker_man')

    return render(request, 'puzzle_front_end/leader_board.html', {
        'users' : users,
        'rank': rank
    })


def hacker_man(request):
    print("Calling....")
    _account_type_ = request.user.profile.account_type
    if _account_type_ == 0:
        # Alumni
        _type = 0
    else:
        # Student
        _type = 1

    hack_text = [
        'ভাই আমার গার্লফ্রেন্ডের ফেইসবুক একাউন্টটা হ্যাক করে দিবা ?',
        'স্যারা ভাই স্যারা.......... পুরা হ্যাকার',
        'ও বাই ও বাই.......... স্যারা',
        'স্যারা ভাই স্যারা.......... পুরা হ্যাকার',
        'ping cute-hamster.com',
        'Ever wonder Freddie Mercury was also a black hat hacker like you'
    ]

    img_folder = 'image/meme/hacking/'
    hack_images = [
        'hack1.jpg', 'hack2.jpg', 'hack3.jpg', 'hack4.jpg', 'hack5.jpg', 'hack6.png',
    ]

    if _type == 0:
        # Alumni
        x = random.randint(1, 6)
        # new meme and caption for alumni
        return render(request, 'puzzle_front_end/student_hacker.html', {
            'hack_txt': hack_text[x-1],
            'hack_img': img_folder + hack_images[x-1]
        })

    else:
        # Student
        # show a bit more slang caption for student
        x = random.randint(1, 6)
        return render(request, 'puzzle_front_end/student_hacker.html', {
            'hack_txt': hack_text[x - 1],
            'hack_img': img_folder + hack_images[x - 1]
        })

