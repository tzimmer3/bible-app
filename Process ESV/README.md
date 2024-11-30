

## ESV bible.pdf

Lots of text nested under each observation

Need to split on \n and see what that yields

Need to remove footnotes pages


Desired End state:

Text separated out by verse

Colums = ['book', 'chapter', 'heading', 'verse', 'text']


## map_structure.ipynb

Checking to see if embedding similarity can be used to approximate the structure of ESV.

 - Created ESV John
 - got everything ready for map_structure except filtering to john (KJV) and doc_compare