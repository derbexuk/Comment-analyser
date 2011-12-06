#!/usr/bin/python

from mongo_connection import MongoConnection
import operator

class CommentModel(MongoConnection) :
  def count(self):
    print self.db.comments.find({"feed" : "suncomments"}).count()

  def getAllComments(self, limit=0) :
    return self.db.comments.find({"feed" : "suncomments"},{"id" : 1, "content" : 1}).limit(limit)

import string

class Indexer :

  def __init__(self):
    self.dictonary = {}
    self.sortedDict = {}

  def index(self, str):
    from stopList import stop_list

    for word in self.preprocess(str):
      if word in stop_list :
        continue
      self.dictonary[word] = self.dictonary.get(word,0) + 1

  def sort(self):
    self.sortedDict = sorted(self.dictonary.iteritems(), key=operator.itemgetter(1), reverse=True)

  def get(self, limit=10):
    if limit > 0:
      return self.sortedDict[0:limit]
    return self.sortedDict

  def preprocess(self, s) :
    #Comes out as unicode ( guess) need to typecast to string for translate
    try :
      s = str(s.lower())
      s = s.translate(None, string.punctuation)
    except UnicodeEncodeError  as msg : 
      print 'Unicode Error : ', msg
    words = s.split()
    return words

if __name__ == "__main__":
  c = CommentModel()
  indexer = Indexer()

  for comment in c.getAllComments(0) :
    indexer.index(comment['content'])

  indexer.sort()
  print indexer.get()
