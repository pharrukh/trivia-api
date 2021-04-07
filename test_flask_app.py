import unittest
 
from flask_app import app
 
# TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        # app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        # app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #     os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()
 
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_get_categories(self):
        response = self.app.get('/categories')
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()