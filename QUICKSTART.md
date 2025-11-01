# Quick Start Guide - Event-Based Redis Setup

Get started with the event-driven architecture in 5 minutes!

## Step 1: Start Redis

Open a terminal and start Redis:

```bash
redis-server
```

You should see Redis start successfully.

**Alternative** (if not installed):
- Windows: `choco install redis-64` or download from https://redis.io/download
- macOS: `brew install redis`
- Linux: `sudo apt-get install redis-server`

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Test Redis Connection

```bash
python test_redis_connection.py
```

You should see all tests passing ✓

## Step 4: Start Event Processor

Open a **new terminal** and run:

```bash
python event_processor.py
```

This will subscribe to events and process them. You should see:
```
INFO:__main__:Starting Event Processor...
INFO:__main__:Connected to Redis at localhost:6379
INFO:__main__:Subscribed to topic: key_submission
INFO:__main__:Subscribed to topic: profile_events
INFO:__main__:Subscribed to topic: processing_results
INFO:__main__:Event listener started with multiple handlers
INFO:__main__:Subscribed to all topics. Listening for events...
```

**Keep this terminal running!**

## Step 5: Publish Events

Open **another terminal** and run:

```bash
python demo_events.py
```

You should see events being published and processed!

## What Just Happened?

1. `event_processor.py` subscribed to Redis topics and is listening
2. `demo_events.py` published events to those topics
3. Events were received, processed, and results published to new topics
4. The full flow completed asynchronously!

## Next Steps

### Publish Your Own Events

Create a script:

```python
from services.event_publisher import get_publisher

publisher = get_publisher()
publisher.publish_key_submitted("my_key_123", "My Token")
```

Run it while `event_processor.py` is running - you'll see it get processed!

### Create Custom Handlers

Edit `event_processor.py` to add your own event processing logic.

### Integrate with Your App

Import the publisher wherever you need to trigger events:

```python
from services.event_publisher import get_publisher

publisher = get_publisher()
publisher.publish('my_topic', {'data': 'anything'})
```

## Troubleshooting

**"Connection refused"**
- Make sure Redis is running: `redis-server`

**"Module not found"**
- Install dependencies: `pip install -r requirements.txt`

**Events not being processed**
- Make sure `event_processor.py` is running in another terminal
- Check Redis is running: `redis-cli ping` should return `PONG`

## Architecture Overview

```
Application → EventPublisher → Redis → EventSubscriber → EventProcessor
                                             ↓
                                        Processing Results
```

Read `README_EVENTS.md` for full documentation!

