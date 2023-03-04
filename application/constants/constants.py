import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../config.json')

f = open(filename)
data = json.load(f)

OPENAI_API_KEY = data['OPENAI_API_KEY']