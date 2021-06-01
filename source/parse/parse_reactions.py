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
performers =  [['spd'], ['cdu/csu'], ['90/die grünen', '90/die' , '90/diegrünen'] ,['fdp'], ['afd'], ['linken', 'linke']]

def as_reaction_and_performer(comments, reactions=reactions, performers=performers):
    result = []
    for c in comments:
        c = c.lower()
        result.append({
            "reactions": [rarr[0] for rarr in reactions if any(r in c for r in rarr)],
            "performers": [parr[0] for parr in performers if any(p in c for p in parr)]
        })
    return result
