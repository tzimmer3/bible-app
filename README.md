# bible-app
Application for semantic search of bible text.


## Notes

- Check README in /app/data/ for data descriptions


## Changelog

- Add relevance_filter to search

- Test out cross encoder and integrate into Search class

- Build out front end
    - picker for level of abstraction.  Will want a way to switch to any level of abstraction [chapter, verse, other]

- Wire up front end with SearchEngine class.  
    - All descriptions, etc.

- Poetry

- Extract ESV and structure, put in app/data/.  Replace in flow.

- Add Section heads as a column  --  later a level of abstraction


## Improvements

Cross Encoder

- Add cross_encoder attributes
    - Currently works on the ~ 5 or so observations (not intended behavior)
    - switch to have larger number of observations to run cross encoder on


Semantic Search
- Check out other LLMs for semantic search


Gradio
