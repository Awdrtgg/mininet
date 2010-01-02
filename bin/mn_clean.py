#!/usr/bin/env python
"""Mininet Cleanup

@author Bob Lantz (rlantz@cs.stanford.edu)

Unfortunately, Mininet and OpenFlow don't always clean up
properly after themselves. Until they do (or until cleanup
functionality is integrated into the python code), this
script may be used to get rid of unwanted garbage. It may
also get rid of 'false positives', but hopefully nothing
irreplaceable!
"""

from subprocess import Popen, PIPE
import re

from mininet.util import quietRun
from mininet.xterm import cleanUpScreens

def sh( cmd ): 
   "Print a command and send it to the shell"
   print cmd
   return Popen( [ '/bin/sh', '-c', cmd ], 
      stdout=PIPE ).communicate()[ 0 ]

 
def cleanup():
   """Clean up junk which might be left over from old runs;
      do fast stuff before slow dp and link removal!"""
      
   print "*** Removing excess controllers/ofprotocols/ofdatapaths/pings/noxes"
   zombies = 'controller ofprotocol ofdatapath ping nox_core lt-nox_core '
   zombies += 'udpbwtest'
   # Note: real zombie processes can't actually be killed, since they 
   # are already (un)dead. Then again,
   # you can't connect to them either, so they're mostly harmless.
   sh( 'killall -9 ' + zombies + ' 2> /dev/null' )

   print "*** Removing junk from /tmp"
   sh( 'rm -f /tmp/vconn* /tmp/vlogs* /tmp/*.out /tmp/*.log' )

   print "*** Removing old screen sessions"
   cleanUpScreens()

   print "*** Removing excess kernel datapaths"
   dps = sh( "ps ax | egrep -o 'dp[0-9]+' | sed 's/dp/nl:/'" ).split( '\n')
   for dp in dps: 
      if dp != '': sh( 'dpctl deldp ' + dp )
      
   print "*** Removing all links of the pattern foo-ethX"
   links = sh( "ip link show | egrep -o '(\w+-eth\w+)'" ).split( '\n' )
   for link in links: 
      if link != '': sh( "ip link del " + link )

   print "*** Cleanup complete."

if __name__ == "__main__":
   cleanup()
