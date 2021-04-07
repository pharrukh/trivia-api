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
        json_data = response.get_json()

        self.assertIsNotNone(json_data['categories'])
        self.assertEqual(response.status_code, 200)

    def test_get_questions(self):
        response = self.app.get('/questions')
        json_data = response.get_json()

        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])
        self.assertIsNotNone(json_data['categories'])
        self.assertIsNotNone(json_data['current_category'])

        self.assertEqual(response.status_code, 200)

    def test_post_questions_search(self):
        response = self.app.post('/questions', json={'searchTerm': 'president'})
        json_data = response.get_json()

        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])
        self.assertIsNotNone(json_data['current_category'])

        self.assertEqual(response.status_code, 200)

    def test_post_questions_create(self):
        response = self.app.post('/questions', json={'id': 99, 'question':'Where is Uzbekistan located?', 'answer':'Central Asia', 'category':'geography'})
        self.assertEqual(response.status_code, 204)

    def test_delete_questions(self):
        response = self.app.delete('/questions/2')
        self.assertEqual(response.status_code, 204)

    def test_get_questions_by_category(self):
        response = self.app.get('/categories/history/questions')
        json_data = response.get_json()

        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])
        self.assertIsNotNone(json_data['current_category'])

        self.assertEqual(response.status_code, 200)

    def test_post_quizzes(self):
        response = self.app.post('/quizzes', json={'quiz_category': 'history', 'previous_questions': []})
        json_data = response.get_json()

        self.assertIsNotNone(json_data['question'])
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()