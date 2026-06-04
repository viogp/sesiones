Testing = True
lang = 'es' # Either 'en' for English or 'es' for Spainish

# Sentence on your big and crazy project
mipgl = 'Pensar a lo grande, sacar el artículo de las líneas, escribir el capítulo de SAMs'

# Set up for scheduling work sessions (vamos.py)
# First block, including the break, goes up to either :00 or :30
# The work session will finilise at the provided time in the command line
short_rest = False

mins_work = 75.  # Minutes per work block
mins_b_0  = 14.  # Shortest first block
mins_b_n  = 30.  # Shortest last block
mins_rest = 15.  # Minutes to rest
mins_res0 = 10.  # First rest
if short_rest:
    mins_rest = 10.  # Minutes to rest 
    mins_res0 =  7.  # First rest

# Set up for reflect and planning (ayuda.py)
# Only in Spanish
min_refl  =  3.  # Minutes to reflect
s_respir  =  5.  # Seconds to breath

# Commands to open information on projects, agenda, etc to be checked
info_projects = True
if info_projects:
    path2project = "emacs ~/roots/project.org &"
    path2papers = "libreoffice ~/roots/papers.ods &"
    path2metas = "emacs ~/roots/annual_reviews.org &"


