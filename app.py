from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DBUSER = "flask"
# useless pass dont worry
DBPASS = "SoP4ZNXk6XSkRgbz"
DBHOST = "127.0.0.1"
DBNAME = "flask"

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % (DBUSER, DBPASS, DBHOST, DBNAME)

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST' and request.form['content']:
        
        cont = request.form['content']
        
        new_task = Todo(content=cont)

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return "error 808"

    tasks = Todo.query.order_by(Todo.created.desc()).all()
    return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):

    to_del = Todo.query.get_or_404(id)

    try:
        db.session.delete(to_del)
        db.session.commit()
        return redirect('/')
    except:
        return "error 809"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST' and request.form['content']:

        task.content = request.form['content']
    
        try:
            db.session.commit()                      
        except:
            return "error 810"
        
        return redirect('/')        
    return render_template("update.html", task=task)

@app.route('/create')
def create():
    db.create_all()
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)