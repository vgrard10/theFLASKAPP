##
## flask imports
##
from flask import Flask, current_app
from flask import (make_response,
                   redirect,
                   abort,
                   session,
                   render_template, 
                   url_for, 
                   flash, 
                   request)
##
## Flask extensions imports
##
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm
from wtforms import (StringField, 
    SubmitField, IntegerField, FloatField, SelectField)
from wtforms.validators import (DataRequired, 
    InputRequired, Length, NumberRange)
##
## configuration file imports
##
import config


##
## creation of the Flask application instance
## 
## passing its configuration, and initializing the extensions along with the flask app.
## The web server passes all requests it receives from clients to this object for handling, using a protocol called Web Server Gateway Interface (WSGI)
app = Flask(__name__, template_folder="templates")
app.config.from_object('config')

manager = Manager(app) # To give provide CLI commands
bootstrap = Bootstrap(app) # Twitter Bootstrap extension
db = SQLAlchemy(app) # SQLAlchemy extension, manipulating the database object db
migrate = Migrate(app, db) # database migrations
manager.add_command('db', MigrateCommand) # to add it as command line using Flask Script


##
## Forms
##

class EnterYourInfosForm(FlaskForm):
    """
    This field is the base for most of the more complicated fields, and represents an <input type="text">.
    """
    name = StringField("Name", validators=[DataRequired()])

    """
    Represents an <input type="number">
    """
    age = IntegerField("Age", 
        validators=[DataRequired(), NumberRange(min=0, max=123)])
    """
    A text field, except all input is coerced to an float. Erroneous input is ignored and will not be accepted as a value
    """
    ticket_price = FloatField("Ticket Price",
        validators=[DataRequired(), NumberRange(min=0)])
    """
    Select fields take a choices parameter which is a list of (value, label) pairs. It can also be a list of only values, in which case the value is used as the label. The value can be any type, but because form data is sent to the browser as strings, you will need to provide a coerce function that converts a string back to the expected type.
    """
    sexe = SelectField("Sexe",
        choices=[(0, "Homme"),(1,"Femme")],
        validators=[InputRequired()],
        coerce=int)
    """
    Represents an <input type="submit">. This allows checking if a given submit button has been pressed.
    """
    submit = SubmitField("Submit")
    
    #def clear(self):
        #self.name.data = ''
        #self.age.raw_data = ['']
        #self.


##
## models
##

class User(db.Model):
    """
    This class describes an user.
    SQLAlchemy extension for flask provides an ORM (Object-relational mappers).
    An ORM is a tool that provides convertion from high-level (object-oriented) objects into low-level database instructions, so you don't have to directly deal with tables, documents, or query languages. 
    + for SQLAlchemy the abstraction is even higher as you can choose different database engines that relies on the same Python object (hence, without having to rewrite or adapt code)!
    """
    __tablename__ = "users" # renaming the table and not default given name "user" not respecting the conventions

    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    sexe = db.Column(db.Boolean, nullable=False)
    survived = db.Column(db.Boolean, nullable=True)
    #date_submitted = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "User {}, with name: {}".format(self.id_, self.name)

##
## errors handlers
## def: is a function that returns a response when a type of error is raised.
## here only one is implemented for the 404 Not Found
## The good old “chap, you made a mistake typing that URL” message. 
##

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', nompath=e), 404

##
## views
##

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = EnterYourInfosForm()
    if request.method=="POST" and form.validate_on_submit():
        # check if a user with the same name already exist in the db
        user = User.query.filter_by(name=form.name.data).first()
        if user is not None:
            flash('It seems you already played, this was your prediction: {}'.format(
                user.survived))
        else:
            import joblib
            loaded_model = joblib.load("model_saved")
            # predict for the user if he/she would have had survived
            prediction = bool(loaded_model.predict(
                [[form.age.data, form.ticket_price.data, form.sexe.data]]
            ))

            # create a new "user" of the service
            user = User(name=form.name.data, 
                    age=form.age.data, 
                    ticket_price=form.ticket_price.data,
                    sexe=form.sexe.data,
                    survived=prediction)
            # add the user to the db
            db.session.add(user)
            db.session.commit()
        session["survived"] = user.survived
        return redirect(url_for('show_result'))
    return render_template('predict.html', form=form)


@app.route('/results')
def show_result():
    return render_template('results.html', success=session.get('survived', 'first'))

@app.route('/users')
def show_all_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/<path:nompath>')
def error_test(nompath):
	# raises an HTTPException of status code 404
	# nompath is the payload
	# retrieved from e in the page_not_found(e) error_handler
	abort(404, nompath)


@manager.command
def test():
    """ Run the integration tests """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    # app.run(debug=True), 
    # changed to manager
    # using the extension 
    # so you can pass options 
    # directly from the command-line
    with app.app_context():
        # create all the tables
        db.create_all()
    manager.run()
