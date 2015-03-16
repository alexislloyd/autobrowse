#!/usr/bin/env python

import os.path
import json
import urllib2
from urllib2 import Request, urlopen, URLError
from urlparse import urlparse
import simplejson
import tornado.web
import tornado.ioloop
from bs4 import BeautifulSoup
import random

class LoadNext(tornado.web.RequestHandler):
     def get(self):
        url = self.get_argument("url", None)
        if url is None:
            url = 'http://en.wikipedia.org/wiki/Special:Random'
            first_load = True
        else:
            first_load=False

        if url.find("//") == 0:
            url = "http:"+url 
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print ("deadend redirect")
            response = {"url": "/deadend?code="+str(e.code)}
            self.write(json.dumps(response))
        else:

            html = response.read()
            soup = BeautifulSoup(html)

            if first_load is True:
                ext_links = soup.find_all("a", class_="external")
                new_url = random.choice(ext_links)["href"]
                if url.find('//') == 0:
                    self.render("index.html", new_url="http:"+new_url)
                else:
                    self.render("index.html", new_url=new_url)

            else:
                links = soup.find_all("a")
                ext_links = []
                for link in links:

                    if link.has_key('href'):
                        print link['href']
                        url = link['href']
                        if url.find('http') != -1:
                            ext_links.append(url)
                        if url.find('//') == 0:
                            ext_links.append("http:"+url)
                
                print len(ext_links)
                if (len(ext_links) == 0):
                    response = {"url": "/deadend?code=0"}
                    response = json.dumps(response)
                else:
                    new_url = random.choice(ext_links)
                    response = json.dumps({"url": new_url})
                self.write(response)
        
class DeadEnd(tornado.web.RequestHandler):
    def get(self):
        errcode = self.get_argument('code', default="-1")

        message = "Something went wrong: error code " + errcode
        errcode = int(errcode)
        if errcode == 0:
            message += ". No external links on page"
        if errcode == 404:
            message += ". Dead link selected from last page"
        self.render("deadend.html", message=message)




settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
)

application = tornado.web.Application([
    (r"/", LoadNext),
    (r"/deadend", DeadEnd)
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

    