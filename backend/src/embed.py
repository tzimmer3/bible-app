
import json
import os
from joblib import load
import numpy as np
import pandas as pd
import pickle
import tiktoken
import pandas as pd

# WIRE THIS UP
#from config import Config
#app_config = Config()


# ================== #
# Tokenize Text
# ================== #

# TODO: change tiktoken out to real tokenizer... or use tiktoken

def get_tokens(text_2_encode: str, tokenizer=None):
    """
    Tokenize text in a string.

    Initialize a tokenizer if tokenizer == None.
    """

    if tokenizer is None:
        tokenizer = tiktoken.encoding_for_model("text-davinci-003")
    return tokenizer.encode(text=text_2_encode)


def get_num_tokens(text_2_encode: str, **kwargs):
    """
    Count the number of tokens in a string.
    """
    return len(get_tokens(text_2_encode=text_2_encode, **kwargs))


# ================== #
#  Get Embeddings
# ================== #

def get_embeddings(text=None, model=None):
    """
    Generate embeddings on a string of text.
    """
    if model==None:
        model = load('./model/SentBERTmodel.pkl')

    return model.encode(text)


# ================== #
#  Calculate Vector Similarity
# ================== #

def vector_similarity(x: "list[float]", y: "list[float]") -> float:
    """
    Returns the similarity between two vectors.

    Because embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


# ================== #
#  Order Chunks by Similarity
# ================== #

def measure_embedding_similarity(
    query: str,
    embeddings
):
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections.

    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embeddings(query)

    return [vector_similarity(query_embedding, embedding) for embedding in embeddings]


# ================== #
#  Get Similar Texts
# ================== #

def get_similar_texts(df, k):
    """
    Slice a dataframe on the top k results.  Sort the sliced dataframe descending on similarity score.

    If there are repeated results in top 5, keep them all.
    """
    response = df.nlargest(k, columns=['similarity score'],keep='all')
    response = response.sort_values(by='similarity score', ascending=False)
    return response