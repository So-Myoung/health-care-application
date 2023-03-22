import mpld3
import np as np
from Demos.SystemParametersInfo import new_x
from django.shortcuts import render
from .models import Bmi
from math import pi
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource

def bmi(request):
    context = {}
    if request.method == "POST":
        weight_metric = request.POST.get("weight-metric")

        if weight_metric:
            weight = float(request.POST.get("weight-metric"))
            height = float(request.POST.get("height-metric"))

        bmi = (weight/(height**2))
        save = request.POST.get("save")
        if save == "on":
            Bmi.objects.create(user=request.user,weight=weight, height=height, bmi=round(bmi))
        if bmi < 16:
            state = "극심한 저체중"
        elif bmi > 16 and bmi < 17:
            state = "저체중"
        elif bmi > 17 and bmi < 18:
            state = "조금 저체중"
        elif bmi > 18 and bmi < 25:
            state = "정상"
        elif bmi > 25 and bmi < 30:
            state = "과체중"
        elif bmi > 30 and bmi < 35:
            state = "경도 비만"
        elif bmi > 35 and bmi < 40:
            state = "비만"
        elif bmi > 40:
            state = "고도 비만"

        context["bmi"] = round(bmi)
        context["state"] = state

    if request.user.is_authenticated:
        dates = []
        bmis = []
        num = 1
        dates_queryset = Bmi.objects.all().filter(user=request.user)
        for qr in dates_queryset:
            dates.append(str(qr.date) + "(" + str(num) + ")")
            bmis.append(float(qr.bmi))
            num += 1

        plot = figure(x_range=dates, plot_height=600, plot_width=600, title="BMI 통계",
                      toolbar_location="right", tools="pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")
        plot.title.text_font_size = "20pt"

        plot.xaxis.major_label_text_font_size = "14pt"

        # add a step renderer
        plot.line(dates, bmis, line_width=2)
        plot.legend.lable_text_font_size = '14pt'

        plot.xaxis.major_label_orientation = pi / 4
        script, div = components(plot)

        context["script"] = script
        context["div"] = div

    return render(request, "bmi2.html", context)


def bmi2(request):
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.metrics import r2_score
    y = [26, 27.3, 27.5, 27.2, 27.3, 25.6, 28]
    x = [1, 2, 3, 4, 5, 6, 7]

    plt.scatter(x, y, color='r', s=20)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    fit_line = np.polyfit(x, y, 1)  # input 의미 : x축 데이터, y축 데이터, 1차원

    print(fit_line)

    x_minmax = np.array([min(x), max(x)])  # x축 최소값, 최대값

    fit_y = x_minmax * fit_line[0] + fit_line[1]  # x축 최소, 최대값을 회귀식에 대입한 값

    plt.scatter(x, y, color='r', s=20)
    plt.plot(x_minmax, fit_y, color='orange')  # 회귀선 그래프 그리기
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    est_y = np.array(x) * fit_line[0] + fit_line[1]  # x의 실제 값들을 회귀식에 대입한 y 추정치

    r2 = r2_score(y, est_y)

    plt.scatter(x, y, color='r', s=20)
    plt.plot(new_x, fit_y, color='orange')  # 회귀선 그래프 그리기
    plt.text(5, 7, '$R^2$ = %.4f' % r2, size=12)  # (5, 7)의 위치에 크기 12로 R값 새김
    plt.text(4.8, 6, 'y = %.4fx + %d' % (fit_line[0], fit_line[1]), size=12)  # (4.8, 6)위치에 추세선 식 표현
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    mpld3.show()
    return render(request, "bmi3.html")
