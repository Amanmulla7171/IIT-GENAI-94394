def calculate_sentence_metrics(sentence):
    
 

    # Count characters
    num_chars = len(sentence.strip())

    # Split the sentence into words

    num_words = len(sentence.split())
    

    num_vowels = 0
    
    # Check each character to see if it's a vowel
    for char in sentence:
        if char.lower() in 'aeiou':
            num_vowels += 1

    print(f"Number of characters: {num_chars}")
    print(f"Number of words: {num_words}")
    print(f"Number of vowels: {num_vowels}")

def main():
    # Get user input
    sentence = input("Enter a sentence: ")

    # Calculate and display metrics
    calculate_sentence_metrics(sentence)

if __name__ == "__main__":
    main()
