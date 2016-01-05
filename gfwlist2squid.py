#!/usr/bin/env python
#encoding: utf-8

# forked from sorz/gfwlist2regex.py

# gwflist | Adblock Format 
# https://adblockplus.org/en/filters

# Squid 'acl dstdom_regex' Rules
# dstdom_regex only matchs DOMAIN, not URL, so the rules in gwflist should changed to DOMAIN.

# Usage:
# Add following lines into squid.conf: (squid v2.7)
# ----
# acl whitelist dstdom_regex 'whitelist.url_regex.lst'
# acl balcklist dstdom_regex 'balcklist.url_regex.lst'
# prefer_direct on
# always_direct allow whitelist
# never_direct  allow balcklist
# cache_peer 127.0.0.1 parent 48081 0 name=ss1 round-robin
# cache_peer 127.0.0.1 parent 48082 0 name=ss2 round-robin
# cache_peer_access ss1 deny whitelist
# cache_peer_access ss2 deny whitelist
# cache_peer_access ss1 allow balcklist
# cache_peer_access ss1 allow balcklist
# forwarded_for transparent
# via off
# ----

# Example:
# china-mmm.jp.net                      -> china\-mmm\.jp\.net
# ||china-mmm.net                       -> ^china\-mmm\.net
# |http://85.17.73.31/                  -> ^85\.17\.73\.31$
# 21andy.com/blog                       -> 21andy\.com$
# |http://cdn*.abc.com/                 -> ^cdn(.*)\.abc\.com
# /^https?:\/\/[^\/]+blogspot\.(.*)/    -> ^blogspot\.(.*)
# @@||baidu.com                         -> ^baidu\.com

import urllib2
import re
from base64 import b64decode


GWFLIST_URL   = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
GWFLIST_FILE  = 'gwflist.txt'
DECODE_FILE  = 'gwflist.decode.txt'
WHITE_FILE = 'whitelist.url_regex.lst'
BLACK_FILE = 'balcklist.url_regex.lst'

def url2domain(s):
  #remove http(s)://
  if (s.startswith('http://')):
    s = s[7:]
  if (s.startswith('https://')):
    s = s[8:]
  #remove url path
  i = s.find('/')
  if (i >= 0){
    s = s[:i]
  }
  #escape regex chars
  r = re.escape(s)
  r = r.replace(r'\*', '(.*)')
  if (r.endswith(r'\/'))
    r = r[:-2] + '$'
  return r

def convert_line(line):
  line = line.rstrip()
  
  #regex rules
  if line[0] == '/' and line[-1] == '/':
    #simple remove https?:\/\/[^\/]+
    rline = line[1:-1]
    rline = rline.replace(r'https?:\/\/[^\/]+', '')
    return rline
  
  #normal rules
  if line.startswith('||'):
    #add ^ at beginning    
    rline = line[2:]
    rline = url2domain(rline)
    return '^' + rline
  elif line.startswith('|'):
    rline = line[1:]
    rline = url2domain(rline)
    return '^' + rline
  elif line[-1] == '|':
    rline = line[:-1]
    rline = url2domain(rline)
    return rline + '$'
  else:
    rline = line
    rline = url2domain(rline)
    return rline
    

        
def convert(gfwlist):
  black = open(BLACK_FILE, 'w')
  white = open(WHITE_FILE, 'w')
  
  for l in gfwlist.split('\n'):
    if not l or l[0] == '!' or l[0] == '[':
      continue
        
    if l.startswith('@@'):
      white.write(convert_line(l[2:]) + '\n')
    else:
      black.write(convert_line(l) + '\n')

            
def main():

  #set read gwflist from URL or FILE
  isFromURL = 1
  
  if (isFromURL):
    #read from URL
    src = urllib2.urlopen(GWFLIST_URL).read()
  else:
    #read from FILE
    open from local file
    src = open(GWFLIST_FILE, 'r').read()

  src = b64decode(src)
  decode = open(DECODE_FILE, 'w')
  decode.write(src)
  convert(src)
             
if __name__ == '__main__':
  main()
