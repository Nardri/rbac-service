"""Module for all constants"""

CHARSETS = ['utf-8', 'ascii']
EXCLUDES = ['password']

SUCCESS_MESSAGES = {
    'CREATED':
    'Successfully created {}.',
    'FETCHED':
    'Successfully fetched {}.',
    'UPDATE':
    'Successfully updated {}.',
    'DELETE':
    'Successfully deleted {}.',
    'ADDED':
    'Successfully granted "{}" rights to the {} role for the {} '
    'service.',
}

ERROR_MESSAGES = {
    'DUPLICATES':
    '{} already exists.',
    'DUPLICATE_PERMISSION':
    'The {} role already has this permission for the '
    '{} service.',
    'NO_SPACE':
    'No spaces between words.',
    'INVALID_ID':
    'Invalid id provided.',
    'NOT_FOUND':
    'Sorry, we could not find what you re looking for.',
    'DOES_EXIST':
    '{} with the provided ID doesn\'t exist.',
    'INVALID_INPUT_NAME':
    'Length must be between 3 and 100.',
    'ALREADY_HAS_FULL_ACCESS':
    'The {} role already has full access to the '
    '{} service.'
}
