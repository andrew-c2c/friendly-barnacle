from multiprocessing.sharedctypes import Value
import psycopg2
import pandas as pd
import datetime
from datetime import date
import getpass

def fail(*args):
    print('\nYour entry is invalid. Please enter a valid entry.')

def fail_digit(*args):
   print('\nYour entry can\'t be a number. Please enter a valid entry.')

conn = psycopg2.connect( 
        database = 'Project',
        user = 'postgres',
        password = 'owner',
        host = 'localhost',
        port = '5432')
cur = conn.cursor() #enter the archive database

while True: #start of main loop - exit option is only way to break the loop

    while True:
        try:
            mm_choice = str(input('\nWelcome to the Insurance Article Archive. Please choose what you\'d like to do:\n1) Search the Archive\n2) Utilize User Functions\n3) Exit\t\t'))    
        except ValueError:
            fail()
        else:
            if mm_choice == '1' or mm_choice == '2' or mm_choice == '3':
                break
            else:
                fail()

    
    
    if mm_choice == '1':
        while mm_choice == '1':
            while True:
                try:
                    search_choice = str(input('\nPlease enter how you\'d like to search the database:\n1) By KeyWord(s)\n2) By Archived Date\n3) By Priority on Pull Date\n4) Exit Search\t\t'))
                except ValueError:
                    fail()
                else:
                    if search_choice == '1' or search_choice == '2' or search_choice == '3' or search_choice == '4':
                        break
                    else:
                        fail()
            if search_choice == '1': #choosing to search by keyword
                while search_choice == '1':
                    kw_list_format = []
                    kw_list = []
                    while True:    
                        key_word = str(input('Please enter a keyword you\'d like to search for. When all keywords have been entered hit return.\n')).strip() #input used to enter keywords to search
                        to_menu = 1
                        if key_word !=  '': #checks if a key_word is entered. If a keyword is entered it gets appended to the list with the SQL query text
                            kw_list_format.append(f'lower(title) LIKE lower(\'%{key_word}%\')')
                            kw_list.append(key_word)
                            # print(kw_list)
                            print(f'{key_word} has been added!\n')
                        elif key_word == '': #checks if a key_word is entered. If no keyword is entered the loop breaks and runs the search
                            if len(kw_list) == 0:
                                while True:
                                    try:
                                        to_menu = str(input('No Keywords entered. Please choose:\n1) Enter more keywords\n2) Exit to main menu\t')) #option to go back if list is empty
                                    except ValueError:
                                        fail()
                                    else:
                                        if to_menu == '1' or to_menu == '2':
                                            break
                                        else:
                                            fail()
                                if to_menu == '1':
                                    continue
                                elif to_menu == '2':
                                    search_results = 'break'
                                    break
                            if len(kw_list) == 1:
                                print('Your Keyword has been entered')
                                search_type = 1
                                export_name = f'articles_for_{kw_list[0]}'
                                break
                            if len(kw_list) > 1:
                                while True:
                                    try:
                                        search_type = str(input('All Keywords have been added. Please enter how you\'d like to search for results:\n1) Return results with ALL keyword(s) included\n2) Return key words with ANY keywords\n3) Enter more keywords\t\t'))
                                    except ValueError:
                                        fail()
                                    else:
                                        if search_type == '1' or search_type == '2' or search_type == '3':
                                            break
                                        else:
                                            fail()
                                if search_type == '1' or search_type == '2':
                                    break
                                elif search_type == '3':
                                    continue


                    if to_menu  == '2':
                        break


                    item_num = 0 #used to determine which item is pulled. This starts at zero so the first list item is pulled
                    key_word_search = '' #empty string used to add key word items
                    
                    if search_type == '1':
                        export_name = ''
                        for item in kw_list: #For Loop used to add all list items to keyword as a string
                            kw_item = kw_list_format[item_num]
                            kw_item_plain = kw_list[item_num]
                            if item_num == 0:
                                key_word_search = f'{key_word_search} {kw_item}'
                                export_name = f'articles_including_{kw_item_plain}'
                            elif item_num >0:
                                key_word_search = f'{key_word_search} AND {kw_item}' #Returns results with all keywords
                                export_name = f'{export_name}_AND_{kw_item_plain}'

                            item_num+=1
                        key_word_search = f'WHERE ({key_word_search})' #formats key_word_search to be used in SQL
                    
                    elif search_type == '2':
                        export_name = ''
                        for item in kw_list: #For Loop used to add all list items to keyword as a string
                            kw_item = kw_list_format[item_num]
                            kw_item_plain = kw_list[item_num]
                            if item_num == 0:
                                key_word_search = f'{key_word_search} {kw_item}'
                                export_name = f'articles_including_{kw_item_plain}'
                            elif item_num >0:
                                key_word_search = f'{key_word_search} OR {kw_item}' #Returns results with all keywords
                                export_name = f'{export_name}_OR_{kw_item_plain}'
                            item_num+=1
                        key_word_search = f'WHERE ({key_word_search})' #formats key_word_search to be used in SQL

                    search_key = f"""SELECT title, link, archive_date
                                    FROM articles
                                    {key_word_search};"""
                    cur.execute(search_key)
                    search_results = cur.fetchall()
                    break
            
            elif search_choice == '2':
                while search_choice == '2':
                    while True:
                        try:
                            search_date_type = str(input('\nPlease choose how you\'d like to search:\n1) Search by Specific Date\n2) Search by Date Range\n3) Go Back\t'))
                        except ValueError:
                            fail()
                        else:
                            if search_date_type == '1' or search_date_type == '2' or search_date_type == '3':
                                break
                            else:
                                fail()
                    date_search = 0
                    if search_date_type == '1':
                        while search_date_type == '1':
                            while True:
                                try:
                                    date_plain = str(input('\nPlease enter the date you\'d like results from. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if date_plain.isdigit() is True:
                                        break
                                    elif len(date_plain) == 0:
                                        break
                                    else:
                                        fail()



                            if len(date_plain) == 0:
                                date_search = ''
                                break
                            elif len(date_plain) == 8:
                                date_format = f'{date_plain[0:4]}-{date_plain[4:6]}-{date_plain[6:]}'
                                date_search = f'Where archive_date = \'{date_format}\';'
                                export_name = (f'articles_from_{date_format}')
                                break 
                            else:
                                print('You entered an Invalid Date. Please try again.')         

                    elif search_date_type == '2':
                        while search_date_type == '2':
                            while True:
                                try:
                                    date1_plain = str(input('Please enter the first date of your range. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if date1_plain.isdigit() is True:
                                        break
                                    elif len(date1_plain) == 0:
                                        break
                                    else:
                                        fail()

                            if len(date1_plain) == 0:
                                search_results = 'break'
                                break
                            elif len(date1_plain) == 8:
                                date1_format = f'{date1_plain[0:4]}-{date1_plain[4:6]}-{date1_plain[6:]}'
                                break
                            else:
                                print('You entered an Invalid Date. Please try again.')
                                continue
                    
                        if len(date1_plain) == 0:
                            continue

                        while True:
                            while True:
                                try:
                                    date2_plain = str(input('Please enter the second date of your range. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if date2_plain.isdigit() is True:
                                        break
                                    elif len(date2_plain) == 0:
                                        break
                                    else:
                                        fail()

                            if len(date2_plain) == 0:
                                search_results = 'break'
                                break
                            elif len(date2_plain) == 8:
                                date2_format = f'{date2_plain[0:4]}-{date2_plain[4:6]}-{date2_plain[6:]}'
                                date_search = f'WHERE archive_date >= \'{date1_format}\' AND archive_date <= \'{date2_format}\';'
                                export_name = (f'articles_from_{date1_format}_to_{date2_format}')
                                break
                            else:
                                print('You entered an Invalid Date. Please try again.')

                        if len(date2_plain) == 0:
                            continue

                    elif search_date_type == '3':
                        search_results = 'break'
                        break                    
                    
                    
                    if date_search != '':
                        search_key = f"""SELECT title, link, archive_date
                                        FROM articles
                                        {date_search};"""
                        cur.execute(search_key)
                        search_results = cur.fetchall()            
                        break

            elif search_choice == '3':
                while search_choice == '3':
                    while True:
                        try:
                            search_priority_type = str(input('\nPlease choose how you\'d like to search:\n1) Search by Specific Priority\n2) Search by Priority Range\n3) Go Back\t'))
                        except ValueError:
                            fail()
                        else:
                            if search_priority_type == '1' or search_priority_type == '2' or search_priority_type == '3':
                                break
                            else:
                                fail()

                    if search_priority_type == '3':
                        break

                    while True:
                        try:
                            search_date_type = str(input('\nPlease choose how you\'d like to search:\n1) Search by Specific Date\n2) Search by Date Range\n3) Go Back\t'))
                        except ValueError:
                            fail()
                        else:
                            if search_date_type == '1' or search_date_type == '2' or search_date_type == '3':
                                break
                            else:
                                fail()

                    if search_date_type == '3':
                        search_results = 'break'
                        break


                    if search_date_type == '1' and search_priority_type == '1':
                        while search_priority_type == '1':
                            while True:
                                try:
                                    priority_plain = str(input('Please enter the priority you\'d like results from. Priority is ranked 1 - 99. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if priority_plain.isdigit() is True:
                                        break
                                    elif len(priority_plain) == 0:
                                        break
                                    else:
                                        fail()

                            if len(priority_plain) == 0:
                                break
                            elif len(priority_plain) == 1 or len(priority_plain) == 2:
                                priority_format = f'{str(priority_plain[0:])}'
                                break 
                            else:
                                fail()

                        if len(priority_plain) == 0:
                            search_results == 'break'
                            break

                        while search_date_type == '1':
                            while True:
                                try:
                                    date_plain = str(input('Please enter the date you\'d like results from. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if date_plain.isdigit() is True:
                                        break
                                    elif len(date_plain) == 0:
                                        break
                                    else:
                                        fail()

                            if len(date_plain) == 0:
                                break
                            elif len(date_plain) == 8:
                                date_format = f'{date_plain[0:4]}-{date_plain[4:6]}-{date_plain[6:]}'
                                date_search = f'{date_plain[0:4]}-{date_plain[4:6]}-{date_plain[6:]}'
                                break 
                            else:
                                print('You entered an Invalid Date. Please try again.')

                        if len(date_plain) == 0:
                            search_results = 'break'
                            break

                        sql_priority_search = f'Where id = \'{priority_format}_{date_format}\';'

                    elif search_date_type == '2' or search_priority_type == '2':
                        while search_priority_type == '1':
                            while True:
                                try:
                                    priority_plain = str(input('Please enter the priority you\'d like results from. Priority is ranked 1 - 99. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if priority_plain.isdigit() is True:
                                        break
                                    elif len(priority_plain) == 0:
                                        break
                                    else:
                                        fail()

                            if len(priority_plain) == 0:
                                break
                            elif priority_plain == '0':
                                fail()
                            elif len(priority_plain) == 1 or len(priority_plain) == 2:
                                priority_search = f'(daily_rank = \'{priority_plain[0:]}\')'
                                export_name_priority = f'priority_{priority_plain[0:]}'
                                break 
                            else:
                                fail()

                        while search_priority_type == '2':
                            while True:
                                try:
                                    priority1_plain = str(input('Please enter the first priority value for the range you\'d like results from. Priority is ranked 1 - 99. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if priority1_plain.isdigit() is True:
                                        break
                                    elif len(priority1_plain) == 0:
                                        break
                                    else:
                                        fail()

                            if len(priority1_plain) == 0:
                                break
                            elif priority1_plain == '0':
                                fail()
                                continue
                            elif len(priority1_plain) == 1 or len(priority1_plain) == 2:
                                pass
                            else:
                                fail()
                                continue

                            while True:
                                while True:
                                    try:
                                        priority2_plain = str(input('Please enter the second priority value for the range you\'d like results from. Priority is ranked 1 - 99. Leave Blank to Go Back.\n'))
                                    except ValueError:
                                        fail()
                                    else:
                                        if priority2_plain.isdigit() is True:
                                            break
                                        elif len(priority2_plain) == 0:
                                            break
                                        else:
                                            fail()


                                if len(priority2_plain) == 0:
                                    search_results = 'break'
                                    break
                                elif priority2_plain == '0':
                                    fail()
                                elif len(priority2_plain) == 1 or len(priority2_plain) == 2:
                                    priority_search = f'(daily_rank >= \'{priority1_plain[0:]}\' AND daily_rank <= \'{priority2_plain[0:]}\')'
                                    export_name_priority = f'priority_{priority1_plain[0:]}_to_{priority2_plain[0:]}'
                                    break 
                                else:
                                    print('You entered an Invalid Priority. Please try again.')
                                    continue

                            break



                                                        

                        while search_date_type == '1':
                            while True:
                                try:
                                    date_plain = str(input('Please enter the date you\'d like results from. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                                except ValueError:
                                    fail()
                                else:
                                    if date_plain.isdigit() is True:
                                        break
                                    else:
                                        fail()
                            
                            if len(date_plain) == 0:
                                break
                            elif len(date_plain) == 8:
                                date_search = f'(archive_date = \'{date_plain[0:4]}-{date_plain[4:6]}-{date_plain[6:]}\')'
                                export_name_date = f'on_{date_plain[4:6]}_{date_plain[6:]}_{date_plain[0:4]}'
                                break 
                            else:
                                print('You entered an Invalid Date. Please try again.')

                        while search_date_type == '2':
                            while True:
                                try:
                                    date1_plain = int(input('Please enter the first date of your range. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                                except date1_plain.isdigit() is True:
                                    fail()
                                else:
                                    break
                            
                            date1_plain = str(date1_plain)
                            if len(date1_plain) == 0:
                                break
                            elif len(date1_plain) == 8:
                                pass
                            else:
                                print('You entered an Invalid Date. Please try again.\n')
                                continue

                            while True:
                                while True:
                                    try:
                                        date2_plain = input('Please enter the second date of your range. Please enter as YYYYMMDD. Leave Blank to Go Back.\n')
                                    except date2_plain.isdigit() is True:
                                        fail()
                                    else:
                                        break

                                date2_plain = str(date2_plain)
                                if len(date2_plain) == 0:                
                                    break
                                elif len(date2_plain) == 8:
                                    date_search = f'(archive_date >= \'{date1_plain[0:4]}-{date1_plain[4:6]}-{date1_plain[6:]}\' AND archive_date <= \'{date2_plain[0:4]}-{date2_plain[4:6]}-{date2_plain[6:]}\')'
                                    export_name_date = f'from_{date1_plain[4:6]}_{date1_plain[6:]}_{date1_plain[0:4]}_to_{date2_plain[4:6]}_{date2_plain[6:]}_{date2_plain[0:4]}'
                                    break 
                                else:
                                    print('You entered an Invalid Date. Please try again\n')

                            break                


                        sql_priority_search = f'WHERE {priority_search} AND {date_search}'
                        export_name = f'articles_with_{export_name_priority}_{export_name_date}'
                        

                    search_key = f"""SELECT title, link, archive_date, daily_rank
                                    FROM articles
                                        {sql_priority_search};"""
                    cur.execute(search_key)
                    search_results = cur.fetchall()
                    break
            
            elif search_choice == '4':
                break


            if search_results == []: #confirming there are results - will message if no results are found
                print('\n\nNo Results found for the requested criteria\n\n') 
                continue

            elif search_results == 'break':
                print('\n')
                continue

            elif search_results != [] and search_results != 'break': #confirming there are results - will message if no results are found
                while True:    
                    while True:
                        try:
                            print_or_export = int(input('How would you like to review these results:\n1) Print\n2) Export\n3) Both\t\t'))
                        except ValueError:
                            fail()
                        else:
                            break

                    if print_or_export == 1 or print_or_export == 3:
                        item_num = 0
                        article_num = 1
                        for item in search_results:
                            print(f'Article #{article_num}\nTitle: {item[0]}\nLink: {item[1]}\nDate: {item[2]}\n')
                            item_num+=1
                            article_num+=1

                    if print_or_export == 2 or print_or_export == 3:
                        # if len(date_search) == 34:
                        #     export_name = (f'articles_from_{date_format}')
                        # elif len(date_search) == 68:
                        #     export_name = (f'articles_from_{date1_format}_to_{date2_format}')

                        path = r"C:\Users\Owner\Desktop\python Files\Project\Final Files\{name}.csv".format(name=export_name)
                        df =pd.DataFrame(search_results)
                        df.to_csv(f'{path}',index=False)
                        print(f'\nFile exported to: {path}\n')

                    if print_or_export == 1 or print_or_export == 2 or print_or_export == 3:
                        print('\nYour request has been completed.\n\n')
                        break
                    
                    else:
                        fail()
                    


    elif mm_choice == '2':
        login_fail = 1
        pass_fail = 'fail'
        while True:
            try:
                user = input(str('\nPlease enter your User ID:\t\t')).strip()
            except ValueError:
                fail()
            else:
                if user.isdigit() is True:
                    fail_digit()
                elif user == '':
                    fail()
                else:
                    break

        while login_fail < 4 and pass_fail == 'fail':
            while True:
                try:
                    password = str(getpass.getpass(prompt='\nPlease enter your password:\t\t').strip())
                except ValueError:
                    fail()
                else:
                    if password.isdigit() is True:
                        fail_digit()
                    elif password == '':
                        fail()
                    else:
                        break

            login = f'WHERE (user_id = \'{user}\') AND (user_pass = \'{password}\')'

            login_sql = f"""SELECT email
                    FROM users
                    WHERE (user_id = \'{user}\') AND (user_pass = \'{password}\') AND (locked = 'N');"""
            cur.execute(login_sql)
            login_check = cur.fetchall()

            if login_check == []:
                lock_check_sql = f"""SELECT locked FROM users WHERE user_id =\'{user}\'"""
                cur.execute(lock_check_sql)
                lock_check = cur.fetchall()
                if lock_check == []:                
                    print('\nNo user was found. Please try again.')
                    break
                elif lock_check[0] == ('Y',):
                    print('\nUser locked out. Please contact system admin to unlock account.')
                    break
                elif lock_check[0] == ('N',):
                    login_fail+=1
                    if login_fail == 4:
                        continue
                    while True:
                        try:
                            again = str(input(f'\nLogin Failed. Your Account will be locked out after {4-login_fail} more failures.\n\nWhat would you like to do:\n1) Try Logging-in as {user} Again\n2) Recover Your Password\n3) Go Back\t\t'))
                        except ValueError:
                            fail()
                        else:
                            if again == '1' or again == '2' or again == '3':
                                break
                            else:
                                fail()

                    if again == '1':
                        continue
                    elif again == '2':
                        recovery_user = f'WHERE user_id = \'{user}\''
                        recovery_question_sql = f"""SELECT rec_question
                        FROM users
                        {recovery_user};"""
                        cur.execute(recovery_question_sql)
                        recovery_question = cur.fetchall()
                        while True:
                            recovery_question_format = str(recovery_question[0])
                            while True:
                                try:
                                    recovery_answer = str(input(f'Please answer the following question:\n{recovery_question_format[2:-3]}\nYour Answer\n')).strip()
                                except ValueError:
                                    fail()
                                else:
                                    if recovery_answer == '':
                                        fail()
                                    else:
                                        break

                            recovery_pw_sql = f"""SELECT user_pass
                            FROM users
                            WHERE (user_id = \'{user}\') AND (rec_ans = \'{recovery_answer}\');"""
                            cur.execute(recovery_pw_sql)
                            recovery_pw = cur.fetchall()
                            if recovery_pw == []:
                                while True:
                                    try:
                                        recov_again = str(input('Your recovery answer was incorrect. Would you like to try again?\n1) Yes\n2) No\t'))
                                    except ValueError:
                                        fail()
                                    else:
                                        if recov_again == '1' or recov_again == '2':
                                            break
                                        else:
                                            fail()
                                if recov_again == '1':
                                    continue
                                elif recov_again == '2':
                                    break

                                
                            elif recovery_pw != []:
                                recover_pw_format = str(recovery_pw[0])
                                print(f'Your password is: {recover_pw_format[2:-3]}')

                            break



                    elif again == '3':
                        break

            elif login_check != []:
                pass_fail = 'pass'
                print (f'User {user} logged in!\n')

            if pass_fail == 'fail':
                break

        if login_fail == 4:
            lock_account_sql = f"""UPDATE users SET locked = 'Y' WHERE user_id =\'{user}\';"""
            cur.execute(lock_account_sql)
            print('User Account has been locked.')
        
        conn.commit()

        while pass_fail == 'pass':
            while True:
                try:
                    logged_in_menu = str(input('\nPlease choose what you\'d like to do:\n1) Update Account information\n2) See user Keyword Results\n3) Log-out\t\t'))
                except ValueError:
                    fail()
                else:
                    if logged_in_menu == '1' or logged_in_menu == '2' or logged_in_menu == '3':
                        break  
                    else:
                        fail()
            while logged_in_menu == '1':
                try:
                    update_menu = str(input('\nPlease choose what you\'d like to update:\n1) Update Keywords\n2) Update user Password\n3) Update user E-mail\n4) Update Recovery Question and Answer\n5) Go Back\t\t'))
                except ValueError:
                    fail()
                    continue
                else:
                    if update_menu == '1' or update_menu == '2' or update_menu == '3' or update_menu == '4' or update_menu == '5':
                        pass
                    else:
                        fail()
                        continue
                while update_menu == '1':
                    user_topics = f"""SELECT topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8, topic_9, topic_10
                    FROM users
                    WHERE (user_id = \'{user}\');"""
                    cur.execute(user_topics)
                    user_topic_tuple = cur.fetchall()
                    user_topic_list = list(user_topic_tuple[0])
                    print('\nYour current Keywords are:')
                    for topic_count in range(len(user_topic_list)):
                        if user_topic_list[topic_count] != None:
                            existing_topic_count = topic_count+1                    
                            print(f'Topic # {existing_topic_count}: {user_topic_list[topic_count]}')
                    while True:
                        try:
                            kw_change = str(input('\nWould you like to:\n1) Add Keywords\n2) Remove Keywords\n3) Go Back\t\t'))
                        except ValueError:
                            fail()
                        else:
                            if kw_change == '1' or kw_change == '2' or kw_change == '3':
                                break
                            else:
                                fail()
                    if kw_change == '1' and existing_topic_count <10:
                        while True:
                            try:
                                kw_add = str(input('Please enter the keyword you\'d like to add:\t\t')).strip()
                            except ValueError:
                                fail()
                            else:
                                if kw_add.isdigit() is True:
                                    fail_digit()
                                elif kw_add == '':
                                    fail()
                                else:
                                    break

                        for topic_count in range(len(user_topic_list)):
                            if user_topic_list[topic_count] != None:
                                existing_topic_count = topic_count+1                    
                                if (user_topic_list[topic_count]).lower() == kw_add.lower():
                                    print('\nKeyword is already in list.')
                                    add_topic = 'N'
                                    break
                                else:
                                    add_topic = 'Y'
                                    continue

                        if add_topic == 'Y':
                            kw_add_sql = f"""UPDATE users SET topic_{existing_topic_count+1} =\'{kw_add}\' WHERE (user_id = \'{user}\') AND (user_pass = \'{password}\') AND (locked = 'N');"""
                            # print(kw_add_sql)
                            cur.execute(kw_add_sql)
                            conn.commit()
                        
                    elif kw_change == '1' and existing_topic_count == 10:
                        print('User already has 10 keywords. This is the maximum number of keywords available.')
                    
                    elif kw_change == '2':
                        while True:
                            try:
                                kw_remove = input('Please enter the keyword you\'d like to remove:\t\t').strip()
                            except ValueError:
                                fail()
                            else:
                                if kw_remove.isdigit() is True:
                                    fail_digit()
                                elif kw_remove == '':
                                    fail()
                                else:
                                    break
                        remove = 0
                        for topic_count in range(len(user_topic_list)):
                            if user_topic_list[topic_count] != None:
                                if user_topic_list[topic_count].lower() == kw_remove.lower():
                                    existing_topic_count = topic_count+1
                                    # print(existing_topic_count)
                                    kw_remove_sql = f"""UPDATE users
                                                        SET topic_{existing_topic_count} = 'DELETE'
                                                        WHERE (lower(topic_{existing_topic_count}) = lower(\'{kw_remove}\')) AND (user_id = '{user}')
                                                        """
                                    cur.execute(kw_remove_sql)
                                    conn.commit()
                                    remove = 1
                                    print(f'{kw_remove} has been removed from your list.')

                        for topic_count in range(len(user_topic_list)):
                            # print(topic_count)
                            # print(existing_topic_count)
                            if topic_count+1 > existing_topic_count:
                                topic_kw_update = user_topic_list[topic_count]
                                # print(topic_kw_update)
                                # print(type(topic_kw_update))
                                topic_num_update = f'topic_{existing_topic_count}'
                                if topic_kw_update == None:
                                    kw_update_sql = f"""UPDATE users
                                    SET {topic_num_update} = NULL
                                    WHERE user_id = '{user}';"""     
                                else:
                                    kw_update_sql = f"""UPDATE users
                                    SET {topic_num_update} = '{topic_kw_update}'
                                    WHERE user_id = '{user}';"""                        
                                # print(kw_update_sql)
                                cur.execute(kw_update_sql)
                                conn.commit()
                                existing_topic_count+=1                           

                        if remove == 0:
                            print(f'\n{kw_remove} was not found in the current keywords list. It was not removed.')
                    
                    elif kw_change == '3':
                        break

                    else:
                        print('Entry was invalid. Please try again.\n')

                    conn.commit()

                while update_menu == '2':
                    while True:
                        try:
                            # pass_update1 = str(input('Please enter your new password:\t\t')).strip()
                            pass_update1 = str(getpass.getpass(prompt='Please enter your new password:\t\t').strip())
                        except ValueError:
                            fail()
                        else:
                            if pass_update1 == '':
                                fail()
                            elif pass_update1.isdigit() is True:
                                fail_digit()
                            else:
                                break

                    while True:
                        try:
                            pass_update2 = str(getpass.getpass('Please confirm your new password:\t\t').strip())
                            # pass_update2 = str(input('Please confirm your new password:\t\t')).strip()
                        except ValueError:
                            fail()
                        else:
                            if pass_update2 == '':
                                fail()
                            elif pass_update2.isdigit() is True:
                                fail_digit()
                            else:
                                break

                    while True:
                        try:
                            password_conf = str(getpass.getpass('Please confirm your current password:\t\t').strip())
                        except ValueError:
                            fail()
                        else:
                            if password_conf == '':
                                fail()
                            elif password_conf.isdigit() is True:
                                fail_digit()
                            else:
                                break

                    pass_update_again = 'NA'
                    while pass_update1 != pass_update2 or password_conf != password:
                        if pass_update1 != pass_update2:
                            pass_update_again = str(input('New passwords do not match. Would you like to try again? Y/N\t\t')).strip().capitalize()        
                        elif password_conf != password:
                            pass_update_again = str(input('Your password confirmation didn\'t match your current password. Would you like to try again? Y/N\t\t')).strip().capitalize()
                        
                        if pass_update_again == 'Y' or pass_update_again == 'N':
                            break
                        else:
                            print('Entry is invalid. Try again.\n')
                            continue
                    if pass_update_again == 'Y':
                        continue
                    elif pass_update_again == 'N':
                        break

                    update_pw = f"""UPDATE users SET user_pass = \'{pass_update1}\' WHERE (user_id = \'{user}\') AND (user_pass = \'{password}\') AND (locked = 'N');"""
                    cur.execute(update_pw)
                    conn.commit()
                    print('User password has been updated.')
                    break
                    
                while update_menu == '3':
                    while True:
                        try:
                            email_update1 = str(input('Please enter your new e-mail:\t\t')).strip()
                        except ValueError:
                            fail()
                        else:
                            at = 'N'
                            period = 'N'
                            for char in email_update1:
                                if char == '@':
                                    at = 'Y'
                                elif char == '.':
                                    period = 'Y'
                                else:
                                    continue
                            if at == 'Y' and period == 'Y':
                                break
                            else:
                                print('New e-mail address must be valid. A valid email include the following characters: \'@\' and a \'.\'')
                    while True:
                        try:
                            email_update2 = str(input('Please confirm your new e-mail:\t\t')).strip()
                        except ValueError:
                            fail()
                        else:
                            at = 'N'
                            period = 'N'
                            for char in email_update2:
                                if char == '@':
                                    at = 'Y'
                                elif char == '.':
                                    period = 'Y'
                                else:
                                    continue
                            
                            if at == 'Y' and period == 'Y':
                                break
                            else:
                                print('New e-mail address must be valid. A valid email include the following characters: \'@\' and a \'.\'')
                    
                    while True:
                        try:
                            password_conf = str(getpass.getpass('Please confirm your current password:\t\t').strip())
                        except ValueError:
                            fail()
                        else:
                            if password_conf.isdigit() is True:
                                fail_digit()
                            elif password_conf == '':
                                fail()
                            else:
                                break

                    email_update_again = 'NA'

                    while email_update1 != email_update2 or password_conf != password:
                        if email_update1 != email_update2:
                            email_update_again = str(input('New emails do not match. Would you like to try again? Y/N\t\t')).strip().capitalize()        
                        elif password_conf != password:
                            pass_update_again = str(input('Your password confirmation didn\'t match your current password. Would you like to try again? Y/N\t\t')).strip().capitalize()
                        
                        if email_update_again == 'Y' or email_update_again == 'N':
                            break
                        else:
                            print('Entry is invalid. Try again.\n')
                            continue

                    if email_update_again == 'Y':
                        continue
                    elif email_update_again == 'N':
                        break
                    elif email_update_again == 'NA':
                        pass

                    update_email_sql = f"""UPDATE users SET email = \'{email_update1}\' WHERE (user_id = \'{user}\') AND (user_pass = \'{password}\') AND (locked = 'N');"""
                    # print(update_email_sql)
                    cur.execute(update_email_sql)
                    conn.commit()
                    print(f'User email has been updated to {email_update1}.')
                    break

                    
                while update_menu == '4':
                    while True:
                        try:
                            password_conf = str(getpass.getpass('Please confirm your current password:\t\t').strip())
                        except ValueError:
                            fail()
                        else:
                            if password_conf.isdigit() is True:
                                fail_digit()
                            elif password_conf == '':
                                fail()
                            else:
                                break
                    while True:
                        try:
                            rec_question_update = str(input('Please enter a new password recovery question:\n')).strip()
                        except ValueError:
                            fail()
                        else:
                            if rec_question_update == '':
                                fail()
                            elif rec_question_update.isdigit() is True:
                                fail_digit()
                            else:
                                break
                    while True:
                        try:
                            rec_ans_update = str(input('Please enter a new password recovery answer:\n')).strip()
                        except ValueError:
                            fail()
                        else:
                            if rec_ans_update == '':
                                fail()
                            else:
                                break
                    while True:
                        try:
                            rec_ans_update1 = str(input('Please confirm your new password recovery answer:\n')).strip()
                        except ValueError:
                            fail()
                        else:
                            if rec_ans_update1 == '':
                                fail()
                            else:
                                break
                    pass_update_again = 'NA'          
                    while rec_ans_update != rec_ans_update1 or password_conf != password:
                        if rec_ans_update != rec_ans_update1:
                            pass_update_again = str(input('New recovery answers do not match. Would you like to try again? Y/N\t\t')).strip().capitalize()        
                        elif password_conf != password:
                            pass_update_again = str(input('Your password confirmation didn\'t match your current password. Would you like to try again? Y/N\t\t')).strip().capitalize()
                        
                        if pass_update_again == 'Y' or pass_update_again == 'N':
                            break
                        else:
                            print('Entry is invalid. Try again.\n')
                            continue
                    
                    if pass_update_again == 'Y':
                        continue
                    elif pass_update_again == 'N':
                        break
                    elif pass_update_again == 'NA':
                        pass

                    update_rec_sql = f"""UPDATE users SET rec_question = \'{rec_question_update}\', rec_ans = \'{rec_ans_update}\' WHERE (user_id = \'{user}\') AND (user_pass = \'{password}\') AND (locked = 'N');"""
                    cur.execute(update_rec_sql)
                    conn.commit()
                    print(f'User recovery information has been updated.')
                    break

                if update_menu == '1' or update_menu == '2' or update_menu == '3' or update_menu == '4':
                    continue
                elif update_menu == '5':
                    break
                else:
                    print('Entry is invalid. Try again.\n')

            while logged_in_menu == '2': 
                search_topics = f"""SELECT user_id, email, topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8, topic_9, topic_10
                                FROM users
                                WHERE user_id = '{user}';"""
                cur.execute(search_topics)
                user_topics = cur.fetchall()

                kw_date_type = str(input('\nPlease choose how you\'d like to populate results:\n1) For Current Day\n2) For Past Week\n3) For stated range\n4) Go Back\t\t'))

                if kw_date_type == '1':
                    search_date = f'(archive_date = \'{date.today()}\')'
                elif kw_date_type == '2':
                    today_date = date.today()
                    last_week = today_date - datetime.timedelta(days=7)
                    # print(today_date,last_week)
                    search_date = f'(archive_date > \'{last_week}\' AND archive_date <= \'{today_date}\')'

                elif kw_date_type == '3':
                    date_exit = 'N'
                    while True:
                        try:
                            date1_plain = input('Please enter the first date of your range. Please enter as YYYYMMDD. Leave Blank to Go Back.\n')
                        except ValueError:
                            fail()
                        else:
                            if date1_plain == '':
                                date_exit = 'Y'
                                break
                            elif date1_plain.isdigit() is True and len(date1_plain) == 8:
                                date1_format = f'{date1_plain[0:4]}-{date1_plain[4:6]}-{date1_plain[6:]}'
                                break
                            else:
                                fail()
                    
                    while date1_plain != '':
                        try:
                            date2_plain = str(input('Please enter the second date of your range. Please enter as YYYYMMDD. Leave Blank to Go Back.\n'))
                        except ValueError:
                            fail()
                        else:
                            if date2_plain == '':
                                date_exit = 'Y'
                                break
                            elif date2_plain.isdigit() is True and len(date2_plain) == 8:
                                date2_format = f'{date2_plain[0:4]}-{date2_plain[4:6]}-{date2_plain[6:]}'
                                search_date = f'(archive_date >= \'{date1_format}\' AND archive_date <= \'{date2_format}\');'
                                break
                            else:
                                fail()

                elif kw_date_type == '4':
                    break
                else:
                    fail()
                    continue   

                if kw_date_type == '1' or kw_date_type == '2' or (kw_date_type == '3' and date_exit != 'Y') :
                    for users in user_topics:
                        user = users[0]
                        user_email = users[1]
                        user_topics = users[2:]
                        topic_num = 0
                        topic_articles = ''
                        for topics in user_topics:
                            if topics != None:
                                active_topic = topics[0:]
                                topic_articles = f'The articles for {topics[0:]} are:\n'
                                search_key = f"""SELECT title, link, archive_date
                                    FROM articles
                                    WHERE lower(title) LIKE lower(\'%{active_topic}%\') AND {search_date};"""
                                cur.execute(search_key)
                                topic_results = cur.fetchall()

                                for articles in topic_results:
                                    article_add = f'Title: {articles[0]} - Archive Date: {articles[2]}\nLink: {articles[1]}\n'
                                    topic_articles = f'{topic_articles}\n{article_add}'
                                    
                                print(topic_articles)

                                if topic_results == []:
                                    print('\n\nNo Results found for the listed keyword(s)\n\n') 
                                    
                    
        
            
            if logged_in_menu == '1' or logged_in_menu == '2':
                continue
            elif logged_in_menu == '3':
                print('User has been logged out.')
                user = ''
                password = ''
                pass_fail = 'fail'
                break
            else:
                'Entry invalid. Try again.\n'

    elif mm_choice == '3':
        conn.close()
        break

    else:
        print('Entry is invalid. Please choose a valid choice.\n')
    
    
