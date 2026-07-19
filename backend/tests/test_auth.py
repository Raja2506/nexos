from app.security.jwt_handler import hash_password, verify_password, create_access_token, decode_access_token

plain = "MySecurePassword123"
hashed = hash_password(plain)
print("Hashed:", hashed[:30], "...")
print("Correct password verifies:", verify_password(plain, hashed))
print("Wrong password rejected:", not verify_password("WrongPassword", hashed))

token = create_access_token(user_id="user_123", email="test@example.com")
print("\nToken:", token[:40], "...")

payload = decode_access_token(token)
print("Decoded payload:", payload)

bad_payload = decode_access_token("this.is.not.a.valid.token")
print("Invalid token result:", bad_payload)
