import psycopg2

def set_conn():
    conn = psycopg2.connect(
        host='localhost',
        database='nfac',
        user='postgres',
        password='newday'
    )
    return conn


def create_table():
    create_level = '''
        create table if not exists current_level(
            id serial primary key, 
            level integer,
            fireboy_x integer,
            fireboy_y integer,
            jam_taken integer,
            watergirl_x integer, 
            watergirl_y integer
        )
    '''
    conn = set_conn()
    cur = conn.cursor()
    cur.execute(create_level)

    create_progress = '''
        create table if not exists progress(
            id integer,
            score integer,
            level integer REFERENCES current_level(id),
            time integer
        )
        ;
        '''
    cur.execute(create_progress)

    create_best = '''
        create table if not exists best_score(
            score integer, 
            time integer
        )
    '''
    cur.execute(create_best)
    
    cur.close()
    conn.commit()
    conn.close()


def insert_to_level(level, fireboy_x,fireboy_y,jam_taken,watergirl_x,watergirl_y):
    exist = 'select * from current_level where id = 1'
    conn = set_conn()
    cur = conn.cursor()
    cur.execute(exist)
    check = cur.fetchone()
    if check == None:
        create = 'insert into current_level(level,fireboy_x,fireboy_y,jam_taken,watergirl_x, watergirl_y) values (%s, %s, %s, %s, %s, %s)'
        cur.execute(create, (level, fireboy_x, fireboy_y, jam_taken, watergirl_x, watergirl_y))
    else:
        update = 'update current_level SET level = %s,fireboy_x= %s,fireboy_y= %s,jam_taken= %s,watergirl_x= %s, watergirl_y= %s'
        cur.execute(update, (level, fireboy_x, fireboy_y, jam_taken, watergirl_x, watergirl_y))
    conn.commit()
    cur.close()
    conn.close()
     

def save(score, level, fireboy_x,fireboy_y,jam_taken,watergirl_x,watergirl_y, finished: bool, time): 
    exist = 'select * from progress where id = 1'
    conn = set_conn()
    cur = conn.cursor()
    cur.execute(exist)
    check = cur.fetchone()
    if not finished:
        if check == None:
            insert_to_level(level, fireboy_x,fireboy_y,jam_taken,watergirl_x,watergirl_y)
            create = 'insert into progress(id, score, level, time) values (1, %s, %s, %s)'
            cur.execute(create, (score, 1, time))
        else: 
            update = 'update progress SET score=%s, level = %s,time= %s'
            cur.execute(update, (score, level, time))
    conn.commit()
    cur.close()
    conn.close()