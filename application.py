import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
#API_KEY = pk_1153dc3e4f6b4f03b93012a9fbffa611
# if not os.environ.get("API_KEY"):
#raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    available = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = available[0]["cash"]
    stocks = usd(10000-cash)
    data = list(db.execute("SELECT * FROM stocks WHERE (id = :id)", id=session["user_id"]))
    return render_template("index.html", data=data, cash=usd(cash), stocks=stocks), 200


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must type in quote symbol", 400)

        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return apology("Sorry, seems that the stock symbol typed in does not exist.", 400)

        if request.form.get("shares") == 0:
            return apology("please select quantity of shares to be bought", 400)

        available = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        quantity = int(request.form.get("shares"))
        total = price * quantity
        cash = available[0]["cash"]
        info = db.execute("SELECT * FROM stocks WHERE (id = :id and symbol = :symbol)", id=session["user_id"], symbol=symbol)

        # Check the user has enough cash to proceed
        if not available or cash < total:
            return apology("total amount exceeds available money. Please select less shares", 400)

        cash = cash - total
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=available[0]["cash"] - total, id=session["user_id"])

        # Update history table
        db.execute("INSERT INTO history VALUES(:datetime, :id, :symbol, :price, :shares, :money, 'bought')",
                  datetime=datetime.datetime.now(), id=session["user_id"], symbol=symbol, price=usd(price), shares=quantity, money=usd(total))

        # Update user stock info if the user already posses that stock
        if len(info) != 0:
            n = info[0]["shares"] + quantity
            if n != 0:
                db.execute("UPDATE stocks SET shares = :shares, money = :money WHERE (id = :id and symbol = :symbol)", shares=n,
                           money=usd(info[0]["money"] + total), id=session["user_id"], symbol=symbol)
            else:
                db.execute("DELETE FROM stocks WHERE (id = :id and symbol = :symbol)", id=session["user_id"], symbol=symbol)

        # Insert a row with the user's new stock purchase's details
        else:
            n = quantity
            db.execute("INSERT INTO stocks VALUES(:id, :symbol, :price, :shares, :money, :name)", id=session["user_id"], symbol=symbol,
                       price=usd(price), shares=n, money=usd(total), name=name)

        # Inform user the purchase was succesful
        return render_template("bought.html", symbol=symbol, name=name, price=usd(price), total=usd(total),
                               cash=cash, quantity=quantity), 200

    else:
        return render_template("buy.html"), 200


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return True, 200


@app.route("/history")
@login_required
def history():
    data = list(db.execute("SELECT * FROM history WHERE (id = :id)", id=session["user_id"]))
    return render_template("history.html", data=data), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html"), 200


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must type in quote symbol", 400)

        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return apology("Sorry, seems that the stock symbol typed in does not exist.", 400)

        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]

        return render_template("quoted.html", symbol=symbol, name=name, price=usd(price)), 200

    else:
        return render_template("quote.html"), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # Ensure username doesn't exists
        if len(rows) != 0:
            return apology("that username is alreaady taken! Please choose a different one", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return apology("please confirm password", 400)

        # Ensure password and confirmation password match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        db.execute("INSERT INTO users(username,hash) VALUES(:username, :hash)", username=request.form.get("username"),
                   hash=generate_password_hash(request.form.get("password")))
        # Remember which user has logged in
        if len(db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))) > 0:
            row = db.execute("SELECT * FROM users WHERE username = :username",
                             username=request.form.get("username"))
            session["user_id"] = row[0]["id"]
            return redirect("/"), 200
    else:
        return render_template("register.html"), 200


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must type in quote symbol", 400)

        symbol = request.form.get("symbol")
        if lookup(symbol) == None:
            return apology("Sorry, seems that the stock symbol typed in does not exist."), 400

        if not request.form.get("shares") or request.form.get("shares") == 0:
            return apology("please select quantity of shares to be bought"), 400

        info = db.execute("SELECT * FROM stocks WHERE (id = :id and symbol = :symbol)", id=session["user_id"], symbol=symbol)
        if len(info) == 0:
            shares = 0
        else:
            shares = info[0]["shares"]

        quantity = int(request.form.get("shares"))
        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        total = price * quantity
        money = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        cash = money[0]["cash"]
        n = shares - quantity

        cash = cash + total

        # Update history table
        db.execute("INSERT INTO history VALUES(:datetime, :id, :symbol, :price, :shares, :money, 'sold')",
                   datetime=datetime.datetime.now(), id=session["user_id"], symbol=symbol, price=usd(price), shares=quantity, money=usd(total))

        # User sold all of his/her stock's tenure
        if shares != 0 and n == 0:
            db.execute("DELETE FROM stocks WHERE (id = :id and symbol = :symbol)", id=session["user_id"], symbol=symbol)

        # Update user stock info if the user sold some shares of his/her tenure or goes short
        elif shares != 0 and n != 0:
            db.execute("UPDATE stocks SET shares = :shares, money = :money WHERE (id = :id and symbol = :symbol)", shares=n,
                       money=info[0]["money"] - total, id=session["user_id"], symbol=symbol)

        else:
            db.execute("INSERT INTO stocks VALUES(:id, :symbol, :price, :shares, :money, :name)", id=session["user_id"], symbol=symbol,
                       price=usd(price), shares=n, money=usd(total), name=name)

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=money[0]["cash"] + total, id= session["user_id"])

        # Inform user the transaction was succesful
        return render_template("sold.html", symbol=symbol, name=name, price=usd(price), total=usd(total),
                               cash=usd(cash), quantity=quantity, n=n), 200

    else:
        return render_template("sell.html"), 200


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
