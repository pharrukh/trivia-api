# Full Stack Trivia API Backend

[![Build Status](https://dev.azure.com/normuradov0143/normuradov/_apis/build/status/pharrukh.trivia-api?branchName=master)](https://dev.azure.com/normuradov0143/normuradov/_build/latest?definitionId=9&branchName=master)

## requirements

Can be found [here](https://github.com/pharrukh/trivia-api/blob/master/requirements.png).

## getting Started

### installing Dependencies

```bash
pip install -r requirements.txt
```

## running the application

```bash
func start
```

## api documentation

### POST /quizzes

single next question for a quiz on a given category or all categories

#### - request body:

```json
{
  "previous_questions": int[],
  "quiz_category": string | null,
}
```

#### - response:

```json
{
  "question": {
    "id": int,
    "question": string,
    "answer": string,
    "difficulty": int,
    "category": string
  }
}
```

### GET /categories

#### - response:

```json
{
  [category_name] : string,
  ...
}
```

#### - response example:

```json
{
  "history": "history",
  "geography": "geography"
}
```

### GET /categories/string:name/questions

### - response

```json
{
  "questions": [
    {
      "id": int,
      "question": string,
      "answer": string,
      "difficulty": int,
      "category": string
    },
    ...
  ],
  "total_questions": int,
  "current_category": string
}
```

### GET /questions
default page size is 10
```json
{
  "questions": [
    {
      "id": int,
      "question": string,
      "answer": string,
      "difficulty": int,
      "category": string
    },
    ...
  ],
  "total_questions": int,
  "categories": { [string]: string },
  "current_category": string
}
```

### DELETE /questions/int:id
response, no content, 204
### POST /questions
#### 1) search by term
request
```json
{
  "search_term": string
}
```
response, 200
```json
{
  "questions": [
    {
      "id": int,
      "question": string,
      "answer": string,
      "difficulty": int,
      "category": string
    },
    ...
  ],
  "total_questions": int,
  "current_category": string
}
```
#### 2) create a question
request
```json
{
  "question": {
      "id": int,
      "question": string,
      "answer": string,
      "difficulty": int,
      "category": string
    }
}
```
response, no content, 204

## testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flask_app.py
```

## deployment

Build and release service by Microsoft, Azure DevOps handles the deployment.
Build pipeline can be found by clicking on the build status badge above 👆.

## acknoledgement

Thanks, Hanzhang Zeng, for the [repo](https://github.com/Hazhzeng/functions-wsgi-demo)
Thanks, Patrick Kennedy for the [neat unittest + flask example](https://www.patricksoftwareblog.com/unit-testing-a-flask-application/)

## about the author

![normuradov logo](https://raw.githubusercontent.com/pharrukh/pharrukh/master/normuradov.png "Logo")

I inspire people and bring value.

[![github](https://raw.githubusercontent.com/pharrukh/pharrukh/master/icons/github.png "GitHub")](https://github.com/pharrukh)
[![linkedin](https://raw.githubusercontent.com/pharrukh/pharrukh/master/icons/linkedin.png "LinkedIn")](https://www.linkedin.com/in/farrukh-normuradov/)
[![stackoverflow](https://raw.githubusercontent.com/pharrukh/pharrukh/master/icons/stackoverflow.png "StackOverflow")](https://stackoverflow.com/users/3407539/farrukh-normuradov)
[![website](https://raw.githubusercontent.com/pharrukh/pharrukh/master/icons/website.png "normuradov.com")](https://www.normuradov.com/)
