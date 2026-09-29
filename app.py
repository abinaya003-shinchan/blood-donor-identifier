from flask import Flask, render_template, request, redirect
from database.database import init_db, get_db_connection

app = Flask(__name__)

# Create database and table
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        blood_group = request.form["blood_group"]
        phone = request.form["phone"]
        city = request.form["city"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO donors
            (name, age, blood_group, phone, city)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, blood_group, phone, city))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    donors = []

    if request.method == "POST":
        blood_group = request.form["blood_group"]
        city = request.form["city"]

        conn = get_db_connection()

        donors = conn.execute("""
            SELECT * FROM donors
            WHERE blood_group = ?
            AND city = ?
            AND availability = 'Available'
        """, (blood_group, city)).fetchall()

        conn.close()

    return render_template("search.html", donors=donors)


if __name__ == "__main__":
    app.run(debug=True)