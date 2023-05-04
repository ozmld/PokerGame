import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("PokerUsers.db")
    cur = base.cursor()
    if base:
        print("All Good!")
    base.execute('CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, name TEXT, players_num TEXT, chips TEXT)')
    base.commit()


def sql_add_user_command(id):
    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (id, "", "", ""))
    base.commit()


def sql_update_user_command(id, name="", players_num="", chips=""):
    if name != "":
        cur.execute("UPDATE users SET name = \"{}\" WHERE id == \"{}\";".format(name, id))
        base.commit()
    if players_num != "":
        cur.execute("UPDATE users SET players_num = \"{}\" WHERE id == \"{}\";".format(players_num, id))
        base.commit()
    if chips != "":
        cur.execute("UPDATE users SET chips = \"{}\" WHERE id == \"{}\";".format(chips, id))
        base.commit()

def sql_get_user_data_comman(id):
    return cur.execute("SELECT * FROM users WHERE id == '{}' LIMIT 1".format(id)).fetchall()[0]