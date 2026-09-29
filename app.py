from flask import Flask, render_template, request, redirect
from database.database import init_db, get_db_connection

app = Flask(__name__)

init_db()


COMPATIBLE_DONORS = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["A-", "B-", "AB-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"]
}


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
        """, (
            name,
            age,
            blood_group,
            phone,
            city
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/search", methods=["GET", "POST"])
def search():

    donors = []

    if request.method == "POST":

        required_blood = request.form["blood_group"]
        city = request.form["city"]

        compatible_groups = COMPATIBLE_DONORS[required_blood]

        placeholders = ",".join(
            ["?"] * len(compatible_groups)
        )

        query = f"""
            SELECT *,
            CASE
                WHEN blood_group = ? THEN 1
                ELSE 2
            END AS match_priority
            FROM donors
            WHERE blood_group IN ({placeholders})
            AND city = ?
            AND availability = 'Available'
            ORDER BY match_priority ASC
        """

        conn = get_db_connection()

        donors = conn.execute(
            query,
            (
                required_blood,
                *compatible_groups,
                city
            )
        ).fetchall()

        conn.close()

    return render_template(
        "search.html",
        donors=donors
    )


# Admin / donor management
@app.route("/admin")
def admin():

    conn = get_db_connection()

    donors = conn.execute("""
        SELECT * FROM donors
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        donors=donors
    )


# Change donor availability
@app.route("/toggle/<int:donor_id>", methods=["POST"])
def toggle_availability(donor_id):

    conn = get_db_connection()

    donor = conn.execute("""
        SELECT availability
        FROM donors
        WHERE id = ?
    """, (donor_id,)).fetchone()

    if donor:

        if donor["availability"] == "Available":
            new_status = "Not Available"
        else:
            new_status = "Available"

        conn.execute("""
            UPDATE donors
            SET availability = ?
            WHERE id = ?
        """, (
            new_status,
            donor_id
        ))

        conn.commit()

    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)