import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  [DONE]
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs 
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  [DONE]
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  '''
  [DONE]
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():  
    try:
      categories = Category.query.all() # query for all categories in the db
      result = {cat.id:cat.type for cat in categories} # hat tip to student in https://knowledge.udacity.com/questions/82388 whose question helped me here

      if len(categories) == 0: 
        abort(404) # Not found

      return jsonify({
      'success': True,
      'categories': result
      })

    except:
      abort(400) # bad request 



  '''
  [DONE]
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
    try:

      page = request.args.get('page', 1, type=int) #if the client does not include the argument for page, the value will default to 1.
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE # gives me start and end index to use when slicing the questions list

      questions = Question.query.all()
      formated_questions = [question.format() for question in questions]
      page_questions = formated_questions[start:end]
      categories = Category.query.all()
       
      '''I choose to show all categories available even if there are no questions in the category.
      An alternative approach would be to show only the categories for which I have questions'''
      formated_categories = [category.type for category in categories] 

      '''current category given by the query string'''
      current_category = request.args.get('category', None, type=int)

      if len(page_questions) == 0:
        abort(404) # Not found: in case I request a page that does not exist
     

      return jsonify({
        'success': True,
        'questions': page_questions,
        'total_questions': len(formated_questions),
        'current_category': current_category,
        'categories': formated_categories
        })

    except:
      abort(400) # bad request

  '''
  [DONE]
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error = False
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404) # Not found
      else:
        question.delete()

        return jsonify({
          'success': True,
          'deleted': question_id
          })


    except:
      abort(422)
  


  '''
  [DONE]
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def create_question():
    body = request.get_json()
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)

    try:
      question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id,
        'question': question.question,
        'answer': question.answer,
        'category': question.category,
        'difficulty': question.difficulty
        })
    except:
      abort(422)


  '''
  [DONE]
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search():
    body = request.get_json()
    search = body.get('searchTerm')
    try:
      results = Question.query.filter(Question.question.ilike('%' + search + '%')).all()
      formated_result = [result.format() for result in results]
      count = Question.query.filter(Question.question.ilike('%' + search + '%')).count()
      current_category = None

      return jsonify({
        'success': True,
        'questions': formated_result,
        'total_questions': count,
        'current_category': current_category
        })

    except:
      abort(422)

  '''
  [DONE]
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def questions_by_category(category_id):
    try:
      questions_by_cat = Question.query.filter(Question.category == category_id).all()
      formated_questions = [question.format() for question in questions_by_cat]

      return jsonify({
        'success': True,
        'questions': formated_questions,
        'total_questions': len(formated_questions),
        'currentCategory': category_id
        })
    except:
      abort(422)


  '''
  [DONE]
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizz():
    body = request.get_json()
    previous_questions = body.get('previous_questions') # gives me a list with previous questions
    category = body.get('quiz_category')

    if category.get('id') == 0: # when user chooses to play all categories
      current_question = Question.query.filter(~Question.id.in_(previous_questions)).first()
      if current_question:
        formated_question = current_question.format()
      else:
        abort(404) # no more questions available
    else:
      current_question = Question.query.filter(Question.category == category.get('id'), ~Question.id.in_(previous_questions)).first()
      if current_question:
        formated_question = current_question.format()
      else:
        abort(404)

    return jsonify({
      'success': True,
      'question': formated_question
      })
      



  '''
  [DONE]
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not found', 
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
      }), 400

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
      }), 422

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
      }), 405

  @app.errorhandler(500)
  def internal(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
      }), 500

  
  return app

    