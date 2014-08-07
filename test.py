import os
from app import app, init_db
import unittest
import tempfile

class BlogrTestCase(unittest.TestCase):

    def setUp(self):
        """creates a new test client, initialize a database"""
        self.__username = app.config['USERNAME']
        self.__password = app.config['PASSWORD']
        # mkstemp() - create temporary db
        #   returns(tuple): os-level file hanlde and its absolute pathname
        self.db_fd, app.config['DATABASE_URI'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        """close and remove db"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE_URI'])

    def test_empty_db(self):
        rv = self.app.get('/') # send HTTP GET with the given path -returns a response obj
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login(self.__username, self.__password)
        assert b'Login successful!' in rv.data
        rv = self.logout()
        assert b'You are now logged out' in rv.data

        rv = self.login('wrong' + self.__username, self.__password)
        assert b'Invalid credentials' in rv.data
        rv = self.login(self.__username, 'wrong' + self.__password)
        assert b'Invalid credentials' in rv.data
        rv = self.logout()
        assert b'You are now logged out' in rv.data

    def test_messages(self):
        self.login(self.__username, self.__password)
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> is allowed in text area'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> is allowed in text area' in rv.data

if __name__ == '__main__':
    unittest.main()
