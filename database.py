import sqlite3

DATABASE = 'YelpDatabase.sqlite'

def execute_query(query):
    '''
    Given a query, this function connects to the Northwind_small.sqlite database, executes
    the query and returns back the result (in form of the tuple)

    Parameters:
    -----------
    query: String
        Query to be executed on th database

    Returns
    -----------
    Tuple: Result from the database
    '''
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()
    return result


def create_city_table():
    city_table_create_query = """CREATE TABLE IF NOT EXISTS city_table (
        id integer PRIMARY_KEY,
        city_name text
    );
    """
    execute_query(city_table_create_query)

def create_category_table():
    category_table_query = """CREATE TABLE IF NOT EXISTS category_table (
        id integer PRIMARY_KEY,
        category_name text
    );
    """
    execute_query(category_table_query);

def create_business_data_table():
    business_table_query = """CREATE TABLE IF NOT EXISTS business_data_table (
        id integer PRIMARY_KEY,
        FOREIGN_KEY (city_id) REFERENCES city_table (id),
        FOREIGN_KEY (category_id) REFERENCES category_table (id),
        percentage real,
        top_attributes text
    );
    """
    execute_query(business_table_query)

def create_ratings_data_table():
    ratings_table_query = """CREATE TABLE IF NOT EXISTS ratings_data_table (
        id integer PRIMARY_KEY,
        FOREIGN_KEY (city_id) REFERENCES city_table (id),
        FOREIGN_KEY (category_id) REFERENCES category_table (id),
        average_rating real
    );
    """
    execute_query(ratings_table_query)


if __name__ == "__main__":
    create_city_table()
    create_category_table()
    create_business_data_table()
    create_ratings_data_table()

