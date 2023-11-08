"""Settings for the app.
"""

END_POINT = 'https://us-west-2.aws.data.mongodb-api.com/app/'
END_POINT += 'data-whziv/endpoint/data/v1/action'
API_KEY = 'FIXME- MONGO DB YOUR API KEY HERE'
DATA_SOURCE = 'Cluster0'
DB_NAME = 'recipe'
COLLECTION = 'spanish'
HEADERS = {'Content-Type': 'application/json',
           'Access-Control-Request-Headers': '*',
           'api-key': f'{API_KEY}'}

PAYLOAD = {
    "collection": COLLECTION,
    "database": DB_NAME,
    "dataSource": DATA_SOURCE
}
