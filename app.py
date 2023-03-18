from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_index import Document, GPTTreeIndex
import os
import json
import PyPDF2
import base64
import io

with open('config.json', 'r') as f:
    config = json.load(f)

os.environ["OPENAI_API_KEY"] = config['api_key']

app = Flask(__name__)
CORS(app)
index = None

@app.route('/initialize', methods=['POST'])
def initialize_index():
    global index
    data = request.get_json()
    base64_string = data['pdf']
    decode = base64.b64decode(base64_string)
    pdf_file = io.BytesIO(decode)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    pdf_text = ''

    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text = page_obj.extract_text()
        pdf_text += text
    pdf_file.close()
    document = [Document(pdf_text)]
    index = GPTTreeIndex(document)
    return jsonify({"response": "Index created successfully."})

@app.route('/query', methods=['POST'])
def query_index():
    query_data = request.get_json()
    query = query_data['query']
    response = index.query(query)
    return jsonify({"response" : response.response})

if __name__ == '__main__':
    app.run(host="198.44.132.153")