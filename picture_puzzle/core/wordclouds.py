# generate wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from puzzle.models import Submitted, Puzzle

for i in range(1,76):
    submitteds = Submitted.objects.filter(puzzle__id=i)
    words = ""
    for submitted in submitteds:
        words = words + submitted.text+ " "

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    min_font_size = 10).generate(words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('generated/wordclouds/'+Puzzle.objects.get(id=i).ans+'.png', bbox_inches='tight')
    plt.show()