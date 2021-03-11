# OG imports
import sys
import os
import numpy as np
import numpy.random as npr
import pandas as pd
import random

# my imports
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import re
import string
from sklearn.metrics import confusion_matrix as c_m

# Module file with functions that you fill in so that they can be
# called by the notebook. This file should be in the same
# directory/folder as the notebook when you test with the notebook.

# You can modify anything here, add "helper" functions, more imports,
# and so on, as long as the notebook runs and produces a meaningful
# result (though not necessarily a good classifier).  Document your
# code with reasonable comments.

# Function for Part 1
def preprocess(inputfile):

    lemmatizer = WordNetLemmatizer()
    verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

    rows = []
    line = [x.strip().split('\t') for x in inputfile.readlines()[1:]]
    for l in line:
        if l[3] not in verbs:
            if l[2] not in string.punctuation:
                l[2] = lemmatizer.lemmatize(l[2].lower())
                rows.append(l)
        else:
            l[2] = wn._morphy(l[2].lower(), pos = 'v')
            lemmatized = str(l[2]).strip("['").strip("']")
            l[2] = lemmatized
            rows.append(l)

    cols = ["word nº", "sentence nº", "word", "POS tag", "entity type"]

    return pd.DataFrame(rows, columns = cols)

# Code for part 2
class Instance:
    def __init__(self, neclass, features):
        self.neclass = neclass
        self.features = features

    def __str__(self):
        return "Class: {} Features: {}".format(self.neclass, self.features)

    def __repr__(self):
        return str(self)

def create_instances(data):
    
    instances = []
    sent_num = list(data['sentence nº'])
    word = list(data['word'])
    ent_typ = list(data['entity type'])

    sent_word_ent = list(zip(sent_num, word, ent_typ))

    for tup in sent_word_ent:
        if 'B-' in tup[2]: #If it has a tag with B-
            neclass = re.sub('B-', '', tup[2])
            features = []
            start_token = '<start>'
            end_token = '<end>'
            befores = []
            for c_before in range((sent_word_ent.index(tup) - 6),(sent_word_ent.index(tup) - 1)): #The 5 features before the word with a NE
                if sent_word_ent[c_before][0] == tup[0]: #If they belong in the same sentence
                    befores.append(sent_word_ent[c_before][1]) #Append the word
                else:
                    befores.append(start_token)
            features = features + befores
            afters = []
            i = 1
            j = 6
            if (sent_word_ent.index(tup) + j) < len(sent_word_ent):
                for c_after in range((sent_word_ent.index(tup) + i),(sent_word_ent.index(tup) + j)):
                    if sent_word_ent[c_after][0] == tup[0]:
                        afters.append(sent_word_ent[c_after][1])
                    else:
                        afters.append(end_token)
            features = features + afters

            instances.append(Instance(neclass, features))
    return instances

from collections import Counter
# Code for part 3
def create_table(instances):

    vocabulary = []
    for instance in instances:
        for feature in instance.features:
            if feature not in vocabulary:
                vocabulary.append(feature)
    classes = []
    for instance in instances:
        classes.append(instance.neclass)
    
    empty_matrix = np.zeros((len(instances), len(vocabulary)))
    table = pd.DataFrame(empty_matrix, columns = vocabulary)

    i = 0
    for instance in instances:
        for context in instance.features:
            table.loc[i, context] += 1
        i +=1
    
    """
    I tried to order the columns in many ways but by simply appending
    a column in the first position or uniting two dataframes, for some reason,
    didn't work. The only way that it worked was by rearranging the columns after.
    The problem is, though, that in the main matrix it doesn't appear as the
    first column position.
    """
    # new_order = ['class'] + vocabulary
    # table = table.reindex(new_order, axis=1)

    ## https://jakevdp.github.io/PythonDataScienceHandbook/03.02-data-indexing-and-selection.html
    table['class'] = classes
    cs = list(table.columns.values)
    table = table[[cs[-1]]+cs[0:-2]]

    # table.insert(0, "class", classes, True) 

    # classes_df = pd.DataFrame(classes, columns = ['classes'])
    # table = classes_df.join(table)


    return table

    """
    Leaving this here in memory of a DataFrame that technically worked but
    made my test functions have a bunch of errors for some reason I don't know.
    I would very much appreciate to know the reason why it doesn't work
    because I spent hours trying to figure it out and I couldn't :(
    So I had to find a new way to make the matrix, and found out that by
    starting with an empty matrix the train and test functions worked.
    It's such a mystery, really *_*
    """
    # vocabulary = []
    # for instance in instances:
    #     for feature in instance.features:
    #         # if feature not in vocabulary:
    #         vocabulary.append(feature)

    # tags = []
    # for instance in instances:
    #     tags.append(instance.neclass)

    # # c = ['class']
    # # columns = c + vocabulary

    # contexts = []
    # for instance in instances:
    #     contexts.append([instance.features])
    
    # matrix = []
    # tags_vocab = list(zip(tags, contexts))
    # for tag, con in tags_vocab:
    #     for w in con:
    #         vec = [w.count(word) for word in tops]
    #         row = [tag] + vec
    #         matrix.append(row)

    # return pd.DataFrame(matrix, columns = columns)

def ttsplit(bigdf):

    df_train = bigdf.sample(frac = 0.8)
    df_test = bigdf.drop(df_train.index)

    df_train = df_train.reset_index()
    df_test = df_test.reset_index()
        
    return df_train.drop('class', axis=1).to_numpy(), df_train['class'], df_test.drop('class', axis=1).to_numpy(), df_test['class']

# Code for part 5
def confusion_matrix(truth, predictions):

    classes = ['art', 'eve', 'geo', 'gpe', 'nat', 'org', 'per', 'tim']
    confusion = pd.DataFrame(c_m(truth, predictions, labels = classes))
    confusion.index = classes
    confusion.columns = classes

    return confusion

# Code for bonus part B
def bonusb(filename):
    pass
