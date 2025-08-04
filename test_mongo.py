# test_mongo.py
import os
from pymongo.mongo_client import MongoClient

uri = os.getenv("MONGODB_URL")
if not uri:
    print("MONGODB_URL 환경변수가 설정되지 않았습니다.")
    exit(1)

client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("✅ MongoDB 연결 성공!")
except Exception as e:
    print("❌ MongoDB 연결 실패:", e)
