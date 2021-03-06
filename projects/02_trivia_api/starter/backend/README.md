# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/questions?page=1'
- Fetches a list of 10 questions, with 10 being the number of questions in one page. Each questions is a dictionary with the keys "answer", "category", "difficulty", "id" and "question"
- Fetches a list of all existing categories
- Fetches the count of total questions
- Fetches id of current category, with category being a query string that can be passed in the request
- Request Arguments: query string 'page' and 'category' 
- Returns: An object with 5 keys: categories, current_category, questions, success, total_questions
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Diogo", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "what is my name?"
    }, 
    {
      "answer": null, 
      "category": null, 
      "difficulty": null, 
      "id": 25, 
      "question": null
    }, 
    {
      "answer": null, 
      "category": null, 
      "difficulty": null, 
      "id": 26, 
      "question": null
    }, 
    {
      "answer": "Fe", 
      "category": 1, 
      "difficulty": 3, 
      "id": 27, 
      "question": "What is the element for iron"
    }, 
    {
      "answer": "Ronaldo", 
      "category": 6, 
      "difficulty": 1, 
      "id": 30, 
      "question": "Who is the best footbal player of all time?"
    }
  ], 
  "success": true, 
  "total_questions": 25
}


DELETE '/questions/<int:question_id>'
- Fetches the questions with id passed in the request
- Request arguments: question id
- Returns id of deleted question and success key. If id passed does not exist returns and error


POST '/questions'
- Request arguments: An object with keys question, answer, difficulty, category.
{question: "asfasd", answer: "asdf", difficulty: 1, category: 1}
- Returns an object with keys, answer, category, created (representing the question id), difficulty, question.
{
  "answer": "asdf", 
  "category": 1, 
  "created": 36, 
  "difficulty": 1, 
  "question": "asfasd", 
  "success": true
}

POST '/questions/search'
- Fetches all questions for which the question field matches fully or partially a search term. Matching is not case sensitive
- Request arguments: An object with key 'searchTerm' and value string with text to search
{searchTerm: "my question"}
- Returns an object with current category, list of questions where the value of the field 'question' matches the search term, total questions that have a match with the search term
{
  "current_category": null, 
  "questions": [], 
  "success": true, 
  "total_questions": 0
}

GET '/categories/<int:category_id>/questions'
- Fetches questions that belong to category id
- Request arguments: category id
- Returns an object with keys, currentCategory, questions and total_questions in this category
{
  "currentCategory": 6, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "Ronaldo", 
      "category": 6, 
      "difficulty": 1, 
      "id": 30, 
      "question": "Who is the best footbal player of all time?"
    }
  ], 
  "sucess": true, 
  "total_questions": 3
}


POST '/quizzes'
- Fetches questions from all or a particular category
- Request arguments: list of previous questions shown to the user and the quiz category
{previous_questions: [], quiz_category: {type: "Science", id: "1"}}
- Returns an object with the keys question and as value a dictionary with the key answer, category, difficulty, id and question
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```