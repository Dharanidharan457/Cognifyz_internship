import numpy as np

def play_guessing_game():
    secret_number = np.int(1, 100)
    attempts = 0
    
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            
           
            if guess < secret_number:
                print("Too low!")
            elif guess > secret_number:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number {secret_number} correctly!")
                print(f"It took you {attempts} attempts.")
                break
                
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    play_guessing_game()
    

    while True:
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again in ["yes", "y"]:
            play_guessing_game()
        elif play_again in ["no", "n"]:
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Please enter 'yes' or 'no'.")