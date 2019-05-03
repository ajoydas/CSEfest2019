# setup Django to load models and apps
import datetime
import os
from math import ceil

from django.core.wsgi import get_wsgi_application
from django.db.models import Q
from wordcloud import WordCloud

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "picture_puzzle.settings")
application = get_wsgi_application()


from django.contrib.auth.models import User
from core.models import Profile
from puzzle.models import Tag, Puzzle, Submission, Meme, Submitted

dir = "generated/"

# Tag - Puzzle pie
import matplotlib.pyplot as plt
import numpy as np

labels = []
sizes = []

tags = Tag.objects.all()
for tag in tags:
    puzzles = Puzzle.objects.filter(tag=tag).count()
    labels.append(tag.name)
    sizes.append(puzzles)

x = np.char.array(labels)
y = np.array(sizes)
percent = 100.*y/y.sum()

patches, texts = plt.pie(y, startangle=90, shadow=True, radius=1.25)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
                                          key=lambda x: x[2],
                                          reverse=True))

plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.5, 1.),
           fontsize=8)
plt.title("Percentage of Tags in the Puzzles")
plt.savefig(dir+'tag_puzzle_pie.png', bbox_inches='tight')
plt.show()


# user type pie
total = User.objects.filter(is_superuser=False).count()
student = User.objects.filter(Q(is_superuser=False) & Q(profile__account_type=1)).count()
alumni = User.objects.filter(Q(is_superuser=False) & Q(profile__account_type=0)).count()
print("Total: "+str(total)+", Student: "+str(student)+", Alumni: "+str(alumni))
labels = ["Students", "Alumni"]
sizes = [student, alumni]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontsize': 18})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Percentage of Account Type")
plt.savefig(dir+'usertype_pie.png', bbox_inches='tight')
plt.show()



solved_dict = {}
unsolved_dict = {}
mintry_dict = {}
maxtry_dict = {}
meme_dict = {}

mintime_dict = {}
solver_dict = {}

for i in range(1,76):
    solved_dict[i] = 0
    unsolved_dict[i] = 0
    mintry_dict[i] = 1000000
    maxtry_dict[i] = 0
    meme_dict[i] = 0

    mintime_dict[i] = datetime.datetime.now()
    solver_dict[i] = None

user_total = []
users = User.objects.filter(is_superuser=False)
for user in users:
    total_subm = 0
    submissions = Submission.objects.filter(user=user)
    for subm in submissions:
        puzzle = subm.puzzle.id
        if subm.accepted :
            solved_dict[puzzle] += 1
        else:
            unsolved_dict[puzzle] += 1

        if mintry_dict[puzzle] > subm.tried:
            mintry_dict[puzzle] = subm.tried

        if maxtry_dict[puzzle] < subm.tried:
            maxtry_dict[puzzle] = subm.tried

        if subm.showed_meme:
            meme_dict[puzzle] += 1

        subm_time = subm.updated_at.replace(tzinfo=None)
        if subm.accepted and mintime_dict[puzzle] > subm_time:
            mintime_dict[puzzle] = subm_time
            solver_dict[puzzle] = subm.user.username

        total_subm += subm.tried

    user_total.append([user.username, total_subm])

for i in range(1,76):
    print(i, end=": ")
    print(solved_dict[i], end=" ")
    print(unsolved_dict[i], end=" ")
    print(mintry_dict[i], end=" ")
    print(maxtry_dict[i], end=" ")
    print(meme_dict[i], end=" ")

    print(solver_dict[i], end="\n")


tags = Tag.objects.all()
tag_solved = {}
tag_unsolved = {}

for tag in tags:
    tag_solved[tag.name] = 0
    tag_unsolved[tag.name] = 0

    puzzles = Puzzle.objects.filter(tag=tag)
    for puzzle in puzzles:
        tag_solved[tag.name] += solved_dict[puzzle.id]
        tag_unsolved[tag.name] += unsolved_dict[puzzle.id]

    print(tag.name, end=": ")
    print(tag_solved[tag.name], end=" ")
    print(tag_unsolved[tag.name])


def draw_tried(n_groups, tag_names,tag_tried,
               tag_solved_list, xlabel, ylabel, title, bar1, bar2, filename):
    import matplotlib.pyplot as plt
    import numpy as np

    # from matplotlib.pyplot import figure
    # figure(num=None, figsize=(10, 6))

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, tag_tried, bar_width,
    alpha=opacity,
    color='b',
    label=bar1)

    rects2 = plt.bar(index + bar_width, tag_solved_list, bar_width,
    alpha=opacity,
    color='g',
    label=bar2)

    # def autolabel(rects):
    #     """
    #     Attach a text label above each bar displaying its height
    #     """
    #     for rect in rects:
    #         height = rect.get_height()
    #         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
    #                 '%d' % int(height),
    #                 ha='center', va='bottom')
    #
    # autolabel(rects1)
    # autolabel(rects2)


    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index + bar_width, tag_names)
    plt.legend()

    plt.tight_layout()
    plt.setp(ax.get_xticklabels(), fontsize=7, rotation=60)
    plt.savefig(dir + filename, bbox_inches='tight')
    plt.show()


# Tag vs solve
n_groups = tags.count()
tag_names = []
tag_tried = []
tag_solved_list = []
for tag in tags:
    tag_names.append(tag.name)
    tag_tried.append(tag_solved[tag.name] + tag_unsolved[tag.name])
    tag_solved_list.append(tag_solved[tag.name])

draw_tried(n_groups, tag_names, tag_tried, tag_solved_list,
           "Tags", '# of Unique Submissions', 'Tags vs Unique Submissions',
           'Total Tried', 'Total Solved', 'tag_subm_bar.png')

# Puzzle related plots
puzzles = Puzzle.objects.all()

puzzle_names = []
puzzle_tried = []
puzzle_solved_list = []
puzzle_mintry = []
puzzle_maxtry = []
puzzle_meme = []
for puzzle in puzzles:
    puzzle_names.append(str(puzzle.id)+": "+puzzle.ans)
    puzzle_tried.append(solved_dict[puzzle.id] + unsolved_dict[puzzle.id])
    puzzle_solved_list.append(solved_dict[puzzle.id])

    puzzle_mintry.append(mintry_dict[puzzle.id])
    puzzle_maxtry.append(maxtry_dict[puzzle.id])

    puzzle_meme.append(meme_dict[puzzle.id])

n_groups = 15
for i in range(1, ceil(puzzles.count()/n_groups)+1):
    # Puzzle vs submission
    draw_tried(n_groups, puzzle_names[(i-1)*n_groups: i*n_groups], puzzle_tried[(i-1)*n_groups: i*n_groups], puzzle_solved_list[(i-1)*n_groups: i*n_groups],
               "Puzzles", '# of Unique Submissions', 'Puzzles vs Unique Submissions',
            'Total Tried', 'Total Solved', 'puzzle_subm_bar'+str(i)+'.png')

    # Puzzle vs max & min tries
    draw_tried(n_groups, puzzle_names[(i-1)*n_groups: i*n_groups], puzzle_maxtry[(i-1)*n_groups: i*n_groups], puzzle_mintry[(i-1)*n_groups: i*n_groups],
               "Puzzles", '# of Submissions', 'Puzzles vs max & min # of submissions by a single user',
            'Max Submission', 'Min Submission', 'puzzle_tries_bar'+str(i)+'.png')

    # Puzzle vs # of memes
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    y_pos = np.arange(n_groups)
    plt.bar(y_pos, puzzle_meme[(i-1)*n_groups: i*n_groups], align='center',
            color=(0.2, 0.4, 0.6, 0.6), alpha=0.8)
    plt.xticks(y_pos, puzzle_names[(i-1)*n_groups: i*n_groups])
    plt.xlabel("Puzzles")
    plt.ylabel("# of MEMEs Showed")
    plt.title("Puzzles vs # of MEMEs Showed")
    plt.setp(ax.get_xticklabels(), fontsize=7, rotation=60)
    plt.savefig(dir + 'puzzle_meme'+str(i)+'.png', bbox_inches='tight')
    plt.show()

# 1st solvers
inv_map = {}
for k, v in solver_dict.items():
    inv_map[v] = inv_map.get(v, 0)
    inv_map[v] += 1

print(inv_map)
print(inv_map.keys())
print(inv_map.values())

n_groups = len(inv_map)

# User vs total # of puzzles 1st solved by them
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

fig, ax = plt.subplots()
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

y_pos = np.arange(n_groups)
plt.bar(y_pos, inv_map.values(), align='center', color='g', alpha=0.8)
plt.xticks(y_pos, inv_map.keys())
plt.xlabel("Username")
plt.ylabel("# of puzzles")
plt.title("Users vs # of puzzles 1st solved")
plt.setp(ax.get_xticklabels(), fontsize=7, rotation=90)
plt.savefig(dir + 'user_first_solved.png', bbox_inches='tight')
plt.show()


# Top user with maximum tries
# print(user_total)
import numpy as np

user_total = sorted(user_total,key=lambda x: x[1], reverse=True)[0:20]
user_total = np.array(user_total)
# print(user_total)
print(user_total[:,0])
print(user_total[:,1].astype(int))

n_groups = user_total.shape[0]
# User vs total # of puzzles solved by them
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

fig, ax = plt.subplots()
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

y_pos = np.arange(n_groups)
plt.bar(y_pos, user_total[:,1].astype(int), align='center', color='r', alpha=0.8)
plt.xticks(y_pos, user_total[:,0])
plt.xlabel("Username")
plt.ylabel("# of total submission")
plt.title("User with maximum # of submissions")
plt.setp(ax.get_xticklabels(), fontsize=7, rotation=90)
plt.savefig(dir + 'user_max_tries.png', bbox_inches='tight')
plt.show()


