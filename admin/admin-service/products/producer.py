import pika, json

params = pika.URLParameters('amqps://whcgljja:X8FVHzxJOttWyVzC-llvJF7jLjgSkkBx@gull.rmq.cloudamqp.com/whcgljja')

try:
    connection = pika.BlockingConnection(params)
    print("Admin Producer: Connection established")
except Exception as e:
    print(f"Producer: Error connecting to RabbitMQ: {str(e)}")


channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)