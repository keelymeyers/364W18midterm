###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
import json
import requests 
from yelp_access import access_key
from flask_script import Manager, Shell
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy


## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values

app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/yelp_db" 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)

manager = Manager(app)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################

def get_or_create_business(db_session, business_ID, business_name, business_rating, business_price):
    business = db_session.query(Businesses).filter_by(name=business_name).first()
    if business:
        return business
    else:
        business = Businesses(business_ID=business_ID, name=business_name, rating=business_rating, price=business_price)
        db_session.add(business)
        db_session.commit()
        return business 

def get_or_create_yelp_reviews(db_session, business_ID, review_identifier, review_text, user, rating):
    review = db_session.query(Yelp_Reviews).filter_by(review_identifier=review_identifier).first()
    if review:
        return review
    else:
        review = Yelp_Reviews(business=business_ID, review_identifier=review_identifier, text=review_text, user=user, rating=rating)
        db_session.add(review)
        db_session.commit()
        return review

def get_or_create_user_reviews(db_session, business_name, review_rating, review_text):
    user_review = db_session.query(User_Reviews).filter_by(review_text=review_text).first()
    if user_review:
        return user_review
    else:
        user_review = User_Reviews(business_name=business_name, review_rating=review_rating, review_text=review_text)
        db_session.add(user_review)
        db_session.commit()
        return user_review


##################
##### MODELS #####
##################


class Businesses(db.Model):
    __tablename__ = "businesses"
    id = db.Column(db.Integer, primary_key=True)
    business_ID = db.Column(db.String(), unique=True)
    name = db.Column(db.String())
    rating = db.Column(db.String())
    price = db.Column(db.String())
    review_relationship = db.relationship('Yelp_Reviews', backref='businesses')

class Yelp_Reviews(db.Model):
    __tablename__ = "yelp reviews"
    id = db.Column(db.Integer, primary_key=True)
    business = db.Column(db.String(), db.ForeignKey('businesses.business_ID'))
    review_identifier = db.Column(db.String(), unique=True)
    text = db.Column(db.String())
    user = db.Column(db.String())
    rating = db.Column(db.String())

class User_Reviews(db.Model):
    __tablename__ = "user reviews"
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String())
    review_text = db.Column(db.String())
    review_rating = db.Column(db.Float())


###################
###### FORMS ######
###################


class BusinessForm(FlaskForm):
    name = StringField("Please enter the name of a business ", validators=[Required()])
    location = StringField("Please enter the business zip code ", validators=[Required()])
    submit = SubmitField('Submit')

    def validate_location(self, field):
        if len(field.data) != 5:
            raise ValidationError('Please enter a valid zip code!')

class ReviewForm(FlaskForm):
    name = StringField("Enter the name of a business you wish to review ", validators=[Required()])
    rating = FloatField("Please enter your rating, on a scale of 0.0 to 5.0 stars ", validators=[Required()])
    review = StringField("Please leave a helpful review of this business ", validators=[Required()])
    submit = SubmitField('Submit')

    def validate_rating(self,field):
        if '.' not in field.data:
            raise ValidationError('Please enter a valid rating!')

        elif len(field.data) > 3:
            raise ValidationError('Please enter a valid rating!')


#######################
###### VIEW FXNS ######
#######################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET','POST'])
def home():
    form = BusinessForm()
    if form.validate_on_submit():
        name_of_business = form.name.data
        location = form.location.data

        ## Making a request to Yelp Search API based on user-input data to get business data and add to database.

        headers = {'Authorization': 'Bearer {}'.format(access_key)}
        params = {'term': name_of_business, 'headers': headers,'location': location}
        business_url = "https://api.yelp.com/v3/businesses/search"
        r = requests.get(business_url, headers=headers,params=params)
        resp = json.loads(r.text)

        business_id = resp['businesses'][0]['id']
        business_name = resp['businesses'][0]['name']
        business_rating = resp['businesses'][0]['rating']
        business_price = resp['businesses'][0]['price']

        newbusiness = get_or_create_business(db.session,business_id, business_name, business_rating, business_price)

        ## Making a request to Yelp Reviews API based on business id returned from previous API, and storing review data in database.

        reviews_url = "https://api.yelp.com/v3/businesses/{}/reviews".format(business_id)
        re = requests.get(reviews_url, headers=headers)
        response = json.loads(re.text)
        reviews = response['reviews']
        reviews_to_be_displayed = []
        for review in reviews:
            review_id = review['id']
            review_text = review['text']
            reviews_to_be_displayed.append(review_text)
            review_user = review['user']['name']
            review_rating = review['rating']
            newreview = get_or_create_yelp_reviews(db.session, newbusiness.business_ID, review_id, review_text, review_user, review_rating)

        return render_template('form.html',form=form, newbusiness=newbusiness, business=business_name, price=business_price,rating=business_rating, reviews=reviews_to_be_displayed)
    flash(form.errors)
    return render_template('form.html',form=form)


@app.route('/reviews')
def all_yelp_reviews():
    all_businesses = [] 
    b = Businesses.query.all()
    for bus in b:
        business_reviews = Yelp_Reviews.query.filter_by(business=bus.business_ID).all()
        revs = []
        for rev in business_reviews:
            revs.append(rev.text)
        all_businesses.append((bus.name, bus.rating, bus.price, revs))
    return render_template('see_all_search_results.html',names=all_businesses)


@app.route('/user_form')
def user_form():
    form = ReviewForm()
    return render_template("user_review_form.html", form=form)


@app.route('/user_review', methods=['GET','POST'])
def show_review():
    form = ReviewForm()
    if request.args:
        results = request.args
        name_of_business_reviewing = results.get('name')
        user_rating = results.get('rating')
        user_review = results.get('review')

        get_or_create_user_reviews(db.session, name_of_business_reviewing, user_rating, user_review)
        return render_template('see_review.html',form=form, business_reviewed=name_of_business_reviewing, rating=user_rating, review=user_review)
    return redirect(url_for('user_form'))


@app.route('/all_user_reviews')
def see_all_user_reviews():
    all_user_reviews = [] 
    u = User_Reviews.query.all()
    for review_by_user in u:
        all_user_reviews.append((review_by_user.business_name, review_by_user.review_rating, review_by_user.review_text))
    return render_template('see_all_user_reviews.html',names=all_user_reviews)
    

## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!

if __name__ == '__main__':
    db.create_all() 
    app.run(use_reloader=True,debug=True) 
    manager.run()
