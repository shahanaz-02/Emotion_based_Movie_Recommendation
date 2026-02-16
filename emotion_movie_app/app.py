from flask import Flask, render_template, request
import mysql.connector
import hashlib

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="emotion_recommendation"
)

@app.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT emotion_name FROM emotion_tag")
    emotions = [row[0] for row in cursor.fetchall()]
    return render_template("index.html", emotions=emotions)


@app.route('/submit', methods=['POST'])
def submit():

    username = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    password = request.form.get('password')
    people_count = request.form.get('people_count')
    mood = request.form.get('mood')

    cursor = db.cursor()

    # ✅ Simple SHA-256 hash (no scrypt)
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Check if email already exists
    cursor.execute("SELECT user_id FROM user WHERE email=%s", (email,))
    row = cursor.fetchone()

    if row:
        user_id = row[0]
        cursor.execute("""
            UPDATE user 
            SET username=%s, age=%s, password_hash=%s 
            WHERE user_id=%s
        """, (username, age, hashed_password, user_id))
    else:
        cursor.execute("""
            INSERT INTO user (username, email, password_hash, age)
            VALUES (%s, %s, %s, %s)
        """, (username, email, hashed_password, age))
        user_id = cursor.lastrowid

    # Insert mood input
    cursor.execute("""
        INSERT INTO mood_input (user_id, emotion_label, people_count)
        VALUES (%s, %s, %s)
    """, (user_id, mood, people_count))
    mood_input_id = cursor.lastrowid

    # Recommend movies (Top 5)
    cursor.execute("""
        SELECT m.movie_id, m.title, m.release_year, m.language, me.intensity_score
        FROM movie m
        JOIN movie_emotion me ON m.movie_id = me.movie_id
        JOIN emotion_tag e ON me.emotion_id = e.emotion_id
        WHERE e.emotion_name = %s
        ORDER BY me.intensity_score DESC
        LIMIT 5
    """, (mood,))
    movies = cursor.fetchall()

    # Store recommendation header
    cursor.execute("""
        INSERT INTO recommendation (user_id, mood_id)
        VALUES (%s, %s)
    """, (user_id, mood_input_id))
    rec_id = cursor.lastrowid

    # Store recommendation items
    rank = 1
    for (movie_id, title, year, lang, score) in movies:
        cursor.execute("""
            INSERT INTO recommendation_item 
            (rec_id, movie_id, rank_position, relevance_score)
            VALUES (%s, %s, %s, %s)
        """, (rec_id, movie_id, rank, score))
        rank += 1

    db.commit()

    # Pass score to template
    movies_for_view = [(title, year, lang, score)
                       for (_, title, year, lang, score) in movies]

    return render_template("result.html", movies=movies_for_view, mood=mood)


if __name__ == '__main__':
    app.run(debug=True)
