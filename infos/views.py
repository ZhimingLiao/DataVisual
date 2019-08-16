import json
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect


# Create your views here.


@csrf_protect
def index(request):
    return render(request, 'infos/case1/index.html')


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
        data['result'][i]['sh_pe_ratio'] = random.randint(15, 24)
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


if __name__ == "__main__":
    file_name = 'count-data.json'
    result = read_json(file_name)['result']
    for k, v in result.items():
        result[k] = random.randint(300, 2000)
    print(result, type(result))
    # print(read_json(file_name)['result'])
