import redis

redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True  # para trabalhar com strings diretamente
)