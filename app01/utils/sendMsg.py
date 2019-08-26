import json, urllib
from urllib.parse import urlencode
# # 发送短信
def request2(mobile,num, m="GET"):
    appkey = 'da2a606c21748d1a13094e025a8f190e'
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": mobile,  # 接收短信的手机号码
        "tpl_id": "166771",  # 短信模板ID，请参考个人中心短信模板设置
        "tpl_value": "#code#=%s"%num,
    # 变量名和变量值对。如果你的变量名或者变量值中带有#&amp;=中的任意一个特殊符号，请先分别进行urlencode编码后再传递，&lt;a href=&quot;http://www.juhe.cn/news/index/id/50&quot; target=&quot;_blank&quot;&gt;详细说明&gt;&lt;/a&gt;
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "dtype": "",  # 返回数据的格式,xml或json，默认json
    }
    params = urlencode(params)#序列化为mobile=15038062130&tpl_id=166467&tpl_value=%23code%23%3d431515&key=dabf6ecaebfa9554395dad7dcc6be7c8
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))#发送params为数据在打开url链接地址
    else:
        f = urllib.request.urlopen(url, params)
    content = f.read()#{"reason":"操作成功","result":{"sid":"201906200911371223162juhe6hy","fee":1,"count":1},"error_code":0}
    res = json.loads(content)#json转字典
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            return 'ok'
            # print(res["result"])
        else:
            return "%s:%s" % (res["error_code"], res["reason"])
            # print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        return "request api error"
        # print("request api error")


