import logging
import json
import utils.m2web_api


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)

    res_info = utils.m2web_api.getaccountinfo()
    if res_info.status_code == 200:

        logging.debug(f"res_info.status_code={res_info.status_code}")
        accountinfo = res_info.json()
        logging.debug(json.dumps(accountinfo, indent=4))

        for pool in accountinfo['pools']:
            id_installation = pool['id']
            res_ewons = utils.m2web_api.getewons(id_installation)
            if res_ewons.status_code == 200:

                logging.debug(f"res_ewons.status_code={res_ewons.status_code}")
                ewons = res_ewons.json()
                logging.debug(json.dumps(ewons, indent=4))

                for ewon in ewons['ewons']:
                    name = ewon['name'] # it could be 'encodedName'
                    res_tag = utils.m2web_api.gettags(name)
                    if res_tag.status_code == 200:
                        tags = res_tag.text
                        logging.debug(tags)

                    else:
                        logging.error(f"Something wrong with `gettags()`: {res_tag}")
            else:
                logging.error(f"Something wrong with `getewons()`: {res_ewons}")
    else:
        logging.error(f"Something wrong with `getaccountinfo()`: {res_info}")


if __name__ == '__main__':
    main()
