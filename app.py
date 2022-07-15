from flask import ( 
    Flask, render_template,url_for, request,
    redirect, flash, session,abort
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mnbearpig_NUMDAN888/Hg"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'

db = SQLAlchemy(app)

class Activity(db.Model):
    id        = db.Column(db.Integer(), primary_key = True)
    name      = db.Column(db.String(120), nullable = False, unique = True)
    persons   = db.relationship('Person', backref='activity', lazy=True, cascade="all, delete")
    def __rep__(self):
        return f'Activity {self.name}'


class Person(db.Model):
    id           = db.Column(db.Integer(), primary_key = True)
    name         = db.Column(db.String(60), nullable = False, unique = True)
    mobile       = db.Column(db.String(10), default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    show_me      = db.Column(db.Boolean(), default = False)
    activity_id  = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
   
    def __rep__(self):
        return f'Person {self.name}'
    
class Info(db.Model):
    id           = db.Column(db.Integer(), primary_key = True)
    email_adress = db.Column(db.String(50), nullable = False, unique = True)
    adress       = db.Column(db.String(60), default = 0)
    description  = db.Column(db.String(1024), default = 0)
    photo        = db.Column(db.String(200), default = 0)
        
    def __rep__(self):
        return f'Info {self.description}'    
    
db.create_all()


@app.route('/',methods=['POST','GET']) 
def index():
    
    #flash("You are in Index page ")
   
    if request.method == 'POST':
        if request.form.get('mycheckbox')=='on':
            show = True
        else:
            show = False
            
        # Check if name is blank
        if not len(request.form['name'])>0:
            flash('Name is required')
            return redirect('/')
        # Check if name is blank
        if not len(request.form['mobile'])>0:
            flash('Mobile is required')
            return redirect('/')
                  
        new_person = Person(
                            name        = request.form['name'],
                            activity_id = request.form.get('activity_id'),
                            mobile      = request.form['mobile'],
                            show_me     = show
                            )
        try:
            db.session.add(new_person)
            db.session.commit()
            return redirect('/')
        except:
            flash('There was an issue adding your person.')
            return redirect('/')
        
    else:
        #persons     = Person.query.order_by(Person.date_created).all()
        persons     = Person.query.filter(Person.show_me == True).all()
        activities  = Activity.query.order_by(Activity.name).all()
        
        return render_template("index.html",
                                title   = "list of persons",
                                persons = persons,
                                activities = activities,
                                )


@app.route('/admin_page') 
def admin():
    flash("You are in Admin page ")
        
    persons = Person.query.order_by(Person.date_created).all()
    activities  = Activity.query.order_by(Activity.name).all()
    return render_template("admin_page.html",
                            title   = "admin page",
                            persons = persons,
                            activities = activities,
                            )



@app.route('/activity_page',methods=['POST','GET']) 
def Activity_def():
    flash("You are in Activities list")
    
    if request.method == 'POST':
        new_activity = Activity(name = request.form['activity_name'])
        try:
            db.session.add(new_activity)
            db.session.commit()
            return redirect('/activity_page')
        
        except:
            return 'There was an issue adding your Activity.'
            
    else:    
        activities = Activity.query.order_by(Activity.name).all()
        return render_template("activity_page.html",
                                title      = "List of Activities",
                                activities = activities
                                )

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    
    person = Person.query.get_or_404(id)
    flash(f'Hello you are updating {person.name}')
    
    if request.form.get('mycheckbox')=='on':
        show = True
    else:
        show = False
    
    if request.method == 'POST':
        person.name        = request.form['name']
        person.activity_id = request.form.get('activity_id')
        person.mobile      = request.form['mobile']
        person.show_me     = show
        try:
            db.session.commit()
            return redirect('/admin_page')
          
        except:
            return 'There was an issue updating your person'
            
    else:
        activities  = Activity.query.order_by(Activity.name).all()
        return render_template('person/person_update.html',
                               person = person,
                               activities = activities)
     
@app.route('/delete/<int:id>')
def delete(id):
    person_to_delete = Person.query.get_or_404(id)
    
    try:
        db.session.delete(person_to_delete)
        db.session.commit()
        return redirect('/admin_page')
        
    except:
        return 'There was an problem deleting that person !'
   




if __name__ == "__main__":
    app.run(debug=True)
    
    
