-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Message types enum; can be expanded to include additional channels
CREATE TYPE channel_type AS ENUM ('email', 'sms');

-- Messages table for storing messages contents
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_type channel_type NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Message Logs table for storing message delivery statuses
CREATE TABLE message_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES messages(id),
    delivery_status VARCHAR(20) NOT NULL,  -- 'pending', 'delivered', 'failed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    provider_response TEXT
);

-- Indexes for faster querying based on channel_type and message_ID
CREATE INDEX idx_messages_channel ON messages(channel_type);
CREATE INDEX idx_message_logs_message_id ON message_logs(message_id);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;
