from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from apps.charts.views import PieChartsView, PieChartsView_2, FunnelChartsView, GraphChartsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('PieChart', PieChartsView.as_view(), name='PieCharts'),    # 饼状图
    path('PieChart_2', PieChartsView_2.as_view(), name='PieCharts_2'),  # 饼状图plus，暂未实现
    path('FunnelCharts', FunnelChartsView.as_view(), name='FunnelCharts'),  # 漏斗图
    path('GraphCharts', GraphChartsView.as_view(), name='GraphCharts'), # 关系图
]
