from flask import Flask, render_template, request, send_from_directory
import sqlite3 as sql


app = Flask(__name__)


@app.route("/hello_world")
def hello_world():
    return "<h1>Hello, Welcome to Flask World</h1>"


@app.route("/")
def index():
    return send_from_directory('static', 'index.html')


@app.route("/home",  methods=['GET'])
def home():
    user = request.args.get('name', None)
    return render_template('home.html', user=user)


@app.route("/productcreate", methods=['POST'])
def product_create():
    product_name = request.form.get('product_name', None)
    product_price = request.form.get('product_price', None)

    # check input validity
    if product_name is None and product_price is None:
        return render_template('home.html', error="Product name and price are mandatory")

    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("create table if not exists products (name TEXT, price INT)")
            cur.execute("INSERT INTO products (name,price)"
                        "VALUES (?,?)", (product_name, product_price))
            con.commit()
            msg = "Record saved successfully"
    except:
        con.rollback()
        msg = "Error in inserting record"
    finally:
        con.close()
        return render_template("home.html", msg=msg)


@app.route("/productlist", methods=['GET'])
def product_list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from products")

    rows = cur.fetchall()
    return render_template("product_list.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
