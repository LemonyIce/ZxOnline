import requests
import json

from zxSchool.settings import YP


def send_single_sms(code, mobile):
    """
    短信发送和返回
    :param code: 验证码
    :param mobile: 电话号码
    :return: 状态码错误信息等
    """
    url = YP["url"]
    text = YP["text"].format(code)
    res = requests.post(url, data={
        "apikey": YP["apikey"],
        "mobile": mobile,
        "text": text,
    })
    re_json = json.loads(res.text)
    return re_json


if __name__ == "__main__":
    """
    函数测试
    """
    res = send_single_sms(YP["apikey"], "123456", "15069120552")
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    if code == 0:
        print("短信验证码发送成功")
    else:
        print("验证码发送失败：{}".format(msg))
    print(res.text)

