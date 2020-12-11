import csv
from whoosh.index import create_in
from whoosh.fields import *

from exit_poll import predict_sentiment, weighted_score

INDEX_DIR = "./index_2"
DATA_FILE = "./data_dir/training.1600000.processed.noemoticon.csv"
FIELDS = ["target", "tid", "date", "flag", "user", "text"]
LABEL_CONFIG = {"label_column": "senti", "labels": ["4", "0"]}


def import_data():
    schema = Schema(tid=ID(stored=True), senti=NUMERIC(stored=True), text=TEXT(stored=True))
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()
    with open(DATA_FILE) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS)
        line = 0
        for row in reader:
            line += 1
            t_id = unicode(row['tid'])
            t_senti = int(row['target'])
            try:
                t_text = row['text'].decode('utf-8')
                writer.add_document(tid=t_id, senti=t_senti, text=t_text)
            except:
                print ('Error in this!')
                pass
            print(line)

        writer.commit()
    pass


if __name__ == '__main__':
    # import_data()
    predict_sentiment(INDEX_DIR, LABEL_CONFIG, weighted_score)
