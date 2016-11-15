# File: transcript/modules/re/__init__.py
# Author: Carl Allendorph
# Date: 13NOV2016
#
# Description:
#    This file contains the definition of a simulated re python
# regular expression parsing module. The idea is to leverage the
# javascript native regular expression interface as much as
# possible. In fact, where necessary, this module chooses the
# javascript idiosyncracies over the python ones.
#
#

from org.transcrypt.stubs.browser import __pragma__

# Flags

T = (1<<0)
TEMPLATE = T

I = (1<<1)
IGNORECASE = I

# Deprecated
L = (1<<2)
LOCALE = L

M = (1<<3)
MULTILINE = M

S = (1 << 4)
DOTALL = S
# Legacy - Unicode by default in Python 3
U = (1 << 5)
UNICODE = U
X = (1 << 6)
VERBOSE = X
DEBUG = (1<<7)

A = (1<<8)
ASCII = A

# This is a javascript specific flag
Y = (1 << 16)
STICKY = Y
G = (1 << 17)
GLOBAL = G

class error(Exception):
    """ Regular Expression Exception Class
    """
    def __init__(self, msg, pattern = None, pos = None):
        """
        """
        self.msg = msg
        self.pattern = pattern
        self.pos = pos
        # @todo - lineno and colno attributes

class Match(object):
    """ Resulting Match from a Regex Operation
    """
    def __init__(self, mObj, string, pos, endpos, rObj):
        """
        """
        self._obj = mObj

        # @todo - make these into properties
        self.pos = pos
        self.endpos = endpos
        self.re = rObj
        self.string = string

        # @note - javascript does not have the concept
        #   of named groups so we will never be able to
        #   implement this.
        self.lastgroup = None
        self.lastindex = self._lastMatchGroup()

    def _lastMatchGroup(self):
        """ Determine the last matching group in the object
        """
        if ( len(self._obj) > 1 ):
            for i in range(len(self._obj)-1,0,-1):
                if (self._obj[i] is not None):
                    return(i)
            # None of the capture groups matched -
            # this seems like it should happen
            return(None)
        else:
            # No Capture Groups
            return(None)

    def expand(self, template):
        """
        """
        raise Exception("Not Implemented")

    def group(self, *args):
        """ Return the string[s] for a group[s]
            if only one group is provided, a string is returned
            if multiple groups are provided, a tuple of strings is returned

        """
        ret = []
        if ( len(args) > 0 ):
            for index in args:
                if ( index >= len(self._obj) ):
                    # js will return an 'undefined' and we
                    # want this to return an index error
                    # Built-in Exceptions not defined ?
                    #raise IndexError("no such group")
                    raise Exception("no such group")
                ret.append(self._obj[index])
        else:
            ret.append(self._obj[0])

        if ( len(ret) == 1 ):
            return(ret[0])
        else:
            return(tuple(ret))

    def groups(self, default = None):
        """ Get all the groups in this match. Replace any
            groups that did not contribute to the match with default
            value.
        """
        if ( len(self._obj) > 1 ):
            ret = self._obj[1:]
            return(tuple([x if x is not None else default for x in ret]))
        else:
            return(tuple())

    def groupdict(self, default = None):
        """ The concept of named captures doesn't exist
        in javascript so this will likely never be implemented.
        """
        raise Exception("Not Implemented")

    def start(self, group = 0):
        """
        """
        if ( group >= len(self._obj) ):
            raise IndexError("no such group")

        if ( group == 0 ):
            return(self._obj.index)
        else:
            # We don't really have a good way to do
            # this in javascript. so we will attempt
            # to match the string we found as a
            # sub position in the main string - this
            # isn't perfect though because you could
            # create a capture that only matches on
            # the last in a group - this is a difficult
            # problem to solve without completely
            # re-writing the regex engine from scratch.
            if ( self._obj[group] is not None ):
                r = compile(escape(self._obj[group]))
                m = r.search(self._obj[0])
                if m:
                    return(self._obj.index + m.start())
                else:
                    raise Exception("Failed to find capture group")
            else:
                # This capture did not contribute the match.
                return(-1)

    def end(self, group = 0):
        """
        """
        if ( group >= len(self._obj) ):
            raise IndexError("no such group")

        if ( group == 0 ):
            return( self._obj.index + len(self._obj[0]))
        else:
            # We don't really have a good way to do
            # this in javascript. so we will attempt
            # to match the string we found as a
            # sub position in the main string - this
            # isn't perfect though because you could
            # create a capture that only matches on
            # the last in a group - this is a difficult
            # problem to solve without completely
            # re-writing the regex engine from scratch.
            if ( self._obj[group] is not None ):
                r = compile(escape(self._obj[group]))
                m = r.search(self._obj[0])
                if m:
                    return(self._obj.index + m.end())
                else:
                    raise Exception("Failed to find capture group")
            else:
                # This capture did not contribute the match.
                return(-1)

    def span(self, group = 0):
        """
        """
        if ( group >= len(self._obj) ):
            raise IndexError("no such group")
        return( (self.start(group), self.end(group)) )

class Regex(object):
    """ Regular Expression Object
    """
    def __init__(self, pattern, flags):
        """
        """
        self._jsFlags = self._convertFlags(flags)
        self._obj = __new__(RegExp(pattern, self._jsFlags))
        # @todo make this readonly property
        self.pattern = pattern
        # @todo make this readonly property
        self.flags = flags
        # @todo - make numGroups a read-only prop
        # we will determine groups by using another regex
        groupCounterRegex = __new__(RegExp(pattern + '|'))
        self.groups = groupCounterRegex.exec('').length-1
        self.groupindex = {}

    def _convertFlags(self, flags):
        """ Convert the Integer map based flags to a
        string list of flags for js
        """
        fMap = {
            ASCII : "",
            DEBUG : "",
            IGNORECASE : "i",
            MULTILINE : "m",
            STICKY : "y",
            UNICODE : "u",
            GLOBAL: "g",
            }
        ret = "".join([fMap[k] for k in fMap.keys() if (flags & k) > 0])
        return(ret)

    def _getTargetStr(self, string, pos, endpos):
        """
        """
        endPtr = len(string)
        if ( endpos is not None ):
            if ( endpos < endPtr):
                endPtr = endpos
        if ( endPtr < 0 ):
            endPtr = 0
        ret = string[pos:endPtr]
        return(ret)

    def _patternHasCaptures(self):
        """ Check if the regex pattern contains a capture
            necessary to make split behave correctly
        """
        return(self.groups > 0)

    def search(self, string, pos=0, endpos=None):
        """
        """
        if ( endpos is None ):
            endpos = len(string)
        # @note - pos/endpos don't operate like a slice
        #   here - we need to search complete string and then
        #   reject if the match happens outside of pos:endpos
        rObj = self._obj
        m = rObj.exec(string)
        if m:
            if ( m.index < pos or m.index > endpos ):
                return(None)
            else:
                # Valid match we will create a match object
                return( Match(m, string, pos, endpos, self))
        else:
            return(None)


    def match(self, string, pos=0, endpos = None):
        """
        """
        target = string
        if ( endpos is not None ):
            target = target[:endpos]
        else:
            endpos = len(string)

        rObj = self._obj
        m = rObj.exec(target)
        if m:
            # Match only at the beginning
            if ( m.index == pos ):
                return( Match(m, string, pos, endpos, self))
            else:
                return(None)
        else:
            return(None)

    def fullmatch(self, string, pos=0, endpos = None):
        """
        """
        target = string
        strEndPos = len(string)
        if ( endpos is not None ):
            target = target[:endpos]
            strEndPos = endpos

        rObj = self._obj
        m = rObj.exec(target)
        if m:
            obsEndPos = (m.index+len(m[0]))
            if ( m.index == pos and obsEndPos == strEndPos ):
                return( Match(m, string, pos, strEndPos, self))
            else:
                return(None)
        else:
            return(None)

    def split(self, string, maxsplit = 0):
        """
        """
        # JS split is slightly different from Python
        # the "limit" arg limits the number of elements in the
        # returned in the list - it doesn't limit the number of
        # splits. So we have to differentiate between regex with
        # captures and

        if ( maxsplit < 0 ):
            return([string])

        mObj = None
        rObj = self._obj
        if ( maxsplit == 0 ):
            __pragma__(
                'js', '{}',
                '''
                mObj = string.split(rObj)
                ''')
            return(mObj)
        else:
            # the split limit parameter in js does not behave like
            # the maxsplit parameter in python - hence we need to
            # do this manually.
            # @todo - make this better handle the flags
            rObj = __new__(RegExp(self.pattern, "g"))
            ret = []
            lastM = None
            cnt = 0
            for i in range(0, maxsplit):
                m = rObj.exec(string)
                if m:
                    cnt += 1
                    if ( lastM is not None ):
                        # subsequent match
                        start = lastM.index + len(lastM[0])
                        head = string[start:m.index]
                        ret.append(head)
                        if ( len(m) > 1 ):
                            ret.extend(m[1:])
                    else:
                        # First match
                        head = string[:m.index]
                        ret.append(head)
                        if ( len(m) > 1 ):
                            ret.extend(m[1:])
                    lastM = m

                else:
                    break

            if ( lastM is not None ):
                endPos = lastM.index + len(lastM[0])
                end = string[endPos:]
                ret.append(end)

            return(ret)

    def findall(self, string, pos = 0, endpos = None):
        """
        """
        target = self._getTargetStr(string, pos, endpos)

        # Unfortunately, js RegExp.match does not behave
        # like findall behaves in python - it doesn't
        # pull out 'captures' like python expects so we
        # are going to use RegExp.exec instead of match
        # @todo - fix flags here
        rObj = __new__(RegExp(self.pattern, "g"))
        ret = []
        while( True ):
            m = rObj.exec(target)
            if m:
                if ( len(m) > 2 ):
                    # Captures Present and we need to
                    # convert to a tuple
                    ret.append( tuple(m[1:]))
                elif ( len(m) == 2 ):
                    # 1 Capture
                    ret.append(m[1])
                else:
                    # No captures
                    ret.append(m[0])
            else:
                break

        return(ret)

    def finditer(self, string, pos, endpos = None):
        """
        """
        raise Exception("Not Implemented")


    def sub(self, repl, string, count = 0):
        """
        """
        ret,_ = self.subn(repl, string, count)
        return(ret)

    def subn(self, repl, string, count = 0):
        """
        """
        rObj = self._obj
        if ( count == 0):
            if ( callable(repl) ):
                # Function - we need to handle each match individually
                # with exec because the necessary functionality doesn't
                # exist in js
                def func(m):
                    return( repl(Match(m, string, 0, len(string), self)))

                ret = string.replace(rObj, func)
                return(ret)
            else:
                # repl is likely a string so we can use it directly
                ret = string.replace(rObj, repl)
                return(ret)
        else:
            # js has no 'count' arg so we will need to implement
            # as a string of execs.
            raise Exception("Not Implemented")


def compile(pattern, flags = 0):
    """ Compile a regex object and return
        an object that can be used for further processing.
    """
    p = Regex(pattern, flags)
    return(p)

def search(pattern, string, flags = 0):
    """ Search a string for a particular matching pattern
    """
    p = Regex(pattern, flags)
    return( p.search(string) )


def match(pattern, string, flags = 0):
    """ Match a string for a particular pattern
    """
    p = Regex(pattern, flags)
    return( p.match(string) )

def fullmatch(pattern, string, flags = 0):
    """
    """
    p = Regex(pattern, flags)
    return( p.fullmatch(string) )

def split(pattern, string, maxsplit = 0, flags = 0):
    """
    """
    p = Regex(pattern, flags)
    return( p.split(string, maxsplit) )

def findall(pattern, string, flags = 0):
    """
    """
    p = Regex(pattern, flags)
    return( p.findall(string) )

def finditer(pattern, string, flags = 0):
    """
    """
    p = Regex(pattern, flags)
    return( p.finditer(string) )

def sub(pattern, repl, string, count = 0, flags = 0):
    """
    """
    p = Regex(pattern, flags)
    return( p.sub(repl, string, count) )

def subn(pattern, repl, string, count = 0, flags = 0):
    """
    """
    p = Regex(pattern, flags)
    return( p.subn(repl, string, count) )

def escape(string):
    """ Escape a passed string so that we can send it to the
    regular expressions engine.
    """
    ret = None
    def replfunc(m):
        if ( m[0] == "\\" ):
            return("\\\\\\\\")
        else:
            return("\\\\" + m[0])

    # @note - this isn't working for '\' characters
    #   I'm not sure why but python puts in "\\\\" for "\"
    #   instead of "\\"
    __pragma__(
        'js', '{}',
        '''
        var r = /[^A-Za-z\d]/g;
        ret = string.replace(r, replfunc);
        ''')
    if ( ret is not None ):
        return(ret)
    else:
        raise Exception("Failed to escape the passed string")

def purge():
    """ I think this function is unnecessary but included to keep interface
    consistent.
    """
    pass
