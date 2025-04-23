import re
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False

def email_validator():
    
    print("Email Validator")
    email = input("Enter an email address to validate: ")
    if validate_email(email):
        print(f"{email} is a valid email address.")
    else:
        print(f"{email} is not a valid email address.")
    
    for test_email in test_email:
        result = "valid" if validate_email(test_email) else "invalid"
        print(f"- {test_email}: {result}")

if __name__ == "__main__":
    email_validator()
    
    
#output
#Email Validator
#Enter an email address to validate: dharrani123@gmail.com
#dharrani123@gmail.com is a valid email address.