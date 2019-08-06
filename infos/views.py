from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'infos/case1/index.html')


def count_data(request):
    import json
    import os
    # 读取静态文件配置文件
    module_dir = os.path.dirname(__file__)  # 获取当前目录
    path_file = os.path.join(module_dir, 'static', 'infos', 'case1', 'data', 'count-data.json')
    with open(path_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # data = dict()
    # data['listed_companies_total'] = 45465
    return JsonResponse(data)


if __name__ == "__main__":
    count_data(None)