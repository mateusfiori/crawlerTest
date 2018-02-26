# -*- coding: utf-8 -*-
from scipy.sparse import csr_matrix as sp
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm.classes import LinearSVC as SVC
from sklearn.metrics.classification import recall_score, precision_score, f1_score, accuracy_score
from unicodedata import normalize
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier, LogisticRegression

dataset = pd.read_csv('datasetFunk.csv') #carrega o dataset

dataset = dataset.dropna(thresh=2)

print(dataset.groupby('label').size())

#Normalização
dataset.letra = dataset.letra.str.replace(r'\b[a-zA-Z]*\d+[a-zA-Z]*\b', '') #remove todas as palavras que contenham numero
dataset.letra = dataset.letra.str.replace(r'\s\s+', ' ') #remove espaços a mais
dataset.letra = dataset.letra.str.lower() #coloca tudo em minusculo
dataset.letra = dataset.letra.map(lambda x: normalize('NFKD', x).encode('ASCII', 'ignore').decode("utf-8").strip()) #remove char especial

#separar o dataset em uma parte para fit e outra para predict
letras_train, letras_test, label_train, label_test = train_test_split(dataset.letra, dataset.label, test_size=0.30, random_state=42)

#setando o Stochastic Gradient Descent
sgd = SGDClassifier(loss='hinge', penalty='l2')

#setando Logistic Regression
lr = LogisticRegression()

#setando o Naive Bayes
gnb = GaussianNB()

#setando o LinearSVC
clf = SVC(C=1, loss='squared_hinge', penalty='l1', dual=False)

#usando Countvectorizer, binary = True -> sparce array
vectorizer = CountVectorizer(max_df=0.5, stop_words=nltk.corpus.stopwords.words('portuguese'),
                            analyzer='word', min_df=2, binary=True)

lyric = vectorizer.fit_transform(letras_train)
lyric_test = vectorizer.transform(letras_test)

print(lyric.shape)

#utilizando Logistic Regression
lr.fit(lyric, label_train)
prediction = lr.predict(lyric_test)

#utilizando o SGD
#sgd.fit(lyric, label_train)
#prediction = sgd.predict(lyric_test)

#o formato do input é diferente (precisa ser uma matriz densa)
#Utilizando o naive Bayes
#gnb.fit(sp.todense(lyric), label_train)
#prediction = gnb.predict(sp.todense(lyric_test))

#Utilização do SVM
#clf.fit(lyric, label_train)
#prediction = clf.predict(lyric_test)

print()
print("Recall {}".format(recall_score(label_test, prediction, average='weighted')))
print("Precision {}".format(precision_score(label_test, prediction ,average='weighted')))
print("F1 {}".format(f1_score(label_test, prediction, average='weighted')))
print("Accuracy {}".format(accuracy_score(label_test, prediction)))