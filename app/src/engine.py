# Packages
import time
import gradio as gr
import pandas as pd
import src.be_variables as be_variables
from azure.storage.blob import ContainerClient


from science_engine.connector import ScienceEngineConnector
from science_engine.utils import SEConnectionConfig



class GradioEngine:

    def __init__(self):
        
        # Create connection
        connection_config = SEConnectionConfig.from_config_file(config_file="environments.ini", environment="AriesProd1")
        self.rc = ScienceEngineConnector(config=connection_config)

        self.canvas_id: str = None

        # Blob Storage Config for Science Engine
        self.data_page_name: str = be_variables.DATA_PAGE_NAME
        self.source_type: str = be_variables.SOURCE_TYPE
        self.storage_account_name: str = be_variables.STORAGE_ACCOUNT_NAME
        self.blob_filepath: str = be_variables.BLOB_FILEPATH
        self.full_filename: str = None

        # Blob Storage Config for Listing Blob Directory
        self.account_url: str = be_variables.ACCOUNT_URL
        self.blob_name: str = be_variables.BLOB_NAME
        self.blob_key: str = be_variables.BLOB_KEY
        self.list_of_filenames_in_blob = ["Select Load Examples Button for Example Files"]

        # Dictionary: [key] Page Name, [value] Formula
        self.formula_pages = be_variables.FORMULA_PAGES

        # Question Answer Stuff
        self.qa_page_name: str = "QuestionAnswer"
        self.user_question: str = None

        # Full Logbook Stuff
        self.digitized_page_name: str = "DigitizedData"
        self.full_logbook_data: str = None

# =========== #
# Science Engine Operations
# =========== #

    def create_canvas(self):
        """ Create a blank canvas """
        self.canvas_id = self.rc.create_canvas()

    def create_formula_page(self, page_name, formula):
        """ Add a formula page to the Canvas """
        self.rc.add_formula(name=page_name,
                        formula=formula)    

    def create_data_page(self):
        """ Add a data page to the Canvas """
        self.rc.add_data_source(name=self.data_page_name,
                        source_type=self.source_type,
                        storage_account_name=self.storage_account_name,
                        path_to_files=self.full_filename)

    def update_formula_page(self):
        """ Update a formula on an existing formula page """
        self.rc.update_formula(name=self.qa_page_name,
                    formula=self.updated_formula)
        

# =========== #
# Utility Functions
# =========== #

## NOT WORKING RIGHT NOW.  NEED TO ADD TWO STRINGS TOGETHER
    def modify_filename(self, filename):
        """ Returns the full filepath given a filename.  Response includes a path prepended and quotes around it. """
        ## qwerty is used to replace default [space] value.  should never split.
        self.full_filename = list(f"{self.blob_filepath}{filename}".split("qwerty"))
  
    def modify_formula(self, user_question):
        """ Modify a formula string """
        self.updated_formula = f"ChatWithLogbook(Digitization, \"{user_question}\", FileName, IndexingList)"

    def parse_response_return_answer(self):
        """ Parses the answer from the chat response """
        return self.chat_response[0]['Answer'].split("\n")
    
    def parse_response_return_logbook(self):
        """ Parses the full logbook data page """
        full_logbook_df = pd.DataFrame()
        activities = []
        timestamps = []
        for element in self.full_logbook_data:
            activities.append(element['activity'])
            timestamps.append(element['timestamp'])
        full_logbook_df['activity'] = activities
        full_logbook_df['timestamp'] = timestamps
        return full_logbook_df
    
    def export_csv(self, data):
        """ Gradio method to prepare a dataframe object as a .csv """
        data.to_csv("output.csv")
        return gr.File(value="output.csv", visible=True)

    def list_blob(self):
        """ Create a list of the files in the '/methane-pyrolysis/notebooks/' blob."""
        container_client = ContainerClient(account_url=self.account_url, container_name= self.blob_name, credential=self.blob_key)
        list_of_filenames_in_blob = []
        for blob in container_client.list_blobs():
            if blob.name.startswith("notebooks/"):
                file = blob.name.split("/")[-1]
                list_of_filenames_in_blob.append(file)
        self.list_of_filenames_in_blob = list_of_filenames_in_blob


# =========== #
# Run
# =========== #
    
    def tab1_engine(self, filename):
        """ Executes all actions for gradio app tab 1.  Executes with Run button on tab 1. """
        # List filenames in the blob directory
        print(self.list_of_filenames_in_blob)
        # Create blank canvas
        self.rc.create_canvas()        
        # Add path to filename
        self.modify_filename(filename)
        # Create data page
        if filename in self.list_of_filenames_in_blob: 
            self.create_data_page()
        else:
            return f"Error importing data: File not present in blob folder."
        
        # Create formula pages. Iterate dict of page names and formulas
        for page, formula in self.formula_pages.items():
            self.create_formula_page(page, formula)

        # Error Handling.  Check if data and downstream data pages are created properly.
        self.data_import_validation = self.rc.get_all_data_from_node(self.digitized_page_name)
        if self.data_import_validation is None:
            return f"Error importing data: File present, but Data page not created properly in Research Canvas. "

        return f"Successfully imported data!!"

    def tab2_engine(self, user_question):
        """ Executes all actions for gradio app tab 2.  Executes with Run button on tab 2. """
        # Update string of formula (Question Answer)
        self.modify_formula(user_question)
        # Update formula on page
        self.update_formula_page()
        # Wait for page to rerun. 8 seconds.
        time.sleep(8)
        # Return data from updated page
        self.chat_response = self.rc.get_all_data_from_node(self.qa_page_name)
        # Create df to house data
        answer_df = pd.DataFrame()
        # Add data to df
        answer_df['Answer'] = self.parse_response_return_answer()
        return answer_df
    
    def tab3_engine(self, input):
        """ Executes all actions for gradio app tab 3.  Executes with Run button on tab 3. """
        ## Input is not used ##
        # Request data from page
        self.full_logbook_data = self.rc.get_all_data_from_node(self.digitized_page_name)
        # Parse string of data and return as df
        return self.parse_response_return_logbook()