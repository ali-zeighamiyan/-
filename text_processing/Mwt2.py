import string
import time 
from nltk.tokenize import MWETokenizer
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

start_time=time.time()
stop_words = list(stopwords.words("english"))
puncts=["''", ".", "``", "'", "''" , "[" ,"]", '(',')', ':',';',',',' ']
adds=stop_words+puncts

f=open("C:\\Users\\abc\Desktop\\nltk1\\Wikipedia_AI_article.txt","r")
str=f.read().lower()

mwt_list=['artificial intelligence','artificial intelligent','machine learning','machine translation','machine perception','machine consciousness','artificial Consciousness','Human Compatible','advanced web','neuromorphic computing','human mind','human speech','machine intelligence','cognitive skills','Google Search','online advertisements','virtual assistants','character recognition','intelligent behaviour']
mwt_tuple=[]
for W_word in mwt_list:
    t=tuple(word_tokenize(W_word))
    mwt_tuple.append(t)
    
mwe = MWETokenizer(mwt_tuple, separator=' ')
words=mwe.tokenize(word_tokenize(str))
tokens_without_sw = [word for word in words if word not in adds]

print(tokens_without_sw)

print("--- %s seconds ---" % (time.time() - start_time))

