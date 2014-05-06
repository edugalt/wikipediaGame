import urllib.request
import urllib.parse
import json


def get_links(start_page, wikipedia_language='en'):
    print('get_links(%s)' % start_page)
    # parameters for building a string later:
    # pllimit limits the number of links to return (max is 500 | 5000 for bots see http://en.wikipedia.org/w/api.php )
    # the plcontinue value returned from the api can be used to continue of this is exceeded
    # plnamespace: see here: http://en.wikipedia.org/wiki/Wikipedia:Namespace

    def get_more_links(more_parameters=()):
        parameters = {"format": "json",
                      "action": "query",
                      "prop": "links",
                      "pllimit": 500,
                      "plnamespace": 0,
                      "titles": urllib.parse.quote(start_page.encode("utf8"))}
        parameters.update(more_parameters)

        queryString = "&".join("%s=%s" % (k, v) for k, v in parameters.items())

        url = "http://%s.wikipedia.org/w/api.php?%s" % (wikipedia_language, queryString)

        #get json data and make a dictionary out of it:
        request = urllib.request.urlopen(url)
        encoding = request.headers.get_content_charset()
        jsonData = request.read().decode(encoding)
        data = json.loads(jsonData)

        print(data['query']['pages'].keys())

        pageId = list(data['query']['pages'])[0]
        linkList = data['query']['pages'][str(pageId)]['links']
        return [entry["title"] for entry in linkList], data

    all_links, data = get_more_links()

    # Each time we get the dictionary we need to check if "query-continue" exists amd then repeat the stuff from before:
    while "query-continue" in data:
        links, data = get_more_links({"plcontinue": data["query-continue"]["links"]["plcontinue"]})
        all_links += links

    return all_links

if __name__ == '__main__':
    #lots of links:
    #startPage = "Albert Einstein"
    #fewer links:
    startPage = "Bruckhäusl (Erlbach)"
    print(get_links(startPage))
