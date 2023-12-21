import json, pika
from main import Product, db, create_app

# Create a Flask app instance
app = create_app()

# Use the app context to perform database operations
with app.app_context():
    params = pika.URLParameters('amqps://whcgljja:X8FVHzxJOttWyVzC-llvJF7jLjgSkkBx@gull.rmq.cloudamqp.com/whcgljja')

    try:
        connection = pika.BlockingConnection(params)
        print("Main Consumer: Connection established")
    except Exception as e:
        print(f"Consumer: Error connecting to RabbitMQ: {str(e)}")

    channel = connection.channel()

    channel.queue_declare(queue='main')

    def callback(ch, method, properties, body):
        print('Received in main')
        data = json.loads(body)
        print(data)

        if properties.content_type == 'product_created':
            print("Creation callback hit")
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product created')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product updated')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product deleted')

    channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
    print('started consuming')

    channel.start_consuming()

    channel.close()
