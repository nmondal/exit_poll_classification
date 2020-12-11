import csv
from whoosh.index import create_in
from whoosh.fields import *

from exit_poll import predict_sentiment, weighted_score

INDEX_DIR = "./index_1"
DATA_FILE_LOCATION = "./data_dir/Tweets.csv"
LABEL_CONFIG = {"label_column": "senti", "labels": ["positive", "negative", "neutral"]}


def import_data():
    schema = Schema(tid=ID(stored=True), senti=TEXT(stored=True), text=TEXT(stored=True))
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()
    with open(DATA_FILE_LOCATION) as csvfile:
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


if __name__ == '__main__':
    # import_data()
    predict_sentiment(INDEX_DIR, LABEL_CONFIG, weighted_score)
