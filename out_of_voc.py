from nltk.tokenize import word_tokenize
import nltk
import json
import time
nltk.download('punkt_tab')
import spacy
import unicodedata

def toks_spacy(textfile):
   with open(textfile) as f:
      text = f.read()

   text = unicodedata.normalize('NFC', text)
   
   t0 = time.time() 

   nlp = spacy.load('fr_core_news_sm')
   doc = nlp(text)
   toks_spacy = [token.lemma_ for token in doc]
   utoks_spacy = list(set(toks_spacy))
   print(time.time()-t0)
   return utoks


def toks_nltk(textfile):
   with open(textfile) as f:
      text = f.read()
   text = unicodedata.normalize('NFC', text)
   t0 = time.time() 
   
   toks = word_tokenize(text, language='french')
   utoks = list(set(toks))
   print(time.time()-t0)
   return utoks

def get_oov(toks, d, svg="data/oov.txt"):
   oov=[]
   for t in toks:
      if (not(t.lower() in morph) and not(t.isdigit())):
         if '-' in t:
            res = t.split('-')
            notseen = 0
            for r in res:
                if not(r in morph): notseen = 1
            if notseen: oov.append(t)   
      else: oov.append(t)
   with open(svg, "w") as f:
      for l in oov:
         f.write(l+"\n")
   

    
textfile = "L_école_du_jardin_potager.txt"
toks = toks_nltk(textfile)

d = json.load(open("data/dict_fr.json","w"))
get_oov(toks, d, svg="data/oov.txt")
