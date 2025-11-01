"""
Demonstration script for event-based architecture using Redis.
This script demonstrates publishing events and processing them.
"""
from services.event_publisher import get_publisher
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_key_events():
    """Demonstrate key submission events."""
    logger.info("=== Key Submission Events Demo ===")
    
    try:
        publisher = get_publisher()
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        logger.error("Please make sure Redis is running on localhost:6379")
        return
    
    # Publish some sample key submission events
    logger.info("Publishing sample key submission events...")
    
    publisher.publish_key_submitted(
        key_value="sample_key_12345",
        token_name="Demo Token 1"
    )
    time.sleep(0.5)
    
    publisher.publish_key_submitted(
        key_value="another_key_67890",
        token_name="Demo Token 2"
    )
    time.sleep(0.5)
    
    publisher.publish_key_submitted(
        key_value="test_key_abcdef",
        token_name="Production Token"
    )
    
    logger.info("Key submission events published!")
    logger.info("\nTip: Run 'python event_processor.py' in another terminal to see these events processed.")


def demo_profile_events():
    """Demonstrate profile-related events."""
    logger.info("\n=== Profile Events Demo ===")
    
    try:
        publisher = get_publisher()
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return
    
    # Publish some sample profile events
    logger.info("Publishing sample profile events...")
    
    publisher.publish_profile_created(
        profile_id=1,
        profile_data={
            'dll_path': '/path/to/demo.dll',
            'token_name': 'Demo Profile',
            'active': True
        }
    )
    time.sleep(0.5)
    
    publisher.publish_profile_updated(
        profile_id=1,
        profile_data={
            'dll_path': '/path/to/updated_demo.dll',
            'token_name': 'Updated Demo Profile',
            'active': True
        }
    )
    time.sleep(0.5)
    
    publisher.publish_profile_deleted(profile_id=1)
    
    logger.info("Profile events published!")
    logger.info("\nTip: Run 'python event_processor.py' in another terminal to see these events processed.")


def demo_custom_events():
    """Demonstrate publishing custom events."""
    logger.info("\n=== Custom Events Demo ===")
    
    try:
        publisher = get_publisher()
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return
    
    # Publish custom events to various topics
    logger.info("Publishing custom events...")
    
    # Custom event to 'user_actions' topic
    publisher.publish('user_actions', {
        'event_type': 'button_clicked',
        'button_name': 'submit',
        'timestamp': '2024-01-01T10:00:00'
    })
    time.sleep(0.5)
    
    # Custom event to 'system_events' topic
    publisher.publish('system_events', {
        'event_type': 'system_startup',
        'mode': 'production',
        'configuration': {
            'database': 'connected',
            'redis': 'connected'
        }
    })
    
    logger.info("Custom events published!")
    logger.info("\nTip: You can subscribe to 'user_actions' and 'system_events' topics using event_processor.py")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("REDIS EVENT-BASED ARCHITECTURE DEMONSTRATION")
    print("="*70)
    print("\nThis script demonstrates publishing events to Redis topics.")
    print("Make sure Redis is running and you have event_processor.py running")
    print("in another terminal to see the events being processed.\n")
    
    try:
        demo_key_events()
        time.sleep(2)
        
        demo_profile_events()
        time.sleep(2)
        
        demo_custom_events()
        
        print("\n" + "="*70)
        print("Demo completed!")
        print("="*70)
        print("\nTo process these events:")
        print("1. Make sure Redis is running (redis-server)")
        print("2. Run: python event_processor.py")
        print("3. Run this demo script again")
        
    except KeyboardInterrupt:
        logger.info("\nDemo interrupted by user")
    except Exception as e:
        logger.error(f"Error during demo: {e}")


if __name__ == "__main__":
    main()

