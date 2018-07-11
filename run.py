from flask import Flask, render_template, request
import sqlite3 as sql


app = Flask(__name__)


@app.route("/")
def hello_method():
    return "<h1>Hello, Welcome to Flask World</h1>"


@app.route("/user/",  methods=['GET', 'POST'])
def hello_user():
    user = request.args.get('name')
    return render_template('index.html', user=user)


@app.route("/productcreate/", methods=['GET', 'POST'])
def product_create():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        if product_name.strip() is None and product_price.strip() is None:
            return render_template('index.html', error="Product name and price are mandatory")
        else:
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
                return render_template("index.html", msg=msg)
    else:
        return render_template('index.html')


@app.route("/productlist/", methods=['GET', 'POST'])
def product_list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from products")

    rows = cur.fetchall()
    return render_template("product_list.html", rows=rows)


@app.route("/productupdate/", methods=['GET', 'POST'])
def product_update():
    pass


@app.route("/productdelete/", methods=['GET', 'POST'])
def product_delete():
    pass


if __name__ == "__main__":
    app.run(debug=True)
