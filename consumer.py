from main import redis_conn, Product
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis_conn.xgroup_create(key, group)
except:
    print('Group already exists')

while True:
    try:
        results = redis_conn.xread_group(group, key, {key: '>'}, None)
        
        if results != []:
            for result in results:
                order = result[1][0][1]
                product = Product.get(order['product_id'])
                product.quantity -= int(order['quantity'])
                product.save()

    except Exception as e:
        print(f'Error reading from Redis: {str(e)}')
        continue

    time.sleep(1)