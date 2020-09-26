import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    """Display form template"""
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    """Save form submissions in a csv file"""
    with open("survey.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((request.form.get("name"), request.form.get("email"), request.form.get("street"), request.form.get("city"), request.form.get("zip"), request.form.get("state"), request.form.get(
            "country"), request.form.get("q_empanadas"), request.form.get("q_milanesas"), request.form.get("q_locro"), request.form.get("q_chocotorta"), request.form.get("q_ddl"), request.form.get("q_mate")))
        """If form submission is successful, redirect to /sheet"""
        return redirect("/sheet")
    """Return error message if it fails"""
    return render_template("error.html", message="Please complete all the fields in the form before submitting!")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    """Open and read csv file"""
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        """Display data table"""
        return render_template("table.html", data=data)
    """Return error message if it fails"""
    return render_template("error.html", message="Please complete all the fields in the form before submitting!")
