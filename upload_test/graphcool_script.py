"""
Testing the upload of files to a graph.cool serverless backend
Don't forget to provide requests with pip/virtualenv or conda/pip
before running this script
"""
import requests
import sys

file_name = sys.argv[1]
url = 'https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl'

file = {'data': open(file_name, 'rb')}

r = requests.post(url, files=file)
