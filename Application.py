from yelp import yelp_api
from database import database_accessor
from data_processing import yelp_api_data_processor
from data_processing import db_data_processor
from data_processing import yelp_review_processor
from flask import Flask, render_template, flash, redirect
from QueryForm import QueryForm
from flask_wtf.csrf import CSRFProtect
from graphs import plotter
import os

SECRET_KEY = os.urandom(32)

app = Flask('/')
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)

PATH_TO_CATEGORY_PIE_CHART = "static/img/category_pie_chart.png"
PATH_TO_CATEGORY_BAR_GRAPH = "static/img/category_bar_graph.png"
PATH_TO_GLOBAL_TOP_CATEGORIES = "static/img/global_top_cat_bar_graph.png"
PATH_TO_TOP_MUSIC = "static/img/global_top_music_pie_chart.png"
PATH_TO_TOP_AMBIENCE = "static/img/global_top_ambience_pie_chart.png"
PATH_TO_TOP_DIET ="static/img/global_top_dietery_restriction_pie_chart.png"
PATH_TO_TOP_PARKING = "static/img/global_top_parking.png"

PATH_TO_DATABASE = "database/YelpDatabase.sqlite"

dao = database_accessor.DatabaseAccessor(PATH_TO_DATABASE)

class Result:
    def __init__(self, business_name, location, avg_review, avg_rating, avg_price, top_categories):
        self.business_name = business_name
        self.location = location
        self.avg_review = avg_review
        self.avg_rating = avg_rating
        self.avg_price = avg_price
        self.top_categories = top_categories

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/query', methods=['GET', 'POST'])
def query_page():
    form = QueryForm()
    if form.validate_on_submit():
        location = form.location.data
        business_name = form.business_name.data
        search_by_zip_code = form.searchByZipCode.data
        return redirect('/query/{}/{}/{}'.format(location, business_name, 'zipCode='+str(search_by_zip_code)))
    return render_template('query.html', form=form)

@app.route('/error')
def oops():
    return render_template("error.html")


@app.route('/query/<location>/<business_name>/<shouldSearchByZipCode>', methods=['GET', 'POST'])
def query_yelp(location, business_name, shouldSearchByZipCode):
    try:
        #print("Querying Yelp API for {} and {}".format(location, business_name) )
        json_result = yelp_api.search_businesses_by_location(business_name, location)
        processor = yelp_api_data_processor.YelpApiBusinessDataProcessor(json_result)

        result = Result(business_name, location, processor.get_avg_review_counts(), processor.get_avg_ratings(), processor.get_avg_price(),
                    processor.get_top_three_popular_categories())

        plt = plotter.GraphPlotter()
        plt.plot_and_save_bar_graph(processor.get_category_distribution_data(), PATH_TO_CATEGORY_BAR_GRAPH, "Percentage", "Category")

        db_processor = db_data_processor.DbDataProcessor(dao)

        if shouldSearchByZipCode == "zipCode=True":
            db_processor.get_zip_code_data_from_db(location)
        else:
            db_processor.get_city_data_from_db(location)

        db_processor.process_data()

        global_avg_review_count = db_processor.get_avg_review_count()
        global_avg_ratings = db_processor.get_avg_ratings_count()
        city_name = db_processor.get_city_name()

        max_review_count = processor.max_review_count
        top_business_id = processor.top_business_id

        #print(top_business_id)

        review_list = None
        top_business = None
        top_business_rating = None
        top_business_price = None
        top_business_url = None
        if top_business_id is not None:
            review_list = []
            review_json = yelp_api.search_reviews_by_business_id(top_business_id)
            reviews = yelp_review_processor.YelpReviewsProcessor(review_json).get_processed_reviews()
            for review in reviews:
                review_list.append(str(review.rating) + "* : " + review.review + " -- " + review.name)

            top_business_json = yelp_api.search_business_by_business_id(top_business_id)
            print(str(top_business_json))
            if top_business_json is not None:
                top_business = top_business_json['name']
                top_business_rating = top_business_json['rating']
                top_business_price = top_business_json['price']
                top_business_url = top_business_json['url']

        show_reviews = True if review_list is not None else False

        #print("Show reviews: " + str(show_reviews))
        #print(str(review_list))

        top_categories = db_processor.get_top_categories()
        top_parking = db_processor.get_top_parking()
        top_music = db_processor.get_top_music()
        top_ambience = db_processor.get_top_ambience()
        top_dietery_restriction = db_processor.get_top_dietery_restriction()


        show_global_top_cat = True if top_categories is not None and len(top_categories) > 0 else False
        show_top_parking = True if top_parking is not None and len(top_parking) > 0 else False
        show_top_music = True if top_music is not None and len(top_music) > 0 else False
        show_top_ambience = True if top_ambience is not None and len(top_ambience) > 0 else False
        show_top_diet = True if top_dietery_restriction is not None and len(top_dietery_restriction) > 0 else False

        if show_global_top_cat:
            plt.plot_and_save_bar_graph(top_categories, PATH_TO_GLOBAL_TOP_CATEGORIES, "Percentage", "Category")
        if show_top_parking:
            plt.plot_and_save_pie_chart(top_parking, PATH_TO_TOP_PARKING)
        if show_top_music:
            plt.plot_and_save_pie_chart(top_music, PATH_TO_TOP_MUSIC)
        if show_top_ambience:
            plt.plot_and_save_pie_chart(top_ambience, PATH_TO_TOP_AMBIENCE)
        if show_top_diet:
            plt.plot_and_save_pie_chart(top_dietery_restriction, PATH_TO_TOP_DIET)


        return render_template('result.html', business_name=result.business_name, location=result.location,
                    avg_rating=result.avg_rating, avg_price=result.avg_price, avg_review_count=result.avg_review,
                    top_categories=result.top_categories, city_name=city_name,
                    global_avg_ratings=global_avg_ratings, global_avg_review_count=global_avg_review_count,
                    show_global_top_cat=str(show_global_top_cat).lower(), show_top_parking=str(show_top_parking).lower(),
                    show_top_music=str(show_top_music).lower(), show_top_ambience=str(show_top_ambience).lower(),
                    show_top_diet=str(show_top_diet).lower(), review_list=review_list, show_reviews=str(show_reviews).lower(),
                    top_business=top_business, top_business_price=top_business_price,
                    top_business_rating=str(top_business_rating), top_business_url=top_business_url)

    except:
        return redirect('/error')

if __name__ == '__main__':
    app.run(debug=True)