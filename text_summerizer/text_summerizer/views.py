from django.http import HttpResponse
from django.shortcuts import render

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from string import punctuation
import pandas as pd
import numpy



# Create your views here.

# def index(request):
#     return render(request, 'index.html')

def index(request):
  
  try:
   text1=request.POST.get('text','default')
   l=request.POST.get('slider-value','0')
   words1=len(text1.split(' '))
   dic={'text': text1,'words1': words1}
   
   if(text1!='default'):
  
    nltk.download('stopwords')

    stop_words=stopwords.words('english')

    
    text=text1
    text1=word_tokenize(text)  
    word_freq={}

    filtered_text=[] 

    for word in text1:
  
     if word.lower() not in stop_words and word.lower() not in punctuation:
     # print(word.lower())
       if word.lower() not in word_freq:
        word_freq[word.lower()]=1
        filtered_text.append(word)

       else:
         word_freq[word.lower()]+=1
         filtered_text.append(word)

    max_freq=max(word_freq.values())

    for word,value in word_freq.items():
        word_freq[word]=value/max_freq


    sent_tokens=sent_tokenize(text)
    sent_freq={}

    for sent in sent_tokens:

     words=word_tokenize(sent)
     for word in words:
      if word.lower() in word_freq.keys():
        if sent not in sent_freq.keys():
         sent_freq[sent]=word_freq[word.lower()]
        else:
         sent_freq[sent]+=word_freq[word.lower()]
    
    
    length=2-2*int(l)/100

    sumValues=0
    for value in sent_freq.values():
     sumValues +=value
    average = int(sumValues / len(sent_freq))

    summary =''
    for sentence in sent_tokens:
     if (sentence in sent_freq) and(sent_freq[sentence] >(length*average)):
       i=0
       while(not sentence[i].isalpha()):
        i+=1
       sentence=sentence[i:]
       if(sentence not in summary):
        summary +=sentence+'  '

    if(len(summary)==0):
        m=max(sent_freq.values())
        sent=[k for k,v in sent_freq.items() if v==m]
        summary=sent[0]

    words2=len(summary.split(' '))
   
    dic['summary'] = summary
    dic['words2']=words2
    dic['val']=l
  
    return render(request,'index.html',dic)
   else:
     return render(request,'index.html')
  except:
    return render(request,'index.html')
  




def summarized(request):
  l=request.POST.get('slider-value','0')
  Text=request.POST.get('text','default')
  dict={'val':l}
  L=100-int(l)
  dict['L']=L
  dict['Text']=Text
  return render(request,'summarized.html',dict)
  
  


