import re

def check_password_strength(password):
    score = 0
    feedback = []
    details = {
        "length": False,
        "uppercase": False,
        "lowercase": False,
        "digits": False,
        "special_chars": False,
        "no_common_patterns": True
    }
    if len(password) >= 8:
        score += 1
        details["length"] = True
    else:
        feedback.append("Password should be at least 8 characters long")
    
    if re.search(r'[A-Z]', password):
        score += 1
        details["uppercase"] = True
    else:
        feedback.append("Include at least one uppercase letter")
    
    if re.search(r'[a-z]', password):
        score += 1
        details["lowercase"] = True
    else:
        feedback.append("Include at least one lowercase letter")
    
    if re.search(r'\d', password):
        score += 1
        details["digits"] = True
    else:
        feedback.append("Include at least one number")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|]', password):
        score += 1
        details["special_chars"] = True
    else:
        feedback.append("Include at least one special character (!@#$%^&*()_+-=[]{}:;\"'<>,.?/|\\)")
    
    common_patterns = [
        r'123', r'abc', r'qwerty', r'password', r'admin', 
        r'welcome', r'letmein', r'iloveyou', r'1234'
    ]
    
    for pattern in common_patterns:
        if re.search(pattern.lower(), password.lower()):
            details["no_common_patterns"] = False
            feedback.append(f"Avoid common patterns like '{pattern}'")
            score = max(0, score - 1) 
            break
    
    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Moderate",
        4: "Strong",
        5: "Very Strong"
    }
    
    strength = strength_levels.get(score, "Unknown")
    
    if not feedback:
        feedback.append("Excellent password!")
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
        "details": details
    }

def main():
    print("=== Password Strength Checker ===")
    print("Enter a password to check its strength.")
    print("Type 'exit' to quit the program.\n")
    
    while True:
        password = input("Enter password: ")
        
        if password.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break
        
        result = check_password_strength(password)
        
        print("\nPassword Strength: " + result["strength"] + f" ({result['score']}/5)")
        print("\nFeedback:")
        for item in result["feedback"]:
            print(f"- {item}")
        
        print("\nDetails:")
        for check, passed in result["details"].items():
            status = "✓" if passed else "✗"
            print(f"{status} {check.replace('_', ' ').title()}")
        
        print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    main()