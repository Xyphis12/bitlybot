# Import some necessary libraries.
import sys
import socket
import re
import urllib2
import bitly
from bs4 import BeautifulSoup

###SETUP###
execfile('setup.txt') # import info #file with login variables in it (info.py)
api = bitly.Api(login=apilogin, apikey=apikey) # bitly information


###FUNCTIONS###

def visible(element):
  if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    return False
  elif re.match('', unicode(element)): return False
  elif re.match('\n', unicode(element)): return False
  return True


#what to do when commands are submitted e.g. !talk
def commands(nick,channel,message):
   if message.find("http")!=-1:
      find_urls_http(nick,channel,message)
   elif message.find("www")!=-1:
      find_urls_http(nick,channel,message)
  # elif message.find("trash")!=-1:
     # ircsock.send("PRIVMSG "+ channel +" :"+ nick +" gets a foobar! woohoo!\n")


#ctcp version request answer from the bot
def version(nick):
   if message.find("VERSION")!=-1:
      ircsock.send('NOTICE : '+nick+' IRC BOT \n')


#This is a must function! It will respond to server Pings and keep bot connected.
def ping():
  ircsock.send("PONG :Pong\n")


# This is the send message function, it simply sends messages to the channel.
def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")


# This function is used to join channels.
def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")


#This function responds to a user that inputs "Hello Mybot"
def hello(nick):
  ircsock.send("PRIVMSG "+ channel +" :Hello "+ nick +"!\n")


#random function to trash talk picked person
def trash(who):
  ircsock.send("PRIVMSG "+ channel +"Shut up. You've been warned"+ who +"\n")


#finds http* urls in chat and processes them for bit.ly links
def find_urls_http(nick,channel,message):
    """ Extract all URL's from a string & return as a list """

    url_list = re.findall("(?P<url>https?://[^\s]+)",message) #look for url with http* on the address
    url_list = re.findall("(?P<url>www[^\s]+)",message) #look for url with www* on the address
    short = api.shorten(url_list) #send url to api
    site = ''.join(url_list) #join list of urls from chat
    shortstr = ''.join(short) # Join list of urls from bitly
    content = urllib2.urlopen(site).read() # read the website
    soup = BeautifulSoup(content) # grab the content
    titl = soup.title.string # grab title strings
    #texts = soup.findAll(text=True) #grab text
    #visible_texts = filter(visible, texts) #make sure its visable 
    #det = (dat[:75] + '..') if len(visible_texts) > 75 else visible_texts # stop after 75 chars
    ircsock.send('PRIVMSG %s :%s\r\n' % (channel,shortstr))#print out url
    ircsock.send('PRIVMSG %s :%s\r\n' % (channel,titl))#print out url

'''
#function for terminating the bot remotely for whatever reason only has owner access
def exit(command):
    if (command == 'exit')
'''
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port)) # Here we connect to the server using port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Hey\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! It might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server
  
  if ircmsg.find(' PRIVMSG ')!=-1:
      nick=ircmsg.split('!')[0][1:]
      channel=ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
      try: #find error in case the command throws an exception
         commands(nick,channel,ircmsg)
      except:
         pass #this skips the error instead of doing anything about it
  
  if ircmsg.find(":!exit") != -1:
      sys.exit(0)
  
  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
      ping()
