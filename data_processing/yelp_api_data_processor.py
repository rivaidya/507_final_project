from yelp import yelp_api

class YelpApiBusinessDataProcessor:
    def __init__(self, business_data_json):
        self.business_data_json = business_data_json
        self.categories_dict = dict()
        self.review_counts_list = []
        self.pricing_list = []
        self.ratings_list = []
        self.top_business_id = None
        self.max_review_count = 0
        self.parse_response()
        self.avg_review_counts = self.calculate_avg_counts(self.review_counts_list)
        self.avg_price = self.calculate_avg_counts(self.pricing_list)
        self.avg_ratings = self.calculate_avg_counts(self.ratings_list)


    def get_avg_review_counts(self):
        return self.avg_review_counts

    def get_avg_price(self):
        return round(float(self.avg_price))*'$'

    def get_avg_ratings(self):
        return self.avg_ratings

    def calculate_avg_counts(self, list_of_values):
        '''Given a list of values, this method calculates the averages across the list.

        Parameters:
        ----------
        list_of_values: List which contains  a list of values .

        Returns:
        -------
        average.
        '''
        return format(sum(list_of_values)/len(list_of_values), '.2f')


    def parse_response(self):
        if self.business_data_json is None:
            return

        max_review_count = 0
        for json_item in self.business_data_json['businesses']:

            #populate the pricing list
            if 'price' in json_item:
                price = self.convert_price_symbol_to_integer(json_item['price'])
                self.pricing_list.append(price)

            #populate the categories
            categories = json_item.get('categories', [])
            for category in categories:
                title = category.get('title', None)
                if title is not None:
                    count = self.categories_dict.get(title, 0)
                    count = count + 1
                    self.categories_dict[title] = count

            review_count = json_item.get('review_count', 0)

            if review_count > max_review_count:
                max_review_count = review_count
                business_id = json_item.get('id', None)
                if business_id is not None:
                    self.top_business_id = business_id

            self.review_counts_list.append(review_count)

            rating = json_item.get('rating', 0.0)
            self.ratings_list.append(rating)

        self.max_review_count = max_review_count


    def convert_price_symbol_to_integer(self, price_symbol):
        '''The Yelp API response contains price in terms of $$$ signs and is not
        very user friendly interface to perform basic arithmetic on. This method
        converts the price symbol into integer.
        eg: $ = 1. $$ = 2, and so on

        Parameter:
        ---------
        price_symbol: String reprenting the price symbol ($)

        Return:
        -------
        int:
            Integer representation of the price symbol
        '''
        if price_symbol is None:
            return 0

        return price_symbol.count("$")

    def sort_dictionary(self, dictionary):
        '''Sorts a dictionary in descending order of their values

        Parameters:
        ----------
        dictionary: Dictionary to be sorted

        Return:
        List:
            Returns a List of Tuples [(Key, Value)]
        '''
        list_of_tuples = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        return list_of_tuples

    def get_top_three_popular_categories(self):
        list_of_tuples = self.sort_dictionary(self.categories_dict)
        list_of_top_categories = []
        for tuple in list_of_tuples:
            list_of_top_categories.append(tuple[0])
        if len(list_of_top_categories) > 3:
            return list_of_top_categories[0:3]
        else:
            return list_of_top_categories

    def get_category_distribution_data(self):
        list_of_tuples = self.sort_dictionary(self.categories_dict)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples


if __name__ == '__main__':
    json_result = yelp_api.search_businesses_by_location("Thai Food", "Seattle")
    processor = YelpApiBusinessDataProcessor(json_result)
    print("get_category_distribution_data: " + str(processor.get_category_distribution_data()))
    print("get_top_three_popular_categories: " + str(processor.get_top_three_popular_categories()))
    print("avg reviews: " + str(processor.get_avg_review_counts()))
    print("avg ratings: " + str(processor.get_avg_ratings()))
    print("avg price: " + str(processor.get_avg_price()))
    print("top_business_id: " + str(processor.top_business_id))
