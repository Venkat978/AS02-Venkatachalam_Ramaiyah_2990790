from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from anagram import Anagram
import re  # regex
from itertools import permutations

with open("wordsEn.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

def getloginurl(main_page):
    return users.create_login_url(main_page.request.url)

def getlogouturl(main_page):
    return users.create_logout_url(main_page.request.url)

def get_user():
    return users.get_current_user()

def getuser():
    user = get_user()
    if user:
        my_user_key = ndb.Key(MyUser, user.user_id())
        return my_user_key.get()

def user_loggedin():
    return True if get_user() else False

def existing_user():
    return True if getuser() else False

def add_new_user(user):
    MyUser(id=user.user_id()).put()

def preparetextinput(input_text):
    result = input_text.lower()
    result = re.sub('[^a-z]+', '', result)
    return result

def getanagrams_from_user(my_user):
    if my_user:
        result = []
        wordCount, totalCount = 0, 0
        for anagram in my_user.anagrams:
            anagrams = anagram.get()
            wordCount += 1
            totalCount += len(anagrams.words)
            result.append(anagrams)

        return result, wordCount, totalCount

def addanagram_new(my_user, text, words, anagram_id, anagram_key):
    if englishword(text):
        anagram = Anagram(id=anagram_id)
        anagram.words.append(text)
        anagram.sorted_word = generateid_for_users(text)
        anagram.length = len(text)
        anagram.words_count = len(anagram.words)
        anagram.sub_words = words
        anagram.user_id = my_user.key.id()
        anagram.put()
        my_user.anagrams.append(anagram_key)
        my_user.put()

def addtoanagram(text, words1, anagram_key):
    anagram = anagram_key.get()
    if text not in anagram.words:
        if englishword(text):
            anagram.words.append(text)
            anagram.words_count = len(anagram.words)
            for i in words1:
                anagram.sub_words.append(i)
            anagram.put()

def generateid_for_users(text):
    key = text.lower()
    return ''.join(sorted(key))

def a_permutations(input_string):
    result = [perm for length in range(1, len(input_string) + 1) for perm in permutations(input_string, length)]
    result = list(set(result))
    r = []
    for i in result:
        if len(i) >= 3:
            r.append(''.join(i))
    return r

def englishword(text):
    return True if text in english_words else False

def filterenglishwords(word_list):
    result = []
    for word in word_list:
        if word in english_words:
            if word not in result:
                result.append(word)

    return result
