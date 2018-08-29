import requests
from settings import EWON_ROOT
from settings import t2maccount, t2mdeveloperid, t2mpassword, t2musername
from settings import t2mdeviceusername, t2mdevicepassword


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
    url = f"{EWON_ROOT}/get/{name}/rcgi.bin/ParamForm"
    if session:
        data = {'t2mdeveloperid': t2mdeveloperid,
                't2msession': session}
        return requests.post(url=url, data=data)
    else:
        data = {'t2maccount': t2maccount,
                't2musername': t2musername,
                't2mpassword': t2mpassword,
                't2mdeveloperid': t2mdeveloperid,
                't2mdeviceusername': t2mdeviceusername,
                't2mdevicepassword': t2mdevicepassword,
                'AST_Param': '$dtIV$ftT'}
        return requests.post(url=url, data=data)
