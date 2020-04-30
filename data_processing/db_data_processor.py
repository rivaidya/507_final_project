from database import database_accessor

class DbDataProcessor:

    def __init__(self, dao):
        self.dao = dao
        self.city_data = [] #List of list of tuples
        self.zipcode_data = [] #List of list of tuples
        self.categories = {}
        self.attributes = {}
        self.ambience = {}
        self.parking = {}
        self.music = {}
        self.dietery_restriction = {}
        self.avg_rating = None
        self.avg_reviews = None
        self.city = None

    def get_city_data_from_db(self, city):
        if city is None:
            return
        self.city = city
        self.city_data.append(self.dao.select_business_data_using_city(city))
        self.zipcode_data.append(self.dao.select_all_zip_codes_with_same_city(city))
        return

    def get_city_from_zip_code(self, zip_code):
        if zip_code is None:
            return
        if self.zipcode_data is not None and len(self.zipcode_data) > 0:
            self.city = self.zipcode_data[0][0][1]
        else:
            self.zipcode_data.append(self.get_zip_code_data_from_db(zip_code))
            if self.zipcode_data is not None and len(self.zipcode_data) > 0:
                self.city = self.zipcode_data[0][1]

        return self.city

    def get_zip_code_data_from_db(self, zip_code):
        if zip_code is None:
            return
        self.zipcode_data.append(self.dao.select_business_data_using_zip_code(zip_code))
        self.zipcode_data.append(self.dao.select_similar_zip_codes(zip_code))
        city = self.get_city_from_zip_code(zip_code)
        self.city_data.append(self.get_city_data_from_db(city))
        return


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

    def get_city_data(self):
        return self.city_data

    def get_zip_code_data(self):
        return self.zipcode_data

    def get_top_attributes(self):
        list_of_tuples = self.sort_dictionary(self.attributes)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples

    def get_top_categories(self):
        list_of_tuples = self.sort_dictionary(self.categories)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples

    def get_avg_review_count(self):
        return self.avg_reviews

    def get_avg_ratings_count(self):
        return self.avg_rating

    def get_top_parking(self):
        list_of_tuples = self.sort_dictionary(self.parking)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples

    def get_top_ambience(self):
        list_of_tuples = self.sort_dictionary(self.ambience)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples

    def get_top_music(self):
        list_of_tuples = self.sort_dictionary(self.music)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples

    def get_top_dietery_restriction(self):
        list_of_tuples = self.sort_dictionary(self.dietery_restriction)
        if len(list_of_tuples) > 10:
            list_of_tuples = list_of_tuples[0:10]
        return list_of_tuples

    def get_city_name(self):
        return self.city

    def process_data(self):
        if self.categories is None:
            self.categories = {}

        ratings = []
        reviews = []

        if self.zipcode_data is not None and len(self.zipcode_data) > 0:
            for list_of_tuples in self.zipcode_data:
                if list_of_tuples is None:
                    continue
                for tup in list_of_tuples:
                    if tup is None:
                        continue
                    top_cat_1 = tup[5]
                    top_cat_2 = tup[6]
                    top_cat_3 = tup[7]
                    if top_cat_1 != "N/A":
                        count = self.categories.get(top_cat_1, 0)
                        count = count + 1
                        self.categories[top_cat_1] = count
                    if top_cat_2 != "N/A":
                        count = self.categories.get(top_cat_2, 0)
                        count = count + 1
                        self.categories[top_cat_2] = count
                    if top_cat_3 != "N/A":
                        count = self.categories.get(top_cat_3, 0)
                        count = count + 1
                        self.categories[top_cat_3] = count

                    ambience_type = tup[8]
                    parking_type = tup[9]
                    music_type = tup[10]
                    dietery_restriction_type = tup[11]

                    if ambience_type != "N/A":
                        count = self.ambience.get(ambience_type, 0)
                        count = count + 1
                        self.ambience[ambience_type] = count
                    if parking_type != "N/A":
                        count = self.parking.get(parking_type, 0)
                        count = count + 1
                        self.parking[parking_type] = count
                    if music_type != "N/A":
                        count = self.music.get(music_type, 0)
                        count = count + 1
                        self.music[music_type] = count
                    if dietery_restriction_type != "N/A":
                        print(dietery_restriction_type)
                        count = self.dietery_restriction.get(dietery_restriction_type, 0)
                        count = count + 1
                        self.dietery_restriction[dietery_restriction_type] = count

                    reviews.append(tup[3])
                    ratings.append(tup[2])

        if self.city_data is not None and len(self.city_data) > 0:
            for list_of_tups in self.city_data:
                if list_of_tups is None:
                    continue
                for tups in list_of_tups:
                    if tups is None:
                        continue
                    top_cat_1 = tups[4]
                    top_cat_2 = tups[5]
                    top_cat_3 = tups[6]
                    if top_cat_1 != "N/A":
                        count = self.categories.get(top_cat_1, 0)
                        count = count + 1
                        self.categories[top_cat_1] = count
                    if top_cat_2 != "N/A":
                        count = self.categories.get(top_cat_2, 0)
                        count = count + 1
                        self.categories[top_cat_2] = count
                    if top_cat_3 != "N/A":
                        count = self.categories.get(top_cat_3, 0)
                        count = count + 1
                        self.categories[top_cat_3] = count

                    ambience_type = tups[7]
                    parking_type = tups[8]
                    music_type = tups[9]
                    dietery_restriction_type = tups[10]

                    if ambience_type != "N/A":
                        count = self.ambience.get(ambience_type, 0)
                        count = count + 1
                        self.ambience[ambience_type] = count
                    if parking_type != "N/A":
                        count = self.parking.get(parking_type, 0)
                        count = count + 1
                        self.parking[parking_type] = count
                    if music_type != "N/A":
                        count = self.music.get(music_type, 0)
                        count = count + 1
                        self.music[music_type] = count
                    if dietery_restriction_type != "N/A":
                        count = self.dietery_restriction.get(dietery_restriction_type, 0)
                        count = count + 1
                        self.dietery_restriction[dietery_restriction_type] = count

                    reviews.append(tups[2])
                    ratings.append(tups[1])

        if len(ratings) > 0:
            self.avg_rating = format(sum(ratings)/len(ratings), '.2f')
        else:
            self.avg_rating = "Data not available"

        if len(reviews) > 0:
            self.avg_reviews = format(sum(reviews)/len(reviews), '.2f')
        else:
            self.avg_reviews = "Data not available"

if __name__ == "__main__":
    dao = database_accessor.DatabaseAccessor("../database/YelpDatabase.sqlite")
    processor = DbDataProcessor(dao)

    #processor.get_city_data_from_db("Phoenix")
    #print(str(processor.get_zip_code_data()))
    #print(str(processor.get_city_data()))

    processor.get_zip_code_data_from_db("88031")
    processor.process_data()
    print(str(processor.get_zip_code_data()))
    print(str(processor.get_city_data()))
    print(str(processor.get_top_categories()))
    print(str(processor.get_avg_ratings_count()))
    print(str(processor.get_avg_review_count()))
    print(str(processor.get_top_ambience()))
    print(str(processor.get_top_parking()))
    print(str(processor.get_top_music()))
    print(str(processor.get_top_dietery_restriction()))



