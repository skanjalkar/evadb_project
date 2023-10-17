import evadb
from collections import defaultdict
from evadb.configuration.constants import EvaDB_INSTALLATION_DIR

def test():
    cursor = evadb.connect().cursor()
    path_to_job = "./JobDescription/*.pdf"

    cursor.query("""CREATE FUNCTION IF NOT EXISTS TextSummarizer
            TYPE HuggingFace
            TASK 'summarization'
            MODEL 'facebook/bart-large-cnn';""").df()

    cursor.query("""DROP TABLE IF EXISTS JobDescription""").df()
    cursor.query(f"LOAD PDF '{path_to_job}' INTO JobDescription").df()
    res = cursor.query("SELECT * FROM JobDescription").df()

    info = defaultdict(str)
    for _row_id, _data in res.iterrows():
        # get all data for same row id given by _data[_row_id]
        info[_data['_row_id']] += _data['data']

    cursor.query("""DROP TABLE IF EXISTS JobDescriptionSummary""").df()
    cursor.query("""CREATE TABLE IF NOT EXISTS JobDescriptionSummary(id INTEGER, summary TEXT)""").df()
    print(cursor.query("""SELECT * FROM JobDescriptionSummary""").df())
    # print(info)
    # Remove the comment for hard code check
    cursor.query(f"""INSERT INTO JobDescriptionSummary (summary) VALUES ('{info[1]}')""").df()
    for key, val in info.items():
        print(cursor.query(f"INSERT INTO JobDescriptionSummary (id, summary) VALUES ({key}, '{val}')").df())

if __name__ == "__main__":
    test()