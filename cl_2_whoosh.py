import csv
from whoosh.index import create_in
from whoosh.fields import *
import whoosh.index as index
from whoosh import qparser
from whoosh.qparser import QueryParser

INDEX_DIR = "./index_2"
DATA_FILE = "./data_dir/training.1600000.processed.noemoticon.csv"
FIELDS = ["target", "tid", "date", "flag", "user", "text"]


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


def analyze(results):
    N = 0.0
    pos = 0
    neg = 0
    for r in results:
        N += 1.0
        if r["senti"] == '4':
            pos += 1
        elif r["senti"] == '0':
            neg += 1
        print(r)
    print ('pos : {}  neg : {}'.format(pos / N, neg / N))


def predict_sentiment():
    ix = index.open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        qp = QueryParser("text", ix.schema, group=qparser.OrGroup)
        while True:
            print("enter>")
            search_text = sys.stdin.readline()
            if search_text == 'q':
                return
            query = qp.parse(search_text)
            results = searcher.search(query)
            analyze(results)
    pass


if __name__ == '__main__':
    # import_data()
    predict_sentiment()
