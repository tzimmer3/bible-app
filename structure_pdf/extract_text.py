
"""

Author: Tyler Zimmer -- tzimme9@gmail.com
Date: 2.23.22

-------
Use this script to extract text from documents and clean it for further downstream processing.

TO USE: Need to modify initial variable definitions in Step 1, and True/False in Step 3.


## Steps ##

1. Define variables: stopwords, special characters -> anything you want removed
2. Extract text from documents
    - searches for specific suffix and runs script on all documents in a folder (i.e. all .pdf documents)
3. Format extracted text as Pandas dataframe and clean using variables defined in step 1
4. Save and export as .csv file

-------
"""

# Import Packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import string
import nltk
import re
import pdfplumber
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


"""
# Step 1: Define Variables

"""

# INCOMING DOCUMENTS
filepath = "C:\\Users\\t_zim\\Desktop\\Projects\\Bible_Project\\"
extension = ".pdf"

# EXPORT CLEANED DATASET
filename_to_export_data = 'extracted_text.csv'
filepath_to_export_data = "C:\\Users\\t_zim\\code\\esv_bible_qa\\Out\\"

# Notes:
#   Example filepath --> C:\\Users\\hlmq\\OneDrive - Chevron\\Data\\DSDP\\ResearchPapers\\
#   Can single out specific files if the end of the file is repeated (ex. ...Release.pdf)


# DEFINING VARIABLES FOR CLEANING

# List of stopwords
newStopWords = ['ourselves', 'here', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 
                'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 
                'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 
                'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 
                'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 
                'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 
                'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 
                'myself', 'which', 'those', 'i', 'I','after', 'few', 'whom', 'being', 'if', 'theirs', 'my', 'against','a', 'by', 'doing', 
                'it', 'how', 'further', 'was', 'here','than','can', 'let', 'll',
                # Chevron specific items added below:
                'chevron', "corporation", "quarter", "financial", 'review', 'release', 'pdt',
                'net','per','2015','2016','2017','2018', '2019', '2020', '2021', '2022','year', 'day'
               ]

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(newStopWords)

# [Blank] Dictionary of contractions
contractions_dictionary = {}
# Notes:
#   Will need a dictionary of contractions and their "real" words

# List of special characters FOR REMOVAL
special_characters = ['!','@','|','`','','.',',',':',';',"'", '-','(',')', '*']
# Notes:
#   If you want to remove digits, do it in this list!!

# [Blank] List of accented characters FOR REMOVAL
accented_characters = []





"""
# Step 2: Identify and Extract Text
"""


# FUNCTION: Extract text from pdf file
def extract_text_and_metadata(filenames):

#Whole document level of detail
    for i in range(len(filenames)):
        # Iterate through all files in the list
        filename = filenames[i]
        # Clean the filename
        trimmed_filename = filename.replace(filepath, "")
        
        # Clear text from document
        document = []
        # Open the file name and save as instance called pdf
        with pdfplumber.open(filename) as pdf:
            # Iterate page by page through the .pdf file
            for pdf_page in pdf.pages:
                # Extract one page of text
                page_text = pdf_page.extract_text()
                # Append document name.  Once for EACH page
                docName.append(trimmed_filename)
                # Append document text by page
                pageContent.append(page_text)
                
                pageNumber.append(pdf_page.page_number)
        # Close the current document
        pdf.close()
        
        
    return [docName, pageContent, pageNumber]


# LIST OF FILES TO EXTRACT TEXT FROM

filenames = ([os.path.join(filepath, filename) for filename in os.listdir(filepath) if filename.endswith(extension)])


# Notes:
#   Check all files in the directory and only allow one particular file extension
#   os.listdir(filepath) creates a list of all files in a directory
#   filename.endswith(extension) dynamically checks the ending characters of a string
#   Extracts text one page at a time, so will result in one row in a table per page in document
#       - Can aggregate back to full document using the title of the document and group by





# EXECUTE FUNCTIONS DEFINED IN STEP 2 ABOVE

# EXTRACT TEXT AND METADATA
docName = []
pageContent = []
pageNumber = []

docName, pageContent, pageNumber = extract_text_and_metadata(filenames)


"""
# Step 3: Text Cleaning
"""

# FUNCTION: Collate lists into DataFrame columns
def dataframe_constructor(docName, pageContent, pageNumber):
    df = pd.DataFrame()
    df['docName'] = docName
    df['pageContent'] = pageContent
    df['pageNumber'] = pageNumber
    return df

# FUNCTION: Iterate through numPages to provide single list of all page numbers
def flatten(pageNum):
    return [item for sublist in pageNum for item in sublist]

# FUNCTION: Steps in the cleaning process. Used in cleaning_operations function below.

def strip_html_tags(page):
    pass

def remove_accented_chars(page, accented_characters):
    pass

def expand_contractions(page, contractions_dictionary):
    pass

def remove_special_characters(page, special_characters):
    page = [word for word in page if word not in special_characters]
    return page

def lemmatize_text(page):
    lemmatizer = WordNetLemmatizer()
    page = [lemmatizer.lemmatize(word, pos='v') for word in page]
    return page

def remove_stopwords(page, stopwords):
    page = [word for word in page if word not in stopwords]
    return page

def spell_check():
    pass

# Tokenize (also removes punctuation and makes everything lowercase)
def tokenize(page):
    tokens = nltk.word_tokenize(page)
    return tokens

def special_operations(page):
    page = [line.strip().split(' ') for line in page]
#    page = page.replace("      ","")
#    page = page.replace("  ",",")
#    page = page.replace(" ","")
#    page = page.replace("\n","")
    return page

# FUNCTION: Actually perform cleaning operations
def cleaning_operations(corpus, stopwords, special_characters, accented_characters, contractions_dictionary,
                     html_stripping=False, 
                     contraction_expansion=False,
                     accented_char_removal=False, 
                     text_lower_case=True, 
                     special_char_removal=True,
                     stopword_removal=True,
                     text_lemmatization=True,
                     remove_digits=False, 
                     tokens = True,
                     special_doc_operations = False,
                     spelling_correction = False):

    """
    Need to modify True/False above depending on needs 

    """



    normalized_corpus = []

    # normalize each document in the corpus

    for doc in corpus:

        # tokenize the words
        if tokens:
            doc = tokenize(doc)
            
        # lowercase the text    
        if text_lower_case:
            doc = [x.lower() for x in doc]
            
        # remove stopwords
        if stopword_removal:
            doc = remove_stopwords(doc, stopwords)
        
        # strip HTML
        if html_stripping:
            doc = strip_html_tags(doc)

        # remove accented characters
        if accented_char_removal:
            doc = remove_accented_chars(doc, accented_characters)

        # expand contractions    
        if contraction_expansion:
            doc = expand_contractions(doc, contractions_dictionary)   

        # remove special characters
        if special_char_removal:
            doc = remove_special_characters(doc, special_characters)  

        # remove newlines   
        if special_doc_operations:
            doc = special_operations(doc)
            
        # lemmatize text
        if text_lemmatization:
            doc = lemmatize_text(doc)
            
        # Spell check
        if spelling_correction:
            doc = spell_check(doc)
            
        ## put it all together
        normalized_corpus.append(doc)
  
    return normalized_corpus




# EXECUTE FUNCTIONS DEFINED IN STEP 3 ABOVE

# CREATE DATAFRAME
df = dataframe_constructor(docName, pageContent, pageNumber)


# NORMALIZE EACH OBSERVATION
df['pageContent'] = cleaning_operations(df['pageContent'], stopwords, special_characters, accented_characters, contractions_dictionary)



"""
# Step 4: Export Cleaned Data
"""

# EXPORT DATAFRAME

df.to_csv(filepath_to_export_data+filename_to_export_data, sep=',', index = False)