from django.urls import path

from .views import (
    HistoricalDetail,
    HistoricalGraph,
    HistoryList,
    MainPage,
    RegionDetail,
    RegionHeatMap,
    RegionsList,
)

urlpatterns = [
    path('', MainPage.as_view()),
    path('region/', RegionDetail.as_view(), name='region'),
    path('region/<str:title>/', RegionHeatMap.as_view(), name='heat'),
    path('history/', HistoricalDetail.as_view(), name='history'),
    path('history/<str:title>/', HistoricalGraph.as_view(), name='historical'),
    path('region-list/', RegionsList.as_view(), name='region-list'),
    path('history-list/', HistoryList.as_view(), name='history-list'),
]