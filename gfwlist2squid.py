#!/usr/bin/env python
#encoding: utf-8

# forked from sorz/gfwlist2regex.py

# gwflist | Adblock Format 
# https://adblockplus.org/en/filters

# squid rules
# squid only matchs DOMAIN, not URL, so the rules in gwflist should changed to DOMAIN.

# Example:
# china-mmm.jp.net                      -> china\-mmm\.jp\.net
# ||china-mmm.net                       -> ^china\-mmm\.net
# |http://85.17.73.31/                  -> ^85\.17\.73\.31
# 21andy.com/blog                       -> 21andy\.com
# |http://cdn*.abc.com/                 -> ^cdn(.*)\.abc\.com
# /^https?:\/\/[^\/]+blogspot\.(.*)/    -> ^blogspot\.(.*)

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

import urllib2
import re
from base64 import b64decode


LIST_URL   = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
DECODE_FILE  = 'gwflist.decode.txt'
WHITE_FILE = 'whitelist.url_regex.lst'
BLACK_FILE = 'balcklist.url_regex.lst'

def convert_line(line):
    line = line.rstrip()
    #regex already
    if line[0] == '/' and line[-1] == '/':
        #remove https?:\/\/[^\/]+
        rline = line[1:-1]
        rline = rline.replace(r'^https?:\/\/[^\/]+', r'^[^\/]+')
        return rline
    
    if line.startswith('||'):
        rline = line[2:]
        rline = rline.replace(r'http://', '')
        rline = rline.replace(r'https://', '')
        rline = re.escape(rline)
        rline = rline.replace(r'\*', '(.*)')
        #return '^https?:\/\/[^\/]+' + rline
        return '^[^\/]*' + rline
    elif line.startswith('|'):
        rline = line[1:]
        rline = rline.replace(r'http://', '')
        rline = rline.replace(r'https://', '')
        rline = re.escape(rline)
        rline = rline.replace(r'\*', '.*')
        return '^' + rline
    elif line[-1] == '|':
        rline = line[:-1]
        rline = rline.replace(r'http://', '')
        rline = rline.replace(r'https://', '')
        rline = re.escape(rline)
        rline = rline.replace(r'\*', '.*')
        return rline + '$'
    else:
        rline = line
        rline = rline.replace(r'http://', '')
        rline = rline.replace(r'https://', '')
        rline = re.escape(rline)
        rline = rline.replace(r'\*', '.*')
        return rline

        
def convert(gfwlist):
    black = open(BLACK_FILE, 'w')
    white = open(WHITE_FILE, 'w')
    
    for l in gfwlist.split('\n'):
        #l = l[:-1]
        if not l or l[0] == '!' or l[0] == '[':
            continue
            
        if l.startswith('@@'):
            white.write(convert_line(l[2:]) + '\n')
        else:
            black.write(convert_line(l) + '\n')

            
def main():

  isFromURL = 1
  
  if (isFromURL):
    #open from URL
    src = urllib2.urlopen(LIST_URL).read()
    src = b64decode(src)
    decode = open(DECODE_FILE, 'w')
    decode.write(src)
    convert(src)
  else:
    open from local file
    src = open(DECODE_FILE, 'r').read()
    convert(src)
             
if __name__ == '__main__':
  main()
