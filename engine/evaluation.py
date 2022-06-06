from engine.ir_engine import IREngine
from sklearn.metrics import precision_recall_fscore_support

def _fetch_test_queries(test_queries_path: str):
    
    queries = []

    with open(test_queries_path, 'r') as f:
        prevLine: str = ""

        text_stage: bool = False
        skip = False

        query = None

        for i, line in enumerate(f.readlines()):
                line = line[:-1]

                if (line.startswith(".A") or line.startswith(".B") or line.startswith(".T") or skip):
                    skip = True
                    text_stage = False

                if (line.startswith(".W")):
                    skip = False
                    pass

                elif (line.startswith(".I")):
                    if (query is not None):
                        queries.append(query)
                        query = None
                    
                    query = {'id': line[line.rindex(" ") + 1:], 'text': ""}
                    text_stage = False
                    skip = False

                elif ((prevLine.startswith(".W") or text_stage) and not skip):
                    text_stage = True
                    skip = False
                    query['text'] = query['text'] + f'{line}\n'

                prevLine = line

        queries.append(query)
        
    return queries

def _fetch_queries_matches(test_queries_matches_path: str):
    matches = {}
    with open(test_queries_matches_path, 'r') as f:
        for _, line in enumerate(f.readlines()):
            numbers = line.split()
            query_id = numbers[0]
            document_id = int(numbers[1])

            if query_id in matches:
                matches[query_id].append(document_id)
            else:
                matches[query_id] = [document_id]
    return matches

def precision_recall(documents_count: int, test_documents, predict_documents):
    test_documents_binary = documents_count * [0]
    predict_documents_binary = documents_count * [0]

    for d in test_documents:
        test_documents_binary[d - 1] = 1
            
    for d in predict_documents:
        predict_documents_binary[d - 1] = 1
            
    precision, recall, _, _ = precision_recall_fscore_support(test_documents_binary, predict_documents_binary)


    return precision[1], recall[1]

def evaluate(engine: IREngine, test_queries_path: str, test_queries_matches_path: str, listener=None):
    """
    :parameters:
    listener:
    def listener(query_id, precision, recall, avg_precision, precision_at_10)


    :return:

    {
        'mean_average_precision': float,
        'mean_reciprocal_rank': float,
        'average_recall': float,
        'average_precision: float,
        'queries': [
            {
                'query_id': int,
                'precision': float,
                'recall': float,
                'avg_precision': float,
                'precision_at_10': float,
                'reciprocal_rank': float
            }
        ]
    }
    """
    queries = _fetch_test_queries(test_queries_path)
    expected_results = _fetch_queries_matches(test_queries_matches_path)

    documents_count = engine.get_documents_count()

    queries_count = 0

    mean_average_precision = 0
    mean_reciprocal_rank = 0
    average_recall = 0
    average_precision = 0

    result = {
        'queries': []
    }

    for i, query in enumerate(queries):
        query_id = query['id']
        query_text = query['text']

        if query_id in expected_results:

            queries_count = queries_count + 1

            test_documents = expected_results[query_id]

            predict_documents = list(
                map(lambda m: int(m[0]), engine.match_query(query_text))
            )

            precision, recall = precision_recall(documents_count, test_documents, predict_documents)

            precision_at_10, _ = precision_recall(documents_count, test_documents, predict_documents[0:10])

            reciprocal_rank = 0
            for i, d in enumerate(predict_documents):
                if d in test_documents:
                    reciprocal_rank = 1/(i + 1)
                    break

            query_avg_precision = 0            
            for i in range(len(predict_documents)):
                k = i + 1
                
                if predict_documents[i] in test_documents:

                    matched_documents_at_k = predict_documents[0:k]

                    intersected = [d for d in matched_documents_at_k if d in test_documents]

                    precision_at_k = 0 if len(matched_documents_at_k) == 0 else float(1.0 * len(intersected) / len(matched_documents_at_k))
                    
                    query_avg_precision = query_avg_precision + precision_at_k

            query_avg_precision = 0 if len(test_documents) == 0 else query_avg_precision / len(test_documents)

            mean_average_precision = mean_average_precision + query_avg_precision
            mean_reciprocal_rank = mean_reciprocal_rank + reciprocal_rank
            average_precision = average_precision + precision
            average_recall = average_recall + recall

            result['queries'].append({
                'query_id': int(query_id),
                'precision': precision,
                'recall': recall,
                'avg_precision': query_avg_precision,
                'precision@10': precision_at_10,
                'reciprocal_rank': reciprocal_rank,
            })

            if listener is not None:
                listener(query_id, precision, recall, query_avg_precision, precision_at_10)
            

    mean_average_precision = mean_average_precision / queries_count
    mean_reciprocal_rank = mean_reciprocal_rank / queries_count
    average_precision = average_precision / queries_count
    average_recall = average_recall / queries_count

    result['mean_average_precision'] = mean_average_precision
    result['mean_reciprocal_rank'] = mean_reciprocal_rank
    result['average_precision'] = average_precision
    result['average_recall'] = average_recall

    return result