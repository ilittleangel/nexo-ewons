import json
import logging

import utils.m2web_api
from utils.elastic import index
from utils.logging import init_logging, close_logging, error
from utils.helpers import csv_to_dict, prepare
from settings import ROOT_DIR


def main():

    res_info = utils.m2web_api.getaccountinfo()
    if res_info.status_code == 200:

        logger.debug(f"res_info.status_code={res_info.status_code}")
        accountinfo = res_info.json()
        logger.debug(json.dumps(accountinfo, indent=4))

        for pool in accountinfo['pools']:
            id_installation = pool['id']
            res_ewons = utils.m2web_api.getewons(id_installation)
            if res_ewons.status_code == 200:

                logger.debug(f"res_ewons.status_code={res_ewons.status_code}")
                ewons = res_ewons.json()
                logger.debug(json.dumps(ewons, indent=4))

                for ewon in ewons['ewons']:
                    name = ewon['name']  # it could be 'encodedName'
                    res_tag = utils.m2web_api.gettags(name)
                    if res_tag.status_code == 200:
                        tags = res_tag.text
                        doc = prepare(csv_to_dict(tags))
                        logger.debug(f"Indexing tags: {doc}")
                        if index(doc=doc, doc_type_mode="tags"):
                            logger.info("Tags ingestion SUCCEDEDD")
                        else:
                            error("Tags ingestion FAILED", logger='pipeline')
                    else:
                        error(f"Something wrong with `gettags()`: {res_tag}", logger='pipeline')
            else:
                error(f"Something wrong with `getewons()`: {res_ewons}", logger='pipeline')
    else:
        error(f"Something wrong with `getaccountinfo()`: {res_info}", logger='pipeline')


if __name__ == '__main__':
    init_logging(f'{ROOT_DIR}/logs/ewons')
    logger = logging.getLogger('pipeline')
    main()
    close_logging()
