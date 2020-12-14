import json
import urllib

from rest_framework.response import Response
from rest_framework.views import APIView
from pandas import DataFrame as df

class DF_open_api_test(APIView):
    def get(self, reqeust):
        apikey = 'IY60cbg7tdVOOcWifeQBnp5PPHXFjbl1'
        url = 'https://api.neople.co.kr/df/servers/cain/characters/853db5c4724d616222cfdd923219509e/timeline?' \
              'limit=<limit>&code=505&apikey='+apikey

        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        print(type(response))
        raw_data = response.read()
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(raw_data.decode(encoding))
        print(type(data))
        print(data.len)

        return Response(data)
