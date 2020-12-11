# "Exit Poll" Classification Algorithms



## Based on the Paper 

You can find our paper here : https://arxiv.org/abs/2011.13832

>Supervised text classification is a classical and active area of ML research. In large enterprise, solutions to this problem has significant importance. This is specifically true in ticketing systems where prediction of the type and subtype of tickets given new incoming ticket text to find out optimal routing is a multi billion dollar industry. 
>In this paper authors describe a class of industrial standard algorithms which can accurately ( 86\% and above ) predict classification of any text given prior labelled text data - by novel use of any text search engine. 
>These algorithms were used to automate routing of issue tickets to the appropriate team. This class of algorithms has far reaching consequences for a wide variety of industrial applications, IT support, RPA script triggering, even legal domain where massive set of pre labelled data are already available.





## Test Data Set 

You can download the data sets from :

1. https://www.kaggle.com/crowdflower/twitter-airline-sentiment 
2. https://www.kaggle.com/kazanova/sentiment140



## Setup System 

1. Create a directory called `data_dir`
2. Download the csv files inside them.
3. Install `whoosh` library for python
4. For unknown reason we have used `python 2`.  If you do not like it, you can update to `Python3`.
5. There are two different files you can run to check how they are performing.
   1. `cl_1_whoosh.py` which handles Airline Tweets.
   2. `cl_2_whoosh.py` which handles the millions of tweets



## Algorithms & Results

We have implemented (? It is a joke) two basic methods - do nothing counter - naive counter method, and sum of scores. Results are actually quite fantastic from a human use perspective.

```
Enter Statement to Classify (q to exit):
It’s also heartbreaking to see talented actors like Vikrant Massey and Yami Gautam weighed down by an average script.
....
{'0': 0.5116012503871078, '4': 0.4883987496128922}
Enter Statement to Classify (q to exit):
Both of them perform sincerely and they’re the only reason the film isn’t a complete write off.
....
{'0': 0.4074789098911728, '4': 0.5925210901088273}
```

 In this million data set `0` is negative sentiment, `4` is positive sentiment. 



## Caution

This is a toy to showcase that there are way too many ways to foundational thinking about the discipline of AI. Authors fully understand it - and is mentioned clearly in the paper. There are of course better class of algorithms available to do 2 classification, but for multi-label classification and as an incredibly easy approach - nothing is simpler.

