from main import redis_conn, Product
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis_conn.xgroup_create(key, group, mkstream=True)
except:
    print('Group already exists')

while True:
    try:
        results = redis_conn.xreadgroup(group, key, {key: '>'}, None)
        
        if results != []:
            for result in results:
                order = result[1][0][1]
                product = Product.get(order['product_id'])
                try:
                    print(product)
                    product.quantity -= int(order['quantity'])
                    product.save()
                except:
                    redis_conn.xadd('refund_order', order)

    except Exception as e:
        print(f'Error reading from Redis: {str(e)}')
        continue

    time.sleep(1)