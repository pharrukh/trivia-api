from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Question, Category
from _data import categories_coll, questions_coll
from .question_service import Question_Service

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
    data = request.get_json()
    if not data:
        return '', 400

    if "searchTerm" in data:
        questions = questions_service.search(data['searchTerm'])

        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': 'history' # TODO: fix me
        })

    if 'question' in data:
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

