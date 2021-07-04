import nltk
import string
from nltk.corpus import stopwords
import itertools
import collections

def tokenize(comments):
    # tokenize the comment as words
    nltk.download('punkt', download_dir='downloads_cache')
    tokens = [token.lower() for c in comments for token in nltk.word_tokenize(c)]
    return tokens


def filter_words(tokens):

    # remove single punctuation: "[", "]", ":", "," etc
    tokens = [t for t in tokens if t not in string.punctuation]

    # remove stopwords
    nltk.download('stopwords', download_dir='downloads_cache')
    tokens = [t for t in tokens if t not in stopwords.words('german')]

    return tokens


def analyze_words(tokens, top_count=50):
    fdict = nltk.FreqDist(tokens)
    sorted_fdict = collections.OrderedDict({k: v for k, v in sorted(fdict.items(), key=lambda item: item[1], reverse=True)})
    selected_words = {k: v for k, v in itertools.islice(sorted_fdict.items(), 0, top_count)}

    return selected_words


reactions = [['beifall'], ['zuruf', 'zurufe'], ['lachen'], ['heiterkeit'], ['sagen', 'sagt'], ['reden', 'rede'], ['hört'], ['wissen'], [ 'steht'], [ 'lesen'], ['kommen', 'kommt'], ['erzählen']]
performers =  [['spd'], ['cdu/csu'], ['gruene', 'grünen', '90/die grünen', '90/die' , '90/diegrünen'] ,['fdp'], ['afd'], ['linke', 'linken']]

def as_reaction_and_performer(comments, reactions=reactions, performers=performers):
    result = []
    for c in comments:
        c = c.lower()
        result.append({
            "reactions": [rarr[0] for rarr in reactions if any(r in c for r in rarr)],
            "performers": [parr[0] for parr in performers if any(p in c for p in parr)]
        })
    return result


class ReactionParser:
    @staticmethod
    def parse_comment(comment):
        c = comment.lower()

        # parse reactions
        parsed_reactions = [rarr[0] for rarr in reactions if any(r in c for r in rarr)]
        parsed_reactions.sort()

        # split the comment corresponding with reactions
        split_comments = []
        current_start = 0
        next_start = -1
        for i in range(1, len(parsed_reactions)):
            next_start = c.index(parsed_reactions[i])
            split_comments.append(c[current_start:next_start])
            current_start = next_start
        split_comments.append(c[current_start:])

        # parse the performers for each reaction
        parsed_performers = []
        for sub_c in split_comments:
            sub_performers = [parr[0] for parr in performers if any(p in sub_c for p in parr)]
            sub_performers.sort()
            parsed_performers.append(sub_performers)

        # parse result to string and normalize
        result = ' '.join([str("COMMENT_" + r) + '_' + '_'.join(p) for r, p in zip(parsed_reactions, parsed_performers)])
        result = result.replace('/', '_').upper()
        return result
