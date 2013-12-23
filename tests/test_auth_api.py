import unittest
from google.appengine.ext import ndb

from merkabah.core import auth
from mock import patch


class BaseAuthApiTest(unittest.TestCase):

    def make_user(self, **kwargs):
        defaults = {}
        defaults['username'] = 'test.username'
        defaults['first_name'] = 'Jane'
        defaults['last_name'] = 'Doe'
        defaults['email'] = 'jane.doe@gmail.com'
        defaults['key'] = ndb.Key('User', '1229')

        defaults.update(kwargs)
        return auth.models.User(**defaults)

    def make_account(self, **kwargs):
        defaults = {}
        defaults['account_name'] = 'ACME'
        defaults['account_id'] = '1234'
        defaults['key'] = ndb.Key('Account', '1234')

        defaults.update(kwargs)
        return auth.models.Account(**defaults)


class AccountApiTests(BaseAuthApiTest):
    """
    Set of tests surrounding the internal account api
    """

    @patch('merkabah.core.auth.models.Account.put')
    @patch('merkabah.core.auth.log_event')
    def test_create(self, m_log, m_put):
        m_put.return_value = 'SOME KEY'
        a_key = auth.create_account('Test Account', '1234')
        self.assertEqual(m_put.call_count, 1)
        self.assertEqual(a_key, 'SOME KEY')

        m_log.assert_called_once_with('account_created', 'SOME KEY', None)


class UserApiTests(BaseAuthApiTest):

    @patch('merkabah.core.auth.models.User.put')
    @patch('merkabah.core.auth.log_event')
    def test_create(self, m_log, m_put):
        m_put.return_value = 'SOME KEY'
        a_key = auth.create_user('jane.doe', 'jane@example.com', 'Jane', 'Doe')
        self.assertEqual(m_put.call_count, 1)
        self.assertEqual(a_key, 'SOME KEY')

        m_log.assert_called_once_with('user_created', 'SOME KEY', None)

    @patch('google.appengine.ext.ndb.query.Query.fetch')
    def test_get_logins(self, m_filter):
        # TODO: Figure out how to mock Query.filter and check the kwargs

        m_filter.return_value = ['l1', 'l2']

        user = self.make_user()
        result = auth.get_logins(user)
        self.assertEqual(['l1', 'l2'], result)

    @patch('google.appengine.ext.ndb.query.Query.get')
    def test_get_user_by_username(self, m_get):
        # TODO: Normalize username
        username = 'jane.doe'
        expected_user = self.make_user()
        m_get.return_value = expected_user
        result = auth.get_user_by_username(username)

        self.assertEqual(result, expected_user)


class LoginApiTests(BaseAuthApiTest):

    @patch('merkabah.core.auth.models.Login.put')
    @patch('merkabah.core.auth.log_event')
    def test_create(self, m_log, m_put):

        user = self.make_user(username='Facebook Bob')
        auth_type = 'facebook'
        auth_token = 'asdf'
        auth_data = 'qwerty'

        m_put.return_value = 'SOME KEY'

        l_key = auth.create_login(user, auth_type, auth_token, auth_data)

        self.assertEqual(m_put.call_count, 1)
        self.assertEqual(l_key, 'SOME KEY')

        m_log.assert_called_once_with('login_added', l_key, None)

    def test_generate_key_name(self):
        test_user_key = ndb.Key('User', '1234')
        user = self.make_user(key=test_user_key)
        result = auth.models.Login.generate_key_name(user, 'facebook')
        self.assertEqual('1234:facebook', result)

    def test_generate_key(self):
        test_user_key = ndb.Key('User', '1234')
        user = self.make_user(key=test_user_key)
        result = auth.models.Login.generate_key(user, 'facebook')

        self.assertEqual(result.parent(), test_user_key)
        self.assertEqual(result.id(), '1234:facebook')
    
    @patch('google.appengine.ext.ndb.key.Key.get')
    def test_get_login_by_user_and_type(self, m_get):
        m_get.return_value = 'Some Login'
        test_user_key = ndb.Key('User', '1234')
        user = self.make_user(key=test_user_key)
        result = auth.get_login_by_user_and_type(user, 'facebook')

        self.assertEqual(result, 'Some Login')


class MembershipApiTests(BaseAuthApiTest):

    @patch('merkabah.core.auth.models.Membership.put')
    @patch('merkabah.core.auth.log_event')
    def test_create(self, m_log, m_put):

        user = self.make_user(username='Facebook Bob')
        account = self.make_account(account_name='Brain Co')

        m_put.return_value = 'SOME KEY'
        m_key = auth.create_membership(user, account)

        self.assertEqual(m_put.call_count, 1)
        self.assertEqual(m_key, 'SOME KEY')

        m_log.assert_called_once_with('membership_added', m_key, None)
