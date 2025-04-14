from flask import Flask, render_template, request, redirect  # No change needed here
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/studybuddy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100), nullable=False)
    preference = db.Column(db.String(100), nullable=True)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"
    
    #adding changes before this code work fine {

class StudyGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # who created the group

    def __repr__(self):
        return f"<StudyGroup {self.group_name}>"
    

@app.route("/create-group", methods=["POST"])
def create_group():
    group_name = request.form['group_name']
    subject = request.form['subject']
    description = request.form['description']
    created_by = request.form['created_by']

    group = StudyGroup(group_name=group_name, subject=subject, description=description, created_by=created_by)
    db.session.add(group)
    db.session.commit()

    return "Group Created!"





    #till here if crash delete between comments }

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['subject']
        availability = request.form['availability']
        preference = request.form.get('preference')

        new_user = User(name=name, subject=subject, availability=availability, preference=preference)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/")  # Prevent form resubmission on refresh

    return render_template('index.html')

# 🔽🔽🔽 NEW ROUTE ADDED HERE FOR LOGIN
@app.route("/login")
def login():
    return render_template("login.html")  # This will look for login.html in the templates folder

# END OF ADDED PART

if __name__ == "__main__":
    app.run(debug=True)
