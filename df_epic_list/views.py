import urllib

from rest_framework.response import Response
from rest_framework.views import APIView


class DF_open_api_test(APIView):
    def get(self, reqeust):
        servicekey = 'IY60cbg7tdVOOcWifeQBnp5PPHXFjbl1'
        url = 'https://api.neople.co.kr/df/servers/all/characters/wide_swords?apikey=IY60cbg7tdVOOcWifeQBnp5PPHXFjbl1'

        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        print(response)
        rescode = response.getcode()
        return Response(response)
