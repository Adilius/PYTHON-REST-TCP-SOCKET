import socket
import sys
from threading import Thread
import json
import os

HOST = "127.0.0.1"
PORT = 80
MAX_BUFFER_SIZE = 1024


def main():
    initialize_database()
    start_server()


# Creates database file
def initialize_database():

    # Create database file
    if not os.path.exists("db.json"):
        with open("db.json", "w+") as db:
            db.write("{\n}")


# Read contents of database file
def read_database():

    # Read database file
    with open("db.json", "r") as db:
        storage_file = json.load(db)

    return storage_file


# Creates headers for the response
def create_headers(status_code: int, status_text: str, message_body=""):

    # Reponse headers
    response_protocol = "HTTP/1.1"
    response_status_code = status_code
    response_status_text = status_text
    response_content_type = "application/json; encoding=utf8"
    response_connection = "close"

    # Create response sections
    status_line = (
        f"{response_protocol} {response_status_code} {response_status_text}\r\n"
    )
    content_type = f"Content-Type: {response_content_type}\r\n"
    connection = f"Connection: {response_connection}\r\n"
    empty_line = f"\r\n"

    # Combine into single string
    response_header = (
        status_line + content_type + connection + empty_line + message_body
    )

    # Encode string to utf-8 bytes
    response_header_encoded = response_header.encode("utf-8")

    return response_header_encoded


# Create & start server socket
def start_server():

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket
    try:
        server_socket.bind((HOST, PORT))
        print(f"Binding server socket to host:{HOST} and port {PORT}")
    except:
        print(f"Bind failed. Error: {str(sys.exc_info())}")
        sys.exit()

    # Enable passive listening sockets
    server_socket.listen(5)

    while True:

        # Accept incoming connection
        (client_socket, address) = server_socket.accept()
        ip, port = str(address[0]), str(address[1])
        print(f"Connection from {ip}:{port} has been established.")

        try:
            Thread(target=client_thread, args=(client_socket, ip, port)).start()
            print(f"Client thread for {ip}:{port} has been created.")
        except:
            print(f"Client thread for {ip}:{port} did not start.")


# Thread for each client
def client_thread(client_socket, ip, port):

    # Listen to incomming data
    data = receive_data(client_socket)

    if data:

        if data[0] == "GET":
            response_headers = do_GET(data)

        print(data)
        # response_headers = create_headers(200, 'OK')
        client_socket.send(response_headers)
        client_socket.close()
        print(f"Connection from {ip}:{port} has been closed.")

    print(f"Client thread for {ip}:{port} has been closed.")


# Handle GET request
def do_GET(data: list):

    # Check for content length
    if "Content-Length:" in data:
        con_len_index = data.index("Content-Length:")
        con_len_value = data[con_len_index + 1]

        # If there is no actual content
        if con_len_value == "0":
            return create_headers(400, "Bad Request")
    else:
        return create_headers(400, "Bad Request")

    # Check for content type
    if "Content-Type:" not in data:
        return create_headers(400, "Bad Request")

    # Get query param
    query = data[con_len_index + 2]

    storage_data = read_database()

    if query in storage_data:
        value = storage_data.get(query)
        return create_headers(200, "OK", value)
    else:
        return create_headers(404, "Not Found")


# Receive & process data
def receive_data(client_socket):
    client_data = client_socket.recv(MAX_BUFFER_SIZE)
    decoded_data = (
        str(client_data).strip("b'").rstrip().replace("\\n", " ").replace("\\r", " ")
    )
    data_variables = str(decoded_data).split()

    return data_variables


if __name__ == "__main__":
    main()
