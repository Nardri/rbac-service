"""API response"""

from src.utils.constants import SUCCESS_MESSAGES


def response(response=None, message=None, status_code=200, object_name=None):
    """A helper method for return api response.
    Args:
        object_name (str):
        message (str):
        response (any): response
        status_code (int): Status code
    Raises:
        Tuple
    """
    msg = 'Operation was successful.'
    data = dict(status='success', message=message or msg)
    if status_code is 201 and object_name is not None:
        data['message'] = SUCCESS_MESSAGES['CREATED'].format(object_name)

    if response:
        data['data'] = response

    return data, status_code
