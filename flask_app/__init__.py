from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

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

    def get_all(self, page=1):
        if page == 0:
            page = 1
        skip = (page - 1) * QUESTIONS_PER_PAGE
        return get(self.questions, skip)

    #   '''
    #   @TODO:
    #   Create a GET endpoint to get questions based on category.

    #   TEST: In the "List" tab / main screen, clicking on one of the
    #   categories in the left column will cause only questions of that
    #   category to be shown.
    #   '''

    def get_by_category_name(self, category_name):
        filtered_questions = [
            question for question in self.questions if question['category'] == category_name
        ]
        return filtered_questions

    #   '''
    #   @TODO:
    #   Create an endpoint to POST a new question,
    #   which will require the question and answer text,
    #   category, and difficulty score.

    #   TEST: When you submit a question on the "Add" tab,
    #   the form will clear and the question will appear at the end of the last page
    #   of the questions list in the "List" tab.
    #   '''
    def add(self, question):
        self.questions.append(question)

    #   '''
    #   @TODO:
    #   Create an endpoint to DELETE question using a question ID.

    #   TEST: When you click the trash icon next to a question, the question will be removed.
    #   This removal will persist in the database and when you refresh the page.
    #   '''
    def remove(self, id):
        filtered_questions = [
            question for question in self.questions if question['id'] != id
        ]
        self.questions = filtered_questions

    #   '''
    #   @TODO:
    #   Create a POST endpoint to get questions based on a search term.
    #   It should return any questions for whom the search term
    #   is a substring of the question.

    #   TEST: Search by any phrase. The questions list will update to include
    #   only question that include that string within their question.
    #   Try using the word "title" to start.
    #   '''
    def search(self, text):
        print('text', text)
        filtered_questions = [
            q for q in self.questions if text in q['question']]
        return filtered_questions

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

    def get_for_quiz(self, category, previous_question_ids):
        questions = self.get_by_category_name(category)
        for q in questions:
            if q['id'] not in previous_question_ids:
                return q
        return None

    def get_total_questions(self):
        return len(self.questions)


def get(questions, skip, take=10):
    count = 0
    result = []
    for question in questions:
        if skip > count:
            count += 1
            continue
        result.append(question)
        count += 1
        if len(result) == take:
            break
    return result


categories_coll = {
    'geography': 'geography',
    'history': 'history',
    'science': 'science'
}

questions_coll = [
    {
        'id': 1,
        'question': 'Who is the author of the anthem of Uzbekistan?',
        'difficulty': 3,
        'answer': 'Abdulla Aripov',
        'category': 'geography'
    },
    {
        'id': 2,
        'question': 'Who is the first president of Uzbekistan?',
        'difficulty': 2,
        'answer': 'Islam Karimov',
        'category': 'geography'
    },
    {
        'id': 3,
        'question': 'On what year did Uzbekistan declare independence?',
        'difficulty': 3,
        'answer': '1991',
        'category': 'geography'
    },
    {
        'id': 4,
        'question': 'What is the name of the second president of Uzbekistan?',
        'difficulty': 1,
        'answer': 'Shavkat Mirziyaev',
        'category': 'geography'
    },
    {
        'id': 5,
        'question': 'What is the northen neighbor of Uzbekistan?',
        'difficulty': 4,
        'answer': 'Kazakhstan',
        'category': 'geography'
    },
    {
        'id': 6,
        'question': 'Is population of Uzbeksistan larger than 30 million?',
        'difficulty': 1,
        'answer': 'Yes',
        'category': 'geography'
    },
    {
        'id': 7,
        'question': 'To whom does this quote belong: "I prefer a short life with width to a narrow one with length."',
        'difficulty': 5,
        'answer': 'Avicenna',
        'category': 'science'
    },
    {
        'id': 8,
        'question': 'To whom does this quote belong: "My own soul is my most faithful friend. My own heart, my trust confidant."',
        'difficulty': 5,
        'answer': 'Babur',
        'category': 'science'
    },
    {
        'id': 9,
        'question': 'Who is the national hero is Uzbekistan?',
        'difficulty': 2,
        'answer': 'Amir Temur',
        'category': 'history'
    },
    {
        'id': 10,
        'question': 'Whot was the capital of Amir Timur\'s country?',
        'difficulty': 4,
        'answer': 'Samarkand',
        'category': 'history'
    },
    {
        'id': 11,
        'question': 'Who is the greatest grandson of Amir Timur?',
        'difficulty': 2,
        'answer': 'Ulugh Bek',
        'category': 'history'
    },
    {
        'id': 12,
        'question': 'Who was Ulugh Bek\'s father?',
        'difficulty': 4,
        'answer': 'Shakhrukh',
        'category': 'history'
    },
    {
        'id': 13,
        'question': 'How did arabs call the territory above Amu Darya?',
        'difficulty': 4,
        'answer': 'Mawarannahr',
        'category': 'history'
    },
    {
        'id': 15,
        'question': 'The name of what city is "rich settlement"?',
        'difficulty': 5,
        'answer': 'Samarkand',
        'category': 'history'
    },
    {
        'id': 16,
        'question': 'Who is the most known poet of Timurid period?',
        'difficulty': 3,
        'answer': 'Ali Shir Nava\'i',
        'category': 'history'
    },
    {
        'id': 17,
        'question': 'What language was used in Timurid empire?',
        'difficulty': 5,
        'answer': 'Chagatai',
        'category': 'history'
    },
    {
        'id': 18,
        'question': 'Which dynasty brought "Uzbek" name to Timurid nations?',
        'difficulty': 4,
        'answer': 'Shaybanid',
        'category': 'history'
    },
    {
        'id': 19,
        'question': 'In what year did mongols besiege Samarkand?',
        'difficulty': 4,
        'answer': '1220',
        'category': 'history'
    },
    {
        'id': 20,
        'question': 'What was the name of the Kharesm emperor that oppossed Ghengis Khan?',
        'difficulty': 4,
        'answer': 'Mukhammad',
        'category': 'history'
    },
    {
        'id': 21,
        'question': 'What name did Vyatkin give to the ruins that were left by mongols?',
        'difficulty': 2,
        'answer': 'Afrosiab',
        'category': 'history'
    },
    {
        'id': 22,
        'question': 'What was the main tool of Ulug Bek\'s observatory?',
        'difficulty': 4,
        'answer': 'Sekstant',
        'category': 'history'
    },
    {
        'id': 23,
        'question': 'Is it true that Uzbek and Turkish belong to the same language family?',
        'difficulty': 3,
        'answer': 'Yes',
        'category': 'history'
    },
    {
        'id': 24,
        'question': 'Is it true that many people in Samarkand speak Tajik?',
        'difficulty': 1,
        'answer': 'Yes',
        'category': 'history'
    }
]

app = Flask(__name__)

cors = CORS(app, resources={r"*": {"origins": "https://www.normuradov.com/"}})
questions_service = Question_Service(questions_coll)

#   '''
#   @TODO: Use the after_request decorator to set Access-Control-Allow
#   '''


@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers',
    #                      'Content-Type,Authorization')
    # response.headers.add('Access-Control-Allow-Methods',
    #                      'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin',
                         'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

#   '''
#   @TODO:
#   Create an endpoint to handle GET requests
#   for all available categories.
#   '''


@app.route('/quizzes', methods=['POST'])
@cross_origin()
def quizzes():
    print(request.get_json())
    data = request.get_json()
    question = questions_service.get_for_quiz(data['quiz_category'], data['previous_questions'])
    return jsonify({'question': question})


@app.route('/categories', methods=['GET'])
@cross_origin()
def categories():
    return jsonify({'categories': categories_coll})


@app.route('/questions', methods=['GET'])
@cross_origin()
def questions():
    value = request.args.get('page')
    if not value:
        value = '1'
    page = int(value)
    questions = questions_service.get_all(page)
    return jsonify({
        'questions': questions,
        'total_questions': questions_service.get_total_questions(),
        'categories': categories_coll,
        'current_category': 'history'
    })


@app.route('/questions', methods=['POST'])
@cross_origin()
def search_questions():
    print('search_post')
    data = request.get_json()
    print(request.get_data())
    if not data:
        return '', 400

    print('before search')
    if "searchTerm" in data:
        print('search')
        questions = questions_service.search(data['searchTerm'])

        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': 'history'
        })

    print('there')
    if 'question' in data:
        print(data)
        questions_service.add(data)

        return '', 204

    return '', 400


@app.route('/questions/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_question(id):
    questions_service.remove(id)
    return '', 204


@app.route('/categories/<string:name>/questions', methods=['GET'])
@cross_origin()
def get_questions_by_category_name(name):
    questions = questions_service.get_by_category_name(name)
    return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'current_category': 'history'
    })

#   '''
#   @TODO:
#   Create error handlers for all expected errors
#   including 404 and 422.
#   '''

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(401)
def server_error(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(403)
def server_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(422)
def server_error(error):
    return render_template('errors/422.html'), 422


@app.errorhandler(405)
def server_error(error):
    return render_template('./errors/405.html'), 405


@app.errorhandler(409)
def server_error(error):
    return render_template('./errors/405.html'), 409

