import redis
import json
import logging
import threading
from typing import Callable, Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventSubscriber:
    """
    Event subscriber that subscribes to Redis topics and processes events.
    """
    
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initialize the Redis event subscriber.
        
        Args:
            host: Redis host (default: localhost)
            port: Redis port (default: 6379)
            db: Redis database number (default: 0)
        """
        try:
            self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.pubsub = self.redis_client.pubsub()
            # Test connection
            self.redis_client.ping()
            self.running = False
            self.subscription_thread = None
            logger.info(f"Connected to Redis at {host}:{port}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def subscribe(self, topics: List[str], handler: Callable[[str, Dict[str, Any]], None]):
        """
        Subscribe to one or more topics and set up a handler.
        
        Args:
            topics: List of topics to subscribe to
            handler: Callback function that receives (topic, event_data)
        """
        for topic in topics:
            self.pubsub.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
        
        self.event_handler = handler
        self.running = True
        self.subscription_thread = threading.Thread(target=self._listen_for_events, daemon=True)
        self.subscription_thread.start()
        logger.info("Event listener started")
    
    def subscribe_to_topics(self, topic_handlers: Dict[str, Callable[[str, Dict[str, Any]], None]]):
        """
        Subscribe to multiple topics with different handlers for each.
        
        Args:
            topic_handlers: Dictionary mapping topic names to handler functions
        """
        for topic in topic_handlers.keys():
            self.pubsub.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
        
        self.topic_handlers = topic_handlers
        self.running = True
        self.subscription_thread = threading.Thread(target=self._listen_for_events_multiple_handlers, daemon=True)
        self.subscription_thread.start()
        logger.info("Event listener started with multiple handlers")
    
    def _listen_for_events(self):
        """Internal method to listen for events and call the handler."""
        try:
            for message in self.pubsub.listen():
                if not self.running:
                    break
                
                if message['type'] == 'message':
                    topic = message['channel']
                    try:
                        event_data = json.loads(message['data'])
                        logger.info(f"Received event on topic '{topic}': {event_data.get('event_type', 'unknown')}")
                        
                        # Call the handler in a separate thread to avoid blocking
                        thread = threading.Thread(
                            target=self._safe_call_handler,
                            args=(topic, event_data, self.event_handler),
                            daemon=True
                        )
                        thread.start()
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse event JSON: {e}")
                    except Exception as e:
                        logger.error(f"Error processing event: {e}")
        except Exception as e:
            logger.error(f"Error in event listener: {e}")
    
    def _listen_for_events_multiple_handlers(self):
        """Internal method to listen for events and call appropriate handler based on topic."""
        try:
            for message in self.pubsub.listen():
                if not self.running:
                    break
                
                if message['type'] == 'message':
                    topic = message['channel']
                    try:
                        event_data = json.loads(message['data'])
                        logger.info(f"Received event on topic '{topic}': {event_data.get('event_type', 'unknown')}")
                        
                        # Get the appropriate handler for this topic
                        handler = self.topic_handlers.get(topic)
                        if handler:
                            thread = threading.Thread(
                                target=self._safe_call_handler,
                                args=(topic, event_data, handler),
                                daemon=True
                            )
                            thread.start()
                        else:
                            logger.warning(f"No handler registered for topic: {topic}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse event JSON: {e}")
                    except Exception as e:
                        logger.error(f"Error processing event: {e}")
        except Exception as e:
            logger.error(f"Error in event listener: {e}")
    
    def _safe_call_handler(self, topic: str, event_data: Dict[str, Any], handler: Callable):
        """Safely call the handler with error handling."""
        try:
            handler(topic, event_data)
        except Exception as e:
            logger.error(f"Error in event handler: {e}", exc_info=True)
    
    def stop(self):
        """Stop the event subscriber."""
        self.running = False
        self.pubsub.unsubscribe()
        if self.subscription_thread and self.subscription_thread.is_alive():
            self.subscription_thread.join(timeout=5)
        logger.info("Event subscriber stopped")
    
    def close(self):
        """Close the Redis connection."""
        self.stop()
        if hasattr(self, 'redis_client'):
            self.redis_client.close()
            logger.info("Redis connection closed")


class EventProcessor:
    """
    Example event processor that demonstrates processing events and publishing to different topics.
    """
    
    def __init__(self, publisher: 'EventPublisher', subscriber: EventSubscriber):
        """
        Initialize the event processor.
        
        Args:
            publisher: EventPublisher instance for publishing processed events
            subscriber: EventSubscriber instance for receiving events
        """
        self.publisher = publisher
        self.subscriber = subscriber
        self.stats = {
            'keys_processed': 0,
            'profiles_processed': 0,
            'events_published': 0
        }
    
    def process_key_submission(self, topic: str, event_data: Dict[str, Any]):
        """
        Process a key submission event.
        
        This is an example of processing an event and publishing a result to a different topic.
        """
        logger.info(f"Processing key submission event: {event_data}")
        
        key_value = event_data.get('key_value', '')
        token_name = event_data.get('token_name', '')
        
        # Example processing logic
        processed_result = {
            'valid': len(key_value) > 0,
            'length': len(key_value),
            'token_name': token_name,
            'processed_at': self._get_current_timestamp()
        }
        
        # Publish processed result to a different topic
        result_event = {
            'event_type': 'key_processed',
            'original_event': event_data,
            'result': processed_result
        }
        self.publisher.publish('processing_results', result_event)
        self.stats['keys_processed'] += 1
        self.stats['events_published'] += 1
        
        logger.info(f"Published processing result for key submission")
    
    def process_profile_events(self, topic: str, event_data: Dict[str, Any]):
        """
        Process profile-related events.
        """
        logger.info(f"Processing profile event: {event_data}")
        
        event_type = event_data.get('event_type', '')
        
        # Example processing logic
        processed_result = {
            'event_type': event_type,
            'processed': True,
            'processed_at': self._get_current_timestamp()
        }
        
        # Publish processed result to a different topic
        result_event = {
            'event_type': 'profile_processed',
            'original_event': event_data,
            'result': processed_result
        }
        self.publisher.publish('processing_results', result_event)
        self.stats['profiles_processed'] += 1
        self.stats['events_published'] += 1
        
        logger.info(f"Published processing result for profile event: {event_type}")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_stats(self) -> Dict[str, int]:
        """Get processing statistics."""
        return self.stats.copy()


def create_key_processor(publisher: 'EventPublisher') -> Callable:
    """
    Factory function to create a key submission event processor.
    
    Args:
        publisher: EventPublisher instance
        
    Returns:
        Handler function
    """
    def handle_key_submission(topic: str, event_data: Dict[str, Any]):
        logger.info(f"Key submission received: {event_data}")
        # Your processing logic here
        result_event = {
            'event_type': 'key_processed',
            'original_data': event_data,
            'status': 'success'
        }
        publisher.publish('processing_results', result_event)
    
    return handle_key_submission

