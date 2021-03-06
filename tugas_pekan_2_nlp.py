# -*- coding: utf-8 -*-
"""Tugas Pekan 2 - NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15pq6ojYUofj3SlUj4UUHmE6LqxmLvhBM

# **Language Model Unigram Bigram**
Topik : Cyber Crime Whatsapp


---
Clarisa Hasya Y - 1301174256
"""

import pandas as pd
from glob import glob
import operator
import nltk
nltk.download('punkt')

#Read file txt
data = []
list_of_files = glob('a*.txt')   
for file_name in list_of_files:
  f = open(file_name, 'r', encoding='utf-8')
  data.append(f.read())
  f.close()
# data

df = pd.DataFrame(data, columns=['text'])
# df

"""Case Folding"""

#Mengubah text menjadi lowercase
df['text'] = df['text'].apply((str.lower))
# df.head()

"""Tokenisasi"""

mod_sentences = [] # array/list untuk menampung semua kalimat teks awal
for par in df['text']:
  sent_text = nltk.sent_tokenize(par) # tokenisasi menjadi beberapa kalimat

  # loop per kalimat, tambahkan tag <s> di awal kalimat dan </s> di akhir kalimat 
  for sentence in sent_text:
    mod_sentence = [] # array/list untuk menampung kalimat setiap paragraf
    sent_tokens = nltk.word_tokenize(sentence)
    mod_sentence.append('<s>')
    for token in sent_tokens:
      mod_sentence.append(token)
    mod_sentence.append('</s>')          
    mod_sentences.append(mod_sentence) 

# print(mod_sentences[0])
# print(len(mod_sentences))

"""Frekuensi Unigram"""

freq_tab = {}
total_count = 0
for sentence in mod_sentences:
  for token in sentence:
    if token in freq_tab:
        freq_tab[token] += 1 # kata sudah ada di dictionary, update frekuensinya
    else:
        freq_tab[token] = 1 # kata belum ada di dictionary 
    total_count += 1
        
# print('Frekuensi Unigram')
# print(freq_tab)
# print(len(freq_tab))
# print(total_count)


# 10 Unigram yang paling sering muncul

print('-----------------------------------------------------')
sorted_u = dict(sorted(freq_tab.items(), key=operator.itemgetter(1),reverse=True)[:10])
print('10 Unigram yang paling sering muncul')
for x,y in sorted_u.items():
  print(x,y)
print('-----------------------------------------------------')

"""Probabilitas Unigram"""

prob_tab = {}
for token in freq_tab:
    prob_tab[token] = freq_tab[token]/total_count
    
# print('Probabilitas Unigram')
# print(prob_tab)


"""Frekuensi Bigram"""

freq_bigram_tab = {}
for sentence in mod_sentences:
  for i in range (1, len(sentence)):
    curr_bigram = (sentence[i-1], sentence[i])
    if curr_bigram in freq_bigram_tab:
      freq_bigram_tab[curr_bigram] += 1 # bigram sudah ada di dictionary, update frekuensinya
    else:
      freq_bigram_tab[curr_bigram] = 1 # bigram belum ada di dictionary

# print('Frekuensi Bigram')
# print(freq_bigram_tab)

"""Probabilitas Bigram"""

bigram_prob_tab = {}
for sentence in mod_sentences:
  for i in range (1, len(sentence)):
    curr_bigram = (sentence[i-1], sentence[i])

    if curr_bigram not in bigram_prob_tab:  
      bigram_prob_tab[curr_bigram] = freq_bigram_tab[curr_bigram]/freq_tab[sentence[i-1]] # bigram belum ada di dictionary, hitung probability  
 
# print('Probabilitas Bigram')
# print(bigram_prob_tab)

# 10 Bigram dengan probability paling tinggi

sorted_b = dict(sorted(bigram_prob_tab.items(), key=operator.itemgetter(1),reverse=True)[:10])
print('10 Bigram dengan probability paling tinggi')
for x,y in sorted_b.items():
  print(x,y)
print('-----------------------------------------------------')  

def tokenisasi(sentence_test):
  sentence_test = sentence_test.lower()
  sentence_test = nltk.sent_tokenize(sentence_test) # tokenisasi menjadi beberapa kalimat

  # loop per kalimat, tambahkan tag <s> di awal kalimat dan </s> di akhir kalimat 
  mod_sentences = [] # array untuk menampung semua kalimat
  for sentence in sentence_test:
    mod_sentence = [] # array/list untuk menampung kalimat setiap paragraf
    tokens = nltk.word_tokenize(sentence)
    mod_sentence.append('<s>')
    for token in tokens:
      mod_sentence.append(token)
    mod_sentence.append('</s>')          
    mod_sentences.append(mod_sentence)

  return mod_sentences

def cek_bigram(mod_sentences):
  tot_prob = 1.0
  for sentences in mod_sentences:
    for i in range (1, len(sentences)):
      curr = (sentences[i-1], sentences[i]) 
      if curr in bigram_prob_tab:
        tot_prob *= bigram_prob_tab[curr] # jika bigram kalimat uji ada di prob bigram, maka prob bigram kalimat uji akan dikalikan dengan prob bigramnya
      else:
        tot_prob *= 0 # jika bigram kalimat uji tidak ada di prob bigram, maka prob bigram kalimat uji akan dikalikan dengan 0

      # print(tot_prob)

  return tot_prob

def cek_bigram_smoothing(mod_sentences):
  tot_prob = 1.0
  for sentences in mod_sentences:
    for i in range (1, len(sentences)):
      curr = (sentences[i-1], sentences[i]) 
      if curr in freq_bigram_tab: # jika bigram kalimat uji ada di freq bigram, maka freq_b bernilai freq_bigram yang didapat dari data train, dan freq_u bernilai freq_unigram yang didapat dari data train
        freq_b = freq_bigram_tab[curr]
        freq_u = freq_tab[sentences[i-1]] 
        # tot_prob *= freq_bigram_tab[curr] + 1 / freq_tab[sentences[i-1]] + len(freq_tab)
      elif sentences[i-1] in freq_tab: # jika bigram kalimat uji tidak ada di freq bigram, tetapi unigram kalimat uji ada di freq unigram, maka freq_b bernilai 0, dan freq_u bernilai freq_unigram yang didapat dari data train
        freq_b = 0
        freq_u = freq_tab[sentences[i-1]]
        # tot_prob *= 1 / freq_tab[sentences[i-1]] + len(freq_tab)
      else: # jika bigram dan unigram kalimat uji tidak ada di freq bigram dan freq unigram, maka freq_b dan freq_u bernilai 0
        freq_b = 0
        freq_u = 0

      tot_prob *= (freq_b + 1 ) / (freq_u + len(freq_tab))

      # print(tot_prob)
  return tot_prob

def perplexity(prob, sentence_test):
  if prob != 0:
    plex = (1/prob)**(1/len(sentence_test)) #jika probability bigram kalimat uji bukan 0, dihitung perplexitynya
    # print('panjang sentence test',len(sentence_test))
  else:
    plex = 0
    # print('panjang sentence test',len(sentence_test))
  return plex

#Read file sentence_test.txt
  
fs = open('sentence_test.txt', 'r')
sentences_test = (fs.read().splitlines())
fs.close()
# print('Kalimat Uji')
# sentences_test

for sentence_test in sentences_test:
  mod_sentence = tokenisasi(sentence_test)
  print(mod_sentence)

  # non smoothing
  print('Non Smoothing')
  prob = cek_bigram(mod_sentence)
  print('Probabilitas Bigram : ', prob)
  perplex = perplexity(prob,mod_sentence[0])
  print('Perplexity : ', perplex)

  #smoothing
  print('Smoothing')
  prob_s = cek_bigram_smoothing(mod_sentence)
  print('Probabilitas Bigram : ', prob_s)
  perplex_s = perplexity(prob_s,mod_sentence[0])
  print('Perplexity : ', perplex_s)

  print('===========================================================')