import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string
import itertools
import collections
import re


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
performers =  [['spd'], ['cdu/csu'], ['gruene', 'grünen', '90/die' , '90/diegrünen', 'bündnis', 'bündnisses'], ['fdp'], ['afd'], ['linke', 'linken']]


def as_reaction_and_performer(comments, reactions=reactions, performers=performers):
    result = []
    for c in comments:
        c = c.lower()
        result.append({
            "reactions": [rarr[0] for rarr in reactions if any(r in c for r in rarr)],
            "performers": [parr[0] for parr in performers if any(p in c for p in parr)]
        })
    return result


def replace_special_cases(string):
    string = re.sub(r"abg\.", "Abgeordneten", string, flags=re.IGNORECASE)
    string = re.sub(r"–", ".", string, flags=re.IGNORECASE)
    return string


def unparentheses(string):
    return string[1:-1] if string[1] == "(" and string[-1] == ")" else string


class ReactionParser:
    @staticmethod
    def parse_comment(comment):
        # preprocess
        cstr = comment.lower()
        cstr = unparentheses(cstr)
        cstr = replace_special_cases(cstr)
        cs = sent_tokenize(cstr, language="german")

        # parse comments
        parsed_reactions, parsed_performers = [], []
        for c in cs:
            if ":" in c:
                sub_reaction = "SPEECH"
            else:
                # TODO: report error case (if parsed_reactions more then one)
                rs = [rarr[0] for rarr in reactions if any(r in c for r in rarr)]
                sub_reaction = rs[0] if len(rs) > 0 else "UNSPECIFIED"
            sub_performers = sorted([parr[0] for parr in performers if any(p in c for p in parr)])
            parsed_reactions.append(sub_reaction)
            parsed_performers.append(sub_performers)

        parsed = sorted(zip(parsed_reactions, parsed_performers), key = lambda x:x[0])

        # parse result to string and normalize
        result = ' '.join([str(r) + '_' + '_'.join(p) for r, p in parsed])
        result = result.replace('/', '_').upper()
        return result
