from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from supabase import create_client
from dateutil import parser
import os

app = Flask(__name__)

# ✅ Supabase setup
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Check Whitelist by Roblox UserId
@app.route('/check/<user_id>')
def check_whitelist(user_id):
    try:
        user_id = str(user_id)

        response = supabase_client.table('whitelists').select('*').eq('id', user_id).execute()

        if response.data:
            record = response.data[0]
            expire_time = parser.isoparse(record['expire_at'])

            if datetime.utcnow() < expire_time:
                return jsonify({'isWhitelisted': True})

        return jsonify({'isWhitelisted': False})

    except Exception as e:
        return jsonify({'error': str(e), 'isWhitelisted': False}), 500

# ✅ Creator Page
@app.route('/api/creator')
def creator_page():
    return render_template('creator.html')

# ✅ Whitelist Creator (POST form)
@app.route('/api/whitelist', methods=['POST'])
def add_whitelist():
    try:
        user_id = request.form.get('user_id')
        access_time = int(request.form.get('access_time'))
        expire_at = (datetime.utcnow() + timedelta(seconds=access_time)).isoformat()

        supabase_client.table('whitelists').insert({
            'id': user_id,         # 👈 Set id = user_id
            'user_id': user_id,
            'expire_at': expire_at
        }).execute()

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
