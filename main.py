import random
import regex as re

dict_text_to_emoji = {
    "A": "😀",
    "B": "😁",
    "C": "😂",
    "D": "🤣",
    "E": "😃",
    "F": "😄",
    "G": "😅",
    "H": "😆",
    "I": "😉",
    "J": "😊",
    "K": "😋",
    "L": "😎",
    "M": "😍",
    "N": "😘",
    "O": "😗",
    "P": "😙",
    "Q": "😚",
    "R": "😇",
    "S": "🙂",
    "T": "🙃",
    "U": "😌",
    "V": "🤗",
    "W": "😏",
    "X": "😐",
    "Y": "😑",
    "Z": "😶",
    "Æ": "😴",
    "Ø": "😛",
    "Å": "😜",
    "0": "😝",
    "1": "🤑",
    "2": "🤒",
    "3": "🤕",
    "4": "🤠",
    "5": "😈",
    "6": "👿",
    "7": "👹",
    "8": "👺",
    "9": "💀",
    ".": "💩",
    ",": "👻",
    "!": "👽",
    "?": "🤖",
    "-": "😺",
    '"': "😸",
    "'": "😹",
    "(": "😻",
    ")": "😼",
    "/": "😽",
    " ": "😤"
}

def process_input(input_text):
    return re.findall(r'\X', input_text)

def create_randomized_mapping(seed):
    random.seed(seed)
    letters = list(dict_text_to_emoji.keys())
    emojis = list(dict_text_to_emoji.values())
    random.shuffle(emojis)
    return dict(zip(letters, emojis))

dict_emoji_to_text = {v: k for k, v in dict_text_to_emoji.items()}

def rotate_key(start_key, rotation, mapping, side):
    keys = list(mapping.keys())
    start_index = keys.index(start_key)
    if side: # True is right and false is left
        new_index = (start_index + rotation) % len(keys)
    else:
        new_index = (start_index - rotation) % len(keys)
    return keys[new_index]

def text_to_emoji(text, mapping, seed):
    text = text.upper()
    new_seed = 0
    translated_accumulated = ""
    error = False
    for char in text:
        try:
            new_seed += seed*65537
            encrypted_char = rotate_key(char, new_seed, mapping, True)
            translated = mapping[encrypted_char]
            translated_accumulated += translated
        except:
            error = True
            print(f"Oops, there was an error '{char}' doesn't exist")
    if error == True:
        print("One or more character doesn't exist, those characters have been skipped")
    
    if len(translated_accumulated) < 100:
        print(translated_accumulated)
    elif len(translated_accumulated) >= 100 and len(translated_accumulated) < 200:
        first_part = translated_accumulated[:100]
        second_part = translated_accumulated[100:]
        print("The terminal can't print more than 100 emojis without corrupting for whatever reason, so it's split")
        print(f"1st: {first_part}")
        print(f"2nd: {second_part}")
    else:
        print("Too long texts doesn't really make sense, try making it shorter :)")

def emoji_to_text(emojis, mapping, seed):
    emoji_list = process_input(emojis)
    translated_accumulated = ""
    new_seed = 0
    error = False

    for emoji in emoji_list:
        if emoji not in mapping: # Corruptions happen that messes with the decryption, but most of it is still readable
            error = True
            print(f"Oops, there was an error '{emoji}' doesn't exist")
            continue

        try:
            new_seed += seed*65537
            decrypted_char = rotate_key(emoji, new_seed, mapping, False)
            translated = mapping[decrypted_char]
            translated_accumulated += translated
        except:
            error = True
            print(f"Oops, there was an error '{emoji}' doesn't exist")
    if error == True:
        print("One or more character doesn't exist, those characters have been skipped ❌")
        print("Terminals are terrible at printing emojis, and so is your computer at copying them. So corruptions happen ☠️")
    print(f"'{translated_accumulated}'")

def gen_seed_and_maps():
    seed = input("Enter a seed for encryption (or leave empty for default seed): ")
    if not seed:
        seed = 42
    else:
        seed = int(seed)
    randomized_mapping = create_randomized_mapping(seed)
    dict_emoji_to_text = {v: k for k, v in randomized_mapping.items()}
    return randomized_mapping, dict_emoji_to_text, seed

emoji_or_text = input("Do you want to translate text to emoji, or emoji to text (a/b): ")

if emoji_or_text == "a":
    randomized_mapping, _, seed = gen_seed_and_maps()
    text = input("Write your text: ")
    text_to_emoji(text, randomized_mapping, seed)
elif emoji_or_text == "b":
    _, dict_emoji_to_text, seed = gen_seed_and_maps()
    emojis = input("Write your emoji text: ")
    emoji_to_text(emojis, dict_emoji_to_text, seed)
else:
    print("Input invalid")