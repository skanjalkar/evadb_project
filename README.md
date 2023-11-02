# evadb_resume_matcher
## Shreyas Kanjalkar

What is EvaDB?
## EvaDB: Database System for AI-Powered Applications

EvaDB is designed to simplify the development of AI-powered applications by enabling software developers to build such applications using just a few lines of SQL code. It provides a robust SQL API that simplifies AI app development for handling both structured and unstructured data.

## Features

- **Simple SQL API**: Build and deploy AI-powered apps using a few short, simple SQL queries over data stored in your existing SQL and vector database systems.
- **Pre-Trained AI Models**: Query your data with pre-trained AI models from renowned AI platforms like Hugging Face, OpenAI, YOLO, PyTorch, and other AI engines.
- **AI-Centric Query Optimization**: Save significant time and resources on AI app development via AI-centric query optimization and execution.

## Use Cases

EvaDB is versatile and suited for a wide range of AI applications including:

- Regression Analysis
- Classification Tasks
- Image Recognition
- Question Answering Systems
- Generative AI Applications

The database system is engineered to address 99% of AI problems that are often repetitive and can be automated with a simple function call in an SQL query. This makes it a valuable tool for automating a broad spectrum of AI tasks without needing a deep understanding of the underlying AI or ML technologies.

## EvaDB: Resume Matcher

This application makes use of EvaDB to do a matching of resume with jobs. The highlevel idea of how it works is as follows

1. Load resumes into PDF into table using EvaQL
2. Pick one resume from the table, and parse that resume.
3. Using that parsed info, create context and pass it to LLM such as GPT 3.5
4. Load job descriptions into a table using EvaQL
5. Parse job descriptions in a for loop and for each job description using the context of resume, get a percentage matching of the resume to the particular job

## Running the application:

In order to run the application, go to ```resume_evadb_project.py``` and first insert your OpenAI key. Let's first set that up

## Setting Up Environment Variables

It's a good practice to keep sensitive data like your OpenAI API key in a `.env` file to keep your project secure. Here's how to set it up without using the `dotenv` module:

### Step 1: Create a .env file

Create a `.env` file in the root directory of your project. Inside this file, specify your OpenAI API key like so:

```export OPENAI_API_KEY=your-api-key-here```

### Step 2: Source the .env file

Before running the ```resume_evadb_project.py``` file, ensure that you run ```source .env```.

## Back to running the application:

Load the job descriptions into JobDescription folder. Provide the path to resume in the file. I will update it so that you will just have to laod it into a resume folder, similar to JobDescription.