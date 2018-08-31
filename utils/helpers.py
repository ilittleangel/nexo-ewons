import requests
import csv, io, json
from datetime import datetime


def counter(init_val=0, step=1):
    counter_val = init_val
    while True:
        counter_val += step
        yield counter_val


def filter_bad_requests(nodes):
    good_nodes = []
    for node in nodes:
        try:
            if requests.get(node).status_code == 200:
                good_nodes.append(node)
        except requests.exceptions.ConnectionError:
            pass
    return good_nodes


def csv_to_dict(str_csv):
    d = {}
    lst = list(csv.DictReader(io.StringIO(str_csv), delimiter=';'))
    for elem in json.loads(json.dumps(lst)):
        d[f"{elem['TagName']}"] = elem['Value']
    return d


def filter_keys_on_doc(doc: dict, fields: list):
    return {key: doc[key] for key in fields}


def prepare(doc):
    doc['@timestamp'] = datetime.now().isoformat()
    return doc
