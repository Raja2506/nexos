from app.memory.short_term import set_session_data, get_session_data, clear_session

session_id = "test_session_001"

# Write
set_session_data(session_id, "last_message", {"role": "user", "text": "Hello NexOS"})

# Read
result = get_session_data(session_id, "last_message")
print("Retrieved:", result)

# Cleanup
clear_session(session_id)
print("Session cleared.")

after_clear = get_session_data(session_id, "last_message")
print("After clear (should be None):", after_clear)
