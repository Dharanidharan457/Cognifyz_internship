import re
import os
from collections import Counter

def count_words_in_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            
            words = re.findall(r'\b[a-z0-9]+\b', content)
            
            word_counts = Counter(words)
            
            return word_counts
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def display_word_counts(word_counts, sort_by='alphabetical', limit=None):
    if not word_counts:
        return
    
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    
    print(f"\nTotal words: {total_words}")
    print(f"Unique words: {unique_words}")
    
    if sort_by == 'alphabetical':
        items = sorted(word_counts.items())
    else: 
        items = word_counts.most_common()
    
    if limit:
        items = items[:limit]
    
    max_word_length = max(len(word) for word, _ in items)
    
    print("\nWord Occurrences:")
    print("-" * 40)
    print(f"{'Word':<{max_word_length + 2}}Count")
    print("-" * 40)
    
    for word, count in items:
        print(f"{word:<{max_word_length + 2}}{count}")

def main():
    print(" Text File Word Counter ")
    
    while True:
        file_path = input("\nEnter the path to a text file (or 'exit' to quit): ")
        
        if file_path.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break
        
        word_counts = count_words_in_file(file_path)
        
        if word_counts:
            while True:
                sort_option = input("\nSort by (a)lphabetical or (f)requency? [a/f]: ").lower()
                
                if sort_option in ['a', 'alphabetical']:
                    sort_by = 'alphabetical'
                    break
                elif sort_option in ['f', 'frequency']:
                    sort_by = 'frequency'
                    break
                else:
                    print("Invalid option. Please enter 'a' or 'f'.")
            
            try:
                limit_input = input("\nLimit results? Enter a number or press Enter for all: ")
                limit = int(limit_input) if limit_input.strip() else None
            except ValueError:
                print("Invalid input. Showing all results.")
                limit = None
            
            display_word_counts(word_counts, sort_by, limit)
            
            save_option = input("\nSave results to file? [y/n]: ").lower()
            if save_option in ['y', 'yes']:
                output_file = input("Enter output file name: ")
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Total words: {sum(word_counts.values())}\n")
                        f.write(f"Unique words: {len(word_counts)}\n\n")
                        f.write("Word Occurrences:\n")
                        f.write("-" * 40 + "\n")
                        
                        if sort_by == 'alphabetical':
                            items = sorted(word_counts.items())
                        else:
                            items = word_counts.most_common()
                        
                        if limit:
                            items = items[:limit]
                        
                        max_word_length = max(len(word) for word, _ in items)
                        f.write(f"{'Word':<{max_word_length + 2}}Count\n")
                        f.write("-" * 40 + "\n")
                        
                        for word, count in items:
                            f.write(f"{word:<{max_word_length + 2}}{count}\n")
                    
                    print(f"Results saved to {output_file}")
                except Exception as e:
                    print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()