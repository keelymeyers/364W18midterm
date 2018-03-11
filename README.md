# SI 364 - Winter 2018 - Midterm Assignment

## App Description

My app is related to Yelp business reviews. It has multiple functions:

* It can be used to look up Yelp data for businesses based on user-input search parameters. Users can input the name and zip code of a business to see the price (in $$), rating, and previews of the top 3 Yelp reviews for a certain business. 
* Users can also see a page with all of the reviews and business data they have searched for thus far. 
* Additionally, users can input their own reviews for a business by entering the business name, a numerical rating, and a text review.
* Users can then see a summary of all the reviews they have left 

## Requirements:

- [ ] **Ensure that the `SI364midterm.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up)**
- [ ] **Add navigation in `base.html` with links (using `a href` tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**
- [ ] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**
- [ ] **Include at least 2 additional template `.html` files we did not provide.**
- [ ] **At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
    - These could be in the same template, and could be 1 of the 2 additional template files.**
- [ ] **At least one errorhandler for a 404 error and a corresponding template.**
- [ ] **At least one request to a REST API that is based on data submitted in a WTForm.**
- [ ] **At least one additional (not provided) WTForm that sends data with a `GET` request to a new page.**
- [ ] **At least one additional (not provided) WTForm that sends data with a `POST` request to the *same* page.**
- [ ] **At least one custom validator for a field in a WTForm.**
- [ ] **At least 2 additional model classes.**
- [ ] **Have a one:many relationship that works properly built between 2 of your models.** 
- [ ] **Successfully save data to each table.**
- [ ] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
- [ ] **Query data using an `.all()` method in at least one view function and send the results of that query to a template.**
- [ ] **Include at least one use of `redirect`. (HINT: This should probably happen in the view function where data is posted...)**
- [ ] **Include at least one use of `url_for`. (HINT: This could happen where you render a form...)**
- [ ] **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of `base.html`.*)** Note: I did not include a link to the route for template see_review.html in the navigation because this page only appears after a user has input their own review into the user_review_form.html page.

### Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

* (100 points) **Include an *additional* model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)**

* (100 points) **Write code in your Python file that will allow a user to submit duplicate data to a form, but will *not* save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**

## Routes and Templates:

* http:localhost:5000/ -> form.html
* http:localhost:5000/reviews -> see_all_search_results.html
* http:localhost:5000/user_form -> user_review_form.html
* http:localhost:5000/user_review -> see_review.html (only page NOT in navigation)
* http:localhost:5000/all_user_reviews -> see_all_user_reviews.html

## Notes

* An access key for the Yelp API is required. I have left an empty string in the file yelp_access.py to input the access key, and have provided my key in the submission comments on Canvas.
* The custom validator for searching businesses on Yelp validates the zip code (as Yelp search terms are not case sensitive and are forgiving in regards to punctuation, etc.), which is similar to code from Discussion Week 5 

