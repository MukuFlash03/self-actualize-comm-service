from flask import Blueprint, request, jsonify
from app.models_pydantic import MessageRequest, MessageResponse, MessageLogResponse
from app.models_sqlachemy import Message, MessageLog
from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from app import db
from pydantic import ValidationError
import logging

# Configure basic logging settings with timestamp, logger name, level and message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger instance for this module
logger = logging.getLogger(__name__)

# Create a Blueprint instance for the API routes
api_bp = Blueprint('api', __name__)

# Define a dictionary of available message services, can be extended to include other services
services = {
    'email': EmailService(),
    'sms': SMSService()
}

# Define a route for the root URL
@api_bp.route('/')
def hello():
    return "Hello from Communication Microservice!"

# Define a route for sending a message
@api_bp.route('/api/sendMessage', methods=['POST'])
def send_message():
	"""Send a message"""
	try:
		# Validate request data using Pydantic
		request_data = MessageRequest(**request.json)
		logger.info(f"Received message request for {request_data.channel_type} channel to {request_data.recipient}")
        
		# Get appropriate service
		service = services.get(request_data.channel_type.lower())
		if not service:
			logger.error(f"Unsupported channel type: {request_data.channel_type}")
			return jsonify({"error": f"Unsupported channel type: {request_data.channel_type}"}), 400

    # Validate recipient format
		if not service.validate_recipient(request_data.recipient):
			logger.error(f"Invalid recipient format: {request_data.recipient}")
			return jsonify({"error": "Invalid recipient format"}), 400
	
		# Create new message
		message = Message(
			channel_type=request_data.channel_type,
			recipient=request_data.recipient,
			content=request_data.content
		)

    # Add message to database
		logger.info(f"Adding new message for {request_data.recipient} via {request_data.channel_type}...")
		db.session.add(message)
    
    # Commit message to database
		logger.info(f"Flushing message to database")
		db.session.flush()

		# Attempt to send message
		logger.info(f"Attempting to send message to {request_data.recipient} via {request_data.channel_type} service...")
		result = service.send_message(request_data.recipient, request_data.content)
		
		# Add initial log entry
		log = MessageLog(
			message_id=message.id,
			created_at=message.created_at,
      delivery_status=result["status"],
      error_message=result.get("error"),
			provider_response=result.get("provider_response")
		)

    # Add log entry to database
		logger.info(f"Adding new message log for {request_data.recipient} via {request_data.channel_type}...")
		db.session.add(log)
		
		# Commit both message and log
		logger.info(f"Committing message and log to database")
		db.session.commit()
		
		# Return response using Pydantic model
		response = MessageResponse(
        id=message.id,
        channel_type=message.channel_type,
        recipient=message.recipient,
        content=message.content,
        created_at=message.created_at
		)
		
		logger.info(f"Returning response for {request_data.recipient} via {request_data.channel_type}...")
		return jsonify(response.model_dump()), 201
	except ValidationError as e:
		logger.error(f"Validation error: {e}")
		return jsonify({'error': str(e)}), 400
	except Exception as e:
		logger.error(f"Error: {e}")
		logger.error(f"Rolling back database session...")
		db.session.rollback()
		return jsonify({'error': str(e)}), 500

# Define a route for getting all messages
@api_bp.route('/api/getMessages', methods=['GET'])
def get_messages():
    """Get all messages"""
    try:
        # Get all messages from database using SQLAlchemy ORM
        messages = Message.query.all()
        logger.info(f"Returning {len(messages)} messages...")

        return jsonify([{
            'id': str(msg.id),
            'channel_type': msg.channel_type,
            'recipient': msg.recipient,
            'content': msg.content,
            'created_at': msg.created_at.isoformat()
        } for msg in messages])
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Define a route for getting all message logs
@api_bp.route('/api/getMessageLogs', methods=['GET'])
def get_message_logs():
    """Get all message logs"""    
    try:
        # Get all message logs from database using SQLAlchemy ORM
        message_logs = MessageLog.query.all()
        logger.info(f"Returning {len(message_logs)} message logs...")

        return jsonify([{
            'id': str(log.id),
            'message_id': str(log.message_id),
            'delivery_status': log.delivery_status,
            'created_at': log.created_at.isoformat(),
            'logged_at': log.logged_at.isoformat(),
            'error_message': log.error_message,
            'provider_response': log.provider_response
        } for log in message_logs])
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
