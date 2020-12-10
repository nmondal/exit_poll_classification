import csv
from whoosh.index import create_in
from whoosh.fields import *
import whoosh.index as index
from whoosh import qparser
from whoosh.qparser import QueryParser


INDEX_DIR = "./indexdir"


def import_data():
    schema = Schema(tid=ID(stored=True), senti=TEXT(stored=True), text=TEXT(stored=True))
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()
    with open('Tweets.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        line = 0
        for row in reader:
            line += 1
            t_id = unicode(row['tweet_id'])
            t_senti = unicode(row['airline_sentiment'])
            t_text = row['text'].decode('utf-8')
            t_text = unicode(t_text.split(' ', 1)[1])
            writer.add_document(tid=t_id, senti=t_senti, text=t_text)
            print(line)
        writer.commit()
    pass


def predict_sentiment(search_text):
    ix = index.open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        query = QueryParser("text", ix.schema, group=qparser.OrGroup).parse(search_text)
        results = searcher.search(query)
        N = 0.0
        pos = 0
        neg = 0
        neu = 0
        for r in results:
            N += 1.0
            if r["senti"] == "positive":
                pos += 1
            elif r["senti"] == "negative":
                neg += 1
            else:
                neu += 1
            print(r)
        print ('pos : {} neu : {} neg : {}'.format(pos/N, neu/N, neg/N))
    pass


if __name__ == '__main__':
    #import_data()
    predict_sentiment("I think this is awesome!")
