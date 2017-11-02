# coding=UTF-8

from __future__ import division
import re
import sys
import nltk
import nltk.data
from nltk.corpus import brown
from senticnet.senticnet import Senticnet
import re
import sys

# This tool was written by Max Sorto on October, 2016
# and it uses the text summarization algorithm
# Created by Shlomi Babluki on April, 2013


class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_sentences_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)

stock = sys.argv[1]
date = sys.argv[2]
article = 1
total_avg_polarity = 0

while (article <= 5):

    file = stock + '/' + date + '_2016/' + str(article) + '.txt'

    try:
        fp = open(file)
        article += 1  
        data = fp.read()

        # print sentences

        title = data.split('\n', 1)[0]

        content = data

        # Create a SummaryTool object
        st = SummaryTool()

        # Build the sentences dictionary
        sentences_dic = st.get_sentences_ranks(content)

        # Build the summary with the sentences dictionary
        sentences = st.get_summary(title, content, sentences_dic)

        # print sentences

        ## instantiate senticnet

        sn = Senticnet()

        counter = 0
        total = 0

        words = re.compile('\w+').findall(sentences)

        for word in words:
            word = word.lower()
            try:
                print word 
                polarity = sn.polarity(word)
                counter += 1
                total += polarity

                # print counter, word, polarity              
            except:
                pass
    except:
        break

    # Print average polarity score
    avg_polarity = total/counter
    print avg_polarity
    total_avg_polarity += avg_polarity

    # # Print the ratio between the summary length and the original length
    # print ""
    # print "Original Length %s" % (len(title) + len(content))
    # print "Summary Length %s" % len(words)
    # print "Summary Ratio: %s" % (100 - (100 * (len(words) / (len(title) + len(content)))))

print 'Average polarity for ' + str((article-1)) + ' article(s): ' + str(total_avg_polarity/(article-1))