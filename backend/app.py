from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import database as db
import os

# Get parent directory path where HTML, CSS, JS files are stored
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

# Enable CORS for frontend applications (allowing localhost, file URLs, etc.)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def home():
    return send_from_directory(frontend_dir, 'index.html')

# ── AUTHENTICATION ROUTES ──

# Student Signup
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide all details'}), 400
        
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not name or not email or not password:
        return jsonify({'error': 'Please provide all details'}), 400
        
    # Check if user already exists
    existing = db.find_user_by_email(email)
    if existing:
        return jsonify({'error': 'User already exists with this email'}), 400
        
    try:
        new_user = db.create_user({'name': name, 'email': email, 'password': password})
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': new_user['id'],
                'name': new_user['name'],
                'email': new_user['email']
            }
        }), 201
    except Exception as e:
        print(f"Signup database error: {e}")
        return jsonify({'error': 'Failed to create user'}), 500

# Student Login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide email and password'}), 400
        
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Please provide email and password'}), 400
        
    user = db.find_user_by_email(email)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid email or password'}), 401
        
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }
    }), 200

# Admin Login
@app.route('/api/auth/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Please provide email and password'}), 400
        
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Please provide email and password'}), 400
        
    # Simple default Admin credentials
    ADMIN_EMAIL = 'admin@campus.com'
    ADMIN_PASSWORD = 'admin123'
    
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return jsonify({
            'message': 'Admin login successful',
            'user': {'email': ADMIN_EMAIL, 'role': 'admin'}
        }), 200
    else:
        return jsonify({'error': 'Invalid admin credentials'}), 401

# ── POSTS ROUTES ──

# Get all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        posts = db.get_all_posts()
        return jsonify(posts), 200
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return jsonify({'error': 'Failed to fetch posts'}), 500

# Create new post
@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
        
    try:
        new_post = db.create_post({
            'title': data.get('title'),
            'caption': data.get('caption', ''),
            'image': data.get('image', ''),
            'author': data.get('author', 'Campus Student'),
            'author_image': data.get('authorImage', '')
        })
        return jsonify(new_post), 201
    except Exception as e:
        print(f"Error creating post: {e}")
        return jsonify({'error': 'Failed to create post'}), 500

# Like a post
@app.route('/api/posts/<id>/like', methods=['POST'])
def like_post(id):
    try:
        updated = db.like_post(id)
        if updated:
            return jsonify(updated), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        print(f"Error liking post: {e}")
        return jsonify({'error': 'Failed to like post'}), 500

# Delete a post
@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        deleted = db.delete_post(id)
        if deleted:
            return jsonify({'message': 'Post deleted successfully'}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        print(f"Error deleting post: {e}")
        return jsonify({'error': 'Failed to delete post'}), 500

# ── COMMENTS FOR POSTS ──

# Get all comments for a post
@app.route('/api/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    try:
        comments = db.get_comments_for_post(post_id)
        return jsonify(comments), 200
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return jsonify({'error': 'Failed to fetch comments'}), 500

# Create a comment for a post
@app.route('/api/posts/<post_id>/comments', methods=['POST'])
def add_post_comment(post_id):
    data = request.get_json()
    if not data or not data.get('content') or not data.get('author'):
        return jsonify({'error': 'Author and comment content are required'}), 400
        
    try:
        new_comment = db.create_comment(post_id, {
            'author': data.get('author'),
            'content': data.get('content')
        })
        return jsonify(new_comment), 201
    except Exception as e:
        print(f"Error creating comment: {e}")
        return jsonify({'error': 'Failed to create comment'}), 500

# Clear all posts (Admin)
@app.route('/api/admin/clear-posts', methods=['DELETE'])
def clear_posts():
    try:
        db.clear_all_posts()
        return jsonify({'message': 'All posts cleared successfully'}), 200
    except Exception as e:
        print(f"Error clearing posts: {e}")
        return jsonify({'error': 'Failed to clear posts'}), 500

# ── EVENTS ROUTES ──

# Get all events
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = db.get_all_events()
        return jsonify(events), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({'error': 'Failed to fetch events'}), 500

# ── REGISTRATIONS ROUTES ──

# Register for an event
@app.route('/api/events/register', methods=['POST'])
def register_event():
    data = request.get_json()
    if not data or not data.get('event') or not data.get('name') or not data.get('email') or not data.get('class'):
        return jsonify({'error': 'All registration details are required'}), 400
        
    try:
        registration = db.create_registration({
            'event': data.get('event'),
            'name': data.get('name'),
            'email': data.get('email'),
            'class': data.get('class')
        })
        return jsonify(registration), 201
    except Exception as e:
        print(f"Error creating registration: {e}")
        return jsonify({'error': 'Failed to create registration'}), 500

# Get all registrations
@app.route('/api/events/registrations', methods=['GET'])
def get_registrations():
    try:
        registrations = db.get_all_registrations()
        return jsonify(registrations), 200
    except Exception as e:
        print(f"Error fetching registrations: {e}")
        return jsonify({'error': 'Failed to fetch registrations'}), 500

# Delete a registration
@app.route('/api/events/registrations/<id>', methods=['DELETE'])
def delete_registration(id):
    try:
        deleted = db.delete_registration(id)
        if deleted:
            return jsonify({'message': 'Registration deleted successfully'}), 200
        else:
            return jsonify({'error': 'Registration not found'}), 404
    except Exception as e:
        print(f"Error deleting registration: {e}")
        return jsonify({'error': 'Failed to delete registration'}), 500

# Clear all registrations (Admin)
@app.route('/api/admin/clear-registrations', methods=['DELETE'])
def clear_registrations():
    try:
        db.clear_all_registrations()
        return jsonify({'message': 'All registrations cleared successfully'}), 200
    except Exception as e:
        print(f"Error clearing registrations: {e}")
        return jsonify({'error': 'Failed to clear registrations'}), 500

# ── ANNOUNCEMENTS ROUTES ──

# Create announcement
@app.route('/api/admin/announcement', methods=['POST'])
def create_announcement():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('message'):
        return jsonify({'error': 'Title and message are required'}), 400
        
    try:
        announce = db.create_announcement({
            'title': data.get('title'),
            'message': data.get('message')
        })
        return jsonify(announce), 201
    except Exception as e:
        print(f"Error creating announcement: {e}")
        return jsonify({'error': 'Failed to create announcement'}), 500

# Get total user count
@app.route('/api/admin/users/count', methods=['GET'])
def get_users_count():
    try:
        count = db.get_user_count()
        return jsonify({'count': count}), 200
    except Exception as e:
        print(f"Error fetching user count: {e}")
        return jsonify({'error': 'Failed to fetch user count'}), 500

if __name__ == '__main__':
    # Start Flask app on port 3000
    app.run(host='0.0.0.0', port=3000, debug=True)

