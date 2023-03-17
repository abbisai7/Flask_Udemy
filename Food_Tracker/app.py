from flask import Flask,render_template,g,request
import sqlite3

app = Flask(__name__)

def connect_db():
    db = sqlite3.connect('database/food_log.db')
    db.row_factory = sqlite3.Row
    return db

def get_db():
    if not hasattr(g,'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#use to disconnet db after every route fucntions return
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/view")
def view():
    return render_template("day.html")

@app.route("/food",methods=["GET","POST"])
def food():
    if request.method == "POST":
        name = request.form["food_name"]
        protein = int(request.form["food_protein"])
        carbohydrates= int(request.form["food_carbohydrates"])
        fat = int(request.form["food_fat"])
        calories = (protein*4) + (carbohydrates * 4) + (fat*9) 
        db = get_db()
        db.execute("insert into food (name,protein,carbohydrates,fat,calories) values(?,?,?,?,?)",\
                   [name,protein,carbohydrates,fat,calories])
        db.commit()
    db = get_db()
    cur = db.execute("select name,protein,carbohydrates,fat,calories from food")   
    results = cur.fetchall() 
    return render_template("add_food.html",results=results)


if __name__ == "__main__":
    app.run(debug=True)