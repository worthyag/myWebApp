from flask import *
import pymysql
import traceback

app = Flask("MoviesCatalog")
app.secret_key = "ddj3934u8en"

app.config["MYSQL_HOST"] = "192.168.0.63"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "School20"
app.config["MYSQL_DB"] = "moviesDB"
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
    return pymysql.connect(**db_config)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies/", methods=['GET'])
def allMovies():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM movie")
        # Fetching all the results.
        all_movies = cursor.fetchall()
        return render_template("movies.html", movies=all_movies)
    except Exception as e:
        error_message = str(e)
        error_trace = traceback.format_exc()
        # print(error_trace)  # Logs error details to the console (useful for debugging)
        return jsonify({"error": f"Error occurred.\nError msg: {error_message}\nError trace: {error_trace}"}), 500
        # return jsonify({"error": "Error occurred."}), 500


@app.route("/movies/add/")
def addMovie():
    return render_template("addMovie.html")


@app.route("/movies/view/", methods=['POST'])
def viewMovie():
    movie_id = request.form.get("movie-id")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM movie WHERE movie_id = %s"
        cursor.execute(sql, (movie_id,))
        selected_movie = cursor.fetchone()

        if selected_movie:
            return render_template("viewMovie.html", movie=selected_movie)
        else:
            return jsonify({"message": f"Movie not found {movie_id}"}), 404
    except:
        return jsonify({"error": "Error occurred."}), 500


@app.route("/movies/search/<id>/", methods=['GET'])
def getMovie(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT * FROM movie WHERE movie_id = %s"
        cursor.execute(sql, (id,))
        selected_movie = cursor.fetchone()

        if selected_movie:
            return render_template("viewMovie.html", movie=selected_movie)
        else:
            return jsonify({"message": "Movie not found"}), 404
    except:
        return jsonify({"error": "Error occurred."}), 500


@app.route("/movies/save/", methods=["POST"])
def addedMovie():
    movie_name = request.form.get("movie-name")
    movie_desc = request.form.get("movie-desc")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO movie (movie_name, movie_desc) VALUES (%s, %s)"
        cursor.execute(sql, (movie_name, movie_desc))
        # Committing the transaction.
        connection.commit()
        return render_template("saved.html", movie_name=movie_name, movie_desc=movie_desc)
    except:
        return jsonify({"error": "Error occurred when adding movie. Movie not added."}), 500


# app.run(debug=True)
app.run(host="0.0.0.0", port=5000, debug=True)
