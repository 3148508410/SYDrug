from django.shortcuts import render
from django.views.generic import View
from apps.goods.models import GoodsSKU
from pyecharts import options as opts
from pyecharts.charts import Pie,Funnel,Graph

# select name,sales from goods_sku
results = GoodsSKU.objects.values('name', 'sales')
# save data to two lists
goods_list = []  # goods name lists
sales_list = []  # goods sales lists
# append
for result in results:
    goods_list.append(result['name'])
    sales_list.append(result['sales'])


class PieChartsView(View):
    """data for pyecharts"""
    def get(self, request):
        data = [(goods_list[i], sales_list[i]) for i in range(len(goods_list))]

        # 创建饼状图示例
        pie_chart = Pie()

        # 配置饼状图参数
        pie_chart.set_global_opts(
            title_opts=opts.TitleOpts(title="商品销量饼状图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="80%"),
        )

        # 添加饼状图数据
        pie_chart.add(
        "",
        data_pair=data,
        radius=["40%", "60%"],
        center=["30%", "50%"],
        label_opts=opts.LabelOpts(
        position="outside",
        formatter="{b}: {c} ({d}%)"
         ),
        )

        # 显示饼状图
        pie_chart.render('/home/chenglong/SYDrug/templates/PieChart.html')
        return render(request, 'PieChart.html')

    def post(self, request):    
        for row in results:
            goods_lists.append(row[0])
            sales_lists.append(row[1])

        return render(request, 'PieChart.html')

class PieChartsView_2(View):
    def get(self, request):
        # append
        for result in results:
            goods_list.append(result['name'])
            sales_list.append(result['sales'])
        data = [(goods_list[i], sales_list[i]) for i in range(len(goods_list))]
        # 创建饼状图示例
        pie_chart = Pie()

        # 配置饼状图参数
        pie_chart.set_global_opts(
            title_opts=opts.TitleOpts(title="商品销量饼状图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="80%"),
            # tooltip参数配置
            tooltip_opts=opts.TooltipOpts(trigger='item', formatter='{b}: {c} ({d}%)'),
            # 工具栏配置
            toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical',
                                          pos_top='25%', pos_bottom='5%'),
            feature={
                'dataView': opts.ToolBoxFeatureOpts(title='数据查看'),
                'saveAsImage': opts.ToolBoxFeatureOpts(title='保存为图片'),
                'magicType': opts.ToolBoxFeatureOpts(title='类型切换', option={'type': ['pie', 'funnel']}),
                'restore': opts.ToolBoxFeatureOpts(title='重置')
            })

        # 添加饼状图数据
        pie_chart.add(
            "",
            data_pair=data,
            radius=["40%", "60%"],
            center=["30%", "50%"],
            label_opts=opts.LabelOpts(position="outside", formatter="{b}: {c} ({d}%)"),
            # 饼图系列参数配置
            series_opts=opts.SeriesOpts(
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{b}: {c} ({d}%) {d|{d}%}",
                    rich={
                        'd': {'fontSize': 12, 'color': '#333'}
                    }
                )
            )
        )

        # 显示饼状图
        pie_chart.render('/home/chenglong/SYDrug/templates/PieChart.html')

class FunnelChartsView(View):

    def get(self, request):
        # 漏斗图代码
        funnel_chart = (
            Funnel(
                init_opts=opts.InitOpts(
                    width="1000px",
                    height="550px",
                    page_title="Sales Analysis",
                    # renderer='canvas'
                )
            )
            .add(
                "商品销售流程",
                [list(z) for z in zip(goods_list, sales_list)],
                sort_='none',
                gap=0,
                label_opts=opts.LabelOpts(
                    is_show=True,   # 图表显示文字
                    position='right',# 标签的位置
                    formatter="{b}：{c}",
                    font_style="normal",
                    font_size=12,
                ),
                itemstyle_opts=opts.ItemStyleOpts(
                    border_color="#fff",
                    border_width=1,
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    formatter="{b}：<br />销量：{c}"
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="商品实时销量图",
                    pos_left='center',
                    pos_bottom='20',
                    padding=[25, 0],
                ),
                legend_opts=opts.LegendOpts(
                    orient='vertical',
                    # pos_top="8%",
                    pos_top='bottom',
                    pos_left="1%",
                    item_width=35,  # 图例宽度
                    item_height=20, # 图例高度
                    item_gap=15,
                    textstyle_opts=opts.TextStyleOpts(
                        color='#293c55',    # 图例文字颜色
                        font_size=12,
                    )
                ),
                toolbox_opts=opts.ToolboxOpts(
                    is_show=True,
                    orient='horizontal',
                    pos_left='right',
                    pos_top='8%',
                    feature={
                        "saveAsImage": {
                            "title": "保存为图片",
                            "type": "png",
                        },
                        "restore": {
                            "title": '还原',
                        },
                        "dataView": {"title": "数据视图", "readOnly": False},
                    },
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    trigger='item',
                    formatter="{b}：<br />销量：{c}",
                    axis_pointer_type = "cross",
                ),
            )
        )
        
        funnel_chart.render("/home/chenglong/SYDrug/templates/FunnelChart.html")
        return render(request, 'FunnelChart.html')
class GraphChartsView(View):
    def get(self, request):
        nodes = []
        links = []
        for i in range(len(goods_list)):
            nodes.append({
                "name": goods_list[i],
                "symbolSize": int(sales_list[i]/10)
            })
            links.append({
                "source": goods_list[i],
                "target": str(sales_list[i])
            })

        graph = (Graph()
                 .add("", nodes, links,
                      repulsion=1000,
                      is_roam=True)
                 .set_global_opts(title_opts=opts.TitleOpts(title="商品名称与销量关系图"))
                 .render("/home/chenglong/SYDrug/templates/GraphChart.html"))
        return render(request, 'GraphChart.html')
