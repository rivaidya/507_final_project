#importing processed business data from data processing

from data_processing.business_data_processor import ProcessedBusinessData
from data_processing.business_data_processor import BUSINESS_DATA_JSON_PATH
from database import database_accessor
from collections import OrderedDict

class DbPopulator:
    def __init__(self, processed_business_data, dao):
        self.processed_business_data = processed_business_data
        self.dao = dao
        #create tables if they are not already created
        self.dao.create_tables()

    def sort_dictionary_and_get_highest(self, dictionary, keyed_item):
        list_of_tuples = sorted(dictionary.get(keyed_item, dict()).items(), key=lambda x: x[1], reverse=True)
        if list_of_tuples is not None and len(list_of_tuples) > 0:
            return list_of_tuples[0][0]
        else:
            return "N/A"

    def populate_business_data_for_city_table(self):
        if self.processed_business_data is None:
            raise Exception("ProcessedBusinessData cannot be None.")

        list_of_cities = self.processed_business_data.get_unique_cities_in_data_set()
        if list_of_cities is None or len(list_of_cities) == 0:
            print("No cities are found in processed business data. No action required.")
            return

        print("Populating database with city index ...")

        average_rating_per_city = self.processed_business_data.get_avg_ratings_per_city()
        average_review_count_per_city = self.processed_business_data.get_avg_review_count_per_city()
        average_business_price_range_per_city = self.processed_business_data.get_restaurant_price_range_per_city()
        categories_per_city = self.processed_business_data.get_categories_per_city()
        business_parking_per_city = self.processed_business_data.get_business_parking_per_city()
        ambience_per_city = self.processed_business_data.get_ambience_per_city()
        dietery_restrictions_per_city = self.processed_business_data.get_dietery_restriction_per_city()
        music_type_per_city = self.processed_business_data.get_music_type_per_city()

        for city in list_of_cities:
            city_name = city
            average_rating = average_rating_per_city.get(city, None)
            average_review_count = average_review_count_per_city.get(city, None)
            average_business_price_range = average_business_price_range_per_city.get(city, 1)

            business_parking = self.sort_dictionary_and_get_highest(business_parking_per_city, city)

            ambience = self.sort_dictionary_and_get_highest(ambience_per_city, city)

            dietery_restriction = self.sort_dictionary_and_get_highest(dietery_restrictions_per_city, city)

            music_type = self.sort_dictionary_and_get_highest(music_type_per_city, city)

            top_category_1 = "N/A"
            top_category_2 = "N/A"
            top_category_3 = "N/A"

            sorted_categories = sorted(categories_per_city.get(city, dict()).items(), key=lambda x: x[1], reverse=True)
            count = 0
            for category in sorted_categories:
                if count == 0:
                    top_category_1 = category[0]
                elif count == 1:
                    top_category_2 = category[0]
                elif count == 3:
                    top_category_3 = category[0]
                count += 1

            #validate the required fields
            if city_name is None or average_rating is None or average_review_count is None:
                print("Cannot populate data for city: " + city_name)
                continue

            self.dao.insert_business_data_for_city(city_name, average_rating, average_review_count,
                                                   average_business_price_range, top_category_1, top_category_2,
                                                   top_category_3, ambience, business_parking, music_type,
                                                   dietery_restriction)

            print("Data for city: " + city_name + " inserted.")

    def populate_business_data_for_zip_code_table(self):
        if self.processed_business_data is None:
            raise Exception("ProcessedBusinessData cannot be None.")

        list_of_zip_codes = self.processed_business_data.get_unique_zip_codes_in_data_set()
        if list_of_zip_codes is None or len(list_of_zip_codes) == 0:
            print("No zip codes are found in processed business data. No action required.")
            return

        average_ratings_per_zip_code = self.processed_business_data.get_avg_ratings_per_zip_code()
        average_review_count_per_zip_code = self.processed_business_data.get_avg_review_count_per_zip_code()
        average_business_price_range_per_zip_code = self.processed_business_data.get_restaurant_price_range_per_zip_code()
        zip_code_to_city_map = self.processed_business_data.get_zip_code_to_city_map()
        categories_per_zip_code = self.processed_business_data.get_categories_per_zip_code()
        business_parking_per_zip_code = self.processed_business_data.get_business_parking_per_zip_code()
        ambience_per_zip_code = self.processed_business_data.get_ambience_per_zip_code()
        dietery_restriction_per_zip_code = self.processed_business_data.get_dietery_restriction_per_zip_code()
        music_type_per_zip_code = self.processed_business_data.get_music_type_per_zip_code()

        for zip_code in list_of_zip_codes:
            if zip_code is None:
                continue

            city_name = zip_code_to_city_map.get(zip_code, "N/A")
            average_rating = average_ratings_per_zip_code.get(zip_code, -1.0)
            average_review_count = average_review_count_per_zip_code.get(zip_code, -1.0)
            average_business_price_range = average_business_price_range_per_zip_code.get(zip_code, -1.0)
            ambience = self.sort_dictionary_and_get_highest(ambience_per_zip_code, zip_code)
            parking = self.sort_dictionary_and_get_highest(business_parking_per_zip_code, zip_code)
            dietery_restriction = self.sort_dictionary_and_get_highest(dietery_restriction_per_zip_code, zip_code)
            music_type = self.sort_dictionary_and_get_highest(music_type_per_zip_code, zip_code)

            top_category_1 = "N/A"
            top_category_2 = "N/A"
            top_category_3 = "N/A"

            sorted_categories = sorted(categories_per_zip_code.get(zip_code, dict()).items(), key=lambda x: x[1], reverse=True)
            count = 0
            for category in sorted_categories:
                if count == 0:
                    top_category_1 = category[0]
                elif count == 1:
                    top_category_2 = category[0]
                elif count == 3:
                    top_category_3 = category[0]
                count += 1

            self.dao.insert_business_data_for_zip_code(zip_code, city_name, average_rating, average_review_count,
                                                       average_business_price_range, top_category_1, top_category_2,
                                                       top_category_3, ambience, parking, music_type, dietery_restriction)

            print("Successfully entered data for zip code: " + zip_code)

if __name__ == '__main__':
    processed_business_data = ProcessedBusinessData("../data_processing/data/yelp_academic_dataset_business.json")
    dao = database_accessor.DatabaseAccessor(database_accessor.DATABASE)
    db_populator = DbPopulator(processed_business_data, dao)
    db_populator.populate_business_data_for_zip_code_table()
