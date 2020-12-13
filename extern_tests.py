import csv
from textblob import TextBlob

__LABEL_COLUMN__ = "label_column"
__TEXT_COLUMN__ = "text_column"
__ID_COLUMN__ = "id_column"


def predict_sentiment_by_text_blob(some_text):
    """
    https://pypi.org/project/textblob/
    :param some_text: text to do senti analysis
    :return: True if positive, False if negative
    """
    blob = TextBlob(some_text)
    score = 0.0
    for sentence in blob.sentences:
        #score += sentence.sentiment.polarity
        if sentence.sentiment.polarity > 0.0:
            return True


def run_sentiment_prediction(question_bank_csv_location, question_bank_config, predictor_function,
                             out_file_path='./out.txt'):
    with open(question_bank_csv_location) as csv_file:
        reader = csv.DictReader(csv_file)
        of = open(out_file_path, 'w')
        id_column = question_bank_config[__ID_COLUMN__]
        label_column = question_bank_config[__LABEL_COLUMN__]
        text_column = question_bank_config[__TEXT_COLUMN__]
        line_no = 1
        for row in reader:
            line_no += 1
            print (line_no)
            t_label = unicode(row[label_column])
            if t_label == 'neutral':
                continue
            t_id = unicode(row[id_column])
            t_text = row[text_column].decode('utf-8')
            prediction = predictor_function(t_text)
            matched = prediction and row[label_column] == 'positive'
            of.write('{} : {} : {}\n'.format(t_id, matched, t_label))
            of.flush()
        of.close()


QUESTION_BANK_CSV = "./data_dir/Tweets.csv"
QUESTION_CSV_CONFIG = {"id_column": "tweet_id", "label_column": "airline_sentiment", "text_column": "text",
                       "label_mapping": {"positive": "4", "negative": "0"}}


if __name__ == '__main__':
    run_sentiment_prediction(QUESTION_BANK_CSV, QUESTION_CSV_CONFIG, predict_sentiment_by_text_blob)
    pass
