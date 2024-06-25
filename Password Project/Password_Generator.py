import random
import string
def generate_password(min_length, numbers=True, special_characters=True):
    letters= string.ascii_letters
    digits= string.digits
    special =string.punctuation
    random_letters=""
    random_digits=""
    random_special=""

   
    if numbers and special_characters:
        letter_count, digit_count, special_count = get_three_numbers(min_length, 0)
        
        # loop through and add random characters to each variable
        for _ in range(letter_count):
            random_letters+= random.choice(letters)
        for _ in range(digit_count):
            random_digits+= random.choice(digits)
        for _ in range(special_count):
            random_special+= random.choice(special)


    # only numbers/letters
    elif numbers:
        letter_count= random.randint(0, min_length)
        digit_count= min_length-letter_count
        for _ in range(letter_count):
            random_letters+= random.choice(letters)
        for _ in range(digit_count):
            random_digits+= random.choice(digits)
    # only special characters/letters
    elif special_characters:
        letter_count= random.randint(0, min_length)
        special_count= min_length-letter_count
        
        for _ in range(letter_count):
            random_letters+= random.choice(letters)
        for _ in range(special_count):
            random_special+= random.choice(special)

    # only letters
    else:
         for _ in range(min_length):
            random_letters+= random.choice(letters)
  

    combined_list = list(random_letters + random_digits + random_special)
    

    random.shuffle(combined_list)
    

    password = ''.join(combined_list)
    
    print(password)
    return password
    

def get_three_numbers(target_sum, min_value):
    while True:
        
        num1 = random.randint(0, target_sum)
        num2 = random.randint(0, target_sum)
        
     
        num3 = target_sum - (num1 + num2)
        
        #Only works if True, so num 3 must be 
        if min_value <= num3 <= target_sum:
            return num1, num2, num3
        