from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from supabase import create_client
import os

app = Flask(__name__)

# Supabase setup
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Check Whitelist by Roblox UserId
@app.route('/check/<user_id>')
def check_whitelist(user_id):
    # Query by user_id field (text)
    response = supabase_client.table('whitelists').select('*').eq('user_id', user_id).execute()

    if response.data:
        expire_time = datetime.fromisoformat(response.data[0]['expire_at'])
        if datetime.utcnow() < expire_time:
            return jsonify({'isWhitelisted': True})

    return jsonify({'isWhitelisted': False})

# ✅ Creator Page
@app.route('/api/creator')
def creator_page():
    return render_template('creator.html')

# ✅ Whitelist Creator (POST form)
@app.route('/api/whitelist', methods=['POST'])
def add_whitelist():
    user_id = request.form.get('user_id')  # Roblox UserId
    access_time = int(request.form.get('access_time'))  # Access time in seconds

    expire_at = (datetime.utcnow() + timedelta(seconds=access_time)).isoformat()

    # Insert with user_id as text
    supabase_client.table('whitelists').insert({
        'user_id': user_id,
        'expire_at': expire_at
    }).execute()

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
