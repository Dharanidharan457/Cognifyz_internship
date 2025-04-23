def is_palindrome(string):
    cleaned_string = ''.join(char.lower() for char in string if char.isalnum())
    return cleaned_string == cleaned_string[::-1]

def palindrome_checker():
    print("Palindrome Checker Program")
    
    string = input("Enter a string to check if it's a palindrome: ")
    
    if is_palindrome(string):
        print(f'"{string}" is a palindrome.')
    else:
        print(f'"{string}" is not a palindrome.')
    

if __name__ == "__main__":
    palindrome_checker()

#output
#Palindrome Checker Program
#Enter a string to check if it's a palindrome: mom
#"mom" is a palindrome.