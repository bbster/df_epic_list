import json
import urllib
from urllib.request import Request

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import now, convert_str_to_datetime

server_name = 'cain'


class EpicList(APIView):
    def convert_start_time(self, datetime_str):
        start_date = convert_str_to_datetime(datetime_str)
        if not start_date:
            return None
        return start_date.strftime('%Y%m%dT0000')

    def convert_end_time(self, datetime):
        return datetime.strftime('%Y%m%dT%H%M')

    def user_info(self, request):
        characterId = []

        # 페이지에서 닉네임 입력 받는 값
        character_name = ['wide_mecanic', 'wide_seraph']

        for i in character_name:
            url = f'https://api.neople.co.kr/df/servers/{server_name}/characters?characterName={i}&jobGrowId=<jobGrowId>&limit=<limit>&wordType=<wordType>&apikey={settings.DF_API_KEY}'

            request = Request(url)
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
        start_date = request.query_params.get('start_date', None)  # 2020-12-01 과 같은 포맷으로 입력

        if not start_date:
            return Response('start_date 파라미터는 필수 입력값입니다.', status=status.HTTP_400_BAD_REQUEST)

        converted_start_date = self.convert_start_time(start_date)

        if not start_date:
            return Response(f'start_date 값 {start_date} 은 datetime 으로 변환할 수 없습니다.', status=status.HTTP_400_BAD_REQUEST)

        converted_end_date = self.convert_end_time(now())

        character_ids = self.user_info(request)
        quantity = []
        epic_quantity = None

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
                    quantity.append(items.values())
                    epic_quantity = len(quantity)
                else:
                    print('에픽 아이템이 아닙니다.')

        print('quantity: ', epic_quantity, type(epic_quantity))

        result = {
            'count': len(quantity),
            'results': quantity
        }

        return Response(result, status=status.HTTP_200_OK)
