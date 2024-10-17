import pika

def receive_message():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue (it needs to match the sender's queue)
    channel.queue_declare(queue='chat_queue')

    # Callback function to process messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    # Set up subscription
    channel.basic_consume(queue='chat_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    receive_message()
