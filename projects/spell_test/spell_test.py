from random import shuffle
import csv
import requests
import bs4
from gtts import gTTS
from playsound import playsound


# function to create initial csv file
# def create_csv():
# spelling_csv = open('spellings.csv', 'w', newline='')
# csv_writer = csv.writer(spelling_csv, delimiter=',')
# spelling_csv.close()

# user inputs spellings and function adds spelling and definition to csv
def add_words(lst):
    new_word = '999'
    print("Type 'done' when you have finished adding words.")
    while new_word.lower() != 'done':
        new_word = input('Add a word to the spelling list: ')
        try:
            if new_word.lower() != 'done':
                lst.append(get_def(new_word.lower().strip('"')))
                print(new_word + ' added.')
            else:
                f = open('spellings.csv', 'a', newline='')
                csv_writer = csv.writer(f)
                csv_writer.writerow(lst)
                f.close()
        except IndexError:
            print('Are you sure you spelt that correctly? ' + new_word + '?')
            continue
    print(lst)
    return lst


# Return definition of word scraped from web dictionary
def get_def(word):
    page = "https://dictionary.cambridge.org/dictionary/english/" + word
    result = requests.get(page, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) "
                                                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 "
                                                       "Safari/537.36"})
    soup = bs4.BeautifulSoup(result.text, 'lxml')
    definition = soup.select('div.def.ddef_d.db')[0].getText()
    return word + ' - ' + definition.rstrip(' :')


# Scrambles letters of the word provided
def jumble(word):
    letters = []
    for i in range(len(word)):
        letters.append(word[0])
        word = word[1:]
    shuffle(letters)
    return ''.join(letters)


def test(word, data_lines):
    score = 0
    count = 0
    help_list = ['clue', 'repeat']
    # create a text-to-speech object, save as mp3 and play mp3
    tts = gTTS('Please spell ' + word)
    tts.save('spelling.mp3')
    playsound('spelling.mp3')
    print("Type 'Clue' if you'd like a clue.")
    guess = input("Spell here...\n")
    # todo while guess in list [clue repeat]
    while guess.lower() in help_list:
        if guess.lower() == 'repeat':
            playsound('spelling.mp3')
        if guess.lower() == 'clue':
            clue(word, data_lines)
        guess = input("Spell here...\n")
    if guess.lower() == word.lower():
        print("Correct")
        score += 1
        count += 1
    else:
        count += 1
        print("Incorrect")
        print("The correct spelling is " + word)
    return score


# test all spellings (1) or last line of csv (0)
def test_spelling(val):
    score = 0
    spellings = []
    f = open('spellings.csv', 'r', encoding='utf-8')
    csv_data = csv.reader(f)
    data_lines = list(csv_data)
    if val:
        for line in data_lines:
            spelling = [x.split()[0] for x in line]
            spellings.append(spelling)
        # read spellings.csv and create list of all spellings
        shuffle(spellings)
        for word in spellings:
            score += test(word, data_lines)
        print(f'You scored {score}/' + str(len(spellings)))
    else:
        for word in data_lines[-1]:
            spellings.append(word.split()[0].strip('"'))
        # read spellings.csv and create list of all spellings
        shuffle(spellings)
        for word in spellings:
            score += test(word, data_lines)
        print(f'You scored {score}/' + str(len(spellings)))


# prints scrambled word and its definition to the screen
def clue(word, definitions_list):
    print(jumble(word))
    for line in definitions_list:
        for definition in line:
            if word == definition.split()[0]:
                print(definition[len(word)+3:])


print("Welcome to the Spelling Quiz")
choices = ['1', '2', '3', '4']
user_choice = 999

while user_choice != '4':
    print('\n')
    user_choice = input('''
    Type 1 to test all spellings...
    Type 2 to test this weeks spellings...
    Type 3 to add new words...
    Type 4 to exit...
    ''')
    if user_choice not in choices:
        print('Pick 1, 2, 3 or 4.')
        pass
    elif user_choice == '1':
        print('Quiz Time!!!!')
        test_spelling(1)
        pass
    elif user_choice == '2':
        print('Quiz Time!!!!')
        test_spelling(0)
    elif user_choice == '3':
        word_list = []
        add_words(word_list)
    else:
        print('Goodbye!!!')
        pass
