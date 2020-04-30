import sqlite3

DATABASE = 'YelpDatabase.sqlite'

class DatabaseAccessor:

    city_table_name = "city_table"
    zip_code_table_name = "zip_code_table"
    categories_table_name = "category_table"
    business_data_per_city_table_name = "business_data_per_city_table"
    business_data_per_zip_code_table_name = "business_data_per_zip_code_table"

    def __init__(self, database):
        self.database = database

    def execute_query(self, query):
        '''
        Given a query, this function connects to the YelpDatabase.sqlite database, executes
        the query and returns back the result (in form of the tuple)

        Parameters:
        -----------
        query: String
            Query to be executed on th database

        Returns
        -----------
        Tuple: Result from the database
        '''
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        result = cursor.execute(query).fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return result

    ## Create table functions

    # def create_city_table(self):
    #     city_table_create_query = """CREATE TABLE IF NOT EXISTS city_table (
    #         id integer PRIMARY KEY,
    #         city_name text
    #     );
    #     """
    #     self.execute_query(city_table_create_query)
    #
    # def create_zip_code_table(self):
    #     zip_code_table_create_query = """CREATE TABLE IF NOT EXISTS zip_code_table (
    #         id integer PRIMARY KEY,
    #         zip_code text,
    #         city_id integer
    #     );
    #     """
    #     self.execute_query(zip_code_table_create_query)
    #
    # def create_category_table(self):
    #     category_table_query = """CREATE TABLE IF NOT EXISTS category_table (
    #         id integer PRIMARY KEY,
    #         category_name text
    #     );
    #     """
    #     self.execute_query(category_table_query)

    def create_business_data_per_city_table(self):
        business_table_query = """CREATE TABLE IF NOT EXISTS business_data_per_city_table (
            city_name text PRIMARY KEY UNIQUE,
            average_rating real NOT NULL,
            average_review_count real NOT NULL,
            average_business_price_range real,
            top_category_1 text DEFAULT "N/A",
            top_category_2 text DEFAULT "N/A",
            top_category_3 text DEFAULT "N/A",
            top_business_ambience_type text DEFAULT "N/A",
            top_business_parking_type text DEFAULT "N/A",
            top_music_type text DEFAULT "N/A",
            top_dietary_restriction text DEFAULT "N/A"
        );
        """
        self.execute_query(business_table_query)

    def create_business_data_per_zip_code_table(self):
        ratings_table_query = """CREATE TABLE IF NOT EXISTS business_data_per_zip_code_table (
            zip_code text PRIMARY KEY UNIQUE,
            city_name text NOT NULL,
            average_rating real NOT NULL,
            average_review_count real,
            average_business_price_range real,
            top_category_1 text DEFAULT "N/A",
            top_category_2 text DEFAULT "N/A",
            top_category_3 text DEFAULT "N/A",
            top_business_ambience_type text DEFAULT "N/A",
            top_business_parking_type text DEFAULT "N/A",
            top_music_type text DEFAULT "N/A",
            top_dietary_restriction text DEFAULT "N/A" 
        );
        """
        self.execute_query(ratings_table_query)

    def create_tables(self):
        self.create_business_data_per_city_table()
        self.create_business_data_per_zip_code_table()

    ## insert functions
    def insert_business_data_for_city(self, city_name, average_rating, average_review_count, average_business_price_range, top_category_1, top_category_2, top_category_3, top_business_ambience_type, top_business_parking_type, top_music_type, top_dietary_restriction):

        query = """INSERT INTO {table_name}(
            city_name,
            average_rating,
            average_review_count,
            average_business_price_range,
            top_category_1,
            top_category_2,
            top_category_3,
            top_business_ambience_type,
            top_business_parking_type,
            top_music_type,
            top_dietary_restriction
        ) VALUES(
            "{city_name}",
            {average_rating},
            {average_review_count},
            {average_business_price_range},
            "{top_category_1}",
            "{top_category_2}",
            "{top_category_3}",
            "{top_business_ambience_type}",
            "{top_business_parking_type}",
            "{top_music_type}",
            "{top_dietary_restriction}"
        );
        """.format(table_name=self.business_data_per_city_table_name, city_name=city_name, average_rating=average_rating, average_review_count=average_review_count, average_business_price_range=average_business_price_range,
                   top_category_1=top_category_1,top_category_2=top_category_2, top_category_3=top_category_3, top_business_ambience_type=top_business_ambience_type,
                   top_business_parking_type=top_business_parking_type, top_music_type=top_music_type, top_dietary_restriction=top_dietary_restriction)

        return self.execute_query(query)

    def insert_business_data_for_zip_code(self, zip_code, city_name, average_rating, average_review_count, average_business_price_range, top_category_1, top_category_2, top_category_3, top_business_ambience_type, top_business_parking_type, top_music_type, top_dietary_restriction):

        query = """INSERT INTO {table_name}(
            zip_code,
            city_name,
            average_rating,
            average_review_count,
            average_business_price_range,
            top_category_1,
            top_category_2,
            top_category_3,
            top_business_ambience_type,
            top_business_parking_type,
            top_music_type,
            top_dietary_restriction
        ) VALUES(
            "{zip_code}",
            "{city_name}",
            {average_rating},
            {average_review_count},
            {average_business_price_range},
            "{top_category_1}",
            "{top_category_2}",
            "{top_category_3}",
            "{top_business_ambience_type}",
            "{top_business_parking_type}",
            "{top_music_type}",
            "{top_dietary_restriction}"
        );
        """.format(table_name=self.business_data_per_zip_code_table_name, zip_code=zip_code,
                   city_name=city_name, average_rating=average_rating, average_review_count=average_review_count,
                   average_business_price_range=average_business_price_range, top_category_1=top_category_1,
                   top_category_2=top_category_2, top_category_3=top_category_3, top_business_ambience_type=top_business_ambience_type,
                   top_business_parking_type=top_business_parking_type,top_music_type=top_music_type,
                   top_dietary_restriction=top_dietary_restriction)

        return self.execute_query(query)


    ##SELECT queries
    def select_business_data_using_city(self, city_name):
        query = """SELECT * FROM {table_name} WHERE city_name LIKE "{city_name}%";
        """.format(table_name=self.business_data_per_city_table_name, city_name=city_name)

        return self.execute_query(query)

    def select_business_data_using_zip_code(self, zip_code):
        query = """SELECT * FROM {table_name} WHERE zip_code="{zip_code}";
        """.format(table_name=self.business_data_per_zip_code_table_name, zip_code=zip_code)

        return self.execute_query(query)

    def select_all_zip_codes_with_same_city(self, city_name):
        query = """SELECT * FROM {table_name} WHERE city_name LIKE "{city_name}%";
        """.format(table_name=self.business_data_per_zip_code_table_name, city_name=city_name)

        return self.execute_query(query)

    def select_similar_zip_codes(self, zip_code):
        if zip_code is None:
            return []

        query = """SELECT * FROM {table_name} WHERE zip_code LIKE "{zip_code}%";
        """.format(table_name=self.business_data_per_zip_code_table_name, zip_code=zip_code)

        result = self.execute_query(query)
        if result is not None and len(result) > 0:
            tup_0 = result[0]
            if tup_0 is None:
                return result
            else:
                city = tup_0[1]
                return self.select_all_zip_codes_with_same_city(city)


if __name__ == "__main__":
    dao = DatabaseAccessor(DATABASE)
    #dao.create_tables()
    #print(dao.insert_business_data_for_city("Mumbai", 3.4, 145, 1.56, "Movies", "Groceries", "Food", "business", "street", "live", "vegan"))
    #print(dao.select_business_data_using_city("Mumbai"))
    #print(dao.insert_business_data_for_zip_code("98109", "Seattle", 3.4, 56, 1.45, "Coffee", "Restaurants", "Groceries", "casual", "street", "live", "vegeterian"))
    #print(dao.select_business_data_using_zip_code("98109"))
    print("Select city: " + str(dao.select_business_data_using_city("Phoenix")))
    print("Select zipcode: " + str(dao.select_business_data_using_zip_code("98101")))
    print("Select all zipcodes from city: " + str(dao.select_all_zip_codes_with_same_city("Toronto")))
    print("Select similar zip codes: " + str(dao.select_similar_zip_codes("98101")))


