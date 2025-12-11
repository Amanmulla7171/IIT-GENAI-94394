def count_even_odd(numbers):
    even_count = 0
    odd_count = 0
    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    
    print(f"Even numbers count: {even_count}")
    print(f"Odd numbers count: {odd_count}")
def main():
    # Get user input
    input_str = input("Enter a list of numbers separated by commas: ")
    user_input = input_str.strip()
    numbers = [int(num) for num in user_input.split(',') if num.strip().isdigit()]
    
    # Count even and odd numbers
    count_even_odd(numbers) 
if __name__ == "__main__":
    main()
    