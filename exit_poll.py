import whoosh.index as index
from whoosh import qparser
from whoosh.qparser import QueryParser
import sys

"""
Here is how a classical config will look like
{
  "label_column" : "senti",
  "label_densities" : { "A" : 0.1, "B" : 0.6, "C" : 0.3 }
}

"""

__LABEL_COLUMN__ = "label_column"
__LABEL_DENSITIES__ = "label_densities"


def naive_counter(result, config):
    return 1


def weighted_score(result, config):
    return result.score


def normalised_weighted_score(result, config):
    label_value = result[config[__LABEL_COLUMN__]]
    relative_freq = config[__LABEL_DENSITIES__][label_value]
    return result.score * (1.0 / relative_freq)


def do_exit_poll(results, config, mapper_algorithm=naive_counter):
    resp = dict()
    n = 0.0
    # init
    for label in config[__LABEL_DENSITIES__]:
        resp[label] = 0.0
    # process
    for r in results:
        cur_score = mapper_algorithm(r, config)
        n += cur_score
        label_value = r[config[__LABEL_COLUMN__]]
        resp[label_value] += cur_score
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
            print("Enter Statement to Classify (q to exit):")
            search_text = sys.stdin.readline()
            if search_text.strip() == 'q':
                break
            query = qp.parse(search_text)
            results = searcher.search(query)
            do_exit_poll(results, label_config, prediction_algorithm)
    pass
