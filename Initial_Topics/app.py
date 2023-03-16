from flask import Flask,jsonify,request,redirect,url_for,session,render_template,g
from datetime import timedelta
import sqlite3

app  = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "ThisisSecret!"
app.permanent_session_lifetime = timedelta(minutes=1)

def connect_db():
    db = sqlite3.connect('database/database.db')
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


#base route
@app.route('/')
def index():
    session.pop('name',None)
    return "<h1> Hello!!</h1>"

# @app.route("/home")
# def home():
#     return "<h1>You are in home page </h1>"

@app.route("/json")
def json():
    if 'name' in session:
        name = session["name"]
    else:
        name = "Not in Session"
    return jsonify({"key1":2,"key2":[2,3,4,5],"name":name})

# #route with name
# @app.route('/<name>')
# def index(name):
#     return "<h1> Hello {}!</h1>".format(name)

##ROUTE VARIABLES
@app.route("/home",methods=["POST","GET"],defaults={"name":"hello"})#default parameter when no variable name is passed
@app.route("/home/<name>",methods=["POST","GET"])
#@app.route("/home/<int:name>",methods=["POST","GET"])#parameter of particulat type
#@app.route("/home/<string:name>",methods=["POST","GET"])#parameter of particulat type
def home(name):
    session.permanent=True
    session["name"]=name
    db = get_db()
    cur = db.execute("select * from users")
    results = cur.fetchall()
    return render_template('home.html',name=name,display=False,myList=[1,2,3,4,5],results=results,myDict={"name":"hello","name1":"world"})

##Query String
@app.route("/query")
def query():
    name = request.args.get("name")
    loc = request.args.get("loc")
    return "<h1> Hi {} you are in {}, and you are in query page </h1>".format(name,loc)


##Form Data
@app.route("/form")
def form():
    return '''
            <form method="POST" action='/process'>
            <input type="text" name="name">
            <input type="text" name="place">
            <input type="submit" value = "submit">
            </form>
    '''

@app.route("/process",methods=["POST"])
def process():
    name = request.form["name"]
    place = request.form["place"]
    db = get_db()
    db.execute("insert into users (name,location) values(?,?)",[name,place])
    db.commit()
    return '<h1> Hi {} you are in {} </h1>'.format(name,place)


##IncomingRequests
@app.route("/form1",methods=["GET","POST"])
def form1():

    if request.method == "GET":
        return render_template('form.html')
    else:
        name = request.form["name"]
        place = request.form["place"]
        return '<h1> Hi {} you are in {} </h1>'.format(name,place)

##Redirect,url_for
@app.route("/form2",methods=["GET","POST"])
def form2():

    if request.method == "GET":
        return '''
            <form method="POST" action='/form2'>
            <input type="text" name="name">
            <input type="text" name="place">
            <input type="submit" value = "submit">
            </form>
        '''
    else:
        name = request.form["name"]
        place = request.form["place"]
        return redirect(url_for("home",name=name,place=place))


##PROCESS JSON
@app.route("/processjson")
def processjson():
    data = request.get_json()
    name = data["name"]
    loc = data["loc"]
    randomKeyList = data["randomKeyList"]
    return jsonify({'result':'Sucess','name':name,'loc':loc,'randomKeyList':randomKeyList})




#by function main function, we can run the app by running python file
if __name__ == "__main__":
    app.run()