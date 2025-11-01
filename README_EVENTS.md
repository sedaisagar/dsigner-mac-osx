# Event-Based Architecture with Redis

This project implements an event-driven architecture using Redis pub/sub for asynchronous event processing.

## Architecture Overview

```
┌─────────────────┐         ┌──────────────┐         ┌──────────────────┐
│   Publisher     │────────▶│    Redis     │────────▶│   Subscriber     │
│   (Producer)    │ publish │   Channels   │subscribe│   (Consumer)     │
└─────────────────┘         └──────────────┘         └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ Event Processor  │
                            │  (Processes &    │
                            │   Publishes)     │
                            └──────────────────┘
```

## Components

### 1. EventPublisher (`services/event_publisher.py`)
- Publishes events to Redis topics/channels
- Singleton pattern for connection management
- Built-in methods for common events:
  - `publish_key_submitted()` - Publishes to `key_submission` topic
  - `publish_profile_created()` - Publishes to `profile_events` topic
  - `publish_profile_updated()` - Publishes to `profile_events` topic
  - `publish_profile_deleted()` - Publishes to `profile_events` topic
  - `publish()` - Generic publish method for custom topics

### 2. EventSubscriber (`services/event_subscriber.py`)
- Subscribes to Redis topics and processes events
- Supports multiple topics with different handlers
- Thread-safe event processing
- Graceful shutdown handling

### 3. EventProcessor (`services/event_subscriber.py`)
- Example processor demonstrating event handling
- Processes incoming events and publishes results to different topics
- Tracks processing statistics

### 4. Standalone Event Processor (`event_processor.py`)
- Ready-to-run subscriber service
- Subscribes to: `key_submission`, `profile_events`, `processing_results`
- Demonstrates the complete event flow

## Installation

1. **Install Redis** (if not already installed):
   ```bash
   # Windows (using Chocolatey)
   choco install redis-64
   
   # macOS (using Homebrew)
   brew install redis
   
   # Linux
   sudo apt-get install redis-server
   ```

2. **Start Redis Server**:
   ```bash
   redis-server
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Event Processor

In one terminal, start the event processor (subscriber):

```bash
python event_processor.py
```

This will:
- Connect to Redis
- Subscribe to topics: `key_submission`, `profile_events`, `processing_results`
- Listen for events and process them
- Publish processing results to `processing_results` topic

### Publishing Events

In another terminal or script, publish events:

#### Using the Demo Script

```bash
python demo_events.py
```

This demonstrates:
- Publishing key submission events
- Publishing profile events
- Publishing custom events to different topics

#### Programmatically

```python
from services.event_publisher import get_publisher

# Get publisher instance
publisher = get_publisher()

# Publish a key submission event
publisher.publish_key_submitted(
    key_value="my_secret_key_12345",
    token_name="Production Token"
)

# Publish a profile event
publisher.publish_profile_created(
    profile_id=1,
    profile_data={
        'dll_path': '/path/to/file.dll',
        'token_name': 'My Profile',
        'active': True
    }
)

# Publish a custom event
publisher.publish('my_custom_topic', {
    'event_type': 'custom_event',
    'data': {'foo': 'bar'}
})
```

### Creating Custom Event Handlers

```python
from services.event_subscriber import EventSubscriber
from services.event_publisher import get_publisher

# Initialize components
publisher = get_publisher()
subscriber = EventSubscriber()

# Define your handlers
def handle_my_event(topic: str, event_data: dict):
    print(f"Received on {topic}: {event_data}")
    
    # Process the event
    processed_data = {
        'event_type': 'processed',
        'original': event_data,
        'result': 'success'
    }
    
    # Publish result to another topic
    publisher.publish('results', processed_data)

# Subscribe with handlers
topic_handlers = {
    'my_topic': handle_my_event,
    'another_topic': handle_my_event
}

subscriber.subscribe_to_topics(topic_handlers)

# Keep running
import time
while True:
    time.sleep(1)
```

## Event Flow Example

1. **Publisher** sends event to `key_submission` topic:
   ```json
   {
     "event_type": "key_submitted",
     "key_value": "abc123",
     "token_name": "Token1",
     "timestamp": "2024-01-01T10:00:00"
   }
   ```

2. **Subscriber** receives the event and processes it

3. **EventProcessor** validates and processes the key

4. **Result** is published to `processing_results` topic:
   ```json
   {
     "event_type": "key_processed",
     "original_event": {...},
     "result": {
       "valid": true,
       "length": 6,
       "token_name": "Token1",
       "processed_at": "2024-01-01T10:00:01"
     }
   }
   ```

## Topics/Channels

| Topic | Description | Publishers | Subscribers |
|-------|-------------|------------|-------------|
| `key_submission` | Key submission events | Publisher | EventProcessor |
| `profile_events` | Profile CRUD operations | Publisher | EventProcessor |
| `processing_results` | Processed results | EventProcessor | EventProcessor |

You can create custom topics for any purpose!

## Redis Configuration

Default configuration:
- Host: `localhost`
- Port: `6379`
- Database: `0`

To change configuration, modify the initialization:

```python
from services.event_publisher import EventPublisher

# Custom Redis configuration
publisher = EventPublisher(host='192.168.1.100', port=6380, db=1)
```

## Error Handling

- All connections test with `ping()` before use
- Event handlers are wrapped in try-catch blocks
- Errors are logged but don't crash the processor
- Graceful shutdown on SIGINT/SIGTERM

## Monitoring

The `EventProcessor` tracks statistics:
- Keys processed
- Profiles processed
- Events published

View stats:
```python
stats = processor.get_stats()
print(stats)  # {'keys_processed': 10, 'profiles_processed': 5, 'events_published': 15}
```

## Best Practices

1. **Always run Redis**: Start `redis-server` before running processors
2. **Separate terminals**: Run publisher and subscriber in different terminals
3. **Error handling**: Implement robust error handling in event handlers
4. **Topics**: Use descriptive, namespaced topic names
5. **Clean shutdown**: Always call `stop()` or `close()` when done
6. **Thread safety**: Event handlers should be thread-safe

## Troubleshooting

**Connection refused**
- Make sure Redis is running: `redis-cli ping` should return `PONG`

**Events not received**
- Verify subscription: Check that subscriber is listening to correct topic
- Check Redis: `redis-cli MONITOR` to see all pub/sub activity

**Import errors**
- Install dependencies: `pip install -r requirements.txt`
- Check Python path: Make sure you're in the project directory

## Example Integration

To integrate with your existing dashboard:

```python
from services.event_publisher import get_publisher

class DashboardApp:
    def __init__(self, root):
        self.publisher = get_publisher()
        # ... rest of initialization
    
    def handle_key_submit(self, key_value, token_name):
        # Your business logic here
        result = validate_key(key_value)
        
        # Publish event for async processing
        self.publisher.publish_key_submitted(key_value, token_name)
```

## Next Steps

- Add database persistence for processed events
- Implement event replay/recovery
- Add event filtering and routing
- Monitor with Redis info/stats commands
- Scale with multiple processor instances
- Add authentication for Redis
- Implement event schema validation

## License

See LICENSE file for details.

