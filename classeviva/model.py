from collections import namedtuple


Grade = namedtuple(
    'Grade', 
    [
        'value',
        'display_value',
        'subject',
        'date',
        'color',
        'comment'
    ])