from exit_poll import verify_classification, weighted_score

INDEX_DIR = "./index_2"
LABEL_CONFIG = {
    "label_column": "senti", "label_densities": {"4": 0.5, "0": 0.5},
    "limit": 15
}
QUESTION_BANK_CSV = "./data_dir/Tweets.csv"
QUESTION_CSV_CONFIG = {"id_column": "tweet_id", "label_column": "airline_sentiment", "text_column": "text",
                       "label_mapping": {"positive": "4", "negative": "0"}}


def do_cross_testing():
    verify_classification(QUESTION_BANK_CSV, QUESTION_CSV_CONFIG, INDEX_DIR,
                          LABEL_CONFIG, prediction_algorithm=weighted_score)
    pass


if __name__ == '__main__':
    do_cross_testing()
