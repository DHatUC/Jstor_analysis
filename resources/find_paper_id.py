import os
import json

with open(os.path.join(os.getcwd(), 'metadata', 'countries.json')) as f:
    data = json.load(f)
ids = [k for k, v in data.items() if 'countries' in v and 'Kenya'in v['countries']]
print(ids[:10])