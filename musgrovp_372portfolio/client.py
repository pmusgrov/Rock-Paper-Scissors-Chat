# Title: TCPClient.py
# Date: 12/7/2023
# Adapted from:  Computer Networking: A Top-Down Approach, 8th Edition,Pearson
# Author: Kurose and Ross
import socket

def run_client():
    # specifics IPv4 network and TCP socket then connects to socket using host and port provided
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345
    client_socket.connect((host, port))
    # messages printed when connected
    print(f"Connected to {host} on port:{port}")
    print("Type /q to quit")
    print("Enter message to send. Please wait for input prompt before message...")
    print('Note: Type "play rps" to start a game of rock paper scissors')

    # try to handle exceptions
    try:
        # while connected
        while True:
            # prompt client for message and then send
            message = input("Enter Input > ")
            client_socket.send(message.encode())

            # if message was to shut down, do so
            if message == "/q":
                print("Shutting Down!")
                break

            # if client wants to play rps
            if message == "play rps":
                play_rps(client_socket)


            # saves data from server to variable, limit 4096 bytes, decodes, prints message
            data = client_socket.recv(4096)
            received_message = data.decode()
            print(f"Received: {received_message}")

            # if message was to shut down, do so
            if received_message == "/q":
                print("Server has requested shut down. Shutting Down!")
                break
            # if message was to play rps, do so
            if received_message == "play rps":
                play_rps(client_socket)
            # if message was to play rps, do so
            if received_message == "You Quit the Game!":
                continue
    finally:
        client_socket.close()


def play_rps(client_socket):
    while True:
        # input clients move and send to server, if move is to quit game, do so
        choice = input("Enter your choice > ")
        if choice == "/q":
            client_socket.send("/q".encode())
            break
        client_socket.send(choice.encode())

        # get result from server and print
        result = receive_message(client_socket)
        if "/q" in result:
            break
        print(result)
        if "Invalid choice. Please choose rock, paper, or scissors." in result:
            break
        if "Congratulations" in result or "Sorry" in result or "tie" in result:
            return
# Title: how to receive all data Python socket programming
# Date: 12/7/2023
# Adapted from:  https://stackoverflow.com/questions/48625102/how-to-receive-all-data-python-socket-programming
# Author:  Carlos Overstreet

def receive_message(client_socket):
    # initialize byte variable
    data = b''
    # while it is receiving data
    while True:
        # grab each chunk
        chunk = client_socket.recv(4096)
        # add to data
        data += chunk
        # if delimiter is in chunk
        if b'\t' in chunk:
            break
    # return all data
    return data.decode().strip()

if __name__ == "__main__":
    run_client()