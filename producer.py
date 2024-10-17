import pika
import sys

def send_message(message):
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='chat_queue')

    # Send the message
    channel.basic_publish(exchange='', routing_key='chat_queue', body=message)
    print(f" [x] Sent '{message}'")

    connection.close()

if __name__ == "__main__":
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    send_message(message)
