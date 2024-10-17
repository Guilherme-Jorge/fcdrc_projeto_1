import pika
import click
import threading

# RabbitMQ server credentials
RABBITMQ_HOST = 'localhost'  # Change this if you're running RabbitMQ elsewhere
RABBITMQ_PORT = 5672

def create_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))

def setup_queue(channel, queue_name):
    # Declare queue to ensure it exists
    channel.queue_declare(queue=queue_name)

def send_message(sender, receiver, message):
    connection = create_connection()
    channel = connection.channel()

    # Setup receiver's queue
    setup_queue(channel, receiver)

    # Publish message
    channel.basic_publish(
        exchange='',
        routing_key=receiver,
        body=f"From {sender}: {message}"
    )

    print(f"[Sent] To {receiver}: {message}")
    connection.close()

def receive_messages(username):
    connection = create_connection()
    channel = connection.channel()

    # Setup user's queue
    setup_queue(channel, username)

    def callback(ch, method, properties, body):
        print(f"\n[Received] {body.decode()}")

    channel.basic_consume(
        queue=username,
        on_message_callback=callback,
        auto_ack=True
    )

    print(f"[*] Waiting for messages for {username}. To exit press CTRL+C")
    channel.start_consuming()

@click.command()
@click.option('--username', prompt='Your username', help='Your unique username for messaging.')
def messaging_app(username):
    def receive_thread():
        # Start the receiving thread for the user
        receive_messages(username)

    # Start a thread to receive messages
    threading.Thread(target=receive_thread, daemon=True).start()

    print(f"Welcome to the messaging app, {username}! You can start sending messages.")
    
    while True:
        receiver = input("Enter receiver's username: ")
        message = input(f"Enter your message to {receiver}: ")
        send_message(username, receiver, message)

if __name__ == '__main__':
    messaging_app()
