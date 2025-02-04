# bible-app
Application for semantic search of bible text.


## To update the python environment 
1.  make changes to `pyproject.toml` to add additional packages
2. `poetry lock`
3. `poetry export --without-hashes --format=requirements.txt > app/requirements.txt`


## Startup/Deployment Commands

## 1. Jupyter Notebook
  - Run search_demo.ipynb with question

## 2. Local Gradio app
  - Run test_front_end.ipynb with front end

## 3. FastAPI Developer Mode
  ### - Open a terminal and put in:
    $ cd /app/ dir
    $ uvicorn app:application
      
** where app is the name of the python file and application is the variable in the python file


## 4. Build Docker conatiner
  ### - Open a terminal and put in:
    $ `docker build -t bibleapp1:latest .`
    $ `docker run -p 8000:8000 bibleapp1`
    - Open your browser and go to `localhost:8000` to test
or

    $ docker compose build
    $ docker compose up
    - Open your browser and go to `localhost:8000` to test







## Notes
- Check README in /app/data/ for data descriptions (Not correct right now)











## Changelog

(internet)
### Front end with SearchEngine class: 
    - Inputs - how to send a list ... @btn.click

### Static Values in Front End, Search Class
    - Move these to be_variables or fe_variables and import in __init__
    - Testament, Relevance values, Level of Abstraction

### Deployment:
    - Issue with huggingface_hub installation.  Seems like the issue is something with the cache:
    https://huggingface.co/docs/huggingface_hub/main/en/guides/overview


### Data:
- Extract ESV and structure, put in app/data/.  Replace in flow.
- Add Section heads as a column  --  later a level of abstraction
- Would be cool to have it by "paragraph"


## Improvements

Analytics
- Logging of params, user query, and returned output
- What can be done with this info?

Cross Encoder
- Research how to tune

Parse text

Semantic Search
- Check out other LLMs for semantic search

Other Biblical Translations

Front End updates









# Original README.md

# Build and Test 
To get started I recommend first creating a python virtual environment and running the app
with conda you can do this with
- `conda create -n bible_app_env pip`
- `conda activate bible_app_env`
- `pip install -r app/requirements.txt`
- create a file called `.env` and put the following inside
  - `DR_API_KEY="************************************" # replace with your DR endpoint key`
- run `python app/app.py`
- open your browser and go to `localhost:8000`

## To test the docker container
This step is to make sure that your requirements can support your application 
Why? sometimes your local python venv and your requirements file become deysnced through ad-hoc pip-installs etc
This step makes ure this didnt happen.

1. `docker build -t bibleapp1:latest .`
2. `docker run -p 8000:8000 bibleapp1`
3. Open your browser and go to `localhost:8000` to test

## To emulate the pipeline run to test variable injection
This step emulates the variable injection that happens in :
`pipeline/publish-app-service.yml`

1. docker compose build
2. docker compose up
3. Open your browser and go to `localhost:8000` to test

Note: This injects varibles into your runtime environment similar to how the azure pipeline will do so with the specified keyvault values.
This step allows to verify that the variable injection is working as intended.


## Docker Commands

- docker build -t god:latest .
- docker-compose up

- docker run -d -p "8081:80" ImageID

- docker images

- Having issue with huggingface_hub pip installation
 cannot import name 'cached_download' from 'huggingface_hub'