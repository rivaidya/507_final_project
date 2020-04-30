import json
from yelp import yelp_api

class Review:
    def __init__(self, rating, review, name):
        self.rating = rating
        self.review = review
        self.name = name

class YelpReviewsProcessor:
    def __init__(self, review_json):
        self.review_json = review_json
        self.reviews = []
        self.process_review()

    def get_processed_reviews(self):
        if len(self.reviews) > 3:
            return self.reviews[0:3]
        else:
            return self.reviews

    def process_review(self):
        review_list = self.review_json['reviews']
        if review_list is not None:
            for review in review_list:
                rating = review.get('rating', None)
                text = review.get('text', None)
                name = review.get('user', dict()).get('name')
                self.reviews.append(Review(rating, text, name))

if __name__ == '__main__':
    review_json = yelp_api.search_reviews_by_business_id("ZUI_aLwc7mXG8Dt1Sz3aXg")
    print('review ' + str(review_json))
    processor = YelpReviewsProcessor(review_json)
    for review in processor.get_processed_reviews():
        print(review.review + " ," + str(review.rating) + " ," + review.name)