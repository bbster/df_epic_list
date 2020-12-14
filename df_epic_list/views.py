import json
import urllib

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

global api_key
global server
global characterId
api_key = 'IY60cbg7tdVOOcWifeQBnp5PPHXFjbl1'
server_name = 'cain'


class EpicList(APIView):

    def user_info(self, request):
        new_data = {}
        characterId = []

        # 페이지에서 닉네임 입력 받는 값
        character_name = ['wide_mecanic', 'wide_seraph']

        for i in character_name:

            url = 'https://api.neople.co.kr/df/servers/' + server_name + '/characters?characterName=' + i + \
                  '&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=' + api_key

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            character_data = json.loads(read_data.decode(encoding))

            for i in character_data['rows']:
                new_data = i
                value = new_data['characterId']

            characterId.append(value)
            return characterId

    def get(self, request):

        for i in self.characterId:

            url = 'https://api.neople.co.kr/df/servers/'+server_name+'/characters/'+characterId+'/timeline?' \
                  'limit=<limit>&code=505&apikey='+api_key

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            print(type(response))
            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            timeline_list = json.loads(read_data.decode(encoding))
            quantity = len(timeline_list) - 1
            print(type(timeline_list))
            print(quantity)

        return Response(data=quantity, status=status.HTTP_200_OK)
