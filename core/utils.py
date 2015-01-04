"""
.. module:: merkabah.core.utils
   :synopsis: Helper methods

.. moduleauthor:: Blaine Garrett <blaine@blainegarrett.com>

"""

def slugify(s):
    s = unicodedata.normalize('NFKD', s)
    s = slug.encode('ascii', 'ignore').lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    s = re.sub(r'[-]+', '-', s)
    return s