# Import some necessary libraries.
import socket
import re
import urllib2
import bitly
from bs4 
import BeautifulSoup
# import urllib
# Some basic variables used to configure the bot
api = bitly.Api(login='dtalley11', apikey='R_86a5369316becf81898a9af33108495d') # bitly information
server = "hubbard.freenode.net" # Server
channel = "#teamgelato" # Channel
botnick = "Botty234" # Your bots nick
pref = "!" #Command Prefix
port = 6666 #Port used to connect with

def visible(element):
      if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
         return False
      elif re.match('', unicode(element)): return False
      elif re.match('\n', unicode(element)): return False
      return True

def commands(nick,channel,message):
   if message.find("http")!=-1:
      try:
         find_urls(nick,channel,message)
      except IOError as e:
         print "http by itself fails to run"
   elif message.find("www")!=-1:
      find_urls(nick,channel,message)

def version(nick):
   if message.find("VERSION")!=-1:
      ircsock.send('NOTICE : '+nick+' IRC BOT \n')

def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send("PONG :Pong\n")

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(newnick): # This function responds to a user that inputs "Hello Mybot"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

def find_urls(nick,channel,message):
    """ Extract all URL's from a string & return as a list """

    url_list = re.findall("(?P<url>https?://[^\s]+)",message) #look for url
    #print "looking for url"
    short = api.shorten(url_list) #send url to api
    #print "shortening it"
    site = ''.join(url_list) #join list of urls from chat
    #print "joining lists"
    shortstr = ''.join(short) # Join list of urls from bitly
    #print site
    content = urllib2.urlopen(site).read()
    soup = BeautifulSoup(content)
    titl = soup.title.string
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    det = (dat[:75] + '..') if len(visible_texts) > 75 else visible_texts
    ircsock.send('PRIVMSG %s :%s\r\n' % (channel,shortstr))#print out url
    ircsock.send('PRIVMSG %s :%s - %s\r\n' % (channel,titl,det))#print out url

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
       try:
          commands(nick,channel,ircmsg)
       except:
          pass
  if ircmsg.find(":Hello "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello()
    hello()
  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
    ping()
