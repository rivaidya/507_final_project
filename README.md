##Dependent packages which need to be installed:

1. Pandas
2. json
3. Requests
4. Flask
5. flask_wtf
6. Matplotlib

##Project Structure:
FinalProject
    - data_processing
        - business_data_processor : Responsible for processing data from the JSON file
        - yelp_api_data_processor : Responseible for processing the data from Yelp business search API
        - uelp_review_processor : Responsible for processing the data from Yelp Review API
        - data 
            - yelp_academic_dataset_business.json : The JSON dataset which contains business information. 
    - database
        - database_accessor : Contains class for accessing database (create, select, insert functions for ease of use in the code)
        - database_populator : Contains functionality for using the business_data_processor to process the data from the JSON file and populate the data base with the records
        - YelpDatabase.sqlite : The database containing the records. 
    - graphs
        - plotter : Contains functionality for plotting pie chart and bar graphs and saving the images to the disk so that they can be rendered by the flask applciation. 
    - static 
        - css
            - index.css : CSS for index.html
            - query.css : CSS for all other files. 
        - img : images of graphs and charts which are created in real time by plotter.py based on the query
    - templates
        - error.html : jinja template for error page
        - index.html : template for landing page
        - query.html : template for the query page
        - result.html : template for the result page
    - yelp
        - secrets : Contains the private key of the application
        - *.json : cache files for caching responses of the APIs. (3 cache files - 1 for each API)
        - yelp_api : Functionality to call Yelp Fusion APIs over HTTP. Responsible for authentication as well. 
- Application : Flask Application. This is the starting point into the web application online part. 
- QueryForm : The query form used by the Application which allows users to insert text in text boxes. 
- README : This file. Hope you find it useful

##Secrets:
You need to create your own private key by registering as a developer at https://www.yelp.com/developers and then creating an application. Copy the private key for the application to yelp/secrets.py . Ensure that your application has access to the Yelp Fusion APIs. 

##Running the application
The application can be run from the root folder by executing the following command:
`python3 Application.py`



##Interactions
The interaction begins on the landing page (application is hosted on address:port 127.0.0.1:5000). The landing page contains a “Get Started” link which directs the user to Page 2. This is the Query page and allows the user to enter the search text for category and location and then submit the page. The user is expected to select “Search by Zip Code” if the location is a zip code (eg: 88001 instead of Phoenix). When the user clicks on “Submit”, the request is processed. If the request is processed without any errors, the user is directed to the Result page which contains the information about the search term and the various other businesses in the area. If an exception is encountered during processing of the request, the Error page is shown instead of the Result page. From any of the pages, the user can redirect back to the landing page in order to begin all over again. 


