from numpy import array
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm.classes import LinearSVC as SVC
import nltk
from sklearn.metrics.classification import recall_score, precision_score, f1_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from unicodedata import normalize

dataset = pd.read_csv('datasetFunk.csv') #carrega o dataset

dataset = dataset.dropna(thresh=2)

#Normalização do texto
dataset.letra = dataset.letra.str.replace(r'\b[a-zA-Z]*\d+[a-zA-Z]*\b', '') #remove todas as palavras que contenham numero
dataset.letra = dataset.letra.str.replace(r'\s\s+', ' ') #remove espaços a mais
dataset.letra = dataset.letra.str.lower() #coloca tudo em minusculo
#dataset.letra = dataset.letra.map(lambda x: normalize('NFKD', x).encode('ASCII', 'ignore').decode("utf-8").strip())

#criacao o dicionario
#dict = []
#cont = 0
#for t in dataset.letra[:]:
#    for w in t.split():
#        dict.append(w)

#dict = set(dict) #dict agora contem todas as palavras existentes no dataset
#dict_array = list(dict) #precisa transformar pois o fit do label encoder nao aceita set

#separar o dataset em uma parte para fit e outra para predict
letras_train, letras_test, label_train, label_test = train_test_split(dataset.letra, dataset.label, test_size=0.30, random_state=42)

#uso do LinearSVC
clf = SVC(C=1, loss='squared_hinge', penalty='l1', dual=False)

#print(dict_array)

#rotinas para alimentar o LabelEnconder
label_encoder = LabelEncoder()
int_encoded_fit = label_encoder.fit_transform(letras_train)
int_encoded_pred = label_encoder.fit_transform(letras_test)

#dict_encode = label_encoder.fit(dict_array)

#test_encode = []
#cont = 0
#while cont < 10:
#    test_encode.append(dataset.letra[cont].split())
#    cont += 1

#teste = label_encoder.transform(test_encode[0])


#Rotinas para alimentar o OneHotEncoder
onehot = OneHotEncoder()

int_encoded_fit = int_encoded_fit.reshape(len(int_encoded_fit), 1)
int_encoded_pred = int_encoded_pred.reshape(len(int_encoded_pred), 1)

letra_fit = onehot.fit_transform(int_encoded_fit)
letra_pred = onehot.transform(int_encoded_pred)

#Utilização do SVM
clf.fit(letra_fit, label_train)

prediction = clf.predict(letra_pred)

print()
print("Recall {}".format(recall_score(label_test, prediction,average='weighted')))
print("Precision {}".format(precision_score(label_test, prediction,average='weighted')))
print("F1 {}".format(f1_score(label_test, prediction,average='weighted')))
print("Accuracy {}".format(accuracy_score(label_test, prediction)))
