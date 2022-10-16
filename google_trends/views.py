import ast
import json

from django.core.exceptions import BadRequest
from django.http import Http404
from django.shortcuts import redirect
from pytrends.request import TrendReq
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import historical, interest_per_region
from .serilizers import HistorySerializer, RegionSerializer


class MainPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        return Response()


class RegionHeatMap(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'heat_map.html'


    def get(self, request, title, format=None):
        data = interest_per_region.objects.filter(title=title).values()[0]
        # print(data)
        # print(data["title"])
        heat_data = []
        first_keyword_data = ast.literal_eval(data["first_keyword_data"])
        second_keyword_data = ast.literal_eval(data["second_keyword_data"])
        first_colors = False
        second_color = False
        for i in (ast.literal_eval(data["first_keyword_data"])).keys():
            if int(first_keyword_data[i]) > int(second_keyword_data[i]):
                heat_data.append({
                    "id": i,
                    "value": 1
                })
                first_colors = True
            else:
                heat_data.append({
                    "id": i,
                    "value": 0
                })
                second_color = True
        print(heat_data)
        if first_colors == True and second_color == True:
            first_keyword = data["first_keyword"]
            second_keyword = data["second_keyword"]
        elif first_colors == False:
            first_keyword = data["second_keyword"]
            second_keyword = data["first_keyword"]
        elif second_color == False:
            first_keyword = data["first_keyword"]
            second_keyword = data["second_keyword"]
        
        return Response({"first": first_keyword, "second": second_keyword, "heat_data": json.dumps(heat_data)})


class RegionDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'interest_per_region_detail.html'

    def get(self, request):
        return Response()

    def post(self, request):
        title = request.POST['name']
        first_kw = request.POST['first_kw']
        second_kw = request.POST['second_kw']
        
        my_objects = list(interest_per_region.objects.filter(title=title))
        print(my_objects)
        if len(my_objects) > 0:
            raise Http404("Title aready existed.")
        try:
            pytrend = TrendReq()
            pytrend.build_payload([first_kw, second_kw], timeframe='now 1-d', geo='US')
            df = (pytrend.interest_by_region(inc_geo_code=True)).to_dict()
            first_kw_data = {}
            second_kw_data = {}

            for geo in df["geoCode"].keys():
                first_kw_data[df["geoCode"][geo]] = df[first_kw][geo]
                second_kw_data[df["geoCode"][geo]] = df[second_kw][geo]
            
            data = interest_per_region.objects.create(title=title, first_keyword=first_kw, second_keyword=second_kw, first_keyword_data=first_kw_data, second_keyword_data=second_kw_data)
        except Exception as e:
            print(str(e))
            raise BadRequest('Invalid request.')

        return redirect('heat', title=title)


class HistoricalDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'historical.html'

    def get(self, request):
        return Response()

    def post(self, request):
        title = request.POST['name']
        kw = request.POST['kw']

        my_objects = list(historical.objects.filter(title=title))
        if len(my_objects) > 0:
            raise Http404("Title aready existed.")
        try:
            pytrend = TrendReq()
            df = pytrend.get_historical_interest([kw],
                                        year_start=2022,
                                        month_start=10,
                                        day_start=10,
                                        hour_start=0,

                                        year_end=2022,
                                        month_end=10,
                                        day_end=11,
                                        hour_end=0,

                                        sleep=180).to_dict()

            data = {}
            count = 0
            for i in df[kw].keys():
                data[count] = df[kw][i] 
                count += 1
            
            data = historical.objects.create(title=title, keyword=kw, data=data)
        except Exception as e:
            print(str(e))
            raise BadRequest('Invalid request.')

        return redirect('historical', title=title)


class HistoricalGraph(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'xychart.html'


    def get(self, request, title, format=None):
        data = historical.objects.filter(title=title).values()[0]
        graph_data = []
        for i in data["data"].keys():
            graph_data.append({
                "time": i,
                "value": data["data"][i]
            })
        print(graph_data)
        return Response({"keyword": data["keyword"], "data": json.dumps(graph_data)})


class RegionsList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        data = interest_per_region.objects.all()
        serializer = RegionSerializer(data, many=True)
        print(serializer.data)

        return Response(serializer.data)


class HistoryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        data = historical.objects.all()
        serializer = HistorySerializer(data, many=True)
        print(serializer.data)

        return Response(serializer.data)