import unittest
from google.appengine.ext import ndb

from merkabah.core import auth
from mock import patch
from merkabah.core.utils import slugify

class SlugifyTests(unittest.TestCase):
    """
    Set of tests surrounding the internal account api
    """

    def test_create(self):
        self.assertEqual(slugify('fish'), 'fish')
        self.assertEqual(slugify('Fish'), 'fish')
        self.assertEqual(slugify('FISH'), 'fish')
        self.assertEqual(slugify('fish sticks'), 'fish-sticks')
        self.assertEqual(slugify('Fish-Sticks'), 'fish-sticks')
        self.assertEqual(slugify('fish_sticks'), 'fish')