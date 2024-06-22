import sqlite3

def init_db():
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            friendly_name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_id INTEGER,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            published TEXT,
            transcription TEXT,
            summary TEXT,
            enclosures_href TEXT,
            FOREIGN KEY(feed_id) REFERENCES feeds(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_feed(url, friendly_name):
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('INSERT INTO feeds (url, friendly_name) VALUES (?, ?)', (url, friendly_name))
    conn.commit()
    conn.close()

def remove_feed(feed_id):
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('DELETE FROM feeds WHERE id = ?', (feed_id,))
    c.execute('DELETE FROM episodes WHERE feed_id = ?', (feed_id,))
    conn.commit()
    conn.close()

def get_feeds():
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feeds')
    feeds = c.fetchall()
    conn.close()
    return feeds

def add_episode(feed_id, title, link, published, enclosures_href):
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('INSERT INTO episodes (feed_id, title, link, published, enclosures_href) VALUES (?, ?, ?, ?, ?)', (feed_id, title, link, published, enclosures_href))
    conn.commit()
    conn.close()

def get_episodes(feed_id, n=None):
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('SELECT * FROM episodes WHERE feed_id = ? ORDER BY published DESC', (feed_id,))
    episodes = c.fetchall()
    conn.close()
    if n is not None:
        return episodes[:n]
    return episodes


def update_episode_transcription(episode_id, transcription):
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('UPDATE episodes SET transcription = ? WHERE id = ?', (transcription, episode_id))
    conn.commit()
    conn.close()

def update_episode_summary(episode_id, summary):
    conn = sqlite3.connect('data/feeds.db')
    c = conn.cursor()
    c.execute('UPDATE episodes SET summary = ? WHERE id = ?', (summary, episode_id))
    conn.commit()
    conn.close()
