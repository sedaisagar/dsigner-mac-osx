"""
Event Processor - Standalone service that subscribes to Redis events and processes them.
Run this separately from the main application.
"""
from services.event_publisher import get_publisher
from services.event_subscriber import EventSubscriber, EventProcessor
from ui.event_dashboard_launcher import (
    handle_key_submission_with_ui,
    handle_profile_event_with_ui,
    handle_processing_result_with_ui
)
import logging
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the event processor."""
    logger.info("Starting Event Processor...")
    
    # Initialize publisher and subscriber
    try:
        publisher = get_publisher()
        subscriber = EventSubscriber()
        processor = EventProcessor(publisher, subscriber)
        logger.info("Event processor initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize event processor: {e}")
        logger.error("Make sure Redis is running!")
        sys.exit(1)
    
    # Define handlers for different topics
    def handle_key_submission(topic: str, event_data: dict):
        """Handle key submission events."""
        logger.info(f"Received key submission event from topic '{topic}'")
        # Process the event
        processor.process_key_submission(topic, event_data)
        # Show UI notification
        handle_key_submission_with_ui(topic, event_data)
    
    def handle_profile_event(topic: str, event_data: dict):
        """Handle profile-related events."""
        logger.info(f"Received profile event from topic '{topic}'")
        # Process the event
        processor.process_profile_events(topic, event_data)
        # Show UI notification
        handle_profile_event_with_ui(topic, event_data)
    
    def handle_processing_result(topic: str, event_data: dict):
        """Handle processed results (for logging/demonstration)."""
        logger.info(f"Processing result received: {event_data.get('event_type', 'unknown')}")
        logger.info(f"Result details: {event_data.get('result', {})}")
        # Show UI notification
        handle_processing_result_with_ui(topic, event_data)
    
    # Subscribe to topics with handlers
    topic_handlers = {
        'key_submission': handle_key_submission,
        'profile_events': handle_profile_event,
        'processing_results': handle_processing_result
    }
    
    subscriber.subscribe_to_topics(topic_handlers)
    logger.info("Subscribed to all topics. Listening for events...")
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("\nShutting down event processor...")
        subscriber.stop()
        publisher.close()
        subscriber.close()
        logger.info("Event processor stopped")
        logger.info(f"Final stats: {processor.get_stats()}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep the main thread alive
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()

