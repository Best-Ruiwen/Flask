import redis


class Cache:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, 
        decode_responses=True)

    # 设置缓存
    def _set(self, key, value):
        try:
            self.r.set(key, value, ex=600)
            return True
        except:
            raise("Set cache error")
    
    # 查询记录
    def _get(self, key):
        try:
            ret = self.r.get(key)
            if ret:
                return ret
            else:
                return False
        except:
            raise("Get cache error")
