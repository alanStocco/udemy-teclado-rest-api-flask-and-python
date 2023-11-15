# Flask REST APIs Udemy course

Links: 

[Flask REST APIs with Flask, Docker](https://www.udemy.com/course/rest-api-flask-and-python/)

[Ebook](https://rest-apis-flask.teclado.com/docs/course_intro/)

[Code](https://github.com/tecladocode/rest-apis-flask-python)

## Content of the course Flask REST APIs by Jose Salvatierra:

* Python refresh
* First Flask API
* Docker
* Flask Smorest
* Flask SQLAlchemy
* Flask-JWT-Extended
* Flask Migration and Alembic
* Git crash course
* Deploy with Render.com
* PostgresSQL, Gunicorn in Docker
* Task Queue with rq and sending emails (Maligun and Redis)

## How to setup and run on Linux

1. Create a folder `mkdir flask-udemy` and go to it `cd flask-udemy`
2. Clone This Project `git clone https://github.com/alanStocco/udemy-teclado-rest-api-flask-and-python`
3. Create a Virtual Environment `python3 -m venv env`
4. Activate Virtual Environment `source env/bin/activate`
5. Install Requirements Package `pip install -r requirements.txt`
6. Run Docker Desktop if needed
7. Build Docker `docker build -t flask-smorest-api .`
8. Run Docker `docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api`
