# Import the EvaDB package
import evadb
import warnings
warnings.filterwarnings("ignore")

# Connect to EvaDB and get a database cursor for running queries
cursor = evadb.connect().cursor()

# List all the built-in functions in EvaDB
# print(cursor.query("SHOW FUNCTIONS;").df())
cursor.query("DROP TABLE IF EXISTS MyPDFs").df()
cursor.query("LOAD PDF 'Shreyas_Kanjalkar_Resume.pdf' INTO MyPDFs").df()
res = cursor.query("""
    SELECT *
    FROM MyPDFs
    WHERE page = 1 AND paragraph = 3
""").df()
print("Result is ", res)

function = cursor.query("""
    CREATE FUNCTION IF NOT EXISTS TextClassifier
    TYPE HuggingFace
    TASK 'text-classification'
    MODEL 'distilbert-base-uncased-finetuned-sst-2-english'
""").df()
print("Function is ", function)

text_summarization = cursor.query("""
    CREATE FUNCTION IF NOT EXISTS TextSummarizer
    TYPE HuggingFace
    TASK 'summarization'
    MODEL 'facebook/bart-large-cnn'
""").df()

print("Text summrization is ", text_summarization)

final_op = cursor.query("""
    SELECT data, TextSummarizer(data)
    FROM MyPDFs
    WHERE page = 1 AND paragraph >= 1 AND paragraph <= 3 AND TextClassifier(data).label = 'NEGATIVE'
""").df()

print("Final is ", final_op)