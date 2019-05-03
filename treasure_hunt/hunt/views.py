import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.models import Profile
from hunt.models import TeamGame, TeamTaskStatus, TeamTask, Game, Tries


def get_current_task(team):
    # task_list = TeamTask.objects.filter(team = team).get().tasks
    # tasks = list(map(int, task_list.split(',')))
    unfinished = TeamTaskStatus.objects.filter(team=team).filter(status='n')
    if unfinished.count() != 0:
        return unfinished[0].task

    # process only penalties
    penalties = TeamTaskStatus.objects.filter(team=team).filter(status='p')
    if penalties.count() != 0:
        return penalties[0].task

    return None

# Create your views here.
@login_required
def hunt(request):
    team = request.user
    is_get = request.method != 'POST'
    if team.profile.start_time is None:
        if is_get:
            step = 0
            return render(request, 'hunt_front_end/puzzle.html', {
                    'step': step,
                })

        # validate Post
        start_code = request.POST.get('start_code')
        if start_code != team.profile.start_code:
            step = 0
            messages.add_message(request, messages.ERROR, 'Start Code Doesn\'t Match.')
            return render(request, 'hunt_front_end/puzzle.html', {
                'step': step,
            })

        team.profile.start_time = datetime.datetime.now()
        team.save()
        is_get = True

    current_task = get_current_task(team)
    if current_task is None:
        # Finished all.
        step = 1
        return render(request, 'hunt_front_end/puzzle.html', {
            'step': step,
        })

    try:
        current_state = TeamGame.objects.filter(team=team).filter(game=current_task).get()
    except:
        current_state = TeamGame()
        current_state.team = team
        current_state.game = current_task
        current_state.save()

    print(current_task)
    print(current_state)

    if not current_state.puzzle_finished:
        # Saving puzzle get time
        if current_state.puzzle_get_time is None:
            current_state.puzzle_get_time = datetime.datetime.now()
            current_state.save()

        # puzzle step
        if is_get:
            # show the puzzle file download
            step = 2
            return render(request, 'hunt_front_end/puzzle.html', {
                'step': step,
                'file': current_task.pdf.url
            })

        # validate Post
        puzzle_ans = request.POST.get('puzzle_ans')

        if puzzle_ans is not None and puzzle_ans != "":
            # truncate and clean it
            puzzle_ans = puzzle_ans.strip().lower()
            try:
                # save tries
                tried = Tries()
                tried.team = team
                tried.task = current_task
                tried.text = puzzle_ans
                tried.save()
            except:
                pass

        # validate answer
        current_state.puzzle_tried += 1
        if puzzle_ans != current_task.answer.lower():
            current_state.save()
            step = 2
            messages.add_message(request, messages.ERROR, 'Nope. Wrong Answer. Try Again!')
            return render(request, 'hunt_front_end/puzzle.html', {
                'step': step,
                'file': current_task.pdf.url
            })

        # save game progress
        current_state.puzzle_finished = True
        current_state.puzzle_sub_time = datetime.datetime.now()
        current_state.save()
        is_get = True

    if not current_state.game_finished:
        # if game has started
        if is_get:
            step = 3
            return render(request, 'hunt_front_end/puzzle.html', {
                'step': step,
                'location': current_task.location,
                'location_clue': current_task.location_clue
            })

        # validate Post
        endgame_key = request.POST.get('endgame_key')

        print(endgame_key)
        print(current_task.endgame_key)

        if endgame_key == current_task.penalty_key:
            # penalty the game
            # current_state.startgame_time = None
            current_state.endgame_time = None
            current_state.save()

            # update team's task status
            status = TeamTaskStatus.objects.filter(team=team).filter(task=current_task).get()
            status.status = 'p'
            status.save()

            messages.add_message(request, messages.ERROR, 'You had penalty in the game!')
            return redirect('hunt:hunt')

        if endgame_key != current_task.endgame_key:
            # key validation error
            step = 3
            return render(request, 'hunt_front_end/puzzle.html', {
                'step': step,
                # 'location': current_task.location,
                'location_clue': current_task.location_clue
            })

        # game finished successfully
        messages.add_message(request, messages.SUCCESS, 'Congrats! Finished Level Successfully.')

        current_state.endgame_time = datetime.datetime.now()
        current_state.game_finished = True
        current_state.game_finished_time = datetime.datetime.now()
        current_state.save()

        # update team's task status
        status = TeamTaskStatus.objects.filter(team=team).filter(task=current_task).get()
        status.status = 'y'
        status.save()

        # update level in profile
        team.profile.level_completed += 1
        team.save()

        # go and find out next game
        return redirect('hunt:hunt')

    print(team)
    print(current_state)
    print("Return None Error")
    return None


def get_req_time(team):
    finished = TeamGame.objects.filter(team=team.user).filter(game_finished=True)
    max_time = finished[0].game_finished_time
    for task in finished:
        if max_time < task.game_finished_time:
            max_time = task.game_finished_time

    print(team.user.username+" "+str(max_time))
    return (team, max_time)


# def leader_board(request):
#     # user_list = Profile.objects.filter(user__is_superuser=False).order_by('-level_completed')
#     tuples = []
#     for i in range(10,-1,-1):
#         common_list = Profile.objects.filter(user__is_superuser=False).filter(level_completed=i)
#         commons = []
#         for team in common_list:
#             commons.append(get_req_time(team))
#
#         sorted_list = sorted(commons, key = lambda x: x[1])
#         tuples.extend(sorted_list)
#
#     teams = []
#     for team in tuples:
#         teams.append(team[0])
#
#     return render(request, 'hunt_front_end/leader_board.html', {
#         'teams': teams,
#     })


def leader_board(request):
    # user_list = Profile.objects.filter(user__is_superuser=False).order_by('-level_completed')
    tuples = []
    for i in range(10, 0, -1):
        common_list = Profile.objects.filter(user__is_superuser=False).filter(level_completed=i)
        commons = []
        for team in common_list:
            commons.append(get_req_time(team))

        sorted_list = sorted(commons, key = lambda x: x[1],reverse=False)
        tuples.extend(sorted_list)

    teams = []
    for team in tuples:
        teams.append(team[0])

    no_subs = Profile.objects.filter(user__is_superuser=False).filter(level_completed=0)
    teams.extend(no_subs)

    return render(request, 'hunt_front_end/leader_board.html', {
        'teams': teams,
    })


@user_passes_test(lambda u: u.is_superuser)
def gen_data(request):
    content = ''
    content += 'Teams:\n'
    teams = Profile.objects.all()
    for team in teams:
        content += 'Username: '+ team.user.username + '\n'
        content += 'Password: '+ str(team.password) + '\n'
        content += 'Start Code: '+ str(team.start_code) + '\n'
        try:
            tasks = TeamTask.objects.filter(team=team.user).get().tasks
        except:
            tasks = 'Not assigned.'
        content += 'Task list: ' + tasks +'\n'
        content += '\n\n'

    content += 'Games:\n'
    games = Game.objects.all()
    for game in games:
        content += 'No: '+ str(game.serial_no) + '\n'
        content += 'Answer: '+ game.answer + '\n'
        content += 'Location: '+ str(game.location) + '\n'
        # content += 'Start Key: '+ game.startgame_key+ '\n'
        content += 'End Key: '+ game.endgame_key + '\n'
        content += 'Penalty Key: '+ game.penalty_key + '\n'
        content += '\n\n'

    return HttpResponse(content, content_type='text/plain')


@user_passes_test(lambda u: u.is_superuser)
def gen_graphs(request):

    return HttpResponse("Done", content_type='text/plain')


def details(request):

    return
