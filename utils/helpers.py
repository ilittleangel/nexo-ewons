import csv
import io
import json
import requests
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
        d[f"{elem['TagName']}"] = to_number(elem['Value'])
    return d


def filter_keys_on_doc(doc: dict, fields: list):
    return {key: doc[key] for key in fields}


def prepare(doc):
    doc['@timestamp'] = datetime.now().isoformat()
    return doc


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def to_number(string):
    if is_int(string):
        return int(string)
    elif is_float(string):
        return float(string)
    else:
        return string
