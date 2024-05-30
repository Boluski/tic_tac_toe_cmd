#! python3.7

from tools import Client
import socket
import tools

done = False
correct = False
validate = 'Welcome'
user_state = None


def signup(info):
    print('{Start}')
    server = Client(socket.gethostbyname(""), 4101, 10)
    server.send_variable(info)
    server.buffer()
    server.receive()
    answer = server.message()
    print(answer.decode())
    global done
    done = True
    print('{End}')


def login(info):
    print('{Start}')
    # server = Client('ADEX', 1101, 10)
    server = Client(socket.gethostbyname(""), 4101, 10)
    server.send_variable(info)
    server.buffer()
    server.receive()
    answer = server.message()
    print(answer.decode())
    if validate in answer.decode():
        global correct
        correct = True
    global done
    done = True
    print('{End}')


def status(info):
    print('{Start}')
    server = Client(socket.gethostbyname(""), 4101, 10)
    server.send_variable(info)
    server.var_buffer()
    server.receive()
    global user_state
    user_state = server.message()
    user_state = tools.get_var(user_state)
    print(str(user_state))
    print('{End}')


def score(info):
    print('{Start}')
    server = Client(socket.gethostbyname(""), 4101, 10)
    server.send_variable(info)
    global done
    done = True
    print('{End}')


def online(info):
    print('{Start}')
    server = Client(socket.gethostbyname(""), 4101, 10)
    server.send_variable(info)
    while True:
        server.buffer()
        server.receive()
        answer = server.message()
        print(answer.decode())
        print('{End}')
