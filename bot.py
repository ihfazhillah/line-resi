#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="ramdani"
__email__="ramdani@sopwer.net"
__date__ ="$Jun 2, 2015 9:04:46 PM$"


from line import LineClient, LineGroup, LineContact
from bs4 import BeautifulSoup
import dryscrape
import time
from config import EMAIL, PASSWORD

DOMAIN = 'http://cekresi.com'
URL = DOMAIN + '/index.php'

class CekResi:

  def __init__(self, no_resi=None):
    self.no_resi = no_resi

  def post(self, no_resi=None):

    session = dryscrape.Session()
    session.visit(DOMAIN)
    noresi = session.at_css('#noresi')

    if self.no_resi:
      noresi.set(self.no_resi)
    elif noresi:
      noresi.set(no_resi)
    else:
      raise 'Something went wrong'

    button = session.at_css('#cekresi')
    button.click()
    time.sleep(2)
    return self.parse(session.body())

  def parse(self, body):
    soup = BeautifulSoup(body)
    data = soup.find('table')
    try:
      data = data.text.replace("\n\n",' ')
      data = data.replace("\n",', ')
    except:
      print "ngk ada data"

      data = 'Resi tidak ditemukan'
    return data.strip()

def run_bot():

  token = 'DSDul00LGgZArl7BpnG9.7G5I6BFxft9H3fpsy5auMq.u/pdhWo6QiO5vB9jW+JwaGSGWdf8/anhhyE7dpiewX0='

  try:
     client = LineClient(EMAIL, PASSWORD)
  #   client = LineClient(authToken=token)
  except:
     print "Login Failed"

  print "===START SERVER==="
  while True:
     op_list = []

     for op in client.longPoll():
        op_list.append(op)

     for op in op_list:
        sender   = op[0]
        receiver = op[1]
        message  = op[2]

        cr = CekResi(message.text)
        print "RESI %s" % message.text
        response = cr.post()
        msg = response
        sender.sendMessage("[%s] %s" % (sender.name, msg))

if __name__ == '__main__':
  run_bot()

