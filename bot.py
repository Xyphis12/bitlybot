import socket
import re
import urllib2
import bitly
from bs4 import BeautifulSoup
 
api = bitly.Api(login='BITLY LOGIN', apikey='BITLY KEY') # bitly information
server = "irc.messwithus.com"   # Server
channel = "#chantobother"       # Channel
botnick = "NICK"                # Your bots nick
pref = "!"                      # Command Prefix
port = 6667                     # Port used to connect with
 
def commands(nick,channel,message):
   if message.find("http")!=-1: #when http is found
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
 
def find_urls(nick,channel,message):
    """ Extract all URL's from a string & return as a list """
 
    url_list = re.findall("(?P<url>https?://[^\s]+)",message) #look for url
    short=api.shorten(url_list)                               #send url to api
    site = ''.join(url_list)                                  #join list of urls from chat
    shortstr = ''.join(short)                                 #Join list of urls from bitly
    content = urllib2.urlopen(site).read()                    #Read the site associated with the URL
    soup = BeautifulSoup(content)
    titl = soup.title.string                                  #Set titl as what was in the title tag
    ircsock.send('PRIVMSG %s :%s : %s\r\n' % (channel,shortstr,titl)) #say short url and title
 
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
