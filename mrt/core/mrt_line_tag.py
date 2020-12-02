from enum import Enum

LineTags = Enum(
    'LineTags',
    ('NS', 'EW', 'CG', 'NE', 'CC', 'CE', 'DT', 'TE',
     'LINE_CHANGE',  # special tag for changing the line
     )
)
