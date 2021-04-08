import os
import unittest
from flask_app import create_app, setup_db
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify

class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
 
 
###############
#### tests ####
###############
 
    def test_get_non_existing_endpoint(self):
        response = self.client().get('/non-existing-endpoint')
        self.assertEqual(response.status_code, 404)
 
    def test_not_allowed_method(self):
        response = self.client().delete('/categories')
        self.assertEqual(response.status_code, 405)

    def test_get_categories(self):
        response = self.client().get('/categories')
        json_data = response.get_json()

        self.assertIsNotNone(json_data['categories'])
        self.assertEqual(response.status_code, 200)

    def test_get_questions(self):
        response = self.client().get('/questions')
        json_data = response.get_json()

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])
        self.assertIsNotNone(json_data['categories'])
        self.assertIsNotNone(json_data['current_category'])


    def test_post_questions_search(self):
        response = self.client().post('/questions', json={'search_term': 'a'})
        json_data = response.get_json()

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])
        self.assertIsNotNone(json_data['current_category'])

    def test_post_questions_create(self):
        response = self.client().post('/questions', json={'question':'Where is Uzbekistan located?', 'answer':'Central Asia', 'difficulty':1,'category':'History', })
        self.assertEqual(response.status_code, 204)

    def test_delete_questions(self):
        response = self.client().delete('/questions/2')
        self.assertEqual(response.status_code, 204)

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/History/questions')
        json_data = response.get_json()

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])
        self.assertIsNotNone(json_data['current_category'])


    def test_post_quizzes(self):
        response = self.client().post('/quizzes', json={'quiz_category': 'History', 'previous_questions': []})
        json_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json_data['question'])
 
 
if __name__ == "__main__":
    unittest.main()