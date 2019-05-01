from flask import Flask
from flask_restful import Resource, Api, reqparse
import psycopg2

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class InstitutionName(Resource):
    def get(self):
        return {
            'ataturk': {
                'quote': ['Yurtta sulh, cihanda sulh.', 
                    'Egemenlik verilmez, alınır.', 
                    'Hayatta en hakiki mürşit ilimdir.']
            },
            'linus': {
                'quote': ['Talk is cheap. Show me the code.']
            }
        }

    def post(self):
        parser.add_argument('quote', type=str)
        args = parser.parse_args()

        return {
            'status': True,
            'quote': '{} added. Good'.format(args['quote'])
        }

api.add_resource(InstitutionName, '/')

if __name__ == '__main__':
    app.run(debug=True)

try:
    conn = psycopg2.connect (
        host     = "localhost",
        database  = "degrees",
        user     = "postgres",
        password = "password",
        port     = 5432
    )

    cur = conn.cursor()
    pg_select_instnames_query = 'select * from college.institutionnames'
    cur.execute(pg_select_instnames_query)
    instname_records = cur.fetchall()

    print("\nPrint each row and it's columns' values:\n")
    for row in instname_records:
        print("id= ", row[0])
        print("institutionname", row[1], '\n')

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if(conn):
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")