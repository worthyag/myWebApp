from flask import *
import pymysql
import traceback

import pymysql.cursors

app = Flask("MoviesCatalog")
app.secret_key = "ddj3934u8en"

app.config["MYSQL_HOST"] = "192.168.2.136"
# app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "flaskJenkinsUser"
app.config["MYSQL_PASSWORD"] = "password12-"
app.config["MYSQL_DB"] = "flaskJenkins"
app.config["MYSQL_PORT"] = 3306

# Database Configuration
db_config = {
    "host": app.config["MYSQL_HOST"],
    "user": app.config["MYSQL_USER"],
    "password": app.config["MYSQL_PASSWORD"],
    "database": app.config["MYSQL_DB"],
    "port": app.config["MYSQL_PORT"]
}

# Function to get DB connection


def get_db_connection():
    # Returning the rows as dictionaries to make them easier to work with.
    return pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)


def create_table(cursor):
    # Checking if the database exists.
    # cursor.execute("SHOW DATABASES LIKE 'flaskJenkins'")
    # db_exists = cursor.fetchone()

    # if not db_exists:
    #     # Creating the database.
    #     cursor.execute("CREATE DATABASE flaskJenkins")

    # Selecting the database.
    cursor.execute("USE flaskJenkins")

    # Checking if the user exists.
    # cursor.execute("SELECT USER FROM MYSQL.USER WHERE USER = 'flaskJenkinsUser'")
    # user_exists = cursor.fetchone()

    # if not user_exists:
    #     # Granting permission.
    #     cursor.execute(
    #         "CREATE USER 'flaskJenkinsUser'@'%' IDENTIFIED WITH mysql_native_password BY 'password12-'")
    #     cursor.execute(
    #         "GRANT ALL PRIVILEGES ON *.* TO 'flaskJenkinsUser'@'%' WITH GRANT OPTION")
    #     cursor.execute("FLUSH PRIVILEGES")

    # Creating the table.
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie (
                    movie_id INT AUTO_INCREMENT PRIMARY KEY,
                    movie_name VARCHAR(500) NOT NULL,
                    movie_desc VARCHAR(2000)
                   )""")
    return cursor


def start_db_connection():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            create_table(cursor)
            # Making sure that the changes persist.
            connection.commit()
    # Returning a new connection for further use.
    return get_db_connection()


def get_error(e, msg=None):
    error_message = str(e)
    error_trace = traceback.format_exc()

    msg = "Error occurred." if msg is None else msg
    return jsonify({"error": f"{msg}\nError msg: {error_message}\nError trace: {error_trace}"}), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies/", methods=['GET'])
def allMovies():
    try:
        # connection = get_db_connection()
        # cursor = connection.cursor()
        # Using with to make sure that all my connections are properly closed to avoid memory leaks.
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Selecting all the movies.
                cursor.execute("SELECT * FROM movie")

                # Fetching all the results.
                all_movies = cursor.fetchall()

                if all_movies:
                    return render_template("movies.html", movies=all_movies)
                return render_template("no-movies.html")

    except Exception as e:
        return get_error(e)


@app.route("/movies/add/")
def addMovie():
    return render_template("addMovie.html")


@app.route("/movies/view/", methods=['POST'])
def viewMovie():
    movie_id = request.form.get("movie-id")

    try:
        # connection = get_db_connection()
        # cursor = connection.cursor()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Selecting a specific movie.
                sql = "SELECT * FROM movie WHERE movie_id = %s"
                cursor.execute(sql, (movie_id,))
                selected_movie = cursor.fetchone()

                if selected_movie:
                    return render_template("viewMovie.html", movie=selected_movie)
                else:
                    return jsonify({"message": f"Movie not found {movie_id}"}), 404
    except Exception as e:
        return get_error(e)


@app.route("/movies/search/<id>/", methods=['GET'])
def getMovie(id):
    try:
        # connection = get_db_connection()
        # cursor = connection.cursor()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM movie WHERE movie_id = %s"
                cursor.execute(sql, (id,))
                selected_movie = cursor.fetchone()

                if selected_movie:
                    return render_template("viewMovie.html", movie=selected_movie)
                else:
                    return jsonify({"message": "Movie not found"}), 404
    except Exception as e:
        return get_error(e)


@app.route("/movies/save/", methods=["POST"])
def addedMovie():
    movie_name = request.form.get("movie-name")
    movie_desc = request.form.get("movie-desc")

    try:
        # connection = get_db_connection()
        # cursor = connection.cursor()
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO movie (movie_name, movie_desc) VALUES (%s, %s)"
                cursor.execute(sql, (movie_name, movie_desc))
                # Committing the transaction.
                connection.commit()
                return render_template("saved.html", movie_name=movie_name, movie_desc=movie_desc)
    except Exception as e:
        return get_error(e, "Error occurred when adding movie. Movie not added.")


# Creating the db and the initial connection.
start_db_connection()
app.run(host="0.0.0.0", port=5001, debug=True)
