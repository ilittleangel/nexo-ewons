import sys
from datetime import datetime
from requests.exceptions import ConnectionError
from elasticsearch import Elasticsearch, ElasticsearchException, TransportError
import elasticsearch.exceptions
import logging
import requests
from requests.auth import HTTPBasicAuth

from utils.helpers import filter_bad_requests
from settings import ESNODES, INDEX_NAME, USER, PASS


logger = logging.getLogger(__name__)


def is_indexed(status):
    return status['_shards']['failed'] == 0


def create_connection():
    try:
        nodes = filter_bad_requests(ESNODES)
        if nodes:
            es = Elasticsearch(ESNODES)
            health = es.cluster.health()
            return es, health['status']
        else:
            logger.error(f"Unable to connect Elasticsearch")
            sys.exit(1)
    except elasticsearch.exceptions.TransportError as te:
        logger.error(f"Unable to connect Elasticsearch: {te}")
        sys.exit(1)
    except ConnectionError as ce:
        logger.error(f"Unable to connect Elasticsearch: {ce}")
        sys.exit(1)


def index(doc, doc_type_mode):
    index_name = f"{INDEX_NAME}-{datetime.today().strftime('%Y%m%d')}"
    if USER and PASS:
        url = f"{ESNODES[0]}/{index_name}/{doc_type_mode}"
        rq = requests.post(url=url, auth=HTTPBasicAuth(USER, PASS), json=doc)
        if rq.status_code == 201:
            res = rq.json()
            logger.debug(f"Tags indexed successfully: {res}")
        else:
            logger.error(f"Failure to index: {te}")
            sys.exit(1)
    else:
        es, _ = create_connection()
        try:
            res = es.index(index=index_name, doc_type=doc_type_mode, body=doc)
        except TransportError as te:
            logger.warning(f"Failure to index: {te}")
            sys.exit(1)
        except ElasticsearchException as ee:
            logger.error(f"Unable to connect Elasticsearch: {ee}")
            sys.exit(1)

    if not is_indexed(res):
        logger.error(f"Conflic response: {res}")
        return False
    else:
        return True


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
        logger.error(f"Index Not found motherfucker: {nfe}")
        sys.exit(1)
