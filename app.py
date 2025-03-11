from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:9019@localhost/mydatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Model
class Todo(db.Model): 
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"

# Create tables inside the app context
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    all_todos = Todo.query.all()
    return render_template('index.html', todos=all_todos)  

@app.route("/add", methods=["POST"])
def add_todo():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('hello_world'))  # Redirect to home page

# ✅ Route to delete a Todo item
@app.route("/delete/<int:sno>")
def delete_todo(sno):
    todo = Todo.query.get_or_404(sno)  # Get the todo item or return 404
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))  # Redirect after deletion

if __name__ == "__main__":
    app.run(debug=True)
