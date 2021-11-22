
import nltk
nltk.download('wordnet')
import csv
import pprint
import random
from nltk.corpus import wordnet as wn

with open('../csv/student.csv') as f1:
    reader = csv.reader(f1)
    st = [row for row in reader]

with open('../csv/verb.csv') as f2:
    reader = csv.reader(f2)
    verb = [row for row in reader]

with open('../csv/adverb.csv') as f3:
    reader = csv.reader(f3)
    adv = [row for row in reader]

print(st)
print(verb)
print(adv)

sscounter=0
idx=2

# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'

def convert(word, from_pos, to_pos):    #nltk
    """ Transform words given from/to POS tags """

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [l]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w:-w[1])

    # return all the possibilities sorted by probability
    # return result
    n=result[0][0]
    if n[0]=="a" or n[0]=="e" or n[0]=="i" or n[0]=="o" or n[0]=="u":
      noun = "an " + n
    else:
      noun = "a " + n
    return noun
    

def verb_judge(x):
    if x==0:
      return 0    # remained stable
    elif x>0:
      return 1    # increased, rose, climbed 
    else:
      return -1   # decreased, fell, dropped

def adv_judge(x):
    if x>15:
      return 1   # big
    else:
      return 0   # small

def select_subject(s):
    global sscounter
    if(sscounter==3):
      sscounter=0
    a = s
    target = ' of'
    idx = a.find(target)
    b = a[:idx]   # ofより前を抽出
    c = "It"
    subject_list = [a,b,c]
    v=subject_list[sscounter]
    sscounter += 1
    return  v

def fbt_pick(list1,diff): #from,by,to
    global idx
    if idx==len(list1):
      idx=2   
    fbt_list = []
    fbt_list.append("from " + list1[idx-1][0] +  " by " + str(diff)) # from by
    fbt_list.append("from " + list1[idx-1][0] + " to " + list1[idx][0])  # from to
    #fbt_list.append("by " + str(diff) + " to " + list1[idx][0]) # by to
    idx += 1
    return fbt_list[random.choice([0,1])]

def make_sentence(list1,list2,list3): # list1:student  list2:verb list3:adverb
    slist = []
    for i in range(len(st)-2):
      subject = select_subject(list1[0][0])
      th=random.choice([0,1])
      s = subject+" "
      diff = int(list1[i+2][1])-int(list1[i+1][1])
      vj = verb_judge(diff)
      adv = adv_judge(abs(diff))
      if th==0:
        sentence = s
        if vj==0:
          sentence += list2[0][0]
        elif vj==1:
          sentence += list2[1][random.choice([0,1,2])] + " "
        else:
          sentence += list2[2][random.choice([0,1,2])] + " "
      else:
        sentence = "There is "
        if vj==0:
          sentence += "no change"
        elif vj==1:
          #a=convert(list2[1][random.choice([0,1,2])],WN_VERB,WN_NOUN)
          #sentence += a[0][0] + " "
          sentence += convert(list2[1][random.choice([0,1,2])],WN_VERB,WN_NOUN) + " in " + s.lower()
        else:
          #b=convert(list2[2][random.choice([0,1,2])],WN_VERB,WN_NOUN)
          #sentence += b[0][0] + " "
          sentence += convert(list2[2][random.choice([0,1,2])],WN_VERB,WN_NOUN) + " in " + s.lower()
      if vj!=0:
        if adv==1:
          sentence += list3[0][random.choice([0,1])]
        else:
          sentence += list3[1][random.choice([0,1])]
          
      if vj!=0:
         fbt = fbt_pick(list1,abs(diff))

      if random.choice([0,1])==0: #fbt,sentence
        sentence = fbt[0].upper()+fbt[1:] + ", " + sentence.lower() 
      else:                       #sentence fbt
        sentence+= " " + fbt
                  
      if vj!=0:
        if "by" not in sentence:
          sentence+=" by "+ str(abs(diff))
      sentence+="."
      slist.append(sentence)
    return slist


#main
sentence = []
sentence=make_sentence(st,verb,adv)
for s in sentence:
  print(s)

