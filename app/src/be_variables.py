

# Retrieve data from blob storage
DATA_PAGE_NAME = "Logbooks"
SOURCE_TYPE = "AzureBlob"
STORAGE_ACCOUNT_NAME = "rcdatat101teststorage"
BLOB_FILEPATH = "/methane-pyrolysis/notebooks/"

# List directory of blob storage
ACCOUNT_URL = "https://rcdatat101teststorage.blob.core.windows.net"
BLOB_NAME = "methane-pyrolysis"
BLOB_KEY = "fShWCc90ji2YVHyqdlzedxIwQ5DPeV3b1yvAq16GhAy3XvJOXemYzGUUQJ/nKPG1JAEAMW0hVysmLNwuOCx8QA=="


# Dict of formula pages. Key is page name, value is formula for the page.
FORMULA_PAGES = {"Digitization":"DigitizeLogBook(Logbooks, fileUrl)",
                 "DigitizedData":"ChainMap(Digitization.IndexingList)",
                 "QuestionAnswer":"ChatWithLogbook(Digitization,'""', FileName, IndexingList)"}
