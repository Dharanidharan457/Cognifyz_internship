def generate_fibonacci(n_terms):
    if not isinstance(n_terms, int) or n_terms <= 0:
        return "Please enter a positive integer."
    
    fibonacci_sequence = []
    
    if n_terms >= 1:
        fibonacci_sequence.append(0)
    if n_terms >= 2:
        fibonacci_sequence.append(1)
    
    for i in range(2, n_terms):
        next_term = fibonacci_sequence[i-1] + fibonacci_sequence[i-2]
        fibonacci_sequence.append(next_term)
    
    return fibonacci_sequence

def main():
    print(" Fibonacci Sequence Generator ")
    
    while True:
        try:
            n = input("\nEnter the number of terms to generate (or 'exit' to quit): ")
            
            if n.lower() == 'exit':
                print("Exiting program. Goodbye!")
                break
            
            n = int(n)
            
            if n <= 0:
                print("Please enter a positive integer.")
                continue
            
            sequence = generate_fibonacci(n)
            
            print(f"\nFibonacci sequence up to {n} terms:")
            
            if len(sequence) <= 15:
                print(sequence)
            else:
                for i, num in enumerate(sequence):
                    if i % 10 == 0 and i > 0:
                        print()  
                    print(f"{num:<15}", end="")
                print() 
            
            print(f"\nSum of the sequence: {sum(sequence)}")
            
            if n > 2:
                golden_ratio = sequence[-1] / sequence[-2]
                print(f"Ratio of last two terms (approximation of golden ratio): {golden_ratio:.8f}")
            
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
            
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting.")
            break

if __name__ == "__main__":
    main()