import pandas as pd
import time
import json

BUSINESS_DATA_JSON_PATH = "data/yelp_academic_dataset_business.json"

UNIQUE_ATTRIBUTES_SUPPORTED = {'Alcohol', 'RestaurantsTableService', 'GoodForKids', 'WheelchairAccessible', 'DriveThru', 'GoodForDancing', 'RestaurantsCounterService', 'Caters', 'RestaurantsGoodForGroups', 'GoodForMeal', 'DietaryRestrictions', 'BestNights', 'HappyHour', 'BikeParking', 'OutdoorSeating', 'CoatCheck', 'BYOBCorkage', 'Smoking', 'Ambience', 'BusinessAcceptsBitcoin', 'BYOB', 'RestaurantsReservations', 'RestaurantsDelivery', 'DogsAllowed', 'HasTV', 'WiFi', 'ByAppointmentOnly', 'RestaurantsAttire', 'AgesAllowed', 'NoiseLevel', 'Corkage', 'BusinessParking', 'RestaurantsTakeOut', 'BusinessAcceptsCreditCards', 'AcceptsInsurance'}

#These attributes have values as True or False.
METADATA_FOR_UNIQUE_ATTRIBUTES = {'BusinessParking': {'street', 'lot', 'valet', 'validated', 'garage'}, 'Ambience': {'romantic', 'upscale', 'touristy', 'divey', 'classy', 'casual', 'hipster', 'trendy', 'intimate'}, 'GoodForMeal': {'latenight', 'lunch', 'brunch', 'dinner', 'dessert', 'breakfast'}, 'BestNights': {'friday', 'monday', 'saturday', 'tuesday', 'wednesday', 'sunday', 'thursday'}, 'Music': {'dj', 'live', 'jukebox', 'no_music', 'karaoke', 'background_music', 'video'}, 'DietaryRestrictions': {'gluten-free', 'halal', 'kosher', 'dairy-free', 'soy-free', 'vegetarian', 'vegan'}}


class ProcessedBusinessData:
    def __init__(self, json_file_path):
        self.df = self.load_business_data(json_file_path)
        self.unique_cities = set()
        self.unique_categories = set()
        self.unique_zip_codes = set()
        self.unique_attributes = set()
        self.avg_rating_per_city = {}
        self.avg_rating_per_zip_code = {}
        self.avg_review_count_per_city = {}
        self.avg_review_count_per_zip_code = {}
        self.zip_code_to_city_map = {}
        self.categories_per_zip_code = {}
        self.categories_per_city = {}
        self.attributes_per_city = {}
        self.attributes_per_zip_code = {}
        self.attributes_metadata = {}
        self.business_parking_per_city = {}
        self.business_parking_per_zip_code = {}
        self.ambience_per_city = {}
        self.ambience_per_zip_code = {}
        self.dietery_restriction_per_city = {}
        self.dietery_restriction_per_zip_code = {}
        self.music_type_per_city = {}
        self.music_type_per_zip_code = {}
        self.restaurant_price_range_per_city = {}
        self.restaurant_price_range_per_zip_code = {}
        self.populate_business_data()
        self.calculate_avg_counts(self.avg_rating_per_city)
        self.calculate_avg_counts(self.avg_rating_per_zip_code)
        self.calculate_avg_counts(self.avg_review_count_per_zip_code)
        self.calculate_avg_counts(self.avg_review_count_per_city)
        self.calculate_avg_counts(self.restaurant_price_range_per_city)
        self.calculate_avg_counts(self.restaurant_price_range_per_zip_code)

    def calculate_avg_counts(self, dict):
        '''Given a dictionary wherein every key has a list of values, this method calculates the averages across the list.

        Parameters:
        ----------
        dict: Dictionary which contains keys with a list of values keyed to it.

        Returns:
        -------
        None.
        '''
        for key in dict:
            list_of_values = dict.get(key)
            #Maintain an accuracy upto 2 decimal points for avergaes.
            dict[key] = format(sum(list_of_values)/len(list_of_values), '.2f')

        return


    def load_business_data(self, json_file_path):
        '''Load the contents of business_data.json into data frame and return the data frame

        Parameters:
        ----------
        None

        Returns:
        -------
        DataFrame:
            DataFrame Object representing the contents of the business_data.json file.
        '''
        print("Loading business_data.json as data frames using pandas")
        return pd.read_json(json_file_path, lines=True)

    def populate_business_data(self):
        '''Populate the unique parameters such as cities and categories across the data set.

        Parameters:
            None

        Return:
            None
        '''
        unique_params = self.df[["city", "state", "categories", "postal_code", "stars", "review_count", "attributes"]]
        print(unique_params.head())
        for index, row in unique_params.iterrows():

            #populate unique cities
            city = self.get_city_from_row(row)
            if city is not None:
                self.unique_cities.add(city)

            #populate the unique categories
            category_list = self.get_category_from_row(row)
            if category_list is not None:
                for category in category_list:
                    self.unique_categories.add(category)


            zip_code = self.get_zip_code_from_row(row)
            ratings = self.get_ratings_from_row(row)
            review_count = self.get_review_count_from_row(row)

            if zip_code is not None:
                self.unique_zip_codes.add(zip_code)

            #populate or update avg rating and avg review count for the city.
            if city is not None:
                if ratings is not None:
                    if city in self.avg_rating_per_city:
                        ratings_list_for_city = self.avg_rating_per_city.get(city)
                        if ratings_list_for_city is None:
                            ratings_list_for_city = []
                        if ratings is not None:
                            ratings_list_for_city.append(ratings)
                        self.avg_rating_per_city[city] = ratings_list_for_city
                    else:
                        self.avg_rating_per_city[city] = [ratings]

                if review_count is not None:
                    if city in self.avg_review_count_per_city:
                        review_count_list_for_city = self.avg_review_count_per_city.get(city)
                        if review_count_list_for_city is None:
                            review_count_list_for_city = []
                        if review_count is not None:
                            review_count_list_for_city.append(review_count)
                        self.avg_review_count_per_city[city] = review_count_list_for_city
                    else:
                        self.avg_review_count_per_city[city] = [review_count]

            #populate or update avg rating and avg review count for the zip code
            if zip_code is not None:

                if ratings is not None:
                    if zip_code in self.avg_rating_per_zip_code:
                        ratings_list_for_zip_code = self.avg_rating_per_zip_code.get(zip_code)
                        if ratings_list_for_zip_code is None:
                            ratings_list_for_zip_code = []
                        if ratings is not None:
                            ratings_list_for_zip_code.append(ratings)
                        self.avg_rating_per_zip_code[zip_code] = ratings_list_for_zip_code
                    else:
                        self.avg_rating_per_zip_code[zip_code] = [ratings]

                if review_count is not None:
                    if zip_code in self.avg_review_count_per_zip_code:
                        review_count_list_for_zip_code = self.avg_review_count_per_zip_code.get(zip_code)
                        if review_count_list_for_zip_code is None:
                            review_count_list_for_zip_code = []
                        if review_count is not None:
                            review_count_list_for_zip_code.append(review_count)
                        self.avg_review_count_per_zip_code[zip_code] = review_count_list_for_zip_code
                    else:
                        self.avg_review_count_per_zip_code[zip_code] = [review_count]

            #populate the zip_code to city_map
            if zip_code is not None and city is not None:
                if zip_code not in self.zip_code_to_city_map:
                    self.zip_code_to_city_map[zip_code] = city

            #add category counts to city and zipcode
            if category_list is not None:
                if city is not None:
                    for cat in category_list:
                        self.add_category_to_map(self.categories_per_city, city, cat)
                if zip_code is not None:
                    for cat in category_list:
                        self.add_category_to_map(self.categories_per_zip_code, zip_code, cat)

            #Parse attributes
            attributes = self.get_attributes_from_row(row)
            self.parse_attributes_dictionary(attributes, zip_code, city)


    def add_category_to_map(self, dictionary, key, category):
        '''Given a dictionary (either categories_per_zip_code or categories_per_city) and
        a key (representing the city or the zip code based on the dictionary), and the corresponding
        cateogry, this function adds the category to the dictionary for the city or zipcode
        and updates the count

        Parameters:
        -----------
        dict: Dictionary (either categories_per_zip_code or categories_per_city)
        key: String (either city or zipcode)
        category: String
        :return:
        '''
        if dictionary is None or key is None or category is None:
            return

        if key not in dictionary:
            category_map = dict()
            category_map[category] = 1
            dictionary[key] = category_map
        else:
            #key exists. get the category map
            category_map = dictionary.get(key)
            #check one more time to avoid NoneType operation errors
            if category_map is None:
                category_map = dict()
                category_map[category] = 1
            else:
                if category in category_map:
                    #Get the category count
                    category_count = category_map.get(category)
                    #update the category count
                    category_count = category_count + 1
                    #update the map
                    category_map[category] = category_count
                else:
                    category_map[category] = 1
            dictionary[key] = category_map

    def parse_attributes_dictionary(self, attributes, zip_code, city):
        '''Given a dictionary of attributes, this function is responsible for parsing
        the dictionary and returning back a list of attributes which are supported by
        the business.

        Parameters:
        -----------
        attributes: Dictionary of attributes

        Returns:
        --------
        List:
            List of attributes supported by the business
        '''
        if attributes is None:
            return

        for key, value in attributes.items():
            self.unique_attributes.add(key)
            #print("Type of value: " + str(type(value)))
            #print("Key: " + key + ", value: " + str(value))

            json_value = None
            try:
                string_as_json = (str(value)).replace("\'", "\"").replace("False", "false").replace("True", "true")
                #print("string as json: " + string_as_json)
                json_value = json.loads(string_as_json)
            except:
                json_value = None

            if key == "BusinessParking":
                self.parse_business_parking_attributes(json_value, zip_code, city)
            elif key == "Ambience":
                self.parse_ambience_attributes(json_value, zip_code, city)
            elif key == "Music":
                self.parse_music_attributes(json_value, zip_code, city)
            elif key == "DietaryRestrictions":
                self.parse_dietery_restrictions_attributes(json_value, zip_code, city)
            elif key == "RestaurantsPriceRange2":
                float_val = None
                try:
                    float_val = float(value)
                except:
                    float_val = None

                if float_val is not None:
                    if city not in self.restaurant_price_range_per_city:
                        self.restaurant_price_range_per_city[city] = []
                    list_of_price = self.restaurant_price_range_per_city.get(city)
                    if list_of_price is None:
                        list_of_price = []
                    list_of_price.append(float_val)
                    self.restaurant_price_range_per_city[city] = list_of_price

                    if zip_code not in self.restaurant_price_range_per_zip_code:
                        self.restaurant_price_range_per_zip_code[zip_code] = []
                    list_of_price = self.restaurant_price_range_per_zip_code.get(zip_code)
                    if list_of_price is None:
                        list_of_price = []
                    list_of_price.append(float_val)
                    self.restaurant_price_range_per_zip_code[zip_code] = list_of_price

            # #print(str(json_value))
            # if json_value is not None and isinstance(json_value, dict):
            #     if key not in self.attributes_metadata:
            #         self.attributes_metadata[key] = set()
            #     for key_value in json_value:
            #         set_of_keys = self.attributes_metadata.get(key)
            #         set_of_keys.add(key_value)
            #         self.attributes_metadata[key] = set_of_keys

        return

    def parse_business_parking_attributes(self, business_parking_json, zip_code, city):
        if business_parking_json is None:
            return

        self.parse_attributes_helper(zip_code, self.business_parking_per_zip_code, business_parking_json)
        self.parse_attributes_helper(city, self.business_parking_per_city, business_parking_json)

    def parse_ambience_attributes(self, ambience_json, zip_code, city):
        if ambience_json is None:
            return

        self.parse_attributes_helper(zip_code, self.ambience_per_zip_code, ambience_json)
        self.parse_attributes_helper(city, self.ambience_per_city, ambience_json)

    def parse_dietery_restrictions_attributes(self, dietery_json, zip_code, city):
        if dietery_json is None:
            return

        self.parse_attributes_helper(zip_code, self.dietery_restriction_per_zip_code, dietery_json)
        self.parse_attributes_helper(city, self.dietery_restriction_per_city, dietery_json)

    def parse_music_attributes(self, music_json, zip_code, city):
        if music_json is None:
            return

        self.parse_attributes_helper(zip_code, self.music_type_per_zip_code, music_json)
        self.parse_attributes_helper(city, self.music_type_per_city, music_json)

    def parse_attributes_helper(self, city_or_zip_code, dictionary, json_to_parse):
        if city_or_zip_code is not None:
            if city_or_zip_code not in dictionary:
                dictionary[city_or_zip_code] = {}
            map = dictionary.get(city_or_zip_code)
            for type, value in json_to_parse.items():
                if value:
                    if type in map:
                        count = map.get(type)
                        map[type] = count + 1
                    else:
                        map[type] = 1
            dictionary[city_or_zip_code] = map

    def get_city_from_row(self, row):
        '''Given a data_frame row representing the business data from business_data.json,
        return the city

        Parameters:
        -----------
        df: data frame representing the business_data.json file

        Returns:
        --------
        String:
            City Name
        '''
        return row["city"] + "," + row["state"]

    def get_category_from_row(self, row):
        '''Given a data_frame row representing the business data from business_data.json,
        this function returns a list of categories.

        Parameters:
        -----------
        row: data frame row representing the business_data.json file

        Returns:
        --------
        List:
            list of unique categories across the data frame.
        '''
        categories = row["categories"]
        if categories is not None:
            return categories.split(',')
        else:
            return categories

    def get_zip_code_from_row(self, row):
        '''Given a data_frame row representing the business data from business_data.json, this function
        returns the zip code from the row.

        Parameters:
        ----------
        row: data frame row

        Returns:
        --------
        String:
            Zip Code for the business
        '''
        return row["postal_code"]

    def get_ratings_from_row(self, row):
        '''Given a data_frame row representing the business data from business_data.json, this function
        returns the rating from the row.

        Parameters:
        ----------
        row: data frame row

        Returns:
        --------
        Float:
            Rating for the business
        '''
        return row["stars"]

    def get_review_count_from_row(self, row):
        '''Given a data_frame row representing the business data from business_data.json, this function
        returns the review count from the row.

        Parameters:
        ----------
        row: data frame row

        Returns:
        --------
        Integer:
            review_count for the business
        '''
        return row["review_count"]

    def get_attributes_from_row(self, row):
        '''Given a data_frame row representing the business data from business_data.json, this function
        returns the attributes from the row.

        Parameters:
        ----------
        row: data frame row

        Returns:
        --------
        dictionary:
            attributes for the business
        '''
        return row["attributes"]

    def get_unique_cities_in_data_set(self):
        return self.unique_cities

    def get_unique_categories_in_data_set(self):
        return self.unique_categories

    def get_unique_zip_codes_in_data_set(self):
        return self.unique_zip_codes

    def get_avg_ratings_per_city(self):
        return self.avg_rating_per_city

    def get_avg_ratings_per_zip_code(self):
        return self.avg_rating_per_zip_code

    def get_avg_review_count_per_city(self):
        return self.avg_review_count_per_city

    def get_avg_review_count_per_zip_code(self):
        return self.avg_review_count_per_zip_code

    def get_zip_code_to_city_map(self):
        return self.zip_code_to_city_map

    def get_categories_per_city(self):
        return self.categories_per_city

    def get_categories_per_zip_code(self):
        return self.categories_per_zip_code

    def get_attributes_per_city(self):
        return self.attributes_per_city

    def get_attributes_per_zip_code(self):
        return self.attributes_per_zip_code

    def get_unique_attributes(self):
        return self.unique_attributes

    def get_attributes_metadata(self):
        return self.attributes_metadata

    def get_business_parking_per_city(self):
        return self.business_parking_per_city

    def get_business_parking_per_zip_code(self):
        return self.business_parking_per_zip_code

    def get_ambience_per_city(self):
        return self.ambience_per_city

    def get_ambience_per_zip_code(self):
        return self.ambience_per_zip_code

    def get_dietery_restriction_per_city(self):
        return self.dietery_restriction_per_city

    def get_dietery_restriction_per_zip_code(self):
        return self.dietery_restriction_per_zip_code

    def get_music_type_per_city(self):
        return self.music_type_per_city

    def get_music_type_per_zip_code(self):
        return self.music_type_per_zip_code

    def get_restaurant_price_range_per_city(self):
        return self.restaurant_price_range_per_city

    def get_restaurant_price_range_per_zip_code(self):
        return self.restaurant_price_range_per_zip_code


if __name__ == "__main__":
    #Debug and test runs. Run the script individually to test this against a data set
    state_millis = int(round(time.time() * 1000))
    business_data = ProcessedBusinessData(BUSINESS_DATA_JSON_PATH)
    categories = business_data.get_unique_categories_in_data_set()
    cities = business_data.get_unique_cities_in_data_set()
    zip_codes = business_data.get_unique_zip_codes_in_data_set()
    #print("Number of unique categories in data set: " + str(len(categories)))
    #print(categories)
    #print("Number of unique cities in data set: " + str(len(cities)))
    #print(cities)
    #print("Number of unique zip codes in data set: " + str(len(zip_codes)))
    #print(zip_codes)
    #print("Average ratings per city: " + str(business_data.get_avg_ratings_per_city()))
    #print("Average ratings per zip code: " + str(business_data.get_avg_ratings_per_zip_code()))
    #avg_review_count_per_zip_code = business_data.get_avg_review_count_per_zip_code()
    #print("Number of Average review count per zip code: " + str(len(avg_review_count_per_zip_code)))
    #print("Average review count per zip code: " + str(avg_review_count_per_zip_code))
    ##avg_review_count_per_city = business_data.get_avg_review_count_per_city()
    #print("Number of Average review count per city: " + str(len(avg_review_count_per_city)))
    #print("Average review count per city: " + str(avg_review_count_per_city))
    #end_millis = int(round(time.time() * 1000))
    #print("Processing time (excluding time to print: " + str((end_millis - state_millis)))
    #print(business_data.get_zip_code_to_city_map())
    #print(business_data.get_categories_per_city())
    #print(business_data.get_categories_per_zip_code())
    # print("Ambience per city: " + str(business_data.get_ambience_per_city()))
    # print("Ambience per zip code: " + str(business_data.get_ambience_per_zip_code()))
    # print("Business parking per city: " + str(business_data.get_business_parking_per_city()))
    # print("Business parking per zip code: " + str(business_data.get_business_parking_per_zip_code()))
    # print("Restaurant price range per city: " + str(business_data.get_restaurant_price_range_per_city()))
    # print("Restuarant price range per zip code: " + str(business_data.get_restaurant_price_range_per_zip_code()))
    # print("Music type per city: " + str(business_data.music_type_per_city))
    # print("Music type per zip code: " + str(business_data.music_type_per_zip_code))
    # print("Dietery type per city: " + str(business_data.get_dietery_restriction_per_city()))
    # print("Dietery type per zip code: " + str(business_data.get_dietery_restriction_per_zip_code()))
