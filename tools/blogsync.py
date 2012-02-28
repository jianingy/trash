#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import feedparser
import xmlrpclib
import getpass
import pprint
from optparse import OptionParser

pp = pprint.PrettyPrinter(indent=4)

def select_blogs(source):
  d = feedparser.parse(source)
  id = 1
  for e in d["entries"]:
    print "%d. %s" % (id, e.title)
    id = id + 1
  entries = []
  print
  print "Please enter the id of blogs you wanna sync (use space to seperate): ",
  for i in sys.stdin.readline().split(" "):
    if int(i) > len(d["entries"]):
      print >>sys.stderr, "WARNING: id %d out of range" % int(i)
      continue
    entries.append(d["entries"][int(i) - 1])
  print
  entries.reverse()
  return entries

def write_blog(target, user, blogs):
  server = xmlrpclib.Server(target);
  print "write blogs to %s using username %s" % (target, user)
  passwd = getpass.getpass()
  num_synced = 0
  for e in blogs:
    traceback = "<p>From: <a href=\"%s\">%s</a></p>" %(e.link, e.link)
    data = {"description": traceback + e.summary, "title": e.title}
    server.metaWeblog.newPost('1', user, passwd, data, True);
    num_synced = num_synced + 1
  print "%d blogs synced" % num_synced

if __name__ == "__main__":
  op = OptionParser();
  op.add_option("-s", "--source", dest="source", help="feed source")
  op.add_option("-t", "--target", dest="target", help="target site")
  op.add_option("-u", "--user", dest="user", help="target username")
  (opt, extra) = op.parse_args();

  blogs = select_blogs(opt.source)

  write_blog(opt.target, opt.user, blogs)
# vim: ts=2 sw=2 ai et
