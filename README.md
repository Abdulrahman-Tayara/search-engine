# Search Engine Project
It's IR System for search about user's needs in a huge documents corpus.

## Features

- Import your dataset
- Train new models
- Search in your documents by your query
- Spelling correction for your query
- HTTP API
- UI


## Main Componenets
It's an N-Tier Application contains three layers:
- Data Persistence Layer
- Application Layer (Engine Layer)
- Presentation Layer

## IR Models
For now We support two types of indexing:
- TfIdf Index
- Word2Vec Model (Word Embedding)

## Setup

### Clone The Project
```sh
git clone https://github.com/Abdulrahman-Tayara/documents-search-engine.git
```

### Setup MinIO
The system uses MinIO to work with files system as an object storage like AWS S3, this will make the work is more easier.

You can setup MinIO using its docker image, ex:
```sh
mkdir -p ~/minio/data

docker run \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio1 \
  -v ~/minio/data:/data \
  -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  quay.io/minio/minio server /data --console-address ":9001"
```

### Setup The Server
First, install the libraries that exist in `requirements.txt`
Then put the `.env` file in project root.

Available ENVs:
| Name | Description | Value Example | Is Required |
| ------ | ------ | ------ | ------ |
| MODEL_THRESHOLD | You can put your threshold for the model's accurecy | 0.2 | No
| MODEL_RESULTS_LIMIT | Number of retrived results for each query | 20 | No
| DOCUMENTS_DIRECTORY | Path to store the dataset files (documents texts) | /home/user/documents | Yes
| DATABASE_NAME | Mongo Database Name | searchEngine | No
| DATABASE_CONNECTION_STRING | Mongo Connection String | mongodb://localhost:27017/ | Yes
| MINIO_HOST | MinIO Host | localhost:9000 | Yes
| MINIO_ACCESS_KEY | MinIO Access Key | AKIAIOSFODNN7EXAMPLE | Yes
| MINIO_SECRET_KEY | [MinIO Secret Key | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY | Yes
| MODELS_DIRECTORY | Path of directory to save the trained model and load the model from it | /home/user/models | Yes
| TEST_QUERIES_PATH | File path that contains test queries for model evaluation | /home/user/queries/queries.txt | Yes (only for the evaluation)
| TEST_QUERIES_MATCHES_PATH | File path that contains test queries matches for model evaluation | /home/user/queries/queries_matches.txt | Yes (only for the evaluation)

After preparing your ENVs, run the project:
```sh
cd documents-search-engine
python main.py
```

### API Endpoints
| Endpoint | Description | Request | Response |
| ------ | ------ | ------ | ------ |
| /search | Search for a documents by user's query |  `{"query": "Your Query"}` | `{"data": [{_id: "1", "title": "Title", "authors": ["Author1"]}]}`|
| /correct | Provide suggestion to correct user's query, it it contains a spelling error | `{"query": "Your Query"}` | `{"data": "Corrected Query"}` |
| /documents/<document_id> | Retrive document metadata | URL param <document_id> | `{"data": {_id: "1", "title": "Title", "authors": ["Author1"]}]}}` |
| /documents/<document_id>/content | Retrive document content | URL param <document_id> | `{"data": "Document ID 1 Content"}`

### Setup UI
To work with our UI you've to install React & Yarn package manager.

```sh
cd documents-search-engine
cd ui

# Install the required packages
yarn install 

# Run the project
yarn start
```

## Import Your Dataset
We support a spesific format of the dataset, the dataset should be a text file contains the following structure:
```
.I ID
.T
Title Here
.A
Author 1 Here
Author 2 Here
.W
Text Here
.I ID
.T
Title Here
.A
Author 1 Here
Author 2 Here
.W
Text Here
```
Example:

```
.I 1
.T
18 Editions of the Dewey Decimal Classifications
.A
Comaromi, J.P.
.W
The present study is a history of the DEWEY Decimal
Classification.
.I 2
.T 
Use Made of Technical Libraries
.A 
Slater, M.
.W
This report is an analysis of 6300 acts of use
in 104 technical libraries in the United Kingdom.
```

If you have different format, you can implement your format as a class that extends `parser.dataset_parser.DatasetParser`

Then run import script:
```sh
cd documents-search-engine
python import_dataset.py -n <dataset-name> -p <dataset-path>
```

## Train Your Model
We already provide you with pre-trained models, you can find them in `documents-search-engine/ir_models` directory.

But for new training you can run:
- `documents-search-engine/engine/tfidf_notebook.ipynb` notebook for TfIdf Model.
- `documents-search-engine/engine/word2_vec_notebook.ipynb` notebook for Word2Vec Model (Word Embedding Model)

After running the notebook you will find the models in `$MODELS_DIRECTORY`.

## Tech
- [MongoDB] - NoSql database to store the documents metadata
- [MinIO] - Object storage to work with the files
- [Flask] - HTTP server library
- [React] - UI Library

## License

MIT

[//]: # (These are reference links used in the body)

   [MongoDB]: <https://www.mongodb.com>
   [MinIO]: <https://min.io/>
   [Flask]: <https://flask.palletsprojects.com/en/2.1.x/>
   [React]: <https://reactjs.org/>