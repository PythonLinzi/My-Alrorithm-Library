import xlrd
import numpy as np


def smooth3(y:np.ndarray, alpha=0.2, k=3):
    '''三次指数平滑法'''
    aa, n = alpha, len(y)
    p1, p2, p3 = [sum(y[0:k]) / k], [sum(y[0:k]) / k], [sum(y[0:k]) / k]
    for i, x in enumerate(y):
        tmp = p1[-1]
        p1.append(aa * x + (1 - aa) * tmp)
        tmp = p2[-1]
        p2.append(aa * p1[-1] + (1 - aa) * tmp)
        tmp = p3[-1]
        p3.append(aa * p2[-1] + (1 - aa) * tmp)
    a, b, c = [], [], []
    y_predict, n = [], len(p1)
    for i in range(n):
        a.append(3 * p1[i] - 3 * p2[i] + p3[i])
        b.append(aa * ((6 - 5 * aa) * p1[i] - 2 * (5 - 4 * aa) * p2[i]
                       + (4 - 3 * aa) * p3[i]) / (2 * (1 - aa) * (1 * aa)))
        c.append(aa * aa * (p1[i] - 2 * p2[i]
                            + p3[i]) / (2 * (1 - aa) * (1 * aa)))
        y_predict.append(int(a[-1] + b[-1] + c[-1]))
    y_predict = np.array(y_predict)
    err = np.sqrt(sum((y[4:] - y_predict[4:n - 1]) ** 2) / (n - 1)) / np.mean(y[4:])
    a, b, c = np.array(a), np.array(b), np.array(c)
    return y_predict, a, b, c, err


def forecast(data:np.ndarray, alpha=0.2, k=3, num=5):
    ''' 预测接下来的 num 期 '''
    y, a, b, c, err = smooth3(y=data, alpha=alpha, k=k)
    print(len(data), len(y))
    print("误差变异系数Cv为 %.2f" % (err))
    a, b, c = a[-1], b[-1], c[-1]
    for i in range(2, num + 1):
        nxt_y = a + b * i + c * i ** 2
        y = np.append(y, nxt_y)
    return y


def read_excel(file: str):
    wb = xlrd.open_workbook(filename=file)
    sheet = wb.sheet_by_index(0)
    idx = sheet.col_values(0)[1:77]
    time = sheet.col_values(1)[1:77]
    sale = sheet.col_values(2)[1:77]
    return idx, time, sale

idx, time, sale = read_excel("example data.xls")
newy = forecast(data=sale, alpha=0.886)


import pyecharts.options as opts
from pyecharts.charts import Line
def line_plot(t, y1, y2) -> Line:
    line = (
        Line()
        .add_xaxis(xaxis_data=t)
        .add_yaxis("观测", y_axis=y1)
        .add_yaxis("预测", y_axis=y2)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="观测-预测"),
            xaxis_opts=opts.AxisOpts(name="Time", is_scale=False),
            yaxis_opts=opts.AxisOpts(name="Sale", is_scale=False),
        )
            .set_series_opts(
            #areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False), # 是否显示每个点的数值
        )
    )
    return line


line_plot(time, sale[4:], newy[4:]).render('smooth3.html')
