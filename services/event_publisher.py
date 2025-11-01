import redis
import json
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Event publisher that publishes events to Redis topics.
    """
    
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initialize the Redis event publisher.
        
        Args:
            host: Redis host (default: localhost)
            port: Redis port (default: 6379)
            db: Redis database number (default: 0)
        """
        try:
            self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis at {host}:{port}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def publish(self, topic: str, event: Dict[str, Any]) -> bool:
        """
        Publish an event to a Redis topic.
        
        Args:
            topic: The topic/channel to publish to
            event: Dictionary containing event data
            
        Returns:
            bool: True if published successfully, False otherwise
        """
        try:
            # Add timestamp to event
            event_with_timestamp = {
                **event,
                'timestamp': event.get('timestamp', self._get_current_timestamp())
            }
            
            # Serialize event to JSON
            event_json = json.dumps(event_with_timestamp)
            
            # Publish to Redis
            result = self.redis_client.publish(topic, event_json)
            logger.info(f"Published event to topic '{topic}': {event_with_timestamp.get('event_type', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish event to topic '{topic}': {e}")
            return False
    
    def publish_key_submitted(self, key_value: str, token_name: str, user_id: Optional[str] = None):
        """
        Publish a key submission event.
        
        Args:
            key_value: The submitted key value
            token_name: The associated token name
            user_id: Optional user identifier
        """
        event = {
            'event_type': 'key_submitted',
            'key_value': key_value,
            'token_name': token_name,
            'user_id': user_id
        }
        return self.publish('key_submission', event)
    
    def publish_profile_created(self, profile_id: int, profile_data: Dict[str, Any]):
        """
        Publish a profile creation event.
        
        Args:
            profile_id: The created profile ID
            profile_data: Profile data
        """
        event = {
            'event_type': 'profile_created',
            'profile_id': profile_id,
            'profile_data': profile_data
        }
        return self.publish('profile_events', event)
    
    def publish_profile_updated(self, profile_id: int, profile_data: Dict[str, Any]):
        """
        Publish a profile update event.
        
        Args:
            profile_id: The updated profile ID
            profile_data: Updated profile data
        """
        event = {
            'event_type': 'profile_updated',
            'profile_id': profile_id,
            'profile_data': profile_data
        }
        return self.publish('profile_events', event)
    
    def publish_profile_deleted(self, profile_id: int):
        """
        Publish a profile deletion event.
        
        Args:
            profile_id: The deleted profile ID
        """
        event = {
            'event_type': 'profile_deleted',
            'profile_id': profile_id
        }
        return self.publish('profile_events', event)
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def close(self):
        """Close the Redis connection."""
        if hasattr(self, 'redis_client'):
            self.redis_client.close()
            logger.info("Redis connection closed")


# Singleton instance
_publisher_instance = None

def get_publisher(host='localhost', port=6379, db=0) -> EventPublisher:
    """
    Get or create a singleton EventPublisher instance.
    
    Args:
        host: Redis host
        port: Redis port
        db: Redis database number
        
    Returns:
        EventPublisher instance
    """
    global _publisher_instance
    if _publisher_instance is None:
        _publisher_instance = EventPublisher(host=host, port=port, db=db)
    return _publisher_instance

