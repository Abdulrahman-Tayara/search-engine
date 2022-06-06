from flask import Flask, jsonify, request
from flask_cors import CORS

from di.containers import inject_ir_model_v1, inject_document_repository, inject_file_storage, inject_spell_checker

app = Flask(__name__)
CORS(app)


@app.route("/search", methods=["POST"])
def search_by_query():
    body = request.json

    if 'query' not in body or len(body['query']) == 0:
        return jsonify({"error": "You have to pass query"})

    query = body['query']

    engine = inject_ir_model_v1()

    matched_documents = engine.match_query(query)

    ids = list(
        map(lambda d: d[0], matched_documents)
    )

    repo = inject_document_repository()


    return jsonify({'data': [d.to_dict() for d in repo.find_many_by_ids(ids)]},)

@app.route("/correct", methods=["POST"])
def correct_query():
    body = request.json

    if 'query' not in body or len(body['query']) == 0:
        return jsonify({"error": "You have to pass query"})

    query = body['query']

    spell_checker = inject_spell_checker()

    corrected_query = spell_checker.correct(query)

    return jsonify({'data': corrected_query})


@app.route("/documents/<document_id>")
def get_document_by_id(document_id: str):
    repo = inject_document_repository()

    document = repo.find_by_id(document_id)

    return jsonify({'data': document.to_dict()})

@app.route("/documents/<document_id>/content")
def get_document_content(document_id: str):
    repo = inject_document_repository()

    document = repo.find_by_id(document_id)

    storage = inject_file_storage()

    content = storage.fetch_file_content("documents", document.document_key)

    return jsonify({'data': content.decode("utf-8") })

def start_server():
    app.run(host='0.0.0.0')
