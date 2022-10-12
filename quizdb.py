import psycopg2
from qbutil import tossup, bonus, game
from configs import (postgresql_user, postgresql_password, postgresql_host, 
                     postgresql_port, postgresql_quizdb_name, MAX_DIFF)
import json

#init postgresql connection
connection = psycopg2.connect(user = postgresql_user, 
                              password = postgresql_password,
                              host = postgresql_host,
                              port = postgresql_port,
                              database = postgresql_quizdb_name)
cursor = connection.cursor()

def c_exec(cmd):
    global cursor
    try:
        cursor.execute(cmd)
    except Exception as inst:
        print(inst)
        connection = psycopg2.connect(user = postgresql_user, 
                              password = postgresql_password,
                              host = postgresql_host,
                              port = postgresql_port,
                              database = postgresql_quizdb_name)
        cursor = connection.cursor()
    

def get_random_tossup():
    c_exec('SELECT * FROM tossups ORDER BY random() LIMIT 1;')
    res = cursor.fetchone()
    return res

def get_difficulty(tid):
    try:
        c_exec("Select * FROM tournaments where id = " + str(tid)  + " LIMIT 1;")
        res = cursor.fetchone()
        diff = res[3]
    except:
        diff = 9 #assume the worst
    return diff
    
def get_tossup(num = 0, cat = None):
    while True:
        tu = get_random_tossup()
        diff = get_difficulty(tu[4])
        #skip tossups that are too short
        if len(tu[1]) < 200 or diff > MAX_DIFF:
            continue
        if cat is None:
            return tossup(num, tu[1], tu[2], tu[5])
        if tu[5] == cat:
            return tossup(num, tu[1], tu[2], tu[5])

def get_random_bonus():
    c_exec('SELECT * FROM bonuses ORDER BY random() LIMIT 1;')
    res = cursor.fetchone()
    return res

def get_bonus_parts(bid):
    c_exec("Select * FROM bonus_parts where bonus_id = " + str(bid)  + " LIMIT 3;")
    res = cursor.fetchall()
    if len(res) < 3:
        return None
    return [(res[i][2], res[i][3]) for i in range(3)]

def get_bonus(cat = None):
    while True:
        bon = None
        if cat is None:
            bon = get_random_bonus()
        else:
            while bon is None:
                b = get_random_bonus()
                diff = get_difficulty(b[6])
                if b[3] == cat and diff < MAX_DIFF:
                    bon = b
        bparts = get_bonus_parts(bon[0])
        if bparts is not None:
            return bonus(bon[7], bparts[0][0], bparts[1][0], bparts[2][0], 
                         bparts[0][1], bparts[1][1], bparts[2][1], bon[3])
        

def get_game(tu_cats, bon_cats):
    tus = [get_tossup(num=ind+1, cat=tu_cats[ind]) for ind in range(len(tu_cats))]
    bons = [get_bonus(cat=bon_cats[ind]) for ind in range(len(bon_cats))]
    return game(tus, )

def dump_that_motherfucker():
    c_exec("pg_dump QuizDB > 'C:/Users/willi/OneDrive/fuckingdump.dump'")




# c_exec(r"CREATE USER yourname WITH SUPERUSER PASSWORD 'yourpassword';")
c_exec("SET AUTOCOMMIT = ON")
# c_exec(r"CREATE DATABASE QUIZBOOGALOO WITH TEMPLATE QuizDB OWNER yourname;")
