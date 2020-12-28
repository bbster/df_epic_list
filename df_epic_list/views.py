import json
import urllib
from urllib.request import Request
from urllib import parse

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import now, convert_str_to_datetime


class EpicList(APIView):
    def convert_start_time(self, datetime_str):
        start_date = convert_str_to_datetime(datetime_str)
        if not start_date:
            return None
        return start_date.strftime('%Y%m%dT0000')

    def convert_end_time(self, datetime):
        return datetime.strftime('%Y%m%dT%H%M')

    def user_info(self, request):
        global server_name
        server_name = 'cain'
        character_id = []

        # 페이지에서 닉네임 입력 받는 값
        character_names = ['wide_mecanic']
        # 다중 input tag를 리스트형태로 받아오는 기능
        # character_names = request.POST.getlist('input name')

        for character_name in character_names:
            url = f'https://api.neople.co.kr/df/servers/{server_name}/characters?characterName={parse.quote(character_name)}&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey={settings.DF_API_KEY}'

            request = Request(url)
            response = urllib.request.urlopen(request)

            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            character_data = json.loads(read_data.decode(encoding))

            for character_row_data in character_data['rows']:

                character_index_data = character_row_data['characterId']

            character_id.append(character_index_data)

        return character_id

    def get(self, request):
        start_date = request.query_params.get('start_date', None)  # 2020-12-01 과 같은 포맷으로 입력

        if not start_date:
            return Response('start_date 파라미터는 필수 입력값입니다.', status=status.HTTP_400_BAD_REQUEST)

        converted_start_date = self.convert_start_time(start_date)

        if not start_date:
            return Response(f'start_date 값 {start_date} 은 datetime 으로 변환할 수 없습니다.', status=status.HTTP_400_BAD_REQUEST)

        converted_end_date = self.convert_end_time(now())

        character_ids = self.user_info(request)

        quantity = []

        items_object = []
        item_image_object = []
        item_rarity_object = []
        item_image_url = 'https://img-api.neople.co.kr/df/items/'

        filter_item_type_weapon = []
        filter_item_type_not_weapon = []

        for character_id in character_ids:
            url = f'https://api.neople.co.kr/df/servers/{server_name}/characters/{character_id}/timeline?startDate={converted_start_date}&endDate={converted_end_date}&code=513&apikey={settings.DF_API_KEY}'

            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            read_data = response.read()
            encoding = response.info().get_content_charset('utf8')
            timeline_list = json.loads(read_data.decode(encoding))

            timeline_rows = timeline_list['timeline']
            timeline_datas = timeline_rows['rows']

            for timeline_data in timeline_datas:
                dungeon_item_datas = timeline_data
                items = dungeon_item_datas['data']

                if items['itemRarity'] == '에픽':
                    items_object.append(items)

                    quantity.append(items.values())

                    item_image_object.append(item_image_url+items['itemId'])

                    item_names = items['itemName']
                    item_rarity_object.append(item_names)

                else:
                    pass

            for filter_item_type in item_rarity_object:
                url = f'https://api.neople.co.kr/df/items?itemName={parse.quote(filter_item_type)}&apikey={settings.DF_API_KEY}'

                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request)

                read_data = response.read()
                encoding = response.info().get_content_charset('utf8')
                filtering_item_data = json.loads(read_data.decode(encoding))
                filtering_item_rows_data = filtering_item_data['rows']

                for filter_item_row_data in filtering_item_rows_data:
                    if filter_item_row_data['itemType'] == '무기':
                        filter_item_type_weapon.append(filter_item_row_data)

                    else:
                        filter_item_type_not_weapon.append(filter_item_row_data)

        result = {
            'count': len(quantity),
            'items_object': items_object,
            'item_image_object': item_image_object,
            'item_wepon_type_object': filter_item_type_weapon,
            'item_not_wepon_type_object': filter_item_type_not_weapon,
        }

        return Response(result, status=status.HTTP_200_OK)
