"""
Main Merkabah Package

License: TODO: Figure out appropriate license ...

"""

def is_appspot():
    import os
    return not os.environ['SERVER_SOFTWARE'].startswith('Development')

def get_domain():
    import os
    return os.environ['DEFAULT_VERSION_HOSTNAME']

