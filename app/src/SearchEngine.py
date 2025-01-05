# Packages
import numpy as np
import pandas as pd
from joblib import load
from sentence_transformers.cross_encoder import CrossEncoder
import src.be_variables as be_variables
import src.fe_variables as fe_variables



import os

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def embed_text(string):
    tokenizer = AutoTokenizer.from_pretrained("path_to_model_weights")
    model = AutoModelForSeq2SeqLM.from_pretrained("path_to_model_weights")

    inputs = tokenizer.encode("Translate this sentence", return_tensors='pt')
    return model.generate(inputs, max_length=125)


def find_file(filename, directory):
    """
    Finds a file in a given directory.

    Args:
        filename (str): The name of the file to search for.
        directory (str): The directory to search in.

    Returns:
        str: The full path to the file if found, otherwise None.
    """

    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)

    return None



class SearchEngine:

    def __init__(self):

        # self.verse_data = pd.read_json(be_variables.VERSE_FILE_NAME)
        file = find_file("KJV_chapter_search.json", "C:\\Users\\t_zim\\code\\bible-app\\app\\data")
        model_path = find_file("SentBERTmodel.pkl", "C:\\Users\\t_zim\\code\\bible-app\\app\\model")

        # Data
        self.verse_data = pd.read_json(file)

        # Global App Variables
        self.app_name:str = fe_variables.APP_NAME
        self.measurement_column:str = 'similarity score'
        # Override k to perform cross encoding.
        self.cross_encoder_k:int = 80

        # Tab 1 Variables
        self.tab1_page_name:str = fe_variables.TAB1_PAGE_NAME
        self.tab1_title:str = fe_variables.TAB1_TITLE
        self.tab1_instructions:str = fe_variables.TAB1_INSTRUCTIONS
            # params
        self.tab1_user_question: str = None
        self.tab1_user_k:int = None
        self.tab1_user_relevance:float = None

        # Tab 4 Variables
        self.tab4_page_name:str = fe_variables.TAB4_PAGE_NAME
        self.tab4_title:str = fe_variables.TAB4_TITLE
        self.tab4_instructions:str = fe_variables.TAB4_INSTRUCTIONS

        self.MODEL_PATH:str = model_path

# =========== #
# Search Functionality
# =========== #

    def get_embeddings(self, text=None, model=None):
        """
        Generate embeddings on a string of text.
        """
        if model==None:
            model = load(self.MODEL_PATH)

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
