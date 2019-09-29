import datetime
import json
import random
import threading

from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, reverse
from django.views.decorators.csrf import csrf_protect

# 日志工具包
from demo.loger.Logger import Logger
# 百度富文本编辑器
from .forms import forms
from .models import InfosConfig

online_sum = 0
logger = Logger("DEBUG", use_console=True, log_path='logs')
# Create your views here.


@csrf_protect
def default(request):
    return HttpResponseRedirect(reverse("infos:index"))


@csrf_protect
def index(request):
    datas = InfosConfig.objects.filter(deleted_flag=False)
    sits_config = serializers.serialize("json", datas)
    global false, null, true
    false = null = true = ''
    # result = eval(sits_config)[0]['fields']
    data = eval(sits_config)
    configs = dict()
    for value in data:
        configs[value['fields']['key']] = value['fields']['value']
    configs['year'] = datetime.datetime.now().year
    # print(configs)
    return render(request, 'infos/case1/index.html', context={'site_configs': configs})


# 1,读取统计数据
@csrf_protect
def count_data(request):
    file_name = 'count-data.json'
    result = read_json(file_name)
    data = result['result']
    # # 演示数据;数据为字典
    for k, v in data.items():
        data[k] = random.randint(300, 2000)
    return JsonResponse(data if not result['error'] else {'error': data['error']})


# 读取json文件数据
def read_json(file_name):
    import os
    # if request.method == 'GET':
    #     return redirect(reverse('infos:index'))

    # 读取静态文件配置文件
    module_dir = os.path.dirname(__file__)  # 获取当前目录
    path_file = os.path.join(module_dir, 'static', 'infos', 'case1', 'data', file_name)
    if not os.path.isfile(path_file):
        return {'error': 1, 'msg': '文件不存在!', 'result': None}
    with open(path_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {'error': 0, 'msg': '获取数据成功!', 'result': data}


# 2,获取排名数据
@csrf_protect
def rank_data(request):
    file_name = 'ranking-list.json'
    data = read_json(file_name)
    # 演示数据
    for i in range(len(data['result'])):
        data['result'][i]['market_capitalization'] = random.randint(300, 2000)
    # print(data['result'])
    return HttpResponse(json.dumps(data['result']) if not data['error'] else json.dumps({'msg': '获取数据失败!', 'error': 3}))


# 3,获取患者区域分布数据
@csrf_protect
def region_data(request):
    file_name = 'regions.json'
    data = read_json(file_name)
    # 演示数据
    for i in range(len(data['result'])):
        data['result'][i]['count'] = random.randint(55, 200)
    # print(data)
    return HttpResponse(json.dumps(data['result']) if not data['error'] else json.dumps({'msg': '获取数据失败!', 'error': 4}))


# 4, 获取CSRC行业分类数据获取
@csrf_protect
def csrc_data(request):
    file_name = 'csrc-industry.json'
    data = read_json(file_name)
    # 演示数据
    for i in range(len(data['result'])):
        data['result'][i]['stock'] = random.randint(55, 200)
    # print(data)
    return HttpResponse(json.dumps(data['result']) if not data['error'] else json.dumps({'msg': '获取数据失败!', 'error': 4}))


# 5,获取每月数据信息
@csrf_protect
def month_data(request):
    file_name = 'month-count.json'
    data = read_json(file_name)
    # 演示数据
    for i in range(len(data['result'])):
        data['result'][i]['sh_market_capitalization'] = random.randint(585, 20000)
        data['result'][i]['sh_transaction_amount'] = random.randint(955, 2900)
        data['result'][i]['sh_pe_ratio'] = random.randint(955, 2900)
        data['result'][i]['sz_market_capitalization'] = random.randint(9155, 12900)
        data['result'][i]['sz_transaction_amount'] = random.randint(9055, 20000)
    # print(data)
    return HttpResponse(json.dumps(data['result']) if not data['error'] else json.dumps({'msg': '获取数据失败!', 'error': 4}))


# 404页面
@csrf_protect
def page_not_found(request, exception):
    response = render_to_response('infos/404.html', {})
    response.status_code = 404
    return response


# 500页面
@csrf_protect
def page_error(request):
    return render(request, 'infos/404.html')


@csrf_protect
def online(request):
    global online_sum
    if online_sum == 0:
        print("查询数据库...")
        try:
            result = read_db()
            if result['error'] == 0:
                sum_online = result['result']
            elif result['error'] == 1:
                sum_online = 0
        except Exception as e:
            print('数据库连接失败...\n报错信息:' + e)
            return render(request, 'infos/case2/index.html', {'sum': 0})
        else:
            online_sum = sum_online
    else:
        sum_online = online_sum
    return render(request, 'infos/case2/index.html', {'sum': sum_online})


@csrf_protect
def online_data(request):
    t = datetime.datetime.now().second + random.randint(0, 10)
    global online_sum
    if t % 10 == 0:
        try:
            result = read_db()
            if result['error'] == 0:
                sum_online = result['result']
            elif result['error'] == 1:
                sum_online = 0
        except Exception as e:
            print('数据库连接失败...\n报错信息:' + str(e))
            # return HttpResponse(json.dumps({'error': 1, 'msg': '数据库断开连接!请联系后台管理员!'}))
        else:
            online_sum = sum_online
            result['sum'] = online_sum
            result['msg'] = '数据库断开连接!请联系后台管理员!'
            print("ajax请求使用全局数据(查询数据库数据):" + str(sum_online) + '&时间秒数t=' + str(t))
        finally:
            return HttpResponse(json.dumps(result))
    else:
        sum_online = online_sum
        # logger.warning("ajax请求使用全局数据(不查询数据库数据):" + str(sum_online)+'&时间秒数t='+str(t))
    data = dict()
    data['sum'] = sum_online
    return HttpResponse(json.dumps(data))


# TODO 继续完善数据库连接失败的情况,如ip或密码不正确以及超时的情况
def read_db():
    global R
    R = threading.Lock()
    R.acquire()
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y%m%d")
    import cx_Oracle
    # t = threading.Timer(2000, conn.cancel)
    ip, port, SID = '192.168.8.235', 1521, "orcl"
    try:
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        conn = cx_Oracle.connect('cdr_zs', 'cdr_zs', dsn_tns)
    except cx_Oracle.DatabaseError as e:
        logger.error(e)
        return {'error': 1, 'msg': '数据库连接错误'}
    except Exception as e:
        logger.error(e)
        # return {'error': -1, 'msg': '未知错误'}
        raise e
    else:
        cur = conn.cursor()
        sql = "select count(*) sum from CDR_ZS.DATA_EXCHANGE_CDR_LOG " \
              "where STORETIME_STOREOBJECT > to_date('{}', 'yyyyMMdd')".format(otherStyleTime)
        cur.execute(sql)
        rows = cur.fetchall()  # 得到所有数据集
        # for row in rows:
        #     print("%s, %s, %s, %s" % (row[0], row[1], row[2], row[3]))
        sum = rows[0][0]
        # print(sum)
        cur.close()
        conn.commit()
        R.release()
        return {'error': 0, 'msg': '处理成功!', 'result': sum}


# home页面
def home(request):
    content_forms = forms.TestForm()
    return render(request, 'infos/home.html', {"forms": content_forms})


if __name__ == "__main__":
    logger = Logger("DEBUG", use_console=True, log_path='logs').warning("调试")
    pass
