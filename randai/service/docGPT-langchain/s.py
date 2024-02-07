import os
import tempfile
import logging
import argparse
from docGPT import GPT4Free, create_doc_gpt
from model import DocumentLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = ''
SERPAPI_API_KEY = ''
model = None

def load_api_keys(openai_api_key, serpapi_api_key):
    os.environ['OPENAI_API_KEY'] = openai_api_key
    os.environ['SERPAPI_API_KEY'] = serpapi_api_key

def upload_and_process_document(file_path):
    docs = DocumentLoader.load_documents(file_path)
    docs = DocumentLoader.split_documents(
        docs, chunk_size=2000,
        chunk_overlap=200
    )
    return docs

def create_model(docs, provider):
    global model
    model = create_doc_gpt(
        docs,
        {k: v for k, v in docs[0].metadata.items() if k not in ['source', 'file_path']},
        provider
    )
    logger.info(f'Created model: {model}')

def get_response(query):
    global model
    try:
        if model is not None and query:
            response = model.run(query)
            logger.info(f'LLM Response: {response}')
            return response
        return (
            'Your model still not created.\n'
            '1. If you are using gpt4free model, '
            'try to re-select a provider.\n'
            '2. If you are using openai model, '
            'try to re-pass openai api key.\n'
            '3. Or you did not pass the file successfully.'
        )
    except Exception as e:
        logger.error(f'Error in docGPT: {e}')
        return (
            'Something wrong in docGPT...\n'
            '1. If you are using gpt4free model, '
            'try to select the different provider.\n'
            '2. If you are using openai model, '
            'check your usage for openai api key.'
        )

def main():
    # parser = argparse.ArgumentParser(description='Document GPT CLI')
    # parser.add_argument('--openai_api_key', type=str, required=True, help='OpenAI API Key')
    # parser.add_argument('--serpapi_api_key', type=str, required=True, help='SERPAPI API Key')
    # parser.add_argument('--file_path', type=str, required=True, help='Path to the document file')
    # parser.add_argument('--provider', type=str, required=True, help='Provider for GPT4Free')
    # args = parser.parse_args()
    file_path = "/home/mohammed/Projects/randapi/randai/output.pdf"
    provider = "GptGo"
    # load_api_keys(args.openai_api_key, args.serpapi_api_key)
    docs = upload_and_process_document(file_path)
    create_model(docs, provider)

    while True:
        query = input("Enter your question: ")
        if query == 'exit':
            break
        response = get_response(query)
        print("Response:", response)

if __name__ == "__main__":
    main()
