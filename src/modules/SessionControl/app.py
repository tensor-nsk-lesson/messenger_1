import redis

def RedisSession():
    r = redis.Redis(host='localhost',port=6379,db=0)
    return r