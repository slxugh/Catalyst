import redis
import os
from dotenv import load_dotenv
load_dotenv()
r_from_user = redis.Redis(host=os.getenv("IP"), port=6379, db=0,password=os.getenv("REDIS_PASS")) # пространство для хранения tg_id - topic_id
r_to_user = redis.Redis(host=os.getenv("IP"), port=6379, db=1, password=os.getenv("REDIS_PASS")) # пространство для хранения topic_id - tg_id
