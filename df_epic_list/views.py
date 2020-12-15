import json
import urllib
from urllib import parse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

global api_key
global server
global characterId
api_key = 'IY60cbg7tdVOOcWifeQBnp5PPHXFjbl1'
server_name = 'cain'


class EpicList(APIView):

    # def user_info(self, request):
    #     new_data = {}
    #     characterId = []
    #
    #     # 페이지에서 닉네임 입력 받는 값
    #     character_name = ['wide_mecanic', 'wide_seraph']
    #
    #     for i in character_name:
    #
    #         url = 'https://api.neople.co.kr/df/servers/' + server_name + '/characters?characterName=' + i + \
    #               '&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=' + api_key
    #
    #         request = urllib.request.Request(url)
    #         response = urllib.request.urlopen(request)
    #
    #         read_data = response.read()
    #         encoding = response.info().get_content_charset('utf8')
    #         character_data = json.loads(read_data.decode(encoding))
    #
    #         for i in character_data['rows']:
    #             new_data = i
    #             value = new_data['characterId']
    #
    #         characterId.append(value)
    #         return characterId

    def get(self, request):

        new_data = {}
        characterId = []
        quantity = []

        # 페이지에서 닉네임 입력 받는 값
        character_names = ['패호거너', 'wide_mecanic']

        for character_name in character_names:

            url = 'https://api.neople.co.kr/df/servers/' + server_name + '/characters?characterName=' + parse.quote(character_name) + \
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
            print('characterId: \n', characterId)

        for i in characterId:

            url = 'https://api.neople.co.kr/df/servers/'+server_name+'/characters/'+i+'/timeline?' \
                  'limit=<limit>&code=513&apikey='+api_key

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            timeline_list = json.loads(read_data.decode(encoding))
            print('timeline_list:  \n', timeline_list['timeline'])
            print()
            print(type(timeline_list))
            timeline_rows = timeline_list['timeline']
            print('timeline_rows: \n', timeline_rows)
            timeline_datas = timeline_rows['rows']
            print('timeline_data: \n', timeline_datas[0])
            for timeline_data in timeline_datas:
                dungeon_item_datas = timeline_data
                test2 = dungeon_item_datas['data']
                if test2['itemRarity'] == '에픽':
                    quantity = character_name, len(test2)
                    print('에픽아이템', character_name, test2)

                else:
                    print('에픽 아이템이 아닙니다.')

        return Response(quantity, status=status.HTTP_200_OK)
