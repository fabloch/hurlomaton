"""
Testing the upload of files to a graph.cool serverless backend
Don't forget to provide requests with pip/virtualenv or conda/pip
before running this script
"""
import requests

url = 'https://api.graph.cool/file/v1/cj77htypt0n7g01762fd1hubl'

file = {'data': open('image1.jpg', 'rb')}

r = requests.post(url, files=file)
