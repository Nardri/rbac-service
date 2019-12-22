"""Module for all constants"""

CHARSETS = ['utf-8', 'ascii']
EXCLUDES = ['password']

SUCCESS_MESSAGES = {
    'CREATED': 'Successfully created {}.',
    'FETCHED': 'Successfully fetched {}.',
    'UPDATE': 'Successfully updated {}.',
    'DELETE': 'Successfully deleted {}.',
}

ERROR_MESSAGES = {
    'DUPLICATES': '{} already exists.',
    'NO_SPACE': 'No spaces between words.',
    'INVALID_ID': 'Invalid id provided.',
    'NOT_FOUND': 'Sorry, we could not find what you re looking for.',
    'INVALID_INPUT_NAME': 'Length must be between 3 and 100.'
}
