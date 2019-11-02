import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ast import literal_eval

@api_view(['GET'])
def getapi(request):
    data = {
        'appid': "wx36c1cdf40194e860",
        'secret': "061e1a2c2c4415fb07b1a13ca286e425",
        'js_code': request.GET.get('js_code'),
        'grant_type': "authorization_code"
    }
    re = requests.get('https://api.weixin.qq.com/sns/jscode2session',params=data)
    re_dict = literal_eval(re.text)
    print(re_dict['openid'])
    return Response(re_dict['openid'])

