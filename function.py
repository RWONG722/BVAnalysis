import random
from urllib.parse import urlparse, urlunparse
import requests
import wbi
import json

def get_bilibili_cookies(SESSDATA=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    try:
        response = requests.get('https://www.bilibili.com', headers=headers)
        response.raise_for_status()
        if SESSDATA is None:
            return response.cookies
        else:
            response.cookies.set('SESSDATA', SESSDATA)
            return response.cookies
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def MyRequest(APIurl, params, cookies):    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'application/json',
    }
    
    APIurl += '?' + wbi.getURL(params)
    try:
        response = requests.get(APIurl, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def checkLoginStatus(cookies):
    APIurl = 'https://api.bilibili.com/x/web-interface/nav'
    params = {}
    return MyRequest(APIurl, params, cookies)

def getSessionData():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data.get('SESSDATA')
    except:
        return None
    
def Search(keyword, page=1):
    cookies = get_bilibili_cookies(getSessionData())
    APIurl = 'https://api.bilibili.com/x/web-interface/wbi/search/all/v2'
    params = {
        'keyword': keyword,
        'page': page,
    }
    return MyRequest(APIurl, params, cookies)

def getCid(BV, cookies):
    APIurl = 'https://api.bilibili.com/x/player/pagelist'
    params = {
        'bvid': BV,
    }
    return MyRequest(APIurl, params, cookies)

def CalOR(a,b): #OR运算 二进制属性位 
    return a|b

def getVideoInfo(BV, CID, cookies):
    APIurl = 'https://api.bilibili.com/x/player/playurl'
    params = {
        'bvid': BV,
        'cid': CID,
        'qn': 120,
        'otype': 'json',
        'platform': 'html5',
        'high_quality': 1,
        'fnval': CalOR(1, 128),
        'fourk': 1
    }
    return MyRequest(APIurl, params, cookies)

def BiliAnalysis(BV,p=1):
    cookies = get_bilibili_cookies(getSessionData())

    CID = getCid(BV, cookies)

    p-=1
    if p<0 or p>=len(CID['data']):
        p=0

    VideoInfo = getVideoInfo(BV, CID['data'][p]['cid'], cookies)

    Video = {
        'BV': BV,
        'page': p+1,
        'url': VideoInfo['data']['durl'][0]['url'],
    }
    return Video

def ChangeBiliCDN( url ):
    BiliCDN = [
        "upos-sz-mirrorcos.bilivideo.com",
        "upos-sz-mirrorali.bilivideo.com",
        "upos-sz-mirror08c.bilivideo.com",
    ]
    parsed_url = urlparse(url)
    new_netloc = random.choice(BiliCDN)
    new_url = urlunparse(parsed_url._replace(netloc=new_netloc))
    return new_url