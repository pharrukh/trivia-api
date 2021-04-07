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
        return [
            q for q in self.questions if q['category'] == category_name
        ]

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
            q for q in self.questions if q['id'] != id
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
        return [ q for q in self.questions if text in q['question']]

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
        questions = self.questions
        if category:
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
    for q in questions:
        if skip > count:
            count += 1
            continue
        result.append(q)
        count += 1
        if len(result) == take:
            break

    return result
