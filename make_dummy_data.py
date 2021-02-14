import json
import uuid
import random
import csv
import sqlite3


def read_name_list():
    name_dict = dict()
    with open("./name_list.tsv") as inf:
        reader = csv.reader(inf, delimiter="\t")
        for line in reader:
            name_dict[line[1]] = "M"
            name_dict[line[3]] = "F"

    return name_dict


def read_states_list():
    states_list = list()
    with open("./states_list.txt") as inf:
        for line in inf:
            states_list.append(line.replace("\n", ""))

    return states_list



def make_user_str(user: str, gender: str, states_list: list):
    key = "#" + str(uuid.uuid4())[-6:]
    status = [True, False]
    status_weights = [7, 3]
    is_active = random.choices(status, k=1, weights = status_weights)[0]
    adress = {"country": "USA","state": random.choice(states_list)}
    user_account = {"user": user.replace(" ", ""),
                    "key": key,
                    "gender": gender,
                    "age": random.choice([i for i in range(18, 50)]),
                    "hight": random.choice([i for i in range(160, 190)]),
                    "weight": random.choice([i for i in range(45, 90)]),
                    "adress": adress,
                    "is_active": is_active
                    }
    return user_account


if __name__ == '__main__':
    dbname = "./db/init.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()


    #cur.execute(
    #    'CREATE TABLE if not exists users(\
    #        user str,\
    #        key str,\
    #        gender str,\
    #        age int,\
    #        hight int,\
    #        weight int,\
    #        adress txt,\
    #        is_active bool\
    #    )'
    #)
    cur.execute(
        'CREATE TABLE if not exists users(\
            user blob\
        )'
    )

    name_dict = read_name_list()
    states_list = read_states_list()

    for i, name in enumerate(name_dict):
        gender = name_dict[name]
        user_account = make_user_str(name, gender, states_list)

        fn = "./file_dir/user{}.json".format(str(i))
        with open(fn, "w") as f:
            #f.write(json.dumps(user_account, indent=4))
            f.write(json.dumps(user_account))

        user_account_data =tuple(user_account.values())
        print(user_account_data)
        #cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)', user_account_data)

    for i in range(len(name_dict)):
        fn = "./file_dir/user{}.json".format(str(i))
        with open(fn, "rb") as f:
            blob = f.read()
        cur.execute('INSERT INTO users VALUES (?)', [blob])

    conn.commit()
    conn.close()
