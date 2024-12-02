import gradio as gr
from fastapi import FastAPI, Request

from src.SearchEngine import SearchEngine
engine = SearchEngine()

# Create FastAPI Object
app = FastAPI()


# ----------------------- #
#
#   Gradio App
#
# ----------------------- #

# ====== #
# Tab1: Chat
# ====== #

# Creating a Gradio interface for the chatbot
with gr.Blocks() as engine.tab1_page_name:
    title = gr.HTML(engine.tab1_title)
    instructions = gr.HTML(engine.tab1_instructions)

    # User tuning parameters
    with gr.Row(equal_height=True):
        similarity_score = gr.Radio(value="In For A Suprize", label="Similarity Filter:", choices=["In For A Suprize", "Pretty Good", "Only The Best"])
        level_of_abstraction = gr.Radio(value="Verse", label="Level of Abstraction:", choices=["Verse", "Heading", "Chapter"])
        testament = gr.Radio(value="Whole Bible", label="Testament:", choices=["Whole Bible", "Old Testament", "New Testament"])
        k = gr.Slider(1,15, value=3, step=1, label="How many results to return?")
        cross_encoding = gr.Checkbox(value=False, label="Advanced Search?                 (Will take longer to receive results.)")

    question = gr.Textbox(label="What would you like to know?")  # Textbox for user input
    tab1_submit_button = gr.Button("Search The Word")  # Button to trigger the agent call
    output = gr.Dataframe(label="Results: ")  # Dataframe for chatbot response

    # Collate the inputs
    tab1_inputs = [question, cross_encoding, testament, k, similarity_score] # Add: level_of_abstraction, 
    # Execute the function
    tab1_submit_button.click(fn=engine.tab1_engine, inputs=tab1_inputs, outputs=output)


# ====== #
# Tab4: FAQ
# ====== #
with gr.Blocks(theme=gr.themes.Glass()) as engine.tab4_title:
    title = gr.HTML(engine.tab4_title)
    # Instructions
    instructions = gr.Markdown(value=engine.tab4_instructions)


# ====== #
# Put it together
# ====== #

# Assemble gradio app
demo = gr.TabbedInterface([engine.tab1_page_name, engine.tab4_page_name], [engine.tab1_title, engine.tab4_title], title=engine.app_name)

# application = gr.mount_gradio_app(app, demo, path="/home", auth_dependency=engine.get_token)
# Mount gradio app into FastAPI
application = gr.mount_gradio_app(app, demo, path="/home")