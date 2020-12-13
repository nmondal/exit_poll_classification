import csv
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
__TEXT_COLUMN__ = "text_column"
__PREDICTION_COLUMN__ = "_p"
__LABEL_MAP__ = "label_mapping"
__ID_COLUMN__ = "id_column"
__DO_PRINT__ = False


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
        if __DO_PRINT__:
            print(r)
    if n != 0.0:
        max_val = 0
        max_label = ''
        for label in resp:
            resp[label] /= n
            if resp[label] > max_val:
                max_label = label
                max_val = resp[label]
        resp[__PREDICTION_COLUMN__] = max_label
        if __DO_PRINT__:
            print (resp)
    else:
        if __DO_PRINT__:
            print ('Sorry!')
    return resp


def predict_classification(search_index_dir, label_config, prediction_algorithm=naive_counter):
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


def verify_classification(question_bank_csv_location, question_bank_config,
                          search_index_dir, label_config, prediction_algorithm=naive_counter):
    ix = index.open_dir(search_index_dir)
    with ix.searcher() as searcher:
        qp = QueryParser("text", ix.schema, group=qparser.OrGroup)
        with open(question_bank_csv_location) as csvfile:
            reader = csv.DictReader(csvfile)
            id_column = question_bank_config[__ID_COLUMN__]
            label_column = question_bank_config[__LABEL_COLUMN__]
            text_column = question_bank_config[__TEXT_COLUMN__]
            label_map = question_bank_config[__LABEL_MAP__]
            for row in reader:
                t_id = unicode(row[id_column])
                t_label = unicode(row[label_column])
                t_text = row[text_column].decode('utf-8')
                query = qp.parse(t_text)
                results = searcher.search(query)
                prediction = do_exit_poll(results, label_config, prediction_algorithm)
                if __PREDICTION_COLUMN__ in prediction:
                    if t_label not in label_map:
                        print ('{} : {} vs {}'.format(t_id, t_label, prediction))
                    else:
                        matched = label_map[t_label] == prediction[__PREDICTION_COLUMN__]
                        print ('{} : {} : {} vs {}'.format(t_id, matched, t_label, prediction))
                    pass
                else:
                    print ('{} : FAILED'.format(t_id))

    pass
