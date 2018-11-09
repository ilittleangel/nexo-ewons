import elasticsearch.exceptions
import logging
import requests
from datetime import datetime
from elasticsearch import Elasticsearch, ElasticsearchException, TransportError
from requests.auth import HTTPBasicAuth

from settings import INDEX_NAME
from utils.helpers import filter_bad_requests


logger = logging.getLogger('pipeline')


def is_indexed(res):
    status = res['_shards']['failed']
    if status == 0:
        return True
    else:
        logger.error(f"Conflic response: {res}")
        return False


def create_connection(esnodes):
    nodes = filter_bad_requests(esnodes)
    if nodes:
        es = Elasticsearch(esnodes)
        health = es.cluster.health()
        return es, health['status']
    else:
        logger.error(f"Unable to connect Elasticsearch")


def index(doc, doc_type_mode, user, password, esnodes):
    index_name = f"{INDEX_NAME}-{datetime.today().strftime('%Y%m%d')}"
    if user and password:
        # health
        try:
            url = f"{esnodes[0]}/_cluster/health"
            rq = requests.get(url=url, auth=HTTPBasicAuth(user, password))
            rq.raise_for_status()
            health = rq.json()['status']
            logger.info(f"Status Health of [{esnodes[0]}]: {health}")
        except requests.exceptions.RequestException as re:
            logger.error(f"Health failure on {esnodes}: http_status={rq.status_code}: {re}")
            return False

        # index
        try:
            url = f"{esnodes[0]}/{index_name}/{doc_type_mode}"
            rq = requests.post(url=url, auth=HTTPBasicAuth(user, password), json=doc)
            rq.raise_for_status()
            res = rq.json()
            logger.debug(f"Tags indexed successfully: {res}")
            return is_indexed(res)
        except requests.exceptions.RequestException as re:
            logger.error(f"Index failure on {esnodes}: http_status={rq.status_code}: {re}")

    else:
        try:
            es, health = create_connection(esnodes)
            logger.info(f"Status Health of [{esnodes}]: {health}")
            res = es.index(index=index_name, doc_type=doc_type_mode, body=doc)
            logger.debug(f"Tags indexed successfully: {res}")
            return is_indexed(res)
        except TransportError as te:
            logger.error(f"Failure to index: {te}")
        except ElasticsearchException as ee:
            logger.error(f"Something wrong with Elasticsearch: {ee}")


def get_newest_index(es):
    """Returns the last indice of elasticsearch
    for perform a search just in one indice"""
    try:
        indices = sorted(es.indices.get_alias(f"{INDEX_NAME}*"),
                         key=lambda x: datetime.strptime(x[-8:], '%Y%m%d'),
                         reverse=True)

        logger.debug(f"Indices found: {len(indices)}")
        logger.debug(f"Last index: {indices[0]}")
        return indices[0]

    except elasticsearch.exceptions.NotFoundError as nfe:
        logger.error(f"Index Not: {nfe}")
