import os
import pickle
from typing import Any

from nltk import tokenize

from engine.preprocess.preprocessor import TextPreprocessor
from envs.env import models_directory

from gensim.models import Word2Vec

def preprocess(content: str) -> str:
    preprocessor = TextPreprocessor(tokenizer=tokenize_content)

    return preprocessor.preprocess(content)


def tokenize_content(content: str) -> list[str]:
    return tokenize.word_tokenize(content)


def save_model(obj: Any, model_name: str):
    dest = os.path.join(models_directory(), model_name)
    with open(dest, 'wb') as f:
        return pickle.dump(obj, f)


def load_model(model_name: str):
    with open(os.path.join(models_directory(), model_name), 'rb') as f:
        return pickle.load(f)

def save_w2v_model(model, model_name: str):
    model.save(os.path.join(models_directory(), model_name))

def load_w2v_model(model_name: str):
    return Word2Vec.load(os.path.join(models_directory(), model_name))


# def save_matrix(matrix: Any, name: str):
#     with open(os.path.join(MODELS_DIRECTORY(), name), 'wb') as f:
#         return np
