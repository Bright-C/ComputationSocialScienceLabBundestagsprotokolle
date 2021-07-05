import matplotlib.pyplot as plt
import itertools
import pandas as pd
import re
from scipy.stats import chi2_contingency
from statsmodels.sandbox.stats.multicomp import multipletests
plt.rcParams["font.family"] = "Lucida Sans Unicode"

class ProtocolData:
    def __init__(self, text, datetime_date):
        self.date = datetime_date
        self.member_affiliations = {}
        self.text = text
        self.interjection_locations = {}

        self.protocol_segments = []


        # Bit tricky
        self.words_preceding_interjections = {}

    def add_member(self, name, party):
        self.member_affiliations[name] = party

    def append_protocol_segment(self, segment):
        self.protocol_segments.append(segment)

    def count_word_preceding_interjection(self, word):
        self.words_preceding_interjections[word] = self.words_preceding_interjections.get(word, 0) + 1

    def print_data(self):
        print(self.date)
        print(self.member_affiliations)
        print(self.text)
        print(self.interjection_locations)
        print(self.words_preceding_interjections)
        print(len(self.interjection_locations))

    def print_data_graph(self):
        #drawnDict = dict(reversed(sorted(self.words_preceding_interjections.items(), key=lambda item: item[1])))
        #drawnDict = {k: v for k, v in drawnDict.items() if len(k) > 4 or k.isupper()}
        #drawnDict = dict(itertools.islice(drawnDict.items(), 15))
        #prediction = self.model.predict_output_word(['COMMENT'], topn = 20)

        #Pattern: Word, comment occurences, no comment occurences
        frequency_data = [(key, value, self.total_searched_words[key] - value) for (key, value) in self.most_frequent_words_near_search_words.items() if self.total_searched_words[key] > 3]
        df = pd.DataFrame(frequency_data, columns=["word", "comments", "no_comments"])
        df = df.set_index("word")
        significant_words = chisq_and_posthoc_corrected(df)
        significance_filtered_words = [(key, value) for (key, value) in self.most_frequent_words_near_search_words.items() if key in significant_words]
        relative_frequency_filtered_words = [(key, value / self.total_searched_words[key]) for (key, value) in significance_filtered_words if self.total_searched_words[key] > 3]
        #prediction = list(itertools.islice(self.most_frequent_words_near_search_words.items(), 20))
        prediction = sorted(relative_frequency_filtered_words[:20], key=lambda x: x[1], reverse=False)
        plt.barh([t[0] for t in prediction], [t[1] for t in prediction])
        #axes = plt.gca()
        #axes.set_ylim([0.011363, 0.011366])
        plt.show()

    def plot_significant_words(self):
        frequency_data = [(key, value, self.total_searched_words[key] - value) for (key, value) in self.most_frequent_words_near_search_words.items()]
        df = pd.DataFrame(frequency_data, columns=["word", "comments", "no_comments"])
        df = df.set_index("word")
        significant_words = chisq_and_posthoc_corrected(df)
        significance_filtered_words = [(key, value) for (key, value) in self.most_frequent_words_near_search_words.items() if key in significant_words if self.total_searched_words[key] > 3]
        relative_frequency_filtered_words = [(key, value / self.total_searched_words[key]) for (key, value) in significance_filtered_words]
        prediction = sorted(relative_frequency_filtered_words[:20], key=lambda x: x[1], reverse=False)
        plt.barh([t[0] for t in prediction], [t[1] for t in prediction])
        plt.show()

    def plot_word_count(self, search_pattern):
        pattern = re.compile(search_pattern)
        plotted_words = []
        for word, count in self.total_searched_words.items():
            if pattern.search(word):
                plotted_words.append([word, count])
        plt.barh([t[0] for t in plotted_words], [t[1] for t in plotted_words])
        plt.show()


    def get_full_text(self):
        full_text = ""
        for segment in self.protocol_segments:
            full_text += segment.get_text_equivalent()
        return full_text

def get_asterisks_for_pval(p_val):
    """Receives the p-value and returns asterisks string."""
    if p_val > 0.05:
        p_text = "ns"  # above threshold => not significant
    elif p_val < 1e-4:  
        p_text = '****'
    elif p_val < 1e-3:
        p_text = '***'
    elif p_val < 1e-2:
        p_text = '**'
    else:
        p_text = '*'
    
    return p_text

# https://neuhofmo.github.io/chi-square-and-post-hoc-in-python/
def chisq_and_posthoc_corrected(df):
    """Receives a dataframe and performs chi2 test and then post hoc.
    Prints the p-values and corrected p-values (after FDR correction)"""
    # start by running chi2 test on the matrix
    chi2, p, dof, ex = chi2_contingency(df, correction=True)
    print(f"Chi2 result of the contingency table: {chi2}, p-value: {p}")

    avg_comments = df["comments"].mean()
    avg_no_comments = df["no_comments"].mean()
    # Any random occurence word, interjection afterwards? 
    df.loc["AVERAGE_WORD"] = [avg_comments, avg_no_comments]
    print(df)
    
    #Bonferroni correction
    # post-hoc
    #all_combinations = list(itertools.com(df.index, 2))  # gathering all combinations for post-hoc chi2
    all_combinations = [(index, "AVERAGE_WORD") for index in df.index]
    p_vals = []
    print("Significance results:")
    for comb in all_combinations:
        new_df = df[(df.index == comb[0]) | (df.index == comb[1])]
        chi2, p, dof, ex = chi2_contingency(new_df, correction=True)
        p_vals.append(p)
        # print(f"For {comb}: {p}")  # uncorrected

    # checking significance
    # correction for multiple testing
    reject_list, corrected_p_vals = multipletests(p_vals, method='fdr_bh', alpha=0.05)[:2]
    for p_val, corr_p_val, reject, comb in zip(p_vals, corrected_p_vals, reject_list, all_combinations):
        print(f"{comb}: p_value: {p_val:5f}; corrected: {corr_p_val:5f} ({get_asterisks_for_pval(p_val)}) reject: {reject}")

    result = [comb[0] for p_val, corr_p_val, reject, comb in zip(p_vals, corrected_p_vals, reject_list, all_combinations) if reject]
    return result