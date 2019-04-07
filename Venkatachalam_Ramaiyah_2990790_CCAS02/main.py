from google.appengine.ext import ndb
import webapp2
import renderer
import utilities
from anagram import Anagram
from addWord import AddWord

class MainPage(webapp2.RequestHandler):
    # GET-request
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        if utilities.user_loggedin():
            if not utilities.existing_user():
                utilities.add_new_user(utilities.get_user())
            result, wordCount, totalCount = utilities.getanagrams_from_user(utilities.getuser())
            renderer.render_main(self, utilities.getlogouturl(self), result, wordCount, totalCount)
        # If user is not logged in create login url
        else:
            renderer.render_login(self, utilities.getloginurl(self))

    # POST-request
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        my_user = utilities.getuser()
        button = self.request.get('button')
        input_text = utilities.preparetextinput(self.request.get('value'))
        # Upload Anagrams
        file = self.request.get('uploadFile')

        if button == 'Upload':
            openFile = open(file)
            readLine = openFile.readline()
            while readLine:
                word = (readLine.strip('\n\r')).lower()

                permutations = utilities.a_permutations(word)
                wordsinfo = utilities.filterenglishwords(permutations)

                # Add anagram
                anagram_id = my_user.key.id() + '/' + utilities.generateid_for_users(word)
                anagram_key = ndb.Key(Anagram, anagram_id)
                anagrams = anagram_key.get()

                if anagrams:
                    # Anagram with primary key already exists
                    utilities.addtoanagram(word, wordsinfo, anagram_key)
                else:
                    # This primary key does not exist so creates a new anagram object to datastore
                    utilities.addanagram_new(my_user, word, wordsinfo, anagram_id, anagram_key)

                readLine = openFile.readline()

            openFile.close()
            self.redirect('/')
        # Search Anagrams
        if button == 'Search':
            search_result = self.search(input_text, my_user)
            renderer.render_search(self, input_text, search_result)
        # Generate Anagrams
        elif button == 'Generate':
            words = self.generate(input_text, my_user)
            renderer.render_search(self, input_text, words)

    # Returns a list with all the items (if nothing found returns None)
    def search(self, text, my_user):
        anagram_id = my_user.key.id() + '/' + utilities.generateid_for_users(text)
        anagram = ndb.Key(Anagram, anagram_id).get()

        if anagram:
            result = anagram.words
            result.remove(text)
            return result
        else:
            return None

    def generate(self, input_text, my_user):
        permutations = utilities.a_permutations(input_text)
        anagrams = Anagram.query().fetch()
        sorted_list= []
        result = []
        for i in range(len(anagrams)):
            sorted_list.append(anagrams[i].sorted_word)
        for i in permutations:
            for j in sorted_list:
                if i == j:
                    anagram_id = my_user.key.id() + '/' + j
                    anagram = ndb.Key(Anagram, anagram_id).get()
                    for x in anagram.words:
                        result.append(str(x))
        if input_text in result:
            result.remove(input_text)
        return result

# Starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
        ('/addWord', AddWord)
    ], debug=True)
