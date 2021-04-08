from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_
from flask_cors import CORS, cross_origin
from .models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app():
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "https://www.normuradov.com/"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',
                            'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def quizzes():
        data = request.get_json()
        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']

        category_result = Category.query.filter(Category.type == quiz_category).first()
        query_result = None

        if not category_result:
            query_result = Question.query.filter( (~Question.id.in_(previous_questions))).first()
        else:
            category = category_result.format()
            query_result = Question.query.filter( (~Question.id.in_(previous_questions)) & (Question.category == category['id'])).first()

        if not query_result:
            return jsonify( { 'question': None } )

        return jsonify({'question': query_result.format()})


    @app.route('/categories', methods=['GET'])
    @cross_origin()
    def categories():
        return jsonify({'categories': get_categories()})


    @app.route('/questions', methods=['GET'])
    @cross_origin()
    def questions():
        value = request.args.get('page')
        if not value:
            value = '1'
        page = int(value)

        if page == 0:
            page = 1
        skip = (page - 1) * QUESTIONS_PER_PAGE

        query_result = db.session.query(Question.id.label('id'), Question.question.label('question'), Question.answer.label('answer'), Question.difficulty.label('difficulty'), Category.type.label('category')).join(Category, Question.category == Category.id).limit(QUESTIONS_PER_PAGE).offset(skip).all()
        questions = [map_to_question(q) for q in query_result]
        return jsonify({
            'questions': questions,
            'total_questions': Question.query.count(),
            'categories': get_categories(),
            'current_category': 'history' # TODO: fix me
        })

    @app.route('/questions', methods=['POST'])
    @cross_origin()
    def search_questions():
        data = request.get_json()
        if not data:
            return '', 400

        if "search_term" in data:
            query_result = db.session.query(Question.id.label('id'), Question.question.label('question'), Question.answer.label('answer'), Question.difficulty.label('difficulty'), Category.type.label('category')).filter(Question.question.ilike(f'%{data["search_term"]}%')).join(Category, Question.category == Category.id).all()
            questions = [map_to_question(q) for q in query_result]

            return jsonify({
                'questions': questions,
                'total_questions': len(questions),
                'current_category': 'history' # TODO: fix me
            })

        if 'question' in data:
            passed_category = data['category']
            category_result = Category.query.filter(Category.type == passed_category).first()
            if not category_result:
                return f'category "{passed_category}" not found', 404
            category = category_result.format()

            question = Question(
                question=data['question'], 
                answer=data['answer'],
                difficulty=data['difficulty'],
                category=category['id']
                )
            question.insert()
            return '', 204

        return '', 400


    @app.route('/questions/<int:id>', methods=['DELETE'])
    @cross_origin()
    def delete_question(id):
        question = Question.query.get(id)
        question.delete()
        return '', 204


    # TODO: this is not paginated it is an obvious bug but not in the spec
    @app.route('/categories/<string:name>/questions', methods=['GET'])
    @cross_origin()
    def get_questions_by_category_name(name):
        category_result = Category.query.filter(Category.type == name).first()
        if not category_result:
            return f'category "{name}" not found', 404

        category = category_result.format()
        query_result = db.session.query(Question.id.label('id'), Question.question.label('question'), Question.answer.label('answer'), Question.difficulty.label('difficulty'), Category.type.label('category')).join(Category, Question.category == category['id']).filter(Category.id == category['id']).all()
        questions = [map_to_question(q) for q in query_result]

        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': name
        })

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

    return app

def get_categories():
    result = {}
    categories = [c.format() for c in Category.query.all()]
    for category in categories:
        result[category['type']] = category['type']
    return result

def map_to_question(result):
    id,question,answer,difficulty,category = result
    return {
      'id': id,
      'question': question,
      'answer': answer,
      'category': category,
      'difficulty': difficulty
    }