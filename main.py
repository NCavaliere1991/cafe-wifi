from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)
Bootstrap(app)



def make_bool(ans):
    if ans == 'yes':
        return True
    else:
        return False

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField("Cafe Location on Google Maps(URL)", validators=[DataRequired(), URL(message="Enter a valid URL")])
    img_url = StringField("Image URL", validators=[DataRequired(), URL(message="Enter a valid URL")])
    location = StringField("Cafe Location", validators=[DataRequired()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    has_toilet = SelectField("Wifi Strength Rating",
                              choices=["yes", "no"],
                              validators=[DataRequired()])
    has_wifi = SelectField("Power Socket Availability",
                               choices=["yes", "no"],
                               validators=[DataRequired()])
    has_sockets = SelectField("Power Socket Availability",
                           choices=["yes", "no"],
                           validators=[DataRequired()])
    can_take_calls = SelectField("Power Socket Availability",
                           choices=["yes", "no"],
                           validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    num = len(all_cafes)
    return render_template("index.html", cafes=all_cafes, num=num)

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url= form.map_url.data,
            img_url= form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=make_bool(form.has_toilet.data),
            has_wifi=make_bool(form.has_wifi.data),
            has_sockets=make_bool(form.has_sockets.data),
            can_take_calls=make_bool(form.can_take_calls.data),
            coffee_price=form.coffee_price.data)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)