from google.appengine.ext import ndb

class Anagram(ndb.Model):
    length = ndb.IntegerProperty()
    sorted_word = ndb.StringProperty()
    sub_words = ndb.StringProperty(repeated=True)
    user_id = ndb.StringProperty()
    words = ndb.StringProperty(repeated=True)
    words_count = ndb.IntegerProperty()
