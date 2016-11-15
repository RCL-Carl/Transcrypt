import re

def run (autoTester):
    # Flag Tests
    autoTester.check(re.T)
    autoTester.check(re.I)
    autoTester.check(re.IGNORECASE)
    autoTester.check(re.M)
    autoTester.check(re.MULTILINE)
    autoTester.check(re.S)
    autoTester.check(re.DOTALL)
    autoTester.check(re.U)
    autoTester.check(re.UNICODE)
    autoTester.check(re.X)
    autoTester.check(re.VERBOSE)
    autoTester.check(re.A)
    autoTester.check(re.ASCII)
    # Test Utility Methods
    autoTester.check(re.escape("buf[34]"))
    autoTester.check(re.escape("C:\\asdf\\wewer\\"))
    autoTester.check(re.escape("func(int a) { return(3)};"))
    testStr1 = "There,is,No,Time"
    testStr2 = "som[23] In[23423] the[34].asd[934].234."
    testStr3 = "s(43) d(03) asdfasd dsfsd(3) sd"
    # Test Search Operation
    autoTester.check( re.compile(",").groups )
    autoTester.check( re.search(",", testStr1).pos )
    autoTester.check( re.search(",", testStr1).endpos )
    autoTester.check( re.search(",", testStr1).group() )
    autoTester.check( re.search(",", testStr1).group(0) )
    autoTester.check( re.search(",", testStr1).string )

    def TestIndexError():
        try:
            re.search(",", testStr1).group(1)
            return("no exception")
        except Exception:
            return("exception")
        return("wierd")
    autoTester.check( TestIndexError() )

    r = "\\[([\\d]+)\\]"
    autoTester.check( re.compile(r).groups )
    autoTester.check( re.search(r, testStr2).pos)
    autoTester.check( re.search(r, testStr2).endpos)
    autoTester.check( re.search(r, testStr2).groups())
    autoTester.check( re.search(r, testStr2).group())
    autoTester.check( re.search(r, testStr2).group(0))
    autoTester.check( re.search(r, testStr2).group(1))
    autoTester.check( re.search(r, testStr2).start())
    autoTester.check( re.search(r, testStr2).start(0))
    autoTester.check( re.search(r, testStr2).start(1))
    autoTester.check( re.search(r, testStr2).end())
    autoTester.check( re.search(r, testStr2).end(0))
    autoTester.check( re.search(r, testStr2).end(1))
    autoTester.check( re.search(r, testStr2).span())
    autoTester.check( re.search(r, testStr2).span(0))
    autoTester.check( re.search(r, testStr2).span(1))
    autoTester.check( re.search(r, testStr2).lastgroup)
    autoTester.check( re.search(r, testStr2).lastindex)

    # Test Match Operation
    autoTester.check( re.match("asdf", "asdf").pos )
    autoTester.check( re.match(r"asdf", "asdf").endpos )
    autoTester.check( re.match("asdf", "asdf").groups() )
    autoTester.check( re.match("a", "asdf").pos )
    autoTester.check( re.match("a", "asdf").endpos )
    autoTester.check( re.match("a", "asdf").groups() )
    autoTester.check( (re.match("s", "asdf") is None) )
    autoTester.check( (re.match(r"^s", "asdf") is None) )
    # @see python docs -->
    autoTester.check( (re.compile("^s").match("asdf", 1) is None) )
    # Test FullMatch Operation
    autoTester.check( (re.fullmatch("asdf", "asdf").pos))
    autoTester.check( (re.fullmatch("asdf", "asdf").endpos))
    autoTester.check( (re.fullmatch("as", "asdf") is None))
    autoTester.check( (re.fullmatch("q", "asdf") is None))
    autoTester.check( (re.compile("o[gh]").fullmatch("dog") is None))
    autoTester.check( (re.compile("o[gh]").fullmatch("ogre") is None))
    autoTester.check( re.compile("o[gh]").fullmatch("doggie",1,3).pos)
    # Test FindAll Operation
    autoTester.check(re.findall(",", testStr1)) # No Caps
    autoTester.check(re.findall("\\[([\\d]+)\\]", testStr2)) # 1 Cap
    r = "([^\d\s]+\\(([\d]+)\\))"
    autoTester.check(re.compile(r).groups)
    autoTester.check(re.findall(r, testStr3)) # 2 Caps
    # Test Split Operation
    autoTester.check(re.split(",", testStr1))
    autoTester.check(re.split("(apple|orange)",
       "Were an apple like an orange then apple orange no appleorange"))
    autoTester.check(re.split("\\[([\\d]+)\\]", "Something som[23] In the..."))
    r = re.compile(",")
    autoTester.check(r.split(testStr1, 0))
    autoTester.check(r.split(testStr1, 1))
    autoTester.check(r.split(testStr1, 2))
    autoTester.check(r.split(testStr1, 3))
    autoTester.check(r.split(testStr1, 4))

    r = re.compile("\\[([\\d]+)\\]")
    autoTester.check(r.split(testStr2,0))
    autoTester.check(r.split(testStr2,1))
    autoTester.check(r.split(testStr2,2))
    autoTester.check(r.split(testStr2,3))
    autoTester.check(r.split(testStr2,4))
