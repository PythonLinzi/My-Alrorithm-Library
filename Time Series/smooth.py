from pyecharts import Line, Overlap


def smooth1(y:list, alpha=0.2, k=3):
    '''一次次指数平滑'''
    return


def smooth2(y:list, alpha=0.2, k=3):
    '''二次指数平滑'''
    return


def smooth3(y:list, alpha=0.2, k=3) -> list:
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
    y_predict = []
    n = len(p1)
    for i in range(n):
        a.append(3 * p1[i] - 3 * p2[i] + p3[i])
        b.append(aa * ((6 - 5 * aa) * p1[i] - 2 * (5 - 4 * aa) * p2[i]
                       + (4 - 3 * aa) * p3[i]) / (2 * (1 - aa) * (1 * aa)))
        c.append(aa * aa * (p1[i] - 2 * p2[i]
                            + p3[i]) / (2 * (1 - aa) * (1 * aa)))
        y_predict.append(int(a[-1] + b[-1] + c[-1]))
    return y_predict[1:]


def plot(x:list, y:list, y_forcast:list):
    line1, line2,  Overlap = Line(), Line(), Overlap()
    line1.add('观测值', x, y, line_color='blue', is_legend_show=True)
    line2.add('预测值', x, y_forcast, line_color='red', is_legend_show=True)
    overlap.add(line1)
    overlap.add(line2)
    overlap.render('result.html')
