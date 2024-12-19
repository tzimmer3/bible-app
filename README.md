# bible-app
Application for semantic search of bible text.


## Notes

- Check README in /app/data/ for data descriptions


## Changelog

(internet)
### Front end with SearchEngine class: 
    - Inputs - how to send a list ... @btn.click

### Static Values in Front End, Search Class
    - Move these to be_variables or fe_variables and import in __init__
    - Testament, Relevance values, Level of Abstraction

### Deployment:
- Poetry
- Dockerfile
- docker-compose
- write app.py

### Data:
- Extract ESV and structure, put in app/data/.  Replace in flow.
- Add Section heads as a column  --  later a level of abstraction


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


## Docker Commands

- docker build -t god:latest .
- docker-compose up

- docker run -d -p "8081:80" ImageID

- docker images

- Having issue with huggingface_hub pip installation
 cannot import name 'cached_download' from 'huggingface_hub'

 likely need to retry creating the local env and potentially using poetry