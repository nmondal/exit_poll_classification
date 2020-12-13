from exit_poll import verify_classification, weighted_score

INDEX_DIR = "./index_1"
LABEL_CONFIG = {
    "label_column": "senti",
    "label_densities": {"positive": 0.16, "negative": 0.63, "neutral": 0.21}
}
QUESTION_BANK_CSV = "./data_dir/Tweets.csv"
QUESTION_CSV_CONFIG = {"id_column": "tweet_id", "label_column": "airline_sentiment", "text_column": "text",
                       "label_mapping": {"positive": "positive", "negative": "negative", "neutral": "neutral"}}


def do_self_testing():
    verify_classification(QUESTION_BANK_CSV, QUESTION_CSV_CONFIG, INDEX_DIR,
                          LABEL_CONFIG, prediction_algorithm=weighted_score)
    pass


if __name__ == '__main__':
    do_self_testing()
