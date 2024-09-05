import sqlite3

DATABASE = 'user_data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            followers TEXT,
                            following TEXT
                        )''')
        conn.commit()

def get_user_data(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT followers, following FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            followers, following = result
            return {
                'followers': followers.split('\n') if followers else [],
                'following': following.split('\n') if following else []
            }
        else:
            return {'followers': [], 'following': []}

def update_user_data(user_id, followers, following):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO users (user_id, followers, following) VALUES (?, ?, ?)',
                       (user_id, '\n'.join(followers), '\n'.join(following)))
        conn.commit()

def clear_user_data(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET followers = ?, following = ? WHERE user_id = ?',
                       ('', '', user_id))
        conn.commit()
