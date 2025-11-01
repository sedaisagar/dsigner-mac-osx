# Project Structure

## 📂 Directory Layout

```
Dsigner MACOSX/
│
├── 📄 main.py                           # Main application entry point
├── 📄 requirements.txt                  # Python dependencies (redis==5.0.1)
├── 📄 LICENSE                           # License file
│
├── 📁 services/                         # Backend services
│   ├── __init__.py                      # Package initializer
│   ├── db.py                            # SQLite database operations
│   ├── crud.py                          # CRUD operations (with event integration)
│   ├── event_publisher.py               # 🆕 Redis event publisher
│   └── event_subscriber.py              # 🆕 Redis event subscriber
│
├── 📁 ui/                               # User interface
│   ├── __init__.py                      # Package initializer
│   └── dashboard.py                     # Tkinter dashboard application
│
├── 📁 venv/                             # Virtual environment (not in repo)
│
├── 📋 EVENT_IMPLEMENTATION_SUMMARY.md   # 🆕 Implementation summary
├── 📋 PROJECT_STRUCTURE.md              # 🆕 This file
├── 📋 README_EVENTS.md                  # 🆕 Event system documentation
├── 📋 QUICKSTART.md                     # 🆕 Quick start guide
│
├── 🔧 event_processor.py                # 🆕 Standalone event processor
├── 🔧 demo_events.py                    # 🆕 Event demonstration script
├── 🔧 test_redis_connection.py          # 🆕 Redis connection test
│
└── 💾 profiles.db                       # SQLite database (generated)

🆕 = New files added for event-based architecture
```

---

## 📦 Key Components

### Core Application
- **main.py**: Application entry point with Tkinter GUI
- **ui/dashboard.py**: Dashboard interface with profile management
- **services/db.py**: Database operations (SQLite)
- **services/crud.py**: CRUD wrapper with event integration

### Event System (NEW)
- **services/event_publisher.py**: Publish events to Redis topics
- **services/event_subscriber.py**: Subscribe to Redis and process events
- **event_processor.py**: Standalone subscriber service
- **demo_events.py**: Event publishing demonstration
- **test_redis_connection.py**: Connection validation

### Documentation (NEW)
- **README_EVENTS.md**: Complete event system documentation
- **QUICKSTART.md**: Quick setup guide
- **EVENT_IMPLEMENTATION_SUMMARY.md**: Implementation overview
- **PROJECT_STRUCTURE.md**: This file

---

## 🔄 Data Flow

### Existing Application Flow
```
main.py → DashboardApp → services/db.py → profiles.db
```

### New Event Flow
```
Application → event_publisher.py → Redis → event_subscriber.py → Processing
                                                  ↓
                                         event_processor.py
                                                  ↓
                                         Publish Results → Redis
```

---

## 🎯 Entry Points

### Run Main Application
```bash
python main.py
```

### Run Event Processor
```bash
python event_processor.py
```

### Run Demo
```bash
python demo_events.py
```

### Test Redis
```bash
python test_redis_connection.py
```

---

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| GUI | Tkinter (Python) |
| Database | SQLite |
| Event System | Redis Pub/Sub |
| Language | Python 3.x |

---

## 🔌 External Dependencies

- **redis**: 5.0.1 (for pub/sub)
- Python standard library (tkinter, sqlite3, threading, etc.)

---

## 📝 File Responsibilities

### Event Publisher (`services/event_publisher.py`)
- Connect to Redis
- Publish events to topics
- Singleton connection management
- Event serialization

### Event Subscriber (`services/event_subscriber.py`)
- Subscribe to Redis topics
- Process incoming events
- Thread-safe handling
- Multi-topic support

### Event Processor (`event_processor.py`)
- Standalone subscriber service
- Run indefinitely
- Process and publish results

### Demo Script (`demo_events.py`)
- Demonstrate event publishing
- Show all event types
- Testing utilities

### Test Script (`test_redis_connection.py`)
- Validate Redis connectivity
- Test pub/sub functionality
- Diagnostic tool

---

## 🔐 Configuration Files

- **requirements.txt**: Python package dependencies
- **profiles.db**: SQLite database (generated)
- Redis config: Default localhost:6379

---

## 🚀 Quick Start

```bash
# 1. Start Redis
redis-server

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test connection
python test_redis_connection.py

# 4. Start event processor (Terminal 1)
python event_processor.py

# 5. Run demo (Terminal 2)
python demo_events.py

# 6. Run main app (Terminal 3)
python main.py
```

---

## 📈 Scaling

The event system supports:
- Multiple publishers
- Multiple subscribers
- Horizontal scaling
- Topic-based routing
- Async processing

---

*Last Updated: 2024*
*Version: 1.0*

