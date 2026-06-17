print("START")

from backend.auth import create_access_token, verify_token

print("IMPORT OK")

token = create_access_token(
    {
        "sub": "imran4@gmail.com"
    }
)

print("TOKEN:")
print(token)

print("\nPAYLOAD:")
print(verify_token(token))

print("DONE")