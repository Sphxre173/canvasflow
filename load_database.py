import sqlite3
import random
import os

""" #load database... ๒สนฟก กฟะฟิฟหำ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
#init cursor for database virtual cursor
cursor = connect.cursor() """


def init_db():
    #load database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    #init cursor for database virtual cursor
    cursor = connect.cursor()
    #CREATE TABLE AND COLUMN
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            role TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commission_table (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            work_name TEXT,
            desc TEXT,
            status TEXT,
            sub_status TEXT,
            price INTEGER,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commission_list_table (
            commission_id INTEGER PRIMARY KEY AUTOINCREMENT,

            commission_name TEXT NOT NULL,       
            commission_type TEXT DEFAULT Normal,                 

            price_start INTEGER NOT NULL,        
            description TEXT,                     

            image_url TEXT,                       
            status TEXT DEFAULT 'open',           
            
            rating REAL DEFAULT 4.8,             
            review_count INTEGER DEFAULT 0,      

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS request_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            image_path TEXT
        )
    """)
    # cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS request_images (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         request_id INTEGER,
    #         image_path TEXT
    #     )
    # """)
    connect.commit()
    connect.close()

def add_admin(user_email):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()


    cursor.execute("SELECT * FROM user WHERE email = ?",
                   (str(user_email),)
    )
    
    is_exist = cursor.fetchone()
    if not is_exist:
        cursor.execute(
            "INSERT INTO user (email, role) VALUES (?, ?)",
            (str(user_email), "admin")
        )
        connect.commit()
    print(is_exist)
    connect.close()

def get_user(user_email):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM user WHERE email = ?",
                   (str(user_email),)
    )
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO user (email, role) VALUES (?, ?)",
            (str(user_email), "user")
        )
        connect.commit()
    connect.close()
    return user



"""
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    work_name TEXT,
    status TEXT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
"""

def add_request_image(request_id, image_path):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()

    cursor.execute("""
        INSERT INTO request_images
        (request_id, image_path)
        VALUES (?, ?)
    """, (request_id, image_path))

    connect.commit()
    connect.close()

def add_commission_request(workname:str, work_description:str, email:str, price:int):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    #find if user is already request before and in state of request
    cursor.execute(f"""
        SELECT * FROM commission_table
        WHERE email = ? AND status = 'requested'
    """, (email,))
    anti_spam = cursor.fetchone()
    if not anti_spam:
        cursor.execute("""
        INSERT INTO commission_table
        (email, work_name, desc, status, sub_status, price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        str(email),
        workname,
        work_description,
        "requested",
        "none",
        price
    ))

    connect.commit()
    request_id = cursor.lastrowid
    connect.close()

    return request_id
    #return work_id to return


def get_commission_request(get_type:str, status:str, email:str=None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    if status == "requested" or status == "cancelled" or status == "pending" or status == "completed":
        if email == None:
            cursor.execute(f"""
                SELECT uid, email, work_name, desc, status, sub_status, price, create_at
                FROM commission_table
                WHERE status = ?
                ORDER BY create_at DESC
            """, (status,))
        else:
            cursor.execute(f"""
                SELECT uid, email, work_name, desc, status, sub_status, price, create_at
                FROM commission_table
                WHERE status = ? AND email = ?
                ORDER BY create_at DESC
            """, (status, email))
        get_all = cursor.fetchall()
        if get_type == "debug":
            for i in get_all:
                print(i)
        elif get_type == "len":
            print(len(get_all))
            connect.close()
            return len(get_all)
        elif get_type == "get_all":
            print(get_all)
            connect.close()
            return get_all

        connect.close()
    else:
        raise ValueError("Error : invalid input")

def reset_data(table:str):
    """
        Choose to delete between

        user and role -> use 'user' as parameter
        or
        commission data -> use 'commission_table' as parameter
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    try:
        cursor.execute(f"""
            DROP TABLE {table};
        """)
        connect.commit()
        connect.close()
        print("COMPLETED")
    except Exception as e:
        print(e)

def update_commission_status(uid, status:str):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    sub_stat = ''
    if status == "pending" or status == "cancelled":
        if status == "pending":
            sub_stat = "sketch"

        elif status == "rejected":
            sub_stat = "none"

        cursor.execute("""
                UPDATE commission_table
                SET status = ?, sub_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE uid = ?
            """, (status, sub_stat, uid))
        
        connect.commit()
        connect.close()
        print(f"Update {uid} status to {status}, sub_status : {sub_stat}")

def update_sub_status(uid, sub_status):
    """
    sketch 20%
    sketch_review 40%
    coloring 60%
    final_review 80%
    completed 100%
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    if sub_status == "sketch" or sub_status == "sketch_review" or sub_status == "coloring" or sub_status == "final_review":
        cursor.execute("""
                UPDATE commission_table
                SET sub_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE uid = ?
            """, (sub_status, uid))
        connect.commit()
        return f"received data : {uid} {sub_status}"
    if sub_status == "completed":
        cursor.execute("""
                UPDATE commission_table
                SET sub_status = ?, status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE uid = ?
            """, (sub_status, "completed", uid))
        connect.commit()
        return f"received data : {uid} {sub_status}"
    connect.close()

""" cursor.execute(
        CREATE TABLE IF NOT EXISTS commission_list_table (
            commission_id INTEGER PRIMARY KEY AUTOINCREMENT,

            commission_name TEXT NOT NULL,       
            commission_type TEXT DEFAULT Normal,                 

            price_start INTEGER NOT NULL,        
            description TEXT,                     

            image_url TEXT,                       
            status TEXT DEFAULT 'open',           
            
            rating REAL DEFAULT 4.8,             
            review_count INTEGER DEFAULT 0,      

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    ) """

def get_cms_oc(work_id):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute("""
        SELECT image_path  FROM request_images
        WHERE request_id = ?
    """, (work_id, ))
    all = cursor.fetchall()
    connect.close()
    return all

def create_comission_list(name:str, price:int, desc:str, img_path:str):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute("""
        INSERT INTO commission_list_table 
        (commission_name, price_start, description, image_url)
        VALUES (?, ?, ?, ?)
    """, (name, price, desc, img_path))

    connect.commit()
    connect.close()
    print("Completely saves info to table")
    return True

def update_commission_list():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute(f"""
        DROP TABLE commission_list_table
    """)
    connect.commit()
    connect.close()

def get_commission_list():
    #WORKING TESTED
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "user.db")
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    cursor.execute("""
        SELECT * FROM commission_list_table
    """)
    inf = cursor.fetchall()
    print(inf)
    connect.close()
    return inf


if __name__ == "__main__":

    init_db()
    print(get_cms_oc(2))
    """ get_commission_list() """
    """ update_commission_list() """
    """ add_commission_request("mambo", "mambomambomambomambomambomambomambomambomambomambomambo", "tonklasoysuwan@gmail.com", 10)
    get_commission_request("get_all", "pending") """