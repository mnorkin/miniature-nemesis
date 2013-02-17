"""
The Utils 
"""

import unidecode
import re

# Settings
DEBUG = True

# Handy utils
def message(str):
  """
  Message parser (logging the activity of the app)
  """
  pass

def slugify(str):
  """
  Slugify the string
  """
  str = unidecode.unidecode(str.encode('utf-8')).lower()
  str = re.sub(r'\W+', '-', str)

  # Just to be on the safe side
  if str[str.__len__()-1] == '-':
    str = str[:-1]

  return str