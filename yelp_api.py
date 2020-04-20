import requests
import urllib
import json
from secrets import API_KEY

ENDPOINT = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

BUSINESS_DATA_CACHE = "business_data_cache.json"

#Dictionary for maintaining the mapping of a cache file with it's URL
CACHE_MAP = {
    ENDPOINT + SEARCH_PATH: BUSINESS_DATA_CACHE
}

def open_cache(cache_file):
    '''opens the cache file if it exists and loads the data in the cache file into
    a dictionary. If the cache file does not exist, an empty dictionary is returned
    back to the user.

    :param cache_file: cache file to be opened. Expects a file in the JSON format.

    Returns
    -------
    The opened cache in dict format
    '''

    cache_dict = None
    try:
        cache = open(cache_file, 'r')
        cache_dict = json.loads(cache.read())
        cache.close()
    except:
        cache_dict = {}

    return cache_dict

def save_cache(cache_dict, cache_file):
    '''Given a dictionary, this method saves the data in the dictionary to the JSON
    file which acts as a cache.

    Parameters
    ---------
    cache_dict: Dictionary to be saved to the disk
    cache_file: File to be used for saving the dictionary

    Returns
    -------
    None

    '''
    dumped_json_cache = json.dumps(cache_dict)
    cache = open(cache_file, 'w')
    cache.write(dumped_json_cache)
    cache.close()

def make_request(url, params):
    cache_key = url + str(params)

    #retrieve the cache file from the CACHE_MAP.
    cache_file = CACHE_MAP.get(url)
    if cache_file is None:
        raise Exception('Cache is not found for URL: ' + url)

    cache_dict = open_cache(cache_file)
    if cache_key in cache_dict.keys():
        print('Entry found in cache. Returning cached response....')
        return cache_dict.get(cache_key)
    else:
        print('Entry is not found in cache. Calling url ' + url + ' with params ' + str(params))

    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    response = requests.get(url, headers=headers, params=params)

    #Save the response to the cache.
    cache_dict[cache_key] = response.json()
    save_cache(cache_dict, cache_file)

    return response.json()

def search_businesses_by_location(business_name, location):
    params = {
        'term': business_name.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': 10
    }

    url = ENDPOINT + SEARCH_PATH
    return make_request(url, params)

if __name__ == "__main__":
    print("Searching Yelp for Starbucks in Seattle: ")
    print(json.dumps(search_businesses_by_location("starbucks", "Seattle"), indent=2))
    print("Searching Yelp for Starbucks in Ann Arbor: ")
    print(json.dumps(search_businesses_by_location("starbucks", "AnnArbor"), indent=2))
    print("Searching Yelp again for Starbucks in Seattle: ")
    print(json.dumps(search_businesses_by_location("starbucks", "Seattle"), indent=2))