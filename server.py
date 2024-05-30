#! python3.7
# this is the central server file.

from tools import Server
from tools import DataBase
import tools
import json
import socket

data = ()


def signup_database():
    user = DataBase()
    user.make_table()
    mail_exist = user.email_exists(data[1])
    user_exist = user.username_exists(data[0])
    if not mail_exist:
        if not user_exist:
            user.add_info(data[0], data[1], data[2])
            state = {
                'username': data[0],
                'email': data[1],
                'password': data[2],
                'xp': 0,
                'e_win': 0,
                'e_lose': 0,
                'e_per': 0,
                'h_win': 0,
                'h_lose': 0,
                'h_per': 0,
            }
            file = open('%s.json' % data[0], 'w')
            json.dump(state, file)
            return 'Congratulation your account as been created! '
        else:
            return 'This username as been taken by someone else! '
    else:
        return 'A tic-tac-toe-cmd account as been created with this email address! '


def login_database():
    user = DataBase()
    user_exists = user.username_exists(data[0])
    account_exists = user.account_exists(data[0], data[1])
    if user_exists:
        if account_exists:
            return 'Welcome!'
        else:
            return 'Invalid password!'
    else:
        return 'This username name does not exist!'


def global_server():
    print('{Start}')
    print(socket.gethostname())
    print(socket.gethostbyname("")) 
    central_server = Server(socket.gethostbyname(""), 4101, 10, 10)
    central_server.var_buffer()
    central_server.receive()
    mess = central_server.message()
    global data
    data = tools.get_var(mess)
    print(str(type(data)))
    if len(data) == 3:
        print('{signup}')
        message_to_send = signup_database()
        central_server.send(message_to_send)
    elif len(data) == 2:
        print('{login}')
        message_to_send = login_database()
        central_server.send(message_to_send)
    elif len(data) == 1:
        file = '%s.json' % data[0]
        file = open(file)
        print(file)
        user_state = json.load(file)
        print(type(user_state))
        central_server.send_variable(user_state)
        print('done sending')
    elif len(data) == 6:
        file = '%s.json' % data[5]
        file = open(file)
        user_state = json.load(file)
        file.close()
        total_xp = data[0] + data[1] + data[2] + data[3]
        user_state['xp'] = user_state['xp'] + total_xp
        if data[3] == 0:
            if data[4] == 'easy':
                user_state['e_lose'] += 1
            else:
                user_state['h_lose'] += 1
        else:
            if data[4] == 'easy':
                user_state['e_win'] += 1
            else:
                user_state['h_win'] += 1
        if data[4] == 'easy':
            wins = user_state['e_win']
            lose = user_state['e_lose']
            all_games = wins + lose
            w_l = int((100 / all_games) * wins)
            user_state['e_per'] = w_l
        else:
            wins = user_state['h_win']
            lose = user_state['h_lose']
            all_games = wins + lose
            w_l = int((100 / all_games) * wins)
            user_state['h_per'] = w_l
        print(user_state)
        file = '%s.json' % data[5]
        file = open(file, 'w')
        json.dump(user_state, file)
        file.close()
    print('{End}')


while True:
    global_server()
