import sqlite3
import os
import uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'campus.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returns dictionaries instead of tuples
    return conn

# Generate unique ID
def generate_id():
    return str(uuid.uuid4())

# ── USER OPERATIONS ──

def find_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def create_user(user_data):
    conn = get_db_connection()
    user_id = generate_id()
    created_at = datetime.now().isoformat()
    
    conn.execute('''
    INSERT INTO users (id, name, email, password, created_at)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, user_data['name'], user_data['email'], user_data['password'], created_at))
    
    conn.commit()
    conn.close()
    
    return {
        'id': user_id,
        'name': user_data['name'],
        'email': user_data['email'],
        'createdAt': created_at
    }

# ── POST OPERATIONS ──

def get_all_posts():
    conn = get_db_connection()
    posts_rows = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    
    posts = []
    for row in posts_rows:
        post_dict = dict(row)
        # Convert sqlite boolean/integer field names to camelCase for frontend
        post_dict['isAnnouncement'] = bool(post_dict.pop('is_announcement'))
        post_dict['createdAt'] = post_dict.pop('created_at')
        post_dict['authorImage'] = post_dict.pop('author_image')
        posts.append(post_dict)
    return posts

def create_post(post_data):
    conn = get_db_connection()
    post_id = generate_id()
    created_at = datetime.now().isoformat()
    is_ann = post_data.get('is_announcement', False)
    
    conn.execute('''
    INSERT INTO posts (id, title, caption, image, likes, author, author_image, is_announcement, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (post_id, post_data['title'], post_data.get('caption', ''), post_data.get('image', ''),
          0, post_data.get('author', 'Campus Student'), post_data.get('author_image', ''), is_ann, created_at))
    
    conn.commit()
    conn.close()
    
    return {
        'id': post_id,
        'title': post_data['title'],
        'caption': post_data.get('caption', ''),
        'image': post_data.get('image', ''),
        'likes': 0,
        'author': post_data.get('author', 'Campus Student'),
        'authorImage': post_data.get('author_image', ''),
        'isAnnouncement': is_ann,
        'createdAt': created_at
    }

def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def like_post(post_id):
    conn = get_db_connection()
    conn.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
    conn.commit()
    
    # Fetch the updated post
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    
    if post:
        post_dict = dict(post)
        post_dict['isAnnouncement'] = bool(post_dict.pop('is_announcement'))
        post_dict['createdAt'] = post_dict.pop('created_at')
        post_dict['authorImage'] = post_dict.pop('author_image')
        return post_dict
    return None

def clear_all_posts():
    conn = get_db_connection()
    conn.execute('DELETE FROM posts')
    conn.commit()
    conn.close()

# ── EVENT OPERATIONS ──

def get_all_events():
    conn = get_db_connection()
    events_rows = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return [dict(e) for e in events_rows]

# ── REGISTRATION OPERATIONS ──

def get_all_registrations():
    conn = get_db_connection()
    regs_rows = conn.execute('SELECT * FROM registrations ORDER BY created_at DESC').fetchall()
    conn.close()
    
    regs = []
    for row in regs_rows:
        reg_dict = dict(row)
        reg_dict['class'] = reg_dict.pop('class_name')
        reg_dict['createdAt'] = reg_dict.pop('created_at')
        regs.append(reg_dict)
    return regs

def create_registration(reg_data):
    conn = get_db_connection()
    reg_id = generate_id()
    created_at = datetime.now().isoformat()
    
    conn.execute('''
    INSERT INTO registrations (id, event, name, email, class_name, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (reg_id, reg_data['event'], reg_data['name'], reg_data['email'], reg_data['class'], created_at))
    
    conn.commit()
    conn.close()
    
    return {
        'id': reg_id,
        'event': reg_data['event'],
        'name': reg_data['name'],
        'email': reg_data['email'],
        'class': reg_data['class'],
        'createdAt': created_at
    }

def delete_registration(reg_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM registrations WHERE id = ?', (reg_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def clear_all_registrations():
    conn = get_db_connection()
    conn.execute('DELETE FROM registrations')
    conn.commit()
    conn.close()

# ── ANNOUNCEMENT OPERATIONS ──

def create_announcement(data):
    conn = get_db_connection()
    post_id = generate_id()
    created_at = datetime.now().isoformat()
    
    # 1. Add as a regular post so students can see it
    conn.execute('''
    INSERT INTO posts (id, title, caption, image, likes, author, author_image, is_announcement, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (post_id, '📢 ' + data['title'], data['message'], 
          'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=800',
          0, 'Admin', 'images/profile1.png', True, created_at))
    
    conn.commit()
    conn.close()
    
    return {
        'id': post_id,
        'title': data['title'],
        'message': data['message'],
        'createdAt': created_at
    }

# ── COMMENT OPERATIONS ──

def get_comments_for_post(post_id):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC', (post_id,)).fetchall()
    conn.close()
    
    comments = []
    for r in rows:
        c_dict = dict(r)
        c_dict['createdAt'] = c_dict.pop('created_at')
        c_dict['postId'] = c_dict.pop('post_id')
        comments.append(c_dict)
    return comments

def create_comment(post_id, data):
    conn = get_db_connection()
    comment_id = generate_id()
    created_at = datetime.now().isoformat()
    
    conn.execute('''
    INSERT INTO comments (id, post_id, author, content, created_at)
    VALUES (?, ?, ?, ?, ?)
    ''', (comment_id, post_id, data['author'], data['content'], created_at))
    
    conn.commit()
    conn.close()
    
    return {
        'id': comment_id,
        'postId': post_id,
        'author': data['author'],
        'content': data['content'],
        'createdAt': created_at
    }

def get_user_count():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    conn.close()
    return count
