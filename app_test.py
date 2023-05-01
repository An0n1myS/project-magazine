import unittest
from io import BytesIO

import main


class FlaskTest(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_login(self):
        response = self.app.post('/login', data=dict(username='test', password='password'))
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        response = self.app.post('/register', data=dict(username='test', email='test@example.com', password='password'))
        self.assertEqual(response.status_code, 302)



    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
