# Udacity's Full Stack Developer Nano Degree

I am enrolled in Udacity's Full Stack Developer Nano Degree. Throughout the course I will list here the projets that I have completed and a summary of learnings of each project.

This is a forked repo. All the projects can be found in the `projects` folder.

## Projects

### 01_fyyur [Passed review]
The goal of the project was to complete the Fyyur app, with the help of Udacity's starter code: adding the missing models, controllers and completing views.

Fyyur is a CRUD app where the user can list venues, artists and shows. The user can create a new venue, artist or show, view the existing venues, artists and shows, update them and delete them.

The app is built with Python, Flask, SQLAlchemy and has a PostgreSQL DB.

#### Learning Highlights:
- How to create a simple CRUD that is connected to a DB 
- Used migrations to update the DB models with Flask db migrate
- Learned about Fetch and the methods POST, GET and DELETE
- Used the Model Controller View pattern to structure my app
- Used the SQLAlchemy query API
- Creating relationships in SQLAlchemy
- Used the WTForms library for form validation and rendering in Python
- How to flash messages to improve user feedback


### 02_trivia_api [In review]
The goal of this project was to implement enpoints, write unit tests and documentation in order to complete the Trivia app. 
Udacity provided a started code that included the frontend and the database models. 

The Trivia app is a game where users can view questions by category such as science, art and sports. Questions are rated by difficulty.

The user can delete questions, add new ones or use search to find questions. Finally there is a game in which the user can choose a category and try to answer questions. For each correct answer the user gets a point.

The app runs on a Flask server, with as PostgresSQL DB. The frontend has NodeJs as dependency and uses React.

#### Learning Highlights:
- Understanding the elements of HTTP requests: Method, Path, HTTP version, Headers, Body
- Understanding the elements of HTTP response: Status code and status message, Headers and content type
- Know the categories of status codes and the most common codes
- Using Chrome's Dev Tools and curl in terminal
- Error handling using `@app.errorhandler` decorator
- Cross-Origin Resource Sharing with the Flask **CORS extension**
- Writing unit tests
- API reference and writing endpoint documentation


