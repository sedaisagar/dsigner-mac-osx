"""
Quick test script to verify Redis connection works.
"""
import sys

print("Testing Redis connection...")
print("=" * 50)

try:
    import redis
    print("✓ Redis library imported successfully")
    
    # Test basic connection
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    client.ping()
    print("✓ Redis connection successful!")
    print(f"  Connected to: localhost:6379")
    
    # Test pub/sub functionality
    pubsub = client.pubsub()
    pubsub.subscribe('test_channel')
    print("✓ Pub/Sub functionality works")
    
    # Clean up
    pubsub.unsubscribe()
    client.close()
    
    print("\n" + "=" * 50)
    print("All tests passed! Redis is ready to use.")
    print("=" * 50)
    
except ImportError as e:
    print("✗ Failed to import Redis library")
    print(f"  Error: {e}")
    print("\nSolution: Run 'pip install -r requirements.txt'")
    sys.exit(1)
    
except redis.ConnectionError as e:
    print("✗ Failed to connect to Redis")
    print(f"  Error: {e}")
    print("\nSolution: Start Redis server with 'redis-server'")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    sys.exit(1)

