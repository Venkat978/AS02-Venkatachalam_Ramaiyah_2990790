from google.appengine.ext import ndb
import webapp2
import renderer
import utilities
import os
import jinja2
from anagram import Anagram

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AddWord(webapp2.RequestHandler):
    # GET-request
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
                'user': utilities.get_user(),
                'anagrams': utilities.getanagrams_from_user(utilities.getuser())
                }
        template = JINJA_ENVIRONMENT.get_template('/html/AddWord.html')
        self.response.write(template.render(template_values))

    # POST-request
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('cancel') == 'Cancel':
            return self.redirect("/")
        # Get user data object from datastore of current user (logged in)
        my_user = utilities.getuser()
        input_text = utilities.preparetextinput(self.request.get('value'))
        self.add(input_text, my_user)

    def add(self, text, my_user):
        permutations = utilities.permutations(text)
        words = utilities.filterenglishwords(permutations)
        if text is not None or text != '':
            # Add anagram to datastore
            anagram_id = my_user.key.id() + '/' + utilities.generateid_for_users(text)
            anagram_key = ndb.Key(Anagram, anagram_id)
            anagrams = anagram_key.get()

            if anagrams:
                # Anagram with this key already exists
                utilities.addtoanagram(text, words, anagram_key)
            else:
                # This key doesnt exist so creates a new anagram object to datastore
                utilities.addanagram_new(my_user, text, words, anagram_id, anagram_key)
        self.redirect("/")
