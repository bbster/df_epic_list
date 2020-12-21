import json
import urllib
from datetime import datetime
from urllib import parse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

global api_key
global server
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
        test = {}

        # 페이지에서 닉네임 입력 받는 값 // type 리스트 형태
        character_names = ['wide_mecanic', 'wide_seraph', 'wide_saint', 'wide_swords', 'wide_prime', 'wide_enchan']
        # character_names = ['광부캐아님', '버프편한세상', '창으로빠따질', '샤이쿠마', '샤이위즈']
        # character_names = ['패호거너', '광휘의수르야', '니들버프안줌', '흑한의찬드라', '은유시아']
        # character_names = ['포니테일녀', '빙교리다요', '세인트다요']

        for character_name in character_names:

            url = 'https://api.neople.co.kr/df/servers/' + server_name + '/characters?characterName=' + parse.quote(character_name) + \
                  '&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey=' + api_key

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            character_data = json.loads(read_data.decode(encoding))

            for character_row_data in character_data['rows']:
                new_data = character_row_data
                value = new_data['characterId']

            characterId.append(value)
            # print('characterId: \n', characterId)

        for character_index in characterId:
            
            url = 'https://api.neople.co.kr/df/servers/'+server_name+'/characters/'+character_index+'/timeline?' \
                  'limit=<limit>&code=513&apikey='+api_key

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            timeline_list = json.loads(read_data.decode(encoding))
            # print('timeline_list:  \n', timeline_list['timeline'])

            # print(type(timeline_list))
            timeline_rows = timeline_list['timeline']
            # print('timeline_rows: \n', timeline_rows)
            timeline_datas = timeline_rows['rows']
            # print('timeline_data: \n', timeline_datas[0])
            for timeline_data in timeline_datas:
                dungeon_item_datas = timeline_data
                items = dungeon_item_datas['data']
                
                if items['itemRarity'] == '에픽':
                    quantity.append(items.values())
                    epic_quantity = len(quantity)

                    # print('에픽아이템', character_name, test2)
                else:
                    print('에픽 아이템이 아닙니다.')

            print('quantity: ', len(epic_quantity), type(epic_quantity))
            print('character_name: ', character_names, '\n', 'quantity: ', test, type(epic_quantity))

        return Response(epic_quantity, status=status.HTTP_200_OK)
