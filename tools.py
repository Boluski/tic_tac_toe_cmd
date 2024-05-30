#! python3.7
# This is the tools file.

import pyinputplus as pyip
import sqlite3
import socket
import pickle
import random


def input_username():
    """
    Used to get username inputs.
    :return:
    """
    inp = pyip.inputStr(prompt='Username: ')
    return inp


def input_email():
    """
    Used to get email address inputs.
    :return:
    """
    inp = pyip.inputEmail(prompt='Email Address: ')
    return inp


def input_password():
    """
    Used to get passwords inputs.
    :return:
    """
    inp = pyip.inputStr(prompt='Password: ')
    return inp


def input_check(username, email, password):
    """
    Returns strings of text for verification.
    :param username:
    :param email:
    :param password:
    :return:
    """
    text = "Username: %s\n" \
           "Email Address: %s\n" \
           "Password: %s" % (username, email, password)
    return text


def get_var(byte):
    """
    Collect bytes and returns a variable
    :param byte:
    :return:
    """
    return pickle.loads(byte)


def get_bot():
    """
    Returns a random bot.
    :return:
    """
    bots = ('Dusty', 'Putin', 'Bob')
    return random.choice(bots)


def status_check(status):
    """
    Returns strings for status verification
    :param status:
    :return:
    """
    print(status)
    text = "Username: %s\n" \
           "Email Address: %s\n" \
           "Password: %s\n" \
           "Experience Point(s): %s\n" \
           "Wins(Easy): %s\n" \
           "Lose(Easy): %s\n" \
           "Win/Lose(Easy): %s\n" \
           "Wins(Hard): %s\n" \
           "Lose(Hard): %s\n" \
           "Win/Lose(Hard): %s"\
           % \
           (status['username'], status['email'],
            status['password'], str(status['xp']) + 'XP',
            status['e_win'], status['e_lose'],
            str(status['e_per']) + '%', status['h_win'],
            status['h_lose'], str(status['h_per']) + '%')
    return text


def result_check(res):
    """
    Returns strings of text for result verification
    :param res:
    :return:
    """
    text = "Round 1 --- %sXP\n" \
           "Round 2 --- %sXP\n" \
           "Round 3 --- %sXP\n" \
           "Winner  --- %sXP\n" \
           "Total   --- %sXP" % \
           (res[0], res[1], res[2], res[3],
            str(res[0] + res[1] + res[2] + res[3]))

    return text


class Server(object):
    def __init__(self, host, port, listen, maximum):
        """
        Makes a server object
        :param host:
        :param port:
        :param listen:
        :param maximum:
        """
        self.maximum = int(maximum)
        self.host = str(host)
        self.port = int(port)
        self.listen = int(listen)
        self.mess = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.host, self.port))
        self.server.listen(self.listen)
        self.client, address = self.server.accept()

    def send(self, mess):
        """
        collect a message and sends it to the client
        :param mess:
        :return:
        """
        mess = str(mess)
        header = str(len(mess)).ljust(self.maximum) + mess
        self.client.send(bytes(header, 'utf-8'))

    def send_variable(self, var):
        """
        collect a variable and sends it to the server
        :param var:
        :return:
        """
        byte = pickle.dumps(var)
        header = bytes(str(len(byte)).ljust(self.maximum), 'utf-8') + byte
        self.client.send(header)

    def buffer(self):
        """
        Makes the right buffer for receiving a message
        :return:
        """
        while True:
            self.buff = self.maximum
            buff = self.client.recv(self.buff)
            if buff != b'':
                buff = int(buff)
                self.buff = buff
                break

    def receive(self):
        """
        receives a message
        :return:
        """
        self.mess = self.client.recv(self.buff)

    def message(self):
        """
        Returns the message received
        :return:
        """
        return self.mess

    def var_buffer(self):
        """
        Makes the right buffer for receiving an object
        :return:
        """
        while True:
            self.buff = self.maximum
            buff = self.client.recv(self.buff)
            if buff != b'':
                buff = int(buff.decode())
                self.buff = buff
                break

    def close_client(self):
        """
        disconnects from the client from the server
        :return:
        """
        self.client.close()

    def close_server(self):
        """
        closes the server
        :return:
        """
        self.server.close()


class Client(object):
    """
    Makes a client object
    """
    def __init__(self, host, port, maximum):
        self.maximum = int(maximum)
        self.mess = None
        self.host = str(host)
        self.port = int(port)
        self.client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_server.connect((self.host, self.port))

    def buffer(self):
        """
        Makes the right buffer for receiving a message
        :return:
        """
        while True:
            self.buff = self.maximum
            buff = self.client_server.recv(self.buff)
            if buff != b'':
                buff = int(buff)
                self.buff = buff
                break

    def var_buffer(self):
        """
        Makes the right buffer for receiving an object
        :return:
        """
        while True:
            self.buff = self.maximum
            buff = self.client_server.recv(self.buff)
            if buff != b'':
                buff = int(buff.decode())
                self.buff = buff
                break

    def receive(self):
        """
        receives a message
        :return:
        """
        self.mess = self.client_server.recv(self.buff)

    def message(self):
        """
        returns the message
        :return:
        """
        return self.mess

    def send(self, mess):
        """
        collects a message and sends it to the server
        :param mess:
        :return:
        """
        header = str(len(str(mess))).ljust(self.maximum) + str(mess)
        header = bytes(header, 'utf-8')
        self.client_server.send(header)

    def send_variable(self, var):
        """
        collect a variable and sends it to the server
        :param var:
        :return:
        """
        byte = pickle.dumps(var)
        header = bytes(str(len(byte)).ljust(self.maximum), 'utf-8') + byte
        self.client_server.send(header)


class DataBase(object):
    def __init__(self):
        """
        Makes a database object
        """
        self.base = sqlite3.connect('tic_tac_toe_cmd.db')
        self.c = self.base.cursor()

    def make_table(self):
        """
        Make a table
        :return:
        """
        self.c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, password TEXT)')

    def add_info(self, username, email, password):
        """
        Adds a new user to the database
        :param username:
        :param email:
        :param password:
        :return:
        """
        self.c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        self.base.commit()

    def email_exists(self, email):
        """
        collect an email and checks if the email exists
        :param email:
        :return:
        """
        self.c.execute("SELECT ALL (email) FROM users")
        email_list = self.c.fetchall()
        for i in email_list:
            email_const = i[0]
            print(email_const)
            if email_const == email:
                return True
        return False

    def username_exists(self, username):
        """
        collect a username and checks if the username exists
        :param username:
        :return:
        """
        self.c.execute("SELECT ALL (username) FROM users")
        username_list = self.c.fetchall()
        for i in username_list:
            username_const = i[0]
            print(username_const)
            if username_const == username:
                return True
        return False

    def account_exists(self, username, password):
        """
        collect both username and password
        returns true if the account exix=st
        :param username:
        :param password:
        :return:
        """
        self.c.execute("SELECT username, password FROM users WHERE username = ? AND password = ?;",
                       (username, password))
        account = self.c.fetchone()
        if account is None:
            return False
        else:
            return True


class TicTacToeHard(object):
    def __init__(self, name):
        """
        makes a bot object at difficult
        :param name:
        """
        self.name = name
        self.play_with = ''
        self.sec_with = ''
        self.position_x = None
        self.position_y = None
        self.round = 0
        self.level = 'hard'

    def play(self, state):
        """
        Collect the state of the game and plays some where in the board
        :param state:
        :return:
        """
        if self.play_with == 'X':
            self.sec_with = 'O'
        else:
            self.sec_with = 'X'

        available = 0

        for i in state:
            for j in i:
                if j == ' ':
                    available += 1

        if available >= 8:
            while True:
                all_x = (0, 1, 2)
                all_y = (0, 1, 2)
                x_position = random.choice(all_x)
                y_position = random.choice(all_y)
                if state[y_position][x_position] == ' ':
                    self.position_x = x_position
                    self.position_y = y_position
                    break
                else:
                    continue

        elif available == 7:
            pointer = []
            if True:
                pos_x = 3
                pos_y = 3

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]

                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]

                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

        elif available == 6:
            pointer = []
            op_two = False
            if True:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0

                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                if not op_two:
                    pos_x = 3
                    pos_y = 3
                    for x in range(pos_x):
                        sport_1 = (state[0][x], (0, x))
                        sport_2 = (state[1][x], (1, x))
                        sport_3 = (state[2][x], (2, x))
                        line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                        tot = (sport_1, sport_2, sport_3)
                        if self.sec_with in line:
                            pass
                        elif self.play_with not in line:
                            pass
                        else:
                            constant = 3
                            for i in range(constant):
                                if tot[i][0] == self.play_with:
                                    pass
                                else:
                                    pointer = pointer + [tot[i][1]]

                    for y in range(pos_y):
                        sport_1 = (state[y][0], (y, 0))
                        sport_2 = (state[y][1], (y, 1))
                        sport_3 = (state[y][2], (y, 2))
                        line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                        tot = (sport_1, sport_2, sport_3)
                        if self.sec_with in line:
                            pass
                        elif self.play_with not in line:
                            pass
                        else:
                            constant = 3
                            for i in range(constant):
                                if tot[i][0] == self.play_with:
                                    pass
                                else:
                                    pointer = pointer + [tot[i][1]]

                    if True:
                        sport_1 = (state[2][0], (2, 0))
                        sport_2 = (state[1][1], (1, 1))
                        sport_3 = (state[0][2], (0, 2))
                        line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                        tot = (sport_1, sport_2, sport_3)
                        if self.sec_with in line:
                            pass
                        elif self.play_with not in line:
                            pass
                        else:
                            constant = 3
                            for i in range(constant):
                                if tot[i][0] == self.play_with:
                                    pass
                                else:
                                    pointer = pointer + [tot[i][1]]

                    if True:
                        sport_1 = (state[0][0], (0, 0))
                        sport_2 = (state[1][1], (1, 1))
                        sport_3 = (state[2][2], (2, 2))
                        line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                        tot = (sport_1, sport_2, sport_3)
                        if self.sec_with in line:
                            pass
                        elif self.play_with not in line:
                            pass
                        else:
                            constant = 3
                            for i in range(constant):
                                if tot[i][0] == self.play_with:
                                    pass
                                else:
                                    pointer = pointer + [tot[i][1]]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

        elif available == 5:
            pointer = []
            two_pl = False
            op_two = False
            no_where_left = False

            if True:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    dot_1 = (state[y][0], (y, 0))
                    dot_2 = (state[y][1], (y, 1))
                    dot_3 = (state[y][2], (y, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    dot_1 = (state[0][x], (0, x))
                    dot_2 = (state[1][x], (1, x))
                    dot_3 = (state[2][x], (2, x))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
                if True:
                    dot_1 = (state[2][0], (2, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[0][2], (0, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                if True:
                    dot_1 = (state[0][0], (0, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[2][2], (2, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
            if not two_pl:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0

                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

            if not op_two:
                pos_x = 3
                pos_y = 3

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

            if not no_where_left:
                for i in range(3):
                    for j in range(3):
                        if state[i][j] == ' ':
                            pointer = pointer + [(i, j)]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

        elif available == 4:
            pointer = []
            two_pl = False
            op_two = False
            no_where_left = False

            if True:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    dot_1 = (state[y][0], (y, 0))
                    dot_2 = (state[y][1], (y, 1))
                    dot_3 = (state[y][2], (y, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    dot_1 = (state[0][x], (0, x))
                    dot_2 = (state[1][x], (1, x))
                    dot_3 = (state[2][x], (2, x))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
                if True:
                    dot_1 = (state[2][0], (2, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[0][2], (0, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                if True:
                    dot_1 = (state[0][0], (0, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[2][2], (2, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
            if not two_pl:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0

                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

            if not op_two:
                pos_x = 3
                pos_y = 3

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

            if not no_where_left:
                for i in range(3):
                    for j in range(3):
                        if state[i][j] == ' ':
                            pointer = pointer + [(i, j)]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

        elif available == 3:
            pointer = []
            two_pl = False
            op_two = False
            no_where_left = False

            if True:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    dot_1 = (state[y][0], (y, 0))
                    dot_2 = (state[y][1], (y, 1))
                    dot_3 = (state[y][2], (y, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    dot_1 = (state[0][x], (0, x))
                    dot_2 = (state[1][x], (1, x))
                    dot_3 = (state[2][x], (2, x))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
                if True:
                    dot_1 = (state[2][0], (2, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[0][2], (0, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                if True:
                    dot_1 = (state[0][0], (0, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[2][2], (2, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
            if not two_pl:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0

                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

            if not op_two:
                pos_x = 3
                pos_y = 3

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True
            if not no_where_left:
                for i in range(3):
                    for j in range(3):
                        if state[i][j] == ' ':
                            pointer = pointer + [(i, j)]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

        elif available == 2:
            pointer = []
            two_pl = False
            op_two = False
            no_where_left = False

            if True:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    dot_1 = (state[y][0], (y, 0))
                    dot_2 = (state[y][1], (y, 1))
                    dot_3 = (state[y][2], (y, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    dot_1 = (state[0][x], (0, x))
                    dot_2 = (state[1][x], (1, x))
                    dot_3 = (state[2][x], (2, x))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
                if True:
                    dot_1 = (state[2][0], (2, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[0][2], (0, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True

                if True:
                    dot_1 = (state[0][0], (0, 0))
                    dot_2 = (state[1][1], (1, 1))
                    dot_3 = (state[2][2], (2, 2))
                    line = '' + dot_1[0] + dot_2[0] + dot_3[0]
                    tot = (dot_1, dot_2, dot_3)
                    num_pl = 0
                    for i in line:
                        if i == self.play_with:
                            num_pl += 1
                    if num_pl == 2:
                        for i in tot:
                            if i[0] == ' ':
                                pointer = pointer + [i[1]]
                                two_pl = True
                                op_two = True
                                no_where_left = True
            if not two_pl:
                pos_x = 3
                pos_y = 3

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0

                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True
                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    _all_ = (sport_1, sport_2, sport_3)
                    num_op = 0
                    for i in line:
                        if i == self.sec_with:
                            num_op += 1
                    if num_op == 2:
                        const = 3
                        for i in range(const):
                            if _all_[i][0] == ' ':
                                pointer = pointer + [_all_[i][1]]
                                op_two = True
                                no_where_left = True

            if not op_two:
                pos_x = 3
                pos_y = 3

                for x in range(pos_x):
                    sport_1 = (state[0][x], (0, x))
                    sport_2 = (state[1][x], (1, x))
                    sport_3 = (state[2][x], (2, x))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                for y in range(pos_y):
                    sport_1 = (state[y][0], (y, 0))
                    sport_2 = (state[y][1], (y, 1))
                    sport_3 = (state[y][2], (y, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[2][0], (2, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[0][2], (0, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

                if True:
                    sport_1 = (state[0][0], (0, 0))
                    sport_2 = (state[1][1], (1, 1))
                    sport_3 = (state[2][2], (2, 2))
                    line = '' + sport_1[0] + sport_2[0] + sport_3[0]
                    tot = (sport_1, sport_2, sport_3)
                    if self.sec_with in line:
                        pass
                    elif self.play_with not in line:
                        pass
                    else:
                        constant = 3
                        for i in range(constant):
                            if tot[i][0] == self.play_with:
                                pass
                            else:
                                pointer = pointer + [tot[i][1]]
                                no_where_left = True

            if not no_where_left:
                for i in range(3):
                    for j in range(3):
                        if state[i][j] == ' ':
                            pointer = pointer + [(i, j)]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

        if available == 1:
            pointer = []
            for i in range(3):
                for j in range(3):
                    if state[i][j] == ' ':
                        pointer = pointer + [(i, j)]

            play_at = random.choice(pointer)
            self.position_x = play_at[1]
            self.position_y = play_at[0]

    def win(self):
        """
        prints some information when the bot object wins a round
        :return:
        """
        print(self.name + ' wins this round')
        self.round = self.round + 1

    def winner(self):
        """
        Print some information when the bot wins the game
        :return:
        """
        print(self.name, 'is the winner')


class TicTacToeEasy(object):
    """
    Make a bot object in easy
    """
    def __init__(self, name):
        """
        Collect the state of the game and and play some where in the board
        :param name:
        """
        self.name = name
        self.play_with = ''
        self.position_x = None
        self.position_y = None
        self.round = 0
        self.level = 'easy'

    def play(self, state):
        while True:
            all_x = (0, 1, 2)
            all_y = (0, 1, 2)
            x_position = random.choice(all_x)
            y_position = random.choice(all_y)
            if state[y_position][x_position] == ' ':
                self.position_x = x_position
                self.position_y = y_position
                break
            else:
                continue

    def win(self):
        """
        prints some information when the bot object wins a round
        :return:
        """
        print(self.name + ' wins this round')
        self.round = self.round + 1

    def winner(self):
        """
        Print some information when the bot wins the game
        :return:
        """
        print(self.name, 'is the winner')


class Player(object):
    def __init__(self, name):
        """
        Makes a player object
        :param name:
        """
        self.name = name
        self.play_with = ''
        self.position_x = None
        self.position_y = None
        self.round = 0
        self.win_game = False

    def play(self, state):
        """
        Collect the state of the game and let the player play somewhere
        :param state:
        :return:
        """
        while True:
            x_position = pyip.inputNum(prompt='X Axi: ')
            y_position = pyip.inputNum(prompt='Y Axi: ')
            constant = 3

            if x_position < constant:

                if y_position < constant:

                    if state[y_position][x_position] == ' ':
                        self.position_x = x_position
                        self.position_y = y_position
                        break

                    else:
                        print('Space as already been taken')
                        continue

                else:
                    print('out of bound')
                    continue

            else:
                print('out of bound')
                continue

    def win(self):
        """
        prints some information when the player object wins a round
        :return:
        """
        print(self.name + ' wins this round')
        self.round = self.round + 1

    def winner(self):
        """
        Print some information when the player wins the game
        :return:
        """
        print(self.name, 'is the winner')
        self.win_game = True


class State(object):
    def __init__(self, player1, player2, games):
        """
        Makes a state object
        :param player1:
        :param player2:
        :param games:
        """
        self.games = int(games)
        self.player1 = player1
        self.player2 = player2
        self.first = None
        self.last = None
        self.tl = ' '
        self.tm = ' '
        self.tr = ' '
        self.cl = ' '
        self.cm = ' '
        self.cr = ' '
        self.bl = ' '
        self.bm = ' '
        self.br = ' '
        self.board = [[self.tl, self.tm, self.tr],
                      [self.cl, self.cm, self.cr],
                      [self.bl, self.bm, self.br]]

    def plot(self):
        """
        prints the game state
        :return:
        """
        board = ' %s | %s | %s \n' \
                '------------\n' \
                ' %s | %s | %s \n' \
                '------------\n' \
                ' %s | %s | %s ' % \
                (self.board[0][0], self.board[0][1], self.board[0][2],
                 self.board[1][0], self.board[1][1], self.board[1][2],
                 self.board[2][0], self.board[2][1], self.board[2][2])
        print(board)

    def tutorial(self):
        """
        print a quick tutorial to the player
        :return:
        """
        print('How to play')
        board = ' 0,0 | 1,0 | 2,0 \n' \
                '-----------------\n' \
                ' 0,1 | 1,1 | 2,1 \n' \
                '-----------------\n' \
                ' 0,2 | 1,2 | 2,2 '
        print('X,Y')
        print(board)

    def fal(self):
        """
        Chooses the first and last player
        :return:
        """
        comp = (self.player1, self.player2)
        first = random.choice(comp)
        last = ''

        if first == comp[0]:
            last = comp[1]

        else:
            last = comp[0]

        first.play_with = 'X'
        last.play_with = 'O'
        self.first, self.last = first, last
        return self.first, self.last

    def ready(self):
        """
        Print some important information before the game states
        :return:
        """
        print('[%s: %s VS %s: %s] Game: %s' %
              (self.first.name, self.first.play_with,
               self.last.name, self.last.play_with,
               self.games))
        print('')

    def reset_board(self):
        """
        Resets the board
        :return:
        """
        self.tl = ' '
        self.tm = ' '
        self.tr = ' '
        self.cl = ' '
        self.cm = ' '
        self.cr = ' '
        self.bl = ' '
        self.bm = ' '
        self.br = ' '
        self.board = [[self.tl, self.tm, self.tr],
                      [self.cl, self.cm, self.cr],
                      [self.bl, self.bm, self.br]]

    def space(self, x, y, play_with):

        if self.board[y][x] == ' ':
            self.board[y][x] = play_with

        for i in self.board:
            for j in i:
                if j == ' ':
                    return True

        return False

    def rules(self, board, player):
        """
        Returns True if the bot or the player wins
        :param board:
        :param player:
        :return:
        """
        constant = 3
        result = ''
        coord_x = 0
        coord_y = 0

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_x += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        coord_y = 1

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_x += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        coord_y = 2

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_x += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_y += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        coord_x = 1

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_y += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        coord_x = 2

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_y += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        coord_y = 2

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_x += 1
            coord_y -= 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        for i in range(constant):
            if board[coord_y][coord_x] == player.play_with:
                result = result + player.play_with
            coord_x += 1
            coord_y += 1
        if len(result) == 3:
            player.win()
            return True
        else:
            result = ''
            coord_x = 0
            coord_y = 0

        return False

    def start(self):
        """
        Gets the game started
        :return:
        """
        score = {'round1': 0, 'round2': 0, 'round3': 0, 'win': 0}
        for i in range(self.games):
            print('Round: %s' % str(i + 1))
            print('')
            constant = 5
            self.reset_board()
            self.plot()

            for _ in range(constant):
                print('%s is playing' % self.first.name)
                print('')
                self.first.play(self.board)
                space = self.space(self.first.position_x, self.first.position_y, self.first.play_with)
                self.plot()
                rule = self.rules(self.board, self.first)

                if rule:
                    if self.first.name == self.player2.name:
                        score['round%s' % str(i + 1)] = 1
                        print(score['round%s' % str(i + 1)])
                    break

                if not space:
                    break

                print('%s is playing' % self.last.name)
                print('')
                self.last.play(self.board)
                space = self.space(self.last.position_x, self.last.position_y, self.last.play_with)
                self.plot()
                rule = self.rules(self.board, self.last)

                if rule:
                    if self.last.name == self.player2.name:
                        score['round%s' % str(i + 1)] = 1
                        print(score['round%s' % str(i + 1)])
                    break

            print('Score:')
            print(self.first.name + ':', self.first.round,
                  '|', self.last.name + ':', self.last.round)
            print('')

        if self.first.round > self.last.round:
            self.first.winner()
            print('')
        elif self.first.round < self.last.round:
            self.last.winner()
            print('')
        else:
            print('Tie')
            print('')
        print(str(score))
        points = [0, 0, 0, 0, 'level', self.player2.name]
        if self.player1.level == 'easy':
            points[4] = 'easy'

            if score['round1'] == 1:
                points[0] = 10
            else:
                points[0] = 0

            if score['round2'] == 1:
                points[1] = 10
            else:
                points[1] = 0

            if score['round3'] == 1:
                points[2] = 10
            else:
                points[2] = 0

            if self.first.name == self.player2.name:
                if self.first.win_game:
                    points[3] = 30
            else:
                if self.last.win_game:
                    points[3] = 30

        else:
            points[4] = 'hard'

            if score['round1'] == 1:
                points[0] = 20
            else:
                points[0] = 0

            if score['round2'] == 1:
                points[1] = 20
            else:
                points[1] = 0

            if score['round3'] == 1:
                points[2] = 20
            else:
                points[2] = 0

            if self.first.name == self.player2.name:
                if self.first.win_game:
                    points[3] = 60
            else:
                if self.last.win_game:
                    points[3] = 60

        print(str(points))
        return points
