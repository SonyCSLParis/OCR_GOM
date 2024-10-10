import numpy as np
import json
from tqdm import tqdm
from symspellpy import SymSpell, Verbosity
import numpy as np
from spellchecker import SpellChecker


def mk_dict():
   f=open("data/FrantextAvr.txt", encoding="ISO-8859-1")
   lines = f.readlines()
   d = {}
   
   f=open("data/mydict.txt","w")
   for l in lines[1:]:
      r=l.strip("\n").split('\t')
      if r[0]: 
         f.write(r[0]+"\t"+r[1]+"\n")
         d[r[0]]=float(r[1])  

   morph = list(json.load(open("data/morphalouV3.json")).keys())

   for m in tqdm(morph, desc="Looking into Morph"):
      if (m and not(m in d)):
         f.write(m+"\t"+"0"+"\n")
         d[m]=0

   json.dump(d,open("mydict.json","w"))
   return d

def spellchecker():
   spell = SpellChecker()
   spell.word_frequency.load_dictionary('./mydict.json')

   file = open("data/oov_nltk.txt")
   oov = file.readlines()
   oov = [l.strip('\n') for l in oov]

   cors={}
   for word in oov:
      cors[word] = spell.correction(word)
   return cors 

def symspell():
   dictionary_path = "data/mydict.txt"
   sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
   sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)   

   file = open("data/oov_nltk.txt")
   oov = file.readlines()
   oov = [l.strip('\n') for l in oov]   

   cors = {}
   for i in range(len(oov)):
       input_term = oov[i]
       suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST, max_edit_distance=2, transfer_casing=True)   

       if len(suggestions): 
           nn1 = [s for s in suggestions if s.distance==1]
           if len(nn1):
              mc = 0
              for s in nn1:
               if s.count>mc: cors[input_term]=s.term
           else: 
               nn2 = [s for s in suggestions if s.distance==2]
               if len(nn2):
                  mc = 0
                  for s in nn1:
                      if s.count>mc: cors[input_term]=s.term
       else: cors[input_term]=[""]
   return cors

d=mk_dict()
