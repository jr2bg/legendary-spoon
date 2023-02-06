from flask import Flask, render_template, request, jsonify

import simple_queries

import simple_queries

app = Flask(__name__)

@app.route("/")
def index():
    simple_queries.get_eg_data(simple_queries.create_session())
    return "hello world"

@app.route("/queries", methods=["GET", "POST"])
def queries():
    if request.method == "GET":
        return render_template("queries.html")

    if request.method == "POST":
        simple_queries.get_data(
            request.form.getlist('country'),
            request.form.getlist('role'),
            request.form.get('experience')
        )
        return request.form

@app.route("/simple-chart")
def simple_chart():
    data = [
        ("01-01-2020", 1597),
        ("02-01-2020", 934),
        ("03-01-2020", 456),
        ("04-01-2020", 2873),
        ("05-01-2020", 1597),
        ("06-01-2020", 934),
        ("07-01-2020", 456),
        ("08-01-2020", 2873),
        ("09-01-2020", 1597),
        ("10-01-2020", 934),
        ("11-01-2020", 456),
        ("12-01-2020", 2873),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("chart.html", labels=labels, values=values)

if __name__=='__main__':
    app.run(debug=True)