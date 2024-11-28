# Packages
import numpy as np
import pandas as pd
from joblib import load
from sentence_transformers.cross_encoder import CrossEncoder
import src.be_variables as be_variables
import src.fe_variables as fe_variables



class SearchEngine:

    def __init__(self):

        # Data
        self.verse_data = pd.read_json(be_variables.VERSE_FILE_NAME)

        # Global App Variables
        self.app_name = fe_variables.APP_NAME
        self.measurement_column:str = 'similarity score'
        # Override k to perform cross encoding.
        self.cross_encoder_k:int = 80

        # Tab 1 Variables
        self.tab1_page_name: str = fe_variables.TAB1_PAGE_NAME
        self.tab1_title = fe_variables.TAB1_TITLE
        self.tab1_instructions = fe_variables.TAB1_INSTRUCTIONS

        self.tab1_user_question: str = None
        self.tab1_user_k:int = None
        self.tab1_user_relevance:float = None


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


    def get_similar_texts(self, df:dict[str,str], k:int=None, measurement_column:str=None, relevance:float=None) -> dict[str,str]:
        """
        Slice a dataframe on the top k results.  Sort the sliced dataframe descending on similarity score.

        If there are repeated results in top 5, keep them all.
        """
        # Trim to obs above relevance threshold
        response = df[df[measurement_column]>=relevance]
        # Trim to num obs user expects
        response = df.nlargest(k, columns=[measurement_column],keep='all')
        response = response.sort_values(by=measurement_column, ascending=False)
        return response


# =========== #
# Cross Encoding
# =========== #

    def cross_encode(self, data:dict[str,str], query:str) -> dict[str,str]:
        """ Perform cross encoding. """
        # Vars      
        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        corpus = data['text'].tolist()
        # Pair sentences
        sentence_combinations = [[query, corpus_sentence] for corpus_sentence in corpus]
        # Predict cross encoder score
        data['cross encoder score'] = cross_encoder.predict(sentence_combinations)
        data.sort_values(by='cross encoder score', inplace=True, ascending=False)
        return data


    def tab1_perform_cross_encode(self) -> dict[str,str]:
        """ Utility function to perform cross encoding. """
        # Return Chunks With Highest Similarity (Text)
        response = self.get_similar_texts(df=self.verse_data, 
                                            k=self.cross_encoder_k, 
                                            measurement_column=self.measurement_column,
                                            relevance=self.tab1_user_relevance)
        # Cross encode to get final response
        response = self.cross_encode(data=response, 
                                    query=self.tab1_user_question)
        # Slice to user k preference
        response = response.iloc[:self.tab1_user_k]
        return response


# =========== #
# Utilities
# =========== #

    def transform_relevance_values(self):
        """ Transforms relevance value from string to a float for actual usage. """
        if self.tab1_user_relevance == "In For A Suprize":
            self.tab1_user_relevance = .40
        elif self.tab1_user_relevance == "Pretty Good":
            self.tab1_user_relevance = .50
        elif self.tab1_user_relevance == "Only The Best":
            self.tab1_user_relevance = .60
        else:
            self.tab1_user_relevance = .40


# =========== #
# Run
# =========== #

    def tab1_engine(self, question: str, 
                    run_cross_encoder:bool=False, 
                    testament:str="Whole Bible",
                    k:int=5,
                    relevance:float=.50) -> dict[str,str]:
        
        # Set up Vars
        self.tab1_user_question = question
        self.tab1_user_k = k
        self.tab1_user_relevance = relevance
        self.transform_relevance_values()

        embeddings = self.verse_data['embeddings'].tolist()
        # Retrieve Top K Most Similar Results
        self.verse_data['similarity score'] = self.measure_embedding_similarity(self.tab1_user_question, embeddings)
        # Decide whether to cross encode or not
        if run_cross_encoder == True:
            print("Cross Encoding...")
            response = self.tab1_perform_cross_encode()
            # Remove embeddings column
            keep_columns = ['book', "chapter", 'text', 'similarity score', 'cross encoder score']
        else:
            # Return Chunks With Highest Similarity (Text)
            response = self.get_similar_texts(df=self.verse_data, 
                                                k=self.tab1_user_k, 
                                                measurement_column=self.measurement_column,
                                                relevance=self.tab1_user_relevance)
            # Remove embeddings column
            keep_columns = ['book', "chapter", 'text', 'similarity score']
        response = response[keep_columns]
        
        return response


# if __name__ == '__main__':

    # question = "who is my father?"
    # run_cross_encoder = False
    # testament = "Whole Bible"
    # k=5
    # relevance=.50

    # tab1_engine(question=question,
    #             run_cross_encoder=run_cross_encoder,
    #             testament=testament,
    #             k=k,
    #             relevance=relevance)





# # ================== #
# #  Calculate Vector Similarity
# # ================== #

# def vector_similarity(x: "list[float]", y: "list[float]") -> float:
#     """
#     Returns the similarity between two vectors.

#     Because embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
#     """
#     return np.dot(np.array(x), np.array(y))


# # ================== #
# #  Order Chunks by Similarity
# # ================== #

# def measure_embedding_similarity(
#     query: str,
#     embeddings
# ):
#     """
#     Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
#     to find the most relevant sections.

#     Return the list of document sections, sorted by relevance in descending order.
#     """
#     query_embedding = get_embeddings(query)

#     return [vector_similarity(query_embedding, embedding) for embedding in embeddings]


# # ================== #
# #  Get Similar Texts
# # ================== #

# def get_similar_texts(df, k):
#     """
#     Slice a dataframe on the top k results.  Sort the sliced dataframe descending on similarity score.

#     If there are repeated results in top 5, keep them all.
#     """
#     response = df.nlargest(k, columns=['similarity score'],keep='all')
#     response = response.sort_values(by='similarity score', ascending=False)
#     return response


# # ================== #
# #  Run (score.py)
# # ================== #

# def run(question: str, k: int, embeddings, df) -> dict[str,str]:

#     # Retrieve Top K Most Similar Results
#     df['similarity score'] = measure_embedding_similarity(question, embeddings)

#     # Count number of tokens in each article
#     df['token count'] = df['text'].apply(get_num_tokens)
    
#     # Return Chunks With Highest Similarity (Text)
#     response = get_similar_texts(df, k)

#     # Remove embeddings column
#     keep_columns = ['book', "chapter", 'text', 'token count', 'similarity score']
#     response = response[keep_columns]
    
#     return response