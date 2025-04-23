import random

def number_guesser():
    print(" Number Guesser Game ")
    
    while True:
        try:
            min_num = int(input("Enter the minimum number for the range: "))
            max_num = int(input("Enter the maximum number for the range: "))
            
            if min_num >= max_num:
                print("Maximum number must be greater than minimum number. Please try again.")
                continue
            break
        except ValueError:
            print("Please enter valid numbers.")
    
    secret_number = random.randint(min_num, max_num)
    attempts = 0
    
    print(f"\nI'm thinking of a number between {min_num} and {max_num}.")
    print("Try to guess it!")
    
    while True:
        try:
           
            guess = int(input("\nEnter your guess: "))
            attempts += 1
            
          
            if guess < min_num or guess > max_num:
                print(f"Your guess is outside the range ({min_num}-{max_num}). Please try again.")
                continue
            
            
            if guess < secret_number:
                print("Too low! Try a higher number.")
            elif guess > secret_number:
                print("Too high! Try a lower number.")
            else:
                print(f"\nCongratulations! You've guessed the number {secret_number} correctly!")
                print(f"It took you {attempts} attempts.")
                break
                
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    number_guesser()
    
   
    while True:
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again in ["yes", "y"]:
            number_guesser()
        elif play_again in ["no", "n"]:
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Please enter 'yes' or 'no'.")