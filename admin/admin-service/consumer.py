import os

import django
import pika, json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://whcgljja:X8FVHzxJOttWyVzC-llvJF7jLjgSkkBx@gull.rmq.cloudamqp.com/whcgljja')

try:
    connection = pika.BlockingConnection(params)
    print("Admin Consumer: Connection established")
except Exception as e:
    print(f"Consumer: Error connecting to RabbitMQ: {str(e)}")

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')



channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('started consuming')

channel.start_consuming()

channel.close()
