

# ========= #
# Global Variables
# ========= #
APP_NAME = "Chat with Methane Pyrolysis Logbook"


# ========= #
# Page Variables
# ========= #

## Page Names
TAB1_PAGE_NAME = "1. Select a Logbook File"
TAB2_PAGE_NAME = "2. Ask a Question"
TAB3_PAGE_NAME = "3. Show All Logbook Data"
TAB4_PAGE_NAME = "Need Help?"


## Page Instructions
TAB1_INSTRUCTIONS = "<h3>Instructions</h3>"\
                            "<b>Enter a filename from the blob directory: </b> <i>/methane-pyrolysis/notebooks/.</i>"\
                            "<p></p>" \
                            "<li>Clicking run will create a Canvas and all pages needed to execute the flow.</li>"\
                            f"<li>Navigate to the <b>{TAB2_PAGE_NAME}</b> tab to ask questions to your logbook after receiving a confirmation message that your file was processed properly.</li>"

TAB4_INSTRUCTIONS = "<h3>Overview</h3>"\
                    "<p>This application allows a user to have a chat experience with a Methane Pyrolysis logbook.</p>"\
                    "<p></p>"\
                    "<h3>Instructions</h3>"\
                    "<p>The user selects a logbook, extracts the handwritten text from the logbook, and can then use a model to ask questions about the content of the handwritten text.</p>"\
                    f"<p>***<i> Note: The user needs to enter a filename in the first tab for the rest of the tabs to work.</i>***  Clicking the 'Run' button on {TAB1_PAGE_NAME} creates a Canvas and builds all the pages needed to perform all the operations.</p>"\
                    "<p></p>"\
                    "<p><b>Example question:</b> <i>List the N2 intervals</i> --> returns a table of the N2 intervals written in the document.</p>"\
                    "<p></p>"\
                    "<h3>Things of Note</h3>"\
                    "<li>Authentication for creating a Canvas and pages on the Canvas using the application is granted using your access to the <b>'crrc-users'</b> AAD group.  <u>You must be in the group to use this application.</u></li>"\
                    "<li>This application is directly dependent on a single container on the rcdatat101teststorage storage account --> /methane-pyrolysis/notebooks/.  If you need to import files from other directories, that will need to be configured. </li>"\
                    "<li>The first tab of this application lists the contents of the <b>'/methane-pyrolysis/notebook/'</b> directory using XXX credentials. </li>"\
                    "<p></p>"\
                    "<p></p>"\
                    "<p></p>"\
                    "<h3>Developer Help</h3>"\
                    "<p>Documentation for the Science Engine Connector can be found here: [API Reference](https://rcinfo-prod.azurewebsites.net/docs/advancedtopics/apireference/)</p>"
                                    


## Other Goodies
TAB1_EXAMPLES = ["Xerox Scan_02152024100620.pdf", "Xerox Scan_02152024140510.pdf"]



