import evadb
import openai
import os
from collections import defaultdict
from evadb.configuration.constants import EvaDB_INSTALLATION_DIR


cursor = evadb.connect().cursor()
path_to_job = "Resume-Matcher/Data/JobDescription/*.pdf"

def read_text_line(path, num_token=1000):
    """#write description here
    Args:
        path ([type]): [description]
        num_token (int, optional): [description]. Defaults to 1000.
    Yields: None
    """
    # For simplicity, we only keep letters.
    whitelist = set(".!?abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890 %")

    with open(path, "r") as f:
        line_itr = 0
        for line in f.readlines():
            line_itr = line_itr + 1
            if line_itr % 10 == 0:
                print("line: " + str(line_itr))
            for i in range(0, len(line), num_token):
                cut_line = line[i : min(i + 1000, len(line))]
                cut_line = "".join(filter(whitelist.__contains__, cut_line))
                yield cut_line

            if line_itr == 1000:
                break

def write_dict_to_files(data_dict, directory_path):
    """#write description here
    Args: data_dict: map of data which contains key value pari to be written to seperate files
          directory_path: path of directory where files will be written
    Yields: None
    """
    import os

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Iterate through the dictionary and write each key-value pair to a separate file
    for key, value in data_dict.items():
        file_path = os.path.join(directory_path, f"{key}.txt")
        with open(file_path, "w") as file:
            file.write(str(value))


def text_summarizer():
    """Summary of the function: This function will take the job description and summarize it using the hugging face model in built in evadb
    Args: None
    Returns: final_data: list of summarized job description
    """
    cursor.query("""CREATE FUNCTION IF NOT EXISTS TextSummarizer
        TYPE HuggingFace
        TASK 'summarization'
        MODEL 'facebook/bart-large-cnn';""").df()

    cursor.query("""DROP TABLE IF EXISTS JobDescription""").df()
    cursor.query(f"LOAD PDF '{path_to_job}' INTO JobDescription").df()

    res = cursor.query("SELECT * FROM JobDescription").df()
    # res = res.tolist()
    # print(res)
    # empty list to store the data
    info = defaultdict(str)
    for _row_id, _data in res.iterrows():
        # get all data for same row id given by _data[_row_id]
        info[_data['_row_id']] += _data['data']
    directory_path = "./output_directory"
    write_dict_to_files(info, directory_path)


    # return info
    # print(info)
    # drop table if exists
    cursor.query("""DROP TABLE IF EXISTS JobDescriptionSummary""").df()
    cursor.query(f"""LOAD DOCUMENT '{directory_path}/*.txt' INTO JobDescriptionSummary""").execute()
    print(cursor.query("""SELECT * FROM JobDescriptionSummary""").df())
    # print(info[1])
    # cursor.query(f"""INSERT INTO JobDescriptionSummary (summary) VALUES ('{info[1]}')""").df()
    # for key, val in info.items():
    #     print(cursor.query(f"INSERT INTO JobDescriptionSummary (id, summary) VALUES ({key}, '{val}')").df())

    # print the info from JobDescriptionSummary
    # res = cursor.query("SELECT * FROM JobDescriptionSummary").df()
    # print(res)


    max_id = cursor.query("""SELECT MAX(_row_id) FROM JobDescription""").df()
    # #print max_id
    max_id = max_id['_row_id'].tolist()
    max_id = int(max_id[-1])
    print(max_id)
    final_data = []
    for i in range(max_id):
        temp_data = cursor.query(f"SELECT TextSummarizer(data) FROM JobDescriptionSummary WHERE _row_id = {i+1}").df()
        final_data.append(temp_data['summary_text'].tolist())

    for data in final_data:
        print("This is the final data", data)
    Text_feat_function_query = f"""CREATE FUNCTION IF NOT EXISTS SentenceFeatureExtractor
            IMPL  '{EvaDB_INSTALLATION_DIR}/functions/sentence_feature_extractor.py';
            """
    cursor.query(Text_feat_function_query).execute()
    cursor.query("""DROP TABLE IF EXISTS FeatureTable""").df()
    cursor.query(
        f"""CREATE TABLE FeatureTable AS
        SELECT SentenceFeatureExtractor(data), data FROM JobDescriptionSummary WHERE _row_id = 1;"""
    ).execute()

    res = cursor.query("""SELECT * FROM FeatureTable""").df()
    print("Final output", res)
    return final_data

def find_match():
    """Find match: This function will take the resume and job description that is given by hugging face and match them using the gpt 3.5 turbo model from openai
    Args: None
    Returns: None
    """
    #get open ai key from .env file
    openai.api_key = "" #OPENAI KEY
    # use the gpt 3.5 turbo model from api of openai
    path_to_resume = "./Resume-Matcher/Data/Resumes/Shreyas_Kanjalkar_Resume.pdf"
    cursor.query("DROP TABLE IF EXISTS MyPDFs").df()
    cursor.query(f"LOAD PDF '{path_to_resume}' INTO MyPDFs").df()


    data = cursor.query("""
        SELECT data
        FROM MyPDFs
    """).df()
    print(data)
    list_data = data['data'].tolist()
    list_string = ''.join(list_data)


    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You will be provided with a block of text about someone's resume, and your task is to extract a list of keywords from it."},
            {"role": "user", "content": f"{list_string}"}
        ]
    )
    resume_summary = completion.choices[0].message
    replies = {}
    final_data_jobs = text_summarizer()
    for i, val in enumerate(final_data_jobs):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are now acting as a professional recruiter. You will be given job description and you have to summarize it so that it can be used to match with the resumes."},
                {"role": "user", "content": f"Here is some context about the resume: {resume_summary}"},
                {"role": "user", "content": f"Match the resume with the job description: {val} and only give me a score based on % from 0 to 100 based on how well the resume keywords matches the job description. Don't give me any extra information, only the percentage score."}
            ]
        )
        replies[i] = completion.choices[0].message
    # print(completion.choices[0].message)
    print(replies)


def main():
    find_match()

if __name__ == '__main__':
    main()