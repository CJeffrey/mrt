from enum import Enum

# Used for make tags for Different MRT lines
LineTags = Enum(
    'LineTags',
    ('NS', 'EW', 'CG', 'NE', 'CC', 'CE', 'DT', 'TE',
     'LINE_CHANGE',  # special tag for changing the line
     )
)
