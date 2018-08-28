import requests
from settings import EWON_ROOT, t2maccount, t2mdeveloperid, t2mpassword, t2musername


def login():
    url = f"{EWON_ROOT}/login"
    data = {'t2maccount': t2maccount,
            't2musername': t2musername,
            't2mpassword': t2mpassword,
            't2mdeveloperid': t2mdeveloperid}
    return requests.post(url=url, data=data).json()


def getaccountinfo(session=""):
    url = f"{EWON_ROOT}/getaccountinfo"
    if session:
        data = {'t2mdeveloperid': t2mdeveloperid,
                't2msession': session}
        return requests.post(url=url, data=data)
    else:
        data = {'t2maccount': t2maccount,
                't2musername': t2musername,
                't2mpassword': t2mpassword,
                't2mdeveloperid': t2mdeveloperid}
        return requests.post(url=url, data=data)


def getewons(pool_id, session=""):
    url = f"{EWON_ROOT}/getewons"
    if session:
        data = {'t2mdeveloperid': t2mdeveloperid,
                't2msession': session,
                'pool': [pool_id]}
        return requests.post(url=url, data=data)
    else:
        data = {'t2maccount': t2maccount,
                't2musername': t2musername,
                't2mpassword': t2mpassword,
                't2mdeveloperid': t2mdeveloperid,
                'pool_id': [pool_id]}
        return requests.post(url=url, data=data)


def gettags(name, session=''):
    # rcgi.bin/ParamForm
    # url = f"{EWON_ROOT}/get/{name}/rcgi.bin/ParamForm"
    url = f"{EWON_ROOT}/get/{name}"
    if session:
        data = {'t2mdeveloperid': t2mdeveloperid,
                't2msession': session}
        return requests.post(url=url, data=data)
    else:
        data = {'t2maccount': t2maccount,
                't2musername': t2musername,
                't2mpassword': t2mpassword,
                't2mdeveloperid': t2mdeveloperid}
        return requests.post(url=url, data=data)
