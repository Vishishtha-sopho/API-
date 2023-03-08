from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import numpy as np

app = Flask(__name__)
api = Api(app)

class Books(Resource):
    def get(self):
        data = pd.read_csv('goodreads_library_export.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('title', type=str, required=True)  # add args
        parser.add_argument('author', type=str, required=True)
        parser.add_argument('rating', type=int, required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('goodreads_library_export.csv')

        if args['title'] in list(data['Title']):
            return {
                'message': f"'{args['title']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'Title': [args['title']],
                'Author': [args['author']],
                'My Rating': [args['rating']],
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('goodreads_library_export.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('title', type=str, required=True)  # add args
        parser.add_argument('author', type=str, required=True)
        parser.add_argument('rating', type=int, required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('goodreads_library_export.csv')
        
        if args['title'] in list(data['Title']):
           
            # update book's rating
            data.loc[data['Title'] == args['title'], 'My Rating'] = args['rating']
            
            # save back to CSV
            data.to_csv('goodreads_library_export.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the book does not exist
            return {
                'message': f"'{args['title']}' book not found."
            }, 404
        
    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('title', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('goodreads_library_export.csv')
        
        if args['title'] in list(data['Title']):
            # remove data entry matching given book title
            data = data[data['Title'] != args['title']]
            
            # save back to CSV
            data.to_csv('goodreads_library_export.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because book does not exist
            return {
                'message': f"'{args['title']}' book not found."
            }, 404

api.add_resource(Books, '/mybooks')  # add endpoints

if __name__ == '__main__':
    app.run()  # run our Flask app
