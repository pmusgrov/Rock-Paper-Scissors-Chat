# Title: TCServer.py
# Date: 12/7/2023
# Adapted from:  Computer Networking: A Top-Down Approach, 8th Edition,Pearson
# Author: Kurose and Ross
import socket

def run_server():
    # create a IPv4, stream TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allow socket to be reused
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # specify host and port and bind to socket then listen
    host = 'localhost'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(1)

    # messages to print when connected
    print(f"Connected by ({host}:{port})")
    print("Waiting for message...")
    # when the server is connected to
    while True:
        # accepts socket and completes handshake
        connection, address = server_socket.accept()
        print(f"Connected to {address}")
        message_number = 0
        # try to handle exceptions
        try:
            # variable to see if client or sever is playing
            # in_game = False
            while True:
                # saves data from client to variable, limit 4096 bytes
                data = connection.recv(4096)
                # if there is no data (closed loop) break
                if not data:
                    break
                # covert data to string and print
                message = data.decode()
                message_number += 1
                # if it is the first message print instructions otherwise proceed as normal
                if message_number == 1:
                    print("Type /q to quit")
                    print("Enter message to send. Please wait for input prompt before message...")
                    print('Note: Type "play rps" to start a game of rock paper scissors')
                    print(f"Received: {message}")
                else:
                    print(f"Received: {message}")

                # if message is shut down protocol, print and shut down, send /q back just in case
                if message == "/q":
                    print("Client has requested shut down. Shutting Down!")
                    connection.send("/q".encode())
                    break

                # if client wants to play rps
                if message == "play rps":
                    play_rps(connection, True)


                # prompt for message and send to client
                reply = input("Enter Input > ")
                connection.send(reply.encode())

                # if server wants to play rps
                if reply == "play rps":
                    play_rps(connection, True)

                # if message is to shut down, do so and send message in case
                if reply == "/q":
                    print("Shutting Down!")
                    connection.send("/q".encode())
                    break
        # close socket
        finally:
            connection.close()
            break
# Title: Build a Python3 Rock Paper Scissor Game Using ASCII Art
# Date: 12/7/2023
# Adapted from:  https://devdojo.com/kmhmubin/build-a-python3-rock-paper-scissor-game-using-ascii-art
# Author:  K M H Mubin
def display_rps(choices):
    rps_art = {
        "rock": '''
        _______
    ---'   ____)
          (_____)
          (_____)
          (____)
    ---.__(___)
            ''',
        "paper": '''
         _______
    ---'    ____)____
               ______)
              _______)
             _______)
    ---.__________)
            ''',
        "scissors": '''
        _______
    ---'   ____)____
              ______)
           __________)
          (____)
    ---.__(___)
            ''',
        "Celebrate": '''
        (ﾉ◕ヮ◕)ﾉ*:・ﾟ✧
            '''
    }
    return [rps_art[choice] for choice in choices]
def play_rps(connection, is_server):
    # initiate choice and ascii variable and allowable choices
    choices = ["rock", "paper", "scissors"]
    client_choice = ""
    server_choice = ""
    client_ascii = ""
    server_ascii = ""
    happy = display_rps(["Celebrate"])[0]

    # if the server is running the code
    if is_server:
        # get clients choice and save proper ascii
        client_choice = connection.recv(4096).decode()
        # if client wants to quit the game do so
        if client_choice == "/q":
            print("Quitting the Game!")
            return

        client_ascii = display_rps([client_choice])[0]
        # if instruction is to quit, do so
        # prompt server for move and save ascii, then print ascii, client's choice, and client's ascii
        # send instructions to client and print them to server terminal
        connection.send("Let's play Rock, Paper, Scissors! Choose by typing: rock, paper, or scissors.".encode())
        print( "Let's play Rock, Paper, Scissors! Choose by typing: rock, paper, or scissors. Wait for the client to go"
              "first!")
        server_choice = input("Enter your choice > ")
        if server_choice == "/q":
            print("Quitting the Game!")
            connection.send("/q\t".encode())
            return
        server_ascii = display_rps([server_choice])[0]
        print(server_ascii)
        print(f"Client's Choice: {client_choice}")
        print(client_ascii)
        # is_server = False
    # ensure choice is valid
    if server_choice.lower() in choices and client_choice.lower() in choices:
        # send client ascii, server choice, server ascii to client
        connection.send(f"{client_ascii}\n".encode())
        connection.send(f"Server's choice: {server_choice}\n".encode())
        connection.send(f"{server_ascii}\n".encode())
        # if choices are equal indicate so for result and send to client
        if client_choice == server_choice:
            result_message = "It's a tie!\t"
            server_message = "It's a tie!"
            connection.send(result_message.encode())
        # apply game logic to see if client won and save result and send to client
        elif (
                (client_choice == "rock" and server_choice == "scissors") or
                (client_choice == "paper" and server_choice == "rock") or
                (client_choice == "scissors" and server_choice == "paper")
        ):
            result_message = "Congratulations! You win!\t"
            server_message = "Sorry, you lose. Better luck next time."
            connection.send(f"{happy}\n".encode())
            connection.send(result_message.encode())
        # if the above scenarios do not apply, the server must have won, save result and send to client
        else:
            result_message = "Sorry, you lose. Better luck next time. \t"
            print(happy)
            server_message = "Congratulations! You win!"
            connection.send(result_message.encode())
        # Print the result in the server's terminal
        print(f"Result: {server_message}")
    # invalid choice was made
    else:
        connection.send("Invalid choice. Please choose rock, paper, or scissors.".encode())
if __name__ == "__main__":
    run_server()
