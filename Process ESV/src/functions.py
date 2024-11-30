import numpy as np
from joblib import load



# =========== #
# Search Functionality
# =========== #

def get_embeddings(self, text=None, model=None):
    """
    Generate embeddings on a string of text.
    """
    if model==None:
        model = load('./model/SentBERTmodel.pkl')

    return model.encode(text)


def vector_similarity(self, x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.

    Because embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


def measure_embedding_similarity(self,
    query: str,
    embeddings
    ):
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections.

    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = self.get_embeddings(query)
    return [self.vector_similarity(query_embedding, embedding) for embedding in embeddings]