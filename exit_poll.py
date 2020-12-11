import whoosh.index as index
from whoosh import qparser
from whoosh.qparser import QueryParser
import sys

"""
Here is how a classical config will look like
{
  "label_column" : "senti",
  "labels" : [ "A", "B", "C", ... ]
}

"""


def naive_counter(r):
    return 1


def weighted_score(r):
    return r.score


def do_exit_poll(results, config, mapper_algorithm=naive_counter):
    resp = dict()
    n = 0.0
    # init
    for label in config["labels"]:
        resp[label] = 0.0
    # process
    for r in results:
        n += mapper_algorithm(r)
        label_value = r[config["label_column"]]
        resp[label_value] += mapper_algorithm(r)
        print(r)
    if n != 0.0:
        for label in resp:
            resp[label] /= n
        print (resp)
    else:
        print ('Sorry!')


def predict_sentiment(search_index_dir, label_config, prediction_algorithm=naive_counter):
    ix = index.open_dir(search_index_dir)
    with ix.searcher() as searcher:
        qp = QueryParser("text", ix.schema, group=qparser.OrGroup)
        while True:
            print("Enter Statement to Analyze Sentiment:")
            search_text = sys.stdin.readline()
            if search_text.strip() == 'q':
                break
            query = qp.parse(search_text)
            results = searcher.search(query)
            do_exit_poll(results, label_config, prediction_algorithm)
    pass
