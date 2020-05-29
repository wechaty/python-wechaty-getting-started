# -*- coding: utf-8 -*-
import json
import time
import sys
import requests
import random
import string
from hashlib import md5

App_ID = "replace your tencent ai plat appid"
App_Key = "replace your tencent ai plat appkey"

if sys.version_info.major == 2:
    from urllib import urlencode
    from urllib import quote
else:
    from urllib.parse import urlencode
    from urllib.parse import quote


class AiTencentBase(object):
    """
        腾讯ai SDK
    """

    def __init__(self, appId, appKey):
        """
            初始化AiTencentBase(appId, apiKey)
        """
        self._appId = appId.strip()
        self._appKey = appKey.strip()
        self.__version = '1_0_0'

    def getVersion(self):
        """
            version
        """
        return self.__version

    def _getReqSign(self, params):
        appkey = self._appKey
        params = self._proccessParams(params)
        if not isinstance(params, dict):
            return {"ret": -1, "msg": '参数不正确'}
        data = dict(sorted(params.items(), key=lambda item: item[0]))
        strparams = urlencode(data)
        strparams += '&app_key=' + quote(appkey)
        m = md5()
        m.update(strparams.encode("utf8"))
        sign = m.hexdigest().upper()
        return sign

    def _doHttpPost(self, params, url):
        data = params
        sign = self._getReqSign(params)
        data['sign'] = sign
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            r = requests.post(url=url, headers=header, data=data)
            obj = self._proccessResult(r.content)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'ret': '-1000',
                'msg': 'connection or read data timeout',
            }

        return obj

    def _proccessResult(self, content):
        """
            返回结果格式化处理
        """
        if sys.version_info.major == 2:
            return json.loads(content) or {}
        else:
            return json.loads(content.decode()) or {}

    def _proccessParams(self, params):
        """
            参数处理，所有接口公共参数
        """
        params['app_id'] = self._appId
        params['time_stamp'] = int(time.time())  # 秒级时间戳
        params['nonce_str'] = ''.join(random.choice(
            string.ascii_letters) for x in range(12))  # 12位随机字符串最多支持32位字符长度

        return params


aiClient = AiTencentBase(App_ID, App_Key)


def TencentAI(msg: str):
    session = str(random.random())[2:9]
    params = {'session': session, 'question': msg}

    url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

    result = aiClient._doHttpPost(params, url)
    if not result.get('ret') and result.get('msg') == 'ok':
        data = result.get('data')
        if session == data.get('session'):
            return data.get('answer')
