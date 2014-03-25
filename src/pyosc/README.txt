NOTE
    This documentation is very similar to the header in OSC.py. One day both should be merged and placed either
	in this file or in OSC.py to avoid diverging documentation.

DESCRIPTION
    This module contains an OpenSoundControl implementation (in Pure Python), based (somewhat) on the
    good old 'SimpleOSC' implementation by Daniel Holth & Clinton McChesney.

    This implementation is intended to still be 'Simple' to the user, but much more complete
    (with OSCServer & OSCClient classes) and much more powerful
    (the OSCMultiClient supports subscriptions & message-filtering,
    OSCMessage & OSCBundle are now proper container-types)

    ================
    OpenSoundControl
    ================

    OpenSoundControl is a network-protocol for sending (small) packets of addressed data over network sockets.
    The original OSC-implementation uses the UDP/IP protocol for sending and receiving packets.

	In early 2010 TCP was added as transport layer. The application of OSC as interprocess communication becomes more and more
	common and ask for increased reliability which can be accomodated by using TCP as transport. The OSC
	specifications 1.0 and 1.1 require that OSC data (messages and bundles) must be framed by their packet size
	as 32 bit integer in network byte order (which is big endian) when using streaming protocols. This new
	implementation provides server and client classes. Their use is illustrated in the testbench.

    OSC-packets come in two kinds:
    - OSC-messages consist of an 'address'-string (not to be confused with a (host:port) network-address!),
    followed by a string of 'typetags' associated with the message's arguments (ie. 'payload'),
    and finally the arguments themselves, encoded in an OSC-specific way.
    The OSCMessage class makes it easy to create & manipulate OSC-messages of this kind in a 'pythonesque' way
    (that is, OSCMessage-objects behave a lot like lists)

    - OSC-bundles are a special type of OSC-message containing only OSC-messages as 'payload'. Recursively.
    (meaning; an OSC-bundle could contain other OSC-bundles, containing OSC-bundles etc.)
    OSC-bundles start with the special keyword '#bundle' and do not have an OSC-address. (but the OSC-messages
    a bundle contains will have OSC-addresses!)
    Also, an OSC-bundle can have a timetag, essentially telling the receiving Server to 'hold' the bundle until
    the specified time.
    The OSCBundle class allows easy cration & manipulation of OSC-bundles.

    see also http://opensoundcontrol.org/spec-1_0

    ---------

    To send OSC-messages, you need an OSCClient, and to receive OSC-messages you need an OSCServer.

    The OSCClient uses an 'AF_INET / SOCK_DGRAM' type socket (see the 'socket' module) to send
    binary representations of OSC-messages to a remote host:port address.

    The OSCServer listens on an 'AF_INET / SOCK_DGRAM' type socket bound to a local port, and handles
    incoming requests. Either one-after-the-other (OSCServer) or in a multi-threaded / multi-process fashion
    (ThreadingOSCServer / ForkingOSCServer). If the Server has a callback-function (a.k.a. handler) registered
    to 'deal with' (i.e. handle) the received message's OSC-address, that function is called, passing it the (decoded) message

    The different OSCServers implemented here all support the (recursive) un-bundling of OSC-bundles,
    and OSC-bundle timetags.

    In fact, this implementation supports:

    - OSC-messages with 'i' (int32), 'f' (float32), 's' (string) and 'b' (blob / binary data) types
    - OSC-bundles, including timetag-support
    - OSC-address patterns including '*', '?', '{,}' and '[]' wildcards.

    (please *do* read the OSC-spec! http://opensoundcontrol.org/spec-1_0 it explains what these things mean.)

    In addition, the OSCMultiClient supports:
    - Sending a specific OSC-message to multiple remote servers
    - Remote server subscription / unsubscription (through OSC-messages, of course)
    - Message-address filtering.

	The streaming server and clients use SOCK_STREAM sockets. Since this protocol is connection oriented
	replies are usually sent to the peer and not to a random server/client as in UDP implementations. If
	one likes to send messages to other clients/servers, a separate connection has to be established.

    ---------

    Stock, V2_Lab, Rotterdam, 2008

    ----------
    Changelog:
    ----------
    v0.3.0  - 27 Dec. 2007
            Started out to extend the 'SimpleOSC' implementation (v0.2.3) by Daniel Holth & Clinton McChesney.
            Rewrote OSCMessage
            Added OSCBundle

    v0.3.1  - 3 Jan. 2008
            Added OSClient
            Added OSCRequestHandler, loosely based on the original CallbackManager
            Added OSCServer
            Removed original CallbackManager
            Adapted testing-script (the 'if __name__ == "__main__":' block at the end) to use new Server & Client

    v0.3.2  - 5 Jan. 2008
            Added 'container-type emulation' methods (getitem(), setitem(), __iter__() & friends) to OSCMessage
            Added ThreadingOSCServer & ForkingOSCServer
                    - 6 Jan. 2008
            Added OSCMultiClient
            Added command-line options to testing-script (try 'python OSC.py --help')

    v0.3.3  - 9 Jan. 2008
            Added OSC-timetag support to OSCBundle & OSCRequestHandler
            Added ThreadingOSCRequestHandler

    v0.3.4  - 13 Jan. 2008
            Added message-filtering to OSCMultiClient
            Added subscription-handler to OSCServer
            Added support fon numpy/scipy int & float types. (these get converted to 'standard' 32-bit OSC ints / floats!)
            Cleaned-up and added more Docstrings

    v0.3.5 - 14 aug. 2008
            Added OSCServer.reportErr(...) method

    v0.3.6 - 19 April 2010
            Added Streaming support (OSC over TCP)
            Updated documentation
            Moved pattern matching stuff into separate class (OSCAddressSpace) to
                facilitate implementation of different server and client architectures.
            Moved testing code into separate testbench (testbench.py)

    -----------------
    Original Comments
    -----------------

    > Open SoundControl for Python
    > Copyright (C) 2002 Daniel Holth, Clinton McChesney
    >
    > This library is free software; you can redistribute it and/or modify it under
    > the terms of the GNU Lesser General Public License as published by the Free
    > Software Foundation; either version 2.1 of the License, or (at your option) any
    > later version.
    >
    > This library is distributed in the hope that it will be useful, but WITHOUT ANY
    > WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    > PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
    > details.

    > You should have received a copy of the GNU Lesser General Public License along
    > with this library; if not, write to the Free Software Foundation, Inc., 59
    > Temple Place, Suite 330, Boston, MA  02111-1307  USA

    > For questions regarding this module contact Daniel Holth <dholth@stetson.edu>
    > or visit http://www.stetson.edu/~ProctoLogic/

    > Changelog:
    > 15 Nov. 2001:
    >       Removed dependency on Python 2.0 features.
    >       - dwh
    > 13 Feb. 2002:
    >       Added a generic callback handler.
    >       - dwh

INSTALLING
    To install, simply run

    $ sudo ./setup.py install

    and provide your password.
    That's it. After this, you can use the 'pyOSC' module in your python-scripts by doing

    import OSC

DOCUMENTATION
    To get help, run

    $ pydoc OSC

    or, from within a python-interpreter

    >>> import OSC
    >>> help(OSC)

TESTING
    This package contains an OSC-testing program (testbench.py).
    Please have a good look at the source for this program for an example on how to use this module.

    To get help on how to invoke the test-program, run

    $ python testbench.py --help

    Usage: testbench.py [options]

    testbench.py OpenSoundControl-for-Python Test Program

    Options:
      -h, --help                  show this help message and exit
      -l LISTEN, --listen=LISTEN  listen on given host[:port]. default = '0.0.0.0:2222'
      -s SENDTO, --sendto=SENDTO  send to given host[:port]. default = '127.0.0.1:2222'
      -t, --threading             Test ThreadingOSCServer
      -f, --forking	              Test ForkingOSCServer
      -u, --usage                 Show this help message and exit
      -c, --streaming             Test streaming OSC (OSC over TCP)

