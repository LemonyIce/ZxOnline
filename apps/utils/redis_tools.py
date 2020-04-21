import redis
from zxSchool.settings import REDIS


def redis_save(data):
    """
    redis保存和读取
    :param data: 字典["key":主键名，'value':内容,"model"模式,"overtime"过期时间]
    :return: 查询内容
    """
    if "overtime" in data:
        overtime = data["overtime"]
    else:
        overtime = 300
    r = redis.Redis(host=REDIS["host"], port=REDIS["port"], db=0, charset="utf8", decode_responses=True)
    if data["model"] == "set":
        r.set(str(data["key"]), data["value"])
        r.expire(str(data["key"]), overtime)
    else:
        value = r.get(data["key"])
        return value


if __name__ == "__main__":
    """
    函数测试
    """
    data = {
        "key": "test",
        "value": "a_test",
        "model": "set"
    }
    data2 = {
        "key": "test",
        "model": "get"
    }
    redis_save(data)
    print(redis_save(data2))
