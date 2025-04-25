# app.py
from flask import Flask, render_template, request, jsonify
from chatbot_agent import get_instant_answer
import uuid
from datetime import datetime
from typing import Dict, List, Any

app = Flask(__name__)

# In-memory database simulation (replace with real database in production)
chats_db: Dict[str, Dict[str, Any]] = {}

def initialize_chat(chat_id: str) -> Dict[str, Any]:
    """Initialize a new chat with welcome message"""
    chat = {
        'id': chat_id,
        'title': 'New Chat',
        'created_at': datetime.now().isoformat(),
        'messages': [
            {
                'role': 'assistant',
                'content': "Hello! I'm your research assistant. Ask me anything and I'll find the latest information for you."
            }
        ]
    }
    chats_db[chat_id] = chat
    return chat

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/new_chat', methods=['POST'])
def create_new_chat():
    """Create a new chat session"""
    chat_id = str(uuid.uuid4())
    chat = initialize_chat(chat_id)
    return jsonify({
        'chat_id': chat_id,
        'title': chat['title']
    })

@app.route('/api/chat/<chat_id>', methods=['POST'])
def handle_chat_message(chat_id: str):
    """Process user message and return AI response"""
    if chat_id not in chats_db:
        return jsonify({'error': 'Chat not found'}), 404
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Add user message to chat history
    chats_db[chat_id]['messages'].append({
        'role': 'user',
        'content': user_message
    })
    
    # Get AI response
    try:
        ai_response = get_instant_answer(user_message)
    except Exception as e:
        ai_response = f"Sorry, I encountered an error: {str(e)}"
    
    # Add AI response to chat history
    chats_db[chat_id]['messages'].append({
        'role': 'assistant',
        'content': ai_response
    })
    
    # Update chat title if it's the first exchange
    if len(chats_db[chat_id]['messages']) == 3:  # Welcome + user + AI
        short_title = (user_message[:20] + '...') if len(user_message) > 20 else user_message
        chats_db[chat_id]['title'] = short_title or 'New Chat'
    
    return jsonify({
        'status': 'complete',
        'messages': chats_db[chat_id]['messages'],
        'title': chats_db[chat_id]['title']
    })

@app.route('/api/chat/<chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id: str):
    """Retrieve all messages for a specific chat"""
    if chat_id not in chats_db:
        return jsonify({'error': 'Chat not found'}), 404
    return jsonify({'messages': chats_db[chat_id]['messages']})

@app.route('/api/chats', methods=['GET'])
def get_all_chats():
    """Get list of all chat sessions (sorted by newest first)"""
    chats = sorted(
        chats_db.values(),
        key=lambda x: x['created_at'],
        reverse=True
    )
    return jsonify({'chats': chats})

@app.route('/api/chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id: str):
    """Delete a chat session"""
    if chat_id not in chats_db:
        return jsonify({'error': 'Chat not found'}), 404
    
    del chats_db[chat_id]
    return jsonify({'status': 'deleted'})

@app.route('/api/status')
def status_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'chats_count': len(chats_db)})

if __name__ == '__main__':
    # Pre-warm the AI models by initializing a dummy chat
    dummy_chat_id = str(uuid.uuid4())
    initialize_chat(dummy_chat_id)
    chats_db[dummy_chat_id]['messages'].append({
        'role': 'user',
        'content': 'ping'
    })
    try:
        get_instant_answer('ping')
    except Exception as e:
        print(f"Model warmup failed: {e}")
    
    # Delete the dummy chat
    del chats_db[dummy_chat_id]
    
    app.run(host='0.0.0.0', port=5000, debug=True)