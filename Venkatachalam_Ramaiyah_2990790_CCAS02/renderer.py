import jinja2
import os
import utilities

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def render_login(self, url):
    template_values = {'url': url}

    template = JINJA_ENVIRONMENT.get_template('/html/login.html')
    self.response.write(template.render(template_values))

def render_main(self, url, anagrams, wordCount,totalCount):
    template_values = {
        'url': url,
        'user': utilities.get_user(),
        'anagrams': anagrams,
        'wordCount': wordCount,
        'totalCount': totalCount
    }

    template = JINJA_ENVIRONMENT.get_template('/html/main.html')
    self.response.write(template.render(template_values))

def render_search(self, search_term, search_result):
    template_search_values = {
        'user': utilities.get_user(),
        'search_term': search_term,
        'search_result': search_result,
    }

    template = JINJA_ENVIRONMENT.get_template('/html/searchResult.html')
    self.response.write(template.render(template_search_values))
