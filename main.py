from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis_om import get_redis_connection, HashModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
)

# Connect to Redis

redis_conn = get_redis_connection(
    host="redis-12894.c1.us-east1-2.gce.redns.redis-cloud.com",
    port=12894,
    password="oUDjGzd2h2ljd6FyVIMdyvTp4gE3celk",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis_conn

@app.get('/products')

async def get_products():
    return await Product.all_pks()