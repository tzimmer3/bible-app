

## ESV bible.pdf

Lots of text nested under each observation

Need to remove footnotes pages


Desired End state:

Text separated out by verse

Colums = ['book', 'chapter', 'heading', 'verse', 'text']


0.extract_text
    - uses pdfplumber to extract text from the .pdf file

1.parse_text
    - fixes formatting and restructures table into headings centric instead of pages centric
    - removes special characters (but some still exist for " " )

2.apply_metadata
    - parses headings into a separate column
    - parses chapter/verse to make a chapter column
    - need to get books somehow



* Still have some weird observations like just a date/time, things that should be merged
** Thinking I could get away with using the KJV to apply books
*** Numbers from footnotes are still in the text, but does that matter much for the embedding?
**** Probably remove some of the "metadata" columns
***** Need to decide on usage.  
****** Only looking at John and Acts for right now -- need to expand.


## map_structure.ipynb

Checking to see if embedding similarity can be used to approximate the structure of ESV.

 - Created ESV John
 - got everything ready for map_structure except filtering to john (KJV) and doc_compare