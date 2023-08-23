import redis

class RedisManager:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    def add_entry(self, site, username, password):
        self.redis_client.hset(site, username, password)

    def get_password(self, site, username):
        return self.redis_client.hget(site, username)

    def clear_database(self):
        self.redis_client.flushdb()

    def delete_entry(self, site, username):
        self.redis_client.hdel(site, username)

#App made by Al3x-Myku