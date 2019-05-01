from flask import Flask
from flask_restful import Resource, Api, reqparse
import psycopg2

try:
    conn = psycopg2.connect (
        host     = "localhost",
        database  = "degrees",
        user     = "postgres",
        password = "password",
        port     = 5432
    )

    cur = conn.cursor()

    # the flask application object
    app = Flask(__name__)
    api = Api(app)

    parser = reqparse.RequestParser()
    class DegreeLevel(Resource):
        def get(self):
            pg_select_degreelvls_query = 'select * from college.degreelevels'
            cur.execute(pg_select_degreelvls_query)
            degreelvl_records = cur.fetchall()
            return degreelvl_records

    class Degree(Resource):
        def get(self):
            pg_select_degrees_query = ('select d.year, '
                                              'il.institutionlevel, '
                                              'd.agedesc, '
                                              'd.gender, '
                                              'r.residency, '
                                              'dl.degreelevel, '
                                              'e.ethnicity, '
                                              'pn.programname '
                                        'from college.degrees d '
                                        'join college.degreelevels dl '
                                            'on d.degreelevelid = dl.id '
                                        'join college.ethnicities e '
                                            'on d.ethnicityid = e.id '
                                        'join college.institutionlevels il '
                                            'on d.institutionlevelid = il.id '
                                        'join college.programnames pn '
                                            'on d.programname = pn.id '
                                        'join college.residencies r '
                                            'on d.residencyid = r.id ')
            cur.execute(pg_select_degrees_query)
            degree_records = cur.fetchall()
            return degree_records

        # def post(self):
        #     parser.add_argument('quote', type=str)
        #     args = parser.parse_args()

        #     return {
        #         'status': True,
        #         'quote': '{} added. Good'.format(args['quote'])
        #     }

    class Ethnicity(Resource):
        def get(self):
            pg_select_ethnicities_query = 'select * from college.ethnicities'
            cur.execute(pg_select_ethnicities_query)
            ethnicity_records = cur.fetchall()
            return ethnicity_records
    
    class InstitutionLevel(Resource):
        def get(self):
            pg_select_instlvls_query = 'select * from college.institutionlevels'
            cur.execute(pg_select_instlvls_query)
            instlvls_records = cur.fetchall()
            return instlvls_records
    
    class ProgramName(Resource):
        def get(self):
            pg_select_programnames_query = 'select * from college.programnames'
            cur.execute(pg_select_programnames_query)
            programnames_records = cur.fetchall()
            return programnames_records

    #  setup the api resource routing
    api.add_resource(DegreeLevel, '/degrees/degreelevels')
    api.add_resource(Degree, '/degrees')
    api.add_resource(Ethnicity, '/degrees/ethnicities')
    api.add_resource(InstitutionLevel, '/degrees/institutionlevels')
    api.add_resource(ProgramName, '/degrees/programnames')

    if __name__ == '__main__':
        app.run(debug=True)

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    # close db connection
    if(conn):
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")