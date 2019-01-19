import elasticsearch.exceptions
import logging
import requests
from datetime import datetime
from elasticsearch import Elasticsearch, ElasticsearchException, TransportError
from requests.auth import HTTPBasicAuth

from settings import INDEX_NAME
from settings import ESNODES, USER, PASS, ENABLE_INDEX
from settings import ESNODES_cloud, USER_cloud, PASS_cloud, ENABLE_INDEX_cloud
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


def _health(user, password, esnodes):
    url = f"{esnodes[0]}/_cluster/health"
    rq = requests.get(url=url, auth=HTTPBasicAuth(user, password))
    rq.raise_for_status()
    health = rq.json()['status']
    logger.info(f"Status Health of [{esnodes[0]}]: {health}")
    return health


def _index(doc, doc_type_mode, user, password, esnodes):
    index_name = f"{INDEX_NAME}-{datetime.today().strftime('%Y%m%d')}"
    if user and password:
        try:
            _health(user, password, esnodes)
            url = f"{esnodes[0]}/{index_name}/{doc_type_mode}"
            rq = requests.post(url=url, auth=HTTPBasicAuth(user, password), json=doc)
            rq.raise_for_status()
            res = rq.json()
            logger.debug(f"Tags indexed successfully: {res}")
            return res
        except requests.exceptions.RequestException as re:
            logger.error(f"Index failure on {esnodes}: {re}")

    else:
        try:
            es, health = create_connection(esnodes)
            logger.info(f"Status Health of [{esnodes}]: {health}")
            res = es.index(index=index_name, doc_type=doc_type_mode, body=doc)
            logger.debug(f"Tags indexed successfully: {res}")
            return res
        except TransportError as te:
            logger.error(f"Failure to index: {te}")
        except ElasticsearchException as ee:
            logger.error(f"Something wrong with Elasticsearch: {ee}")


def index(doc):
    results = []

    if ENABLE_INDEX:
        res = _index(doc, "tags", USER, PASS, ESNODES)
        logger.info(f"Indexing on {ESNODES}: {res}")
        results.append(("on-premise", is_indexed(res)))

    if ENABLE_INDEX_cloud:
        res_cloud = _index(doc, "tags", USER_cloud, PASS_cloud, ESNODES_cloud)
        logger.info(f"Indexing on {ESNODES_cloud}: {res_cloud}")
        results.append(("cloud", is_indexed(res_cloud)))

    return results


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
