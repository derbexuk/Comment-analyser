#!/usr/bin/python

from mongo_connection import MongoConnection
from array import array
import operator

class CommentModel(MongoConnection) :
  def count(self):
    print self.db.comments.find({"feed" : "suncomments"}).count()

  def getAllComments(self, limit=0) :
    return self.db.comments.find({"feed" : "suncomments"},{"id" : 1, "content" : 1}).limit(limit)

import string

class Indexer :

  def __init__(self):
    """Words and stats"""
    self.dictonary = {} 
    self.reverseWord = {} 
    self.sortedDict = {}
    """articles to words"""
    self.reverseDict = {}
    """words to articles"""
    self.forwardDict = {}
    self.lastWord = 0

  def index(self, comment):
    from stopList import stop_list

    article_words = array('i')
    for word in self.preprocess(comment['content']):
      if word in stop_list :
        continue
      if  word in self.dictonary:
        self.dictonary[word]['count'] = self.dictonary[word]['count'] + 1
        #This won't be unique probably should be
        self.forwardDict[self.dictonary[word]['index']].append(comment['id'])
      else :
        self.dictonary[word] = {'index': self.lastWord, 'count': 1}
        self.forwardDict[self.lastWord] = array('i')
        self.forwardDict[self.lastWord].append(comment['id'])
        self.reverseWord[self.lastWord] = word
        self.lastWord = self.lastWord + 1

      article_words.append(self.dictonary[word]['index'])

    self.reverseDict[comment['id']] = article_words;

  def sort(self):
    self.sortedDict = sorted(self.dictonary.iteritems(), key=operator.itemgetter(1), reverse=True)

  def get(self, limit=10):
    #print repr(self.dictonary)
    if limit > 0:
      return self.sortedDict[0:limit]
    return self.sortedDict

  def preprocess(self, s) :
    #Comes out as unicode ( guess) need to typecast to string for translate
    try :
      s = str(s.lower())
      s = s.translate(None, string.punctuation)
    except UnicodeEncodeError  as msg : 
      X = 1
      #print 'Unicode Error : ', msg

    words = s.split()
    return words

if __name__ == "__main__":
  c = CommentModel()
  indexer = Indexer()

  for comment in c.getAllComments(100) :
    indexer.index(comment)

  indexer.sort()
  print str(comment['id'])  + ' : ' +  comment['content'] + '\n'
  for i in indexer.reverseDict[comment['id']]:
    print indexer.reverseWord[i] + ' '
