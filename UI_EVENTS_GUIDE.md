# UI Event Launcher Guide

## Overview

The event processor now automatically shows Tkinter notification windows when events are received! Each event triggers a beautiful modal notification dialog that displays the event details.

---

## 🎯 How It Works

### Flow
```
Event Published → Redis → Event Subscriber → Processing → UI Notification
```

When you publish events to Redis, the event processor will:
1. Receive the event
2. Process it (validate, transform, etc.)
3. **Automatically show a Tkinter notification window**
4. Display event details in a beautiful modal dialog

---

## 🚀 Usage

### Step 1: Start Event Processor

```bash
python event_processor.py
```

You'll see:
```
INFO:__main__:Starting Event Processor...
INFO:__main__:Connected to Redis at localhost:6379
INFO:__main__:Subscribed to all topics. Listening for events...
```

**Keep this running!**

### Step 2: Publish Events

In another terminal:
```bash
python demo_events.py
```

**Or** publish events from your code:
```python
from services.event_publisher import get_publisher

publisher = get_publisher()
publisher.publish_key_submitted("my_key_123", "My Token")
```

### Step 3: Watch the Magic! ✨

A notification window will automatically appear showing:
- Event type
- Timestamp
- Complete event data
- Beautiful styled UI

---

## 🎨 Notification Features

### Visual Design
- **Modal dialog** - Focused attention
- **Styled header** - Professional look
- **Color scheme** - Matches your dashboard
- **Scrollable text** - Full event data display
- **Read-only** - Safe to view
- **One-click close** - Easy to dismiss

### Capabilities
- ✅ Shows for all event types
- ✅ Displays full event data
- ✅ Formatted JSON display
- ✅ Timestamp included
- ✅ Multi-window support (up to 3 concurrent)
- ✅ Thread-safe
- ✅ Non-blocking (doesn't freeze event processor)

---

## 📋 Event Types

### Key Submission Events
- Event type: `key_submitted`
- Shows: Key value, token name, timestamp
- Action: Notification only

### Profile Events
- Event types: `profile_created`, `profile_updated`, `profile_deleted`
- Shows: Profile data, action taken
- Action: Notification + optionally launches full dashboard for critical events

### Processing Results
- Event types: `key_processed`, `profile_processed`
- Shows: Original event + processing results
- Action: Notification only

---

## 🎛️ Configuration

### Change Notification Behavior

Edit `ui/event_dashboard_launcher.py`:

**Option 1: Notification Only** (Default)
```python
EventNotificationWindow.create_notification(event_type, event_data)
```

**Option 2: Launch Full Dashboard**
```python
DashboardLauncher.launch_full_dashboard(event_type, event_data)
```

**Option 3: Both**
```python
EventNotificationWindow.create_notification(event_type, event_data)
DashboardLauncher.launch_full_dashboard(event_type, event_data)
```

### Limit Concurrent Windows

Edit `EventNotificationWindow` class:
```python
_max_windows = 3  # Change this number
```

### Customize Styling

Edit the colors in `_create_modal_notification()`:
```python
bg="#f6f8fa"           # Background
header_bg="#2a5b74"    # Header color
success_bg="#43a047"   # Button color
```

---

## 🧪 Testing

### Quick Test

**Terminal 1:**
```bash
python event_processor.py
```

**Terminal 2:**
```bash
python demo_events.py
```

### Expected Behavior

1. Notification windows appear automatically
2. Each shows different event data
3. Windows are independent (can close individually)
4. Event processor continues running
5. No blocking or freezing

---

## 🔧 Troubleshooting

### "No notification appears"
- ✅ Make sure `event_processor.py` is running
- ✅ Check Redis is running: `redis-cli ping`
- ✅ Verify events are being published
- ✅ Check console for errors
- ✅ Look for log messages: "Creating notification window for event: ..."
- ✅ Check for "Notification thread started" in logs
- ✅ Ensure you're on Windows/macOS GUI environment (not headless)

### "Too many windows open"
- Current limit: 3 concurrent windows
- Close some windows to allow more
- Adjust `_max_windows` in the launcher

### "Windows freeze"
- Make sure you're using threads
- Already implemented automatically
- Should never freeze the processor

### "Styling looks wrong"
- Check tkinter is installed: `python -c "import tkinter"`
- Verify window manager is running
- Update colors in the launcher file

---

## 📝 Code Examples

### Publishing Events from Your App

```python
from services.event_publisher import get_publisher

# Get publisher
publisher = get_publisher()

# Publish key event (triggers notification)
publisher.publish_key_submitted("abc123", "Token1")

# Publish profile event (triggers notification)
publisher.publish_profile_created(
    profile_id=1,
    profile_data={'name': 'Test Profile'}
)

# Publish custom event (triggers notification)
publisher.publish('my_topic', {
    'event_type': 'custom_event',
    'data': {'foo': 'bar'}
})
```

### Custom Event Handler with UI

```python
from ui.event_dashboard_launcher import EventNotificationWindow

def my_custom_handler(topic, event_data):
    # Process the event
    print(f"Processing: {event_data}")
    
    # Show notification
    EventNotificationWindow.create_notification(
        "Custom Event", 
        event_data
    )
```

---

## 🎉 Benefits

✅ **Visual Feedback** - See events happening in real-time  
✅ **Non-Intrusive** - Modal dialogs don't block processing  
✅ **Informative** - Full event data displayed  
✅ **Professional** - Beautiful, styled UI  
✅ **Configurable** - Easy to customize  
✅ **Thread-Safe** - Multiple events handled safely  
✅ **Automatic** - No manual intervention needed  

---

## 🔄 Event Flow Example

```
1. Your app publishes: publisher.publish_key_submitted("abc123", "Token1")
   ↓
2. Redis receives and broadcasts
   ↓
3. Event processor subscribes and receives
   ↓
4. Processing occurs
   ↓
5. UI notification window appears automatically
   ↓
6. User sees event details
   ↓
7. User closes window
   ↓
8. Ready for next event
```

---

## 📊 Architecture

```
┌─────────────────┐
│   Your App      │
│  (Publisher)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐         ┌─────────────────┐
│     Redis       │────────▶│ Event Processor │
│    Pub/Sub      │subscribe│  (Subscriber)   │
└─────────────────┘         └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   Processing    │
                            │   (business     │
                            │    logic)       │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  UI Launcher    │
                            │  (Tkinter       │
                            │  Notification)  │
                            └─────────────────┘
```

---

## 🎯 Next Steps

1. **Run the processor**: `python event_processor.py`
2. **Publish events**: `python demo_events.py`
3. **Watch notifications**: See windows appear automatically!
4. **Customize**: Edit the launcher for your needs
5. **Integrate**: Add to your existing application

---

**Enjoy the automatic UI notifications!** 🎉

*For detailed event system documentation, see `README_EVENTS.md`*

