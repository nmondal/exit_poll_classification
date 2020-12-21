import csv
from whoosh.index import create_in
from whoosh.fields import *

from exit_poll import predict_classification, weighted_score

INDEX_DIR = "./index_3"
LABEL_CONFIG = {"label_column": "label", "label_densities": {"F": 0.5, "R": 0.5}}
TRAIN_DATA_FILE = "./data_dir/news/train.txt"
TEST_DATA_FILE = "./data_dir/news/test.txt"
FIELD_NAMES = ["title", "text", "sub", "date", "label"]


def import_data():
    schema = Schema(label=TEXT(stored=True), title=TEXT(stored=True), text=TEXT(stored=True))
    ix = create_in(INDEX_DIR, schema)
    writer = ix.writer()
    with open(TRAIN_DATA_FILE) as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')
        line = 0
        for row in reader:
            line += 1
            try:
                t_label = unicode(row['label'])
                t_title = row['title'].decode('utf-8')
                t_text = row['text'].decode('utf-8')
                writer.add_document(title=t_title, text=t_text, label=t_label)
            except Exception as err:
                print ('Failed! ' + str(err))
                pass
            print(line)
        writer.commit()
    pass


if __name__ == '__main__':
    import_data()
