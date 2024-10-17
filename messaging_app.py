from pika import BlockingConnection, ConnectionParameters
import click
from threading import Thread
from time import sleep


RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672


def create_connection():
    return BlockingConnection(
        ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )


def setup_queue(channel, queue_name):
    # Declare queue to ensure it exists
    channel.queue_declare(queue=queue_name)


def send_message(sender, receiver, message):
    connection = create_connection()
    channel = connection.channel()

    setup_queue(channel, receiver)

    channel.basic_publish(
        exchange="", routing_key=receiver, body=f"From {sender}: {message}"
    )

    print(f"[Sent] To {receiver}: {message}")
    connection.close()


def receive_messages(username, receiver):
    connection = create_connection()
    channel = connection.channel()

    setup_queue(channel, username)

    def callback(ch, method, properties, body):
        print(
            f"\n[Received] {body.decode()}\
            \nEnter your message to {receiver}: ",
            end="",
        )

    channel.basic_consume(queue=username, on_message_callback=callback, auto_ack=True)

    print(f"[*] Waiting for messages for {username}. To exit press CTRL+C")
    channel.start_consuming()


@click.command()
@click.option(
    "--username", prompt="Your username", help="Your unique username for messaging."
)
@click.option(
    "--receiver",
    prompt="Enter receiver's username",
    help="Receiver's unique username for messaging.",
)
def messaging_app(username, receiver):
    def receive_thread():
        # Start the receiving thread for the user
        receive_messages(username, receiver)

    # Start a thread to receive messages
    Thread(target=receive_thread, daemon=True).start()
    sleep(1)

    print(f"Welcome to the messaging app, {username}! You can start sending messages.")

    while True:
        message = input(f"Enter your message to {receiver}: ")
        send_message(username, receiver, message)


if __name__ == "__main__":
    messaging_app()
