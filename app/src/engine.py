# Packages
import numpy as np
import pandas as pd
from joblib import load
import pickle
from sentence_transformers.cross_encoder import CrossEncoder
import src.be_variables as be_variables
import src.fe_variables as fe_variables



class GradioEngine:

    def __init__(self):

        self.verse_data = pd.read_csv(be_variables.VERSE_FILE_NAME)

        # Verse Variables
        self.verse_page_name: str = fe_variables.TAB1_PAGE_NAME
        self.verse_user_question: str = None

        # Section Variables
        self.section_page_name: str = fe_variables.TAB2_PAGE_NAME
        self.section_user_question: str = None

        # Chapter Variables
        self.chapter_page_name: str = fe_variables.TAB3_PAGE_NAME
        self.chapter_user_question: str = None

     

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


    def vector_similarity(self, x: "list[float]", y: "list[float]") -> float:
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


    def get_similar_texts(self, df, k, column):
        """
        Slice a dataframe on the top k results.  Sort the sliced dataframe descending on similarity score.

        If there are repeated results in top 5, keep them all.
        """
        response = df.nlargest(k, columns=[column],keep='all')
        response = response.sort_values(by=column, ascending=False)
        return response


    def cross_encode(self, data, query):
        # Sentence Combinations
        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

        corpus = data['text'].tolist()
        sentence_combinations = [[query, corpus_sentence] for corpus_sentence in corpus]

        data['cross_encoder_score'] = cross_encoder.predict(sentence_combinations)

        data.sort_values(by='cross_encoder_score', inplace=True, ascending=False)

        return data

# =========== #
# Run
# =========== #

    def tab1_engine(self, question: str, run_cross_encoder="No", testament="All") -> dict[str,str]:
        # Set up Vars
        embeddings = self.verse_data['embeddings']
        k=5

        # Retrieve Top K Most Similar Results
        self.verse_data['similarity score'] = self.measure_embedding_similarity(question, embeddings)
        # Count number of tokens in each article
        self.verse_data['token count'] = self.verse_data['text'].apply(self.get_num_tokens)
        # Return Chunks With Highest Similarity (Text)
        response = self.get_similar_texts(self.verse_data, k, 'similarity score')

        # Remove embeddings column
        keep_columns = ['book', "chapter", 'text', 'token count', 'similarity score']
        response = response[keep_columns]

        if run_cross_encoder=="Yes":
            print("Cross Encoding...")
            response = self.cross_encode(response, question)

            # Return Chunks With Highest Similarity (Text)
            response = self.get_similar_texts(response, k, 'cross_encoder_score')
        
        
        return response



# if __name__ == '__main__':
#     run()