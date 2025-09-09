def sum_of_element(elements):
    """
    1 Kata

    :param elements: list of integers
    :return: Return int - the sum of all elements.
    """
    # elements=[1,2]
    sum=0

    for i in elements:
        sum=sum+i

    return sum

def verbing(word):
    lengh = len(word)
    if lengh >= 3:
        if word [-3:] == 'ing':
            word += 'ly'
        else:
            word += 'ing'
    return word



def words_concatenation(words):
    sentence = ''
    for i in words:
        sentence += i + ' '
    return sentence.strip()


   


def reverse_words_concatenation(words):
    sentence = ''
    for i in words:
        if sentence:
            sentence = i + ' ' + sentence
        else:
            sentence = i
    return sentence




def is_unique_string(some_str):
    a = set()
    for i in some_str:
        if i in a:
            return False
        else:
            a.add(i)
    return True


def list_diff(elements):
    if not elements:
        return []
    diff = [None]
    previous_num = elements[0]
    for i in elements[1:]:
        diff.append(i - previous_num)
        previous_num = i
    return diff


def prime_number(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True



def palindrome_num(num):
    list_num=list(str(num))
    half=len(list_num)//2
    if len(list_num)%2==0:
        first_half=list_num[:half]
        second_half=list_num[half:]
    else:
        first_half=list_num[:half]
        second_half=list_num[(half+1):]
    second_half.reverse()
    if first_half==second_half:
        return True
    else:
        return False


def pair_match(men, women):
    men_dict=dict(men)
    women_dict=dict(women)
    min_diff=float('inf')
    match=()
    for name_men, age_men in men_dict.items():
        for name_women, age_women in women_dict.items():
             if abs(age_men-age_women)<min_diff:
                 min_diff=abs(age_men-age_women)
                 match=(name_men,name_women)
    return match



def bad_average(a, b, c):
    return (a + b + c) / 3


def best_student(grades):
    max_grade=0
    best_student=''
    for name in grades:
        if grades[name]>max_grade:
            max_grade=grades[name]
            best_student=name
    return best_student

def print_dict_as_table(some_dict):
    table=''
    for name in some_dict:
        some_dict[name]=str(some_dict[name])
        table+=f"{name:<10}"+some_dict[name]+'\n'
    return table


def merge_dicts(dict1, dict2):
    for key in dict2:
        dict1[key]=dict2[key]
    return dict1


def seven_boom(n):
    list_num=list(range(1,n))
    seven_boom_list=[]
    for num in list_num:
        if num%7==0:
            seven_boom_list.append(num)
            continue
        checking_num=list(str(num))
        for digit in checking_num:
            int_digit=int(digit)
            if int_digit==7:
                  seven_boom_list.append(num)
    return seven_boom_list  

def caesar_cipher(str_to_encrypt):
    encrypt=''
    lower_str='abcdefghijklmnopqrstuvwxyz'
    upper_str='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for char in str_to_encrypt:
        if char==' ':
            encrypt+=char
        elif char in lower_str:
            index_lower=(lower_str.index(char)+3)%26
            encrypt+=lower_str[index_lower]
        elif char in upper_str:
            index_upper=(upper_str.index(char)+3)%26
            encrypt+=upper_str[index_upper]
    return encrypt



def sum_of_digits(digits_str):
    sum=0
    for digit in digits_str:
        int_digit=int(digit)
        sum+=int_digit
    return sum



if __name__ == '__main__':

    print(sum_of_element([1, 2]))
    print(sum_of_element([1, 3]))
    print(sum_of_element([4, 5, 6]))
    
    print('\nverbing:\n--------------------')
    print(verbing('walk'))
    print(verbing('swimming'))
    print(verbing('do'))
    
    print('\nwords_concatenation:\n--------------------')
    print(words_concatenation(['take', 'me', 'home']))
    
    print('\nreverse_words_concatenation:\n--------------------')
    print(reverse_words_concatenation(['take', 'me', 'home']))
    
    print('\nis_unique_string:\n--------------------')
    print(is_unique_string('aasdssdsederd'))
    print(is_unique_string('12345tgbnh'))
    
    print('\nlist_diff:\n--------------------')
    print(list_diff([1, 2, 3, 8, 77, 0]))
    
    print('\nprime_number:\n--------------------')
    print(prime_number(5))
    print(prime_number(22))

    
    print('\npalindrome_num:\n--------------------')
    print(palindrome_num(12221))
    print(palindrome_num(577))

    
    print('\npair_match:\n--------------------')
    print(pair_match(
        {
             "John": 20,
             "Abraham": 45
         },
         {
             "July": 18,
             "Kim": 26
         }
     ))
    
    print('\nbad_average:\n--------------------')
    print(bad_average(1, 2, 3))
    
    print('\nbest_student:\n--------------------')
    print(best_student({
         "Ben": 78,
         "Hen": 88,
         "Natan": 99,
         "Efraim": 65,
         "Rachel": 95
     }))
    
    print('\nprint_dict_as_table:\n--------------------')
    print(print_dict_as_table({
         "Ben": 78,
         "Hen": 88,
         "Natan": 99,
         "Efraim": 65,
         "Rachel": 95
     }))
    
    print('\nmerge_dicts:\n--------------------')
    print(merge_dicts({'a': 1}, {'b': 2}))
    
    print('\nseven_boom:\n--------------------')
    print(seven_boom(30))
    
    print('\ncaesar_cipher:\n--------------------')
    print(caesar_cipher('Fly Me To The Moon'))
    
    print('\nsum_of_digits:\n--------------------')
    print(sum_of_digits('1223432'))

