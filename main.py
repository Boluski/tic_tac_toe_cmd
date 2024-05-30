#! python3.7
# This is the main file.

from datetime import timedelta
import pyinputplus as pyip
import schedule
import client
import tools
import time


run = True
package = ()

while run:
    print('')
    print('Tic Tac Toe cmd:')
    print('Inputs:', 'Signup, Login, Quit, "_"-[refresh]')
    print('')
    controls = ('signup', 'login', 'quit', '')
    _input_ = pyip.inputStr(prompt='Input> ', blank=True).lower()

    if _input_ == controls[0]:
        while True:
            print('Signup:')
            print('Inputs:', 'Back, "_"-[continue]')
            print('')
            controls = ('back', '')
            _input_ = pyip.inputStr(prompt='Input>', blank=True).lower()

            if _input_ == controls[0]:
                break

            elif _input_ == controls[1]:
                while True:
                    username = tools.input_username()
                    email = tools.input_email()
                    password = tools.input_password()
                    password_again = tools.input_password()
                    while password != password_again:
                        print('passwords are not the same')
                        print('')
                        password = tools.input_password()
                        password_again = tools.input_password()
                    print('Is this the information you entered ? ')
                    print('Inputs:', 'Yes, No')
                    print(tools.input_check(username, email, password))
                    print('')
                    controls = ('yes', 'no')
                    _input_ = pyip.inputYesNo(prompt='Input> ').lower()

                    if _input_ == controls[0]:
                        constant = 5
                        moment = time.localtime()
                        now = timedelta(hours=moment[3], minutes=moment[4], seconds=moment[5])
                        future = timedelta(seconds=constant)
                        moment = '%s' % (str(now + future))
                        package = [username, email, password]
                        task = schedule.Scheduler()
                        client.done = False
                        task.every().day.at(moment).do(client.signup, package)

                        while True:
                            task.run_pending()
                            time.sleep(1)

                            if client.done:
                                break

                        break
                    elif _input_ == controls[1]:
                        continue

    elif _input_ == controls[1]:
        while True:
            print('Login: ')
            print('Inputs:', 'Back, "_"-[Continue]')
            print('')
            controls = ('back', '')
            _input_ = pyip.inputStr(prompt='Input> ', blank=True).lower()

            if _input_ == controls[0]:
                break

            elif _input_ == controls[1]:

                while True:
                    username = tools.input_username()
                    password = tools.input_password()
                    constant = 5
                    moment = time.localtime()
                    now = timedelta(hours=moment[3], minutes=moment[4], seconds=moment[5])
                    future = timedelta(seconds=constant)
                    moment = '%s' % (str(now + future))
                    package = [username, password]
                    task = schedule.Scheduler()
                    client.done = False
                    task.every().day.at(moment).do(client.login, package)

                    while True:
                        task.run_pending()
                        time.sleep(1)
                        if client.done:
                            break

                    if not client.correct:
                        print('bad')
                        continue

                    while True:
                        print('%s: ' % username)
                        print('Inputs:', '\nSingle-[single player mode]\n'
                                         'Online-[online play]\n'
                                         'Status\n'
                                         'Quit')
                        print('')
                        controls = ('single', 'online', 'status', 'quit')
                        _input_ = pyip.inputStr(prompt='Input> ').lower()
                        if _input_ == controls[0]:
                            while True:
                                print('Single player: ')
                                print('Inputs', '\nEasy-[easy mode]\n'
                                                'Hard-[hard mode]\n'
                                                'back')
                                print('')
                                controls = ('easy', 'hard', 'back')
                                _input_ = pyip.inputStr(prompt='Input> ').lower()

                                if _input_ == controls[0]:
                                    bot = tools.get_bot()
                                    person = username
                                    bot = tools.TicTacToeEasy(bot)
                                    person = tools.Player(person)
                                    game_state = tools.State(bot, person, 3)
                                    game_state.tutorial()
                                    first, last = game_state.fal()
                                    game_state.ready()
                                    score = game_state.start()
                                    client.score(score)
                                    print(tools.result_check(score))
                                    space = pyip.inputStr(prompt='Press ' + 'Enter' + ' to continue', blank=True)
                                    print('')

                                elif _input_ == controls[1]:
                                    bot = tools.get_bot()
                                    person = username
                                    bot = tools.TicTacToeHard(bot)
                                    person = tools.Player(person)
                                    game_state = tools.State(bot, person, 3)
                                    game_state.tutorial()
                                    first, last = game_state.fal()
                                    game_state.ready()
                                    score = game_state.start()
                                    client.score(score)
                                    print(tools.result_check(score))
                                    space = pyip.inputStr(prompt='Press ' + 'Enter' + ' to continue', blank=True)
                                    print('')

                                elif _input_ == controls[2]:
                                    break

                        elif _input_ == controls[1]:
                            while True:
                                print('Online Mode : ')
                                print('Input', '\nJoin-[new game]'
                                               '\nRank'
                                               '\nBack')
                                print('')
                                controls = ('join', 'rank', 'back')
                                _input_ = pyip.inputStr(prompt='Input> ').lower()

                                if _input_ == controls[0]:
                                    while True:
                                        print('Online Mode')
                                        print('')

                                elif _input_ == controls[1]:
                                    pass

                                elif _input_ == controls[2]:
                                    break

                        elif _input_ == controls[2]:
                            key = [username]
                            client.status(key)
                            user_status = client.user_state
                            text = tools.status_check(user_status)
                            print('')
                            print(text)
                            print('')
                            space = pyip.inputStr(prompt='Press ' + 'Enter' + ' to continue', blank=True)
                            print('')
                        elif _input_ == controls[3]:
                            pass

    elif _input_ == controls[2]:
        run = False

    elif _input_ == controls[3]:
        pass
