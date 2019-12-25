"""Miscellaneous helpers"""


def get_service_name(service_object):
    """Helper function to get the service name from the service object."""
    return service_object.name.split('_')[0].title()
