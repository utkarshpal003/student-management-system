from flask import Flask, render_template, request, redirect
from database import get_connection

from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    return redirect("/students")


# Add Student
@app.route("/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        age = request.form["age"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO students (name, email, phone, course, age)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (name, email, phone, course, age)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/students")

    return render_template("add_student.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
    total_courses = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_courses=total_courses
    )


# View and Search Students
@app.route("/students")
def students():

    search = request.args.get("search", "")

    connection = get_connection()
    cursor = connection.cursor()

    if search:
        query = """
        SELECT * FROM students
        WHERE name LIKE %s
        OR email LIKE %s
        OR course LIKE %s
        """

        search_value = "%" + search + "%"

        cursor.execute(
            query,
            (search_value, search_value, search_value)
        )

    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )


# Edit / Update Student
@app.route("/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        age = request.form["age"]

        query = """
        UPDATE students
        SET name=%s,
            email=%s,
            phone=%s,
            course=%s,
            age=%s
        WHERE id=%s
        """

        values = (name, email, phone, course, age, id)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/students")

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# Delete Student
@app.route("/delete-student/<int:id>")
def delete_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/students")


if __name__ == "__main__":
    app.run(debug=True)