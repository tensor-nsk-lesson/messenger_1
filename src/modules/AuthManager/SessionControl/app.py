import redis



def initRedis_db():
    r = redis.Redis(host='localhost',port=6379)
    return r

def getUserID(uuid):
    r = initRedis_db()
    return r.get(uuid)