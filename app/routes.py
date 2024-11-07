from flask import Blueprint, request, jsonify
from app.models_pydantic import MessageRequest, MessageResponse, MessageLogResponse
from app.models_sqlachemy import Message, MessageLog
from app import db
from pydantic import ValidationError

api_bp = Blueprint('api', __name__)

@api_bp.route('/hello')
def hello():
    return "Hello from Communication Microservice!"

@api_bp.route('/sendMessage', methods=['POST'])
def send_message():
	"""Send a message"""
	try:
		# Validate request data using Pydantic
		request_data = MessageRequest(**request.json)
	
		# Create new message
		message = Message(
			channel_type=request_data.channel_type,
			recipient=request_data.recipient,
			content=request_data.content
		)

		db.session.add(message)
		
		# Add initial log entry
		log = MessageLog(
			message_id=message.id,
			delivery_status='pending'
		)

		db.session.add(log)
		
		# Commit both message and log
		db.session.commit()
		
		# Return response using Pydantic model
		response = MessageResponse(
      		id=message.id,
			channel_type=message.channel_type,
			recipient=message.recipient,
			content=message.content,
			created_at=message.created_at
		)
		
		return jsonify(response.model_dump()), 201
	except ValidationError as e:
		return jsonify({'error': str(e)}), 400
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500

@api_bp.route('/getMessages', methods=['GET'])
def get_messages():
    """Get all messages"""
    try:
        messages = Message.query.all()
        return jsonify([{
            'id': str(msg.id),
            'channel_type': msg.channel_type,
            'recipient': msg.recipient,
            'content': msg.content,
            'created_at': msg.created_at.isoformat()
        } for msg in messages])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
