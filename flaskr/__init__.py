import logging
import azure.functions as func
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

categories_coll = [
    {'id': 1, 'name': 'politics'},
    {'id': 2, 'name': 'history'},
    {'id': 3, 'name': 'Quotes'},
]

questions_coll = [
    {
        'id': 1,
        'text': 'Who is the author of the anthem of Uzbekistan?',
        'answer': 'Abdulla Aripov',
        'category': 1
    },
    {
        'id': 2,
        'text': 'Who is the first president of Uzbekistan?',
        'answer': 'Islam Karimov',
        'category': 1
    },
    {
        'id': 3,
        'text': 'On what year did Uzbekistan declare independence?',
        'answer': '1991',
        'category': 1
    },
    {
        'id': 4,
        'text': 'What is the name of the second president of Uzbekistan?',
        'answer': 'Shavkat Mirziyaev',
        'category': 1
    },
    {
        'id': 5,
        'text': 'What is the northen neighbor of Uzbekistan?',
        'answer': 'Kazakhstan',
        'category': 1
    },
    {
        'id': 6,
        'text': 'Is population of Uzbeksistan larger than 30 million?',
        'answer': 'Yes',
        'category': 1
    },
    {
        'id': 7,
        'text': 'To whom does this quote belong: "I prefer a short life with width to a narrow one with length."',
        'answer': 'Avicenna',
        'category': 3
    },
    {
        'id': 8,
        'text': 'To whom does this quote belong: "My own soul is my most faithful friend. My own heart, my trust confidant."',
        'answer': 'Babur',
        'category': 3
    },
    {
        'id': 9,
        'text': 'Who is the national hero is Uzbekistan?',
        'answer': 'Amir Temur',
        'category': 2
    },
    {
        'id': 10,
        'text': 'Whot was the capital of Amir Timur\'s country?',
        'answer': 'Samarkand',
        'category': 2
    },
    {
        'id': 11,
        'text': 'Who is the greatest grandson of Amir Timur?',
        'answer': 'Ulugh Bek',
        'category': 2
    },
    {
        'id': 12,
        'text': 'Who was Ulugh Bek\'s father?',
        'answer': 'Shakhrukh',
        'category': 2
    },
    {
        'id': 13,
        'text': 'How did arabs call the territory above Amu Darya?',
        'answer': 'Mawarannahr',
        'category': 2
    },
    {
        'id': 14,
        'text': 'How did arabs call the territory above Amu Darya?',
        'answer': 'Mawarannahr',
        'category': 2
    },
    {
        'id': 15,
        'text': 'The name of what city is "rich settlement"?',
        'answer': 'Samarkand',
        'category': 2
    },
    {
        'id': 16,
        'text': 'Who is the most known poet of Timurid period?',
        'answer': 'Ali Shir Nava\'i',
        'category': 2
    },
    {
        'id': 17,
        'text': 'What language was used in Timurid empire?',
        'answer': 'Chagatai',
        'category': 2
    },
    {
        'id': 18,
        'text': 'Which dynasty brought "Uzbek" name to Timurid nations?',
        'answer': 'Shaybanid',
        'category': 2
    },
    {
        'id': 19,
        'text': 'In what year did mongols besiege Samarkand?',
        'answer': '1220',
        'category': 2
    },
    {
        'id': 20,
        'text': 'What was the name of the Kharesm emperor that oppossed Ghengis Khan?',
        'answer': 'Mukhammad',
        'category': 2
    },
    {
        'id': 21,
        'text': 'What name did Vyatkin give to the ruins that were left by mongols?',
        'answer': 'Afrosiab',
        'category': 2
    },
    {
        'id': 22,
        'text': 'What was the main tool of Ulug Bek\'s observatory?',
        'answer': 'Sekstant',
        'category': 2
    },
    {
        'id': 23,
        'text': 'Is it true that Uzbek and Turkish belong to the same language family?',
        'answer': 'Yes',
        'category': 2
    },
    {
        'id': 24,
        'text': 'Is it true that many people in Samarkand speak Tajik?',
        'answer': 'Yes',
        'category': 2
    }
]

app = Flask(__name__)
#   '''
#   @TODO: Use the after_request decorator to set Access-Control-Allow
#   '''
cors = CORS(app, resources={r"/questions": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/categories', methods=['GET'])
@cross_origin()
def categories():
    return jsonify(categories_coll)


@app.route('/questions', methods=['GET'])
@cross_origin()
def questions():
    return jsonify(questions_coll)

#   '''
#   @TODO:
#   Create an endpoint to handle GET requests
#   for all available categories.
#   '''


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(req.params)
    uri = req.params['uri']
    with app.test_client() as c:
        doAction = {
            "GET": c.get(uri).data,
            "POST": c.post(uri).data
        }
        resp = doAction.get(req.method).decode()
        return func.HttpResponse(resp, mimetype='text/html')


class Question_Service:
    def __init__(self, questions):
        self.questions = questions

    #   '''
    #   @TODO:
    #   Create an endpoint to handle GET requests for questions,
    #   including pagination (every 10 questions).
    #   This endpoint should return a list of questions,
    #   number of total questions, current category, categories.

    #   TEST: At this point, when you start the application
    #   you should see questions and categories generated,
    #   ten questions per page and pagination at the bottom of the screen for three pages.
    #   Clicking on the page numbers should update the questions.
    #   '''
    def get_by(category):
        return self.questions

    #   '''
    #   @TODO:
    #   Create an endpoint to POST a new question,
    #   which will require the question and answer text,
    #   category, and difficulty score.

    #   TEST: When you submit a question on the "Add" tab,
    #   the form will clear and the question will appear at the end of the last page
    #   of the questions list in the "List" tab.
    #   '''
    def add(question):
        self.questions.append(question)

    #   '''
    #   @TODO:
    #   Create an endpoint to DELETE question using a question ID.

    #   TEST: When you click the trash icon next to a question, the question will be removed.
    #   This removal will persist in the database and when you refresh the page.
    #   '''
    def remove(id):
        filtered_questions = [question for question in self.questions if question.id != id]
        self.questions = filtered_questions

# def create_app(test_config=None):
#   # create and configure the app
#   app = Flask(__name__)
#   setup_db(app)

#   '''
#   '''






#   '''
#   @TODO:
#   Create a POST endpoint to get questions based on a search term.
#   It should return any questions for whom the search term
#   is a substring of the question.

#   TEST: Search by any phrase. The questions list will update to include
#   only question that include that string within their question.
#   Try using the word "title" to start.
#   '''

#   '''
#   @TODO:
#   Create a GET endpoint to get questions based on category.

#   TEST: In the "List" tab / main screen, clicking on one of the
#   categories in the left column will cause only questions of that
#   category to be shown.
#   '''


#   '''
#   @TODO:
#   Create a POST endpoint to get questions to play the quiz.
#   This endpoint should take category and previous question parameters
#   and return a random questions within the given category,
#   if provided, and that is not one of the previous questions.

#   TEST: In the "Play" tab, after a user selects "All" or a category,
#   one question at a time is displayed, the user is allowed to answer
#   and shown whether they were correct or not.
#   '''

#   '''
#   @TODO:
#   Create error handlers for all expected errors
#   including 404 and 422.
#   '''

#   return app
