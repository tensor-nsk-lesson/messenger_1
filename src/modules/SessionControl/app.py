import redis

def initRedis_db():
    r = redis.Redis(host='127.0.0.1',port=6379,db=0)
    return r