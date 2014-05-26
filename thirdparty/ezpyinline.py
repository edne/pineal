#!/usr/bin/env python
'''ezpyinline

The ezpyinline is a pure python module which requires almost no setup to
allows you put C source code directly "inline" in a Python script or module,
then the C code is automatically compiled and then loaded for immediate access from Python.

ezpyinline is forked from PyInline (http://pyinline.sourceforge.net/)
but aim to be as easy as possible and do all the magics for you.

It's great for test usage, since it's requires almost no setup for ezpyinline.
Just grab ezpyinline.py into your program directory and start to use it.

The compiled python extension will placed at ~/.ezpyinline/ ,
however, you could easily change this via EZPYINLINE_ROOTDIR to any where you want.
Also you don't need to care recompile or older version function/files,
ezpyinline will auto remove older version functions which you no longer needed.

ezpyinline tested in python2.4+ on linux,
however it should works in python2.3+.
You'll need python-dev and working C compilers/toolchains to compile C.
However, if you just wanna deploy on non-develop environment,
just copy the ~/.ezpyinline directory and it should also works.

Tutorial:

Using ezpyinline is very simple: (also see example 1:  helloworld.py )

1. write a C function and put this function in a raw string literal.
2. create a name binding use ezpyinline.C()
3. call your C function in python from where you need it.
4. run your python program as there's no C code inside it.
 
So grab ezpyinline.py and copy it to your current directory, 
(or just use easy_install -Z ezpyinline if you have setuptools installed),
and try the following example.

Note: use raw string parameter in ezpyinline.C() will be a good practice. 
This prevents problems caused from the escape characters in C string literal.

 * Example 1: helloworld.py

--- cut-here ---

#!/usr/bin/python
import ezpyinline

#step 1
code = r"""
    int helloworld() {
        printf("hello ezpyinline!\n");
    }
"""
#step 2
ezc = ezpyinline.C(code)

#step 3
ezc.helloworld()

----------------
and step 4: type python helloworld.py in shell:

#python helloworld.py
hello ezpyinline!

program should works now, if you have any problem, 
check if your C compiler and python-dev package installed.

You could also write like this:

 * Example 1.b: helloworld2.py

--- cut-here ---

#!/usr/bin/python
import ezpyinline

ezc = ezpyinline.C(
r"""
    int helloworld() {
        printf("hello ezpyinline\n");
    }
""")

ezc.helloworld()

----------------

 * Example 2: prime.py

--- cut-here ---

#!/usr/bin/python
import ezpyinline

ezc = ezpyinline.C(
r"""
    int prime(int num) {
      int x; 
      for (x = 2; x < (num - 1) ; x++) {
        if (num == 2) {
          return 1;
        }
        if (num % x == 0) {
          return x;
        }
      }
      return 1;
    }
""")

for num in xrange(10000):
    is_prime = ezc.prime(num)
    if is_prime == 1:
        print "%d is a prime number" % num
    else:
        print "%d equals %d * %d" %(num,is_prime,num/is_prime)

----------------
run time in my p4-3.0G box:

real    0m0.590s
user    0m0.430s
sys     0m0.020s

----------------
#!/usr/bin/python
for num in xrange(10000):
    is_prime = 1
    for x in xrange(2,num-1):
        if (num % x == 0):
            is_prime = x
            break

    if is_prime == 1:
        print "%d is a prime number" % num
    else:
        print "%d equals %d * %d" %(num,is_prime,num/is_prime)

----------------
run time in my p4-3.0G box:

real    0m3.300s
user    0m3.190s
sys     0m0.090s

 * Example 3: oldstyle_pyinline.py

PyInline compatibility, you old PyInline code still works!

As for now, most of code in ezpyinline was from PyInline,
everything you can do in PyInline should still works.

--- cut-here ---
#import PyInline
from ezpyinline import PyInline # only change PyInline import to this line

m = PyInline.build(code="""
  double my_add(double a, double b) {
    return a + b;
  }
""", language="C")

print m.my_add(4.5, 5.5) # Should print out "10.0"
----------------

If you need more complex usage please also see PyInline's README
(http://pyinline.cvs.sourceforge.net/pyinline/PyInline/README.txt?revision=1.2&view=markup)
,distutils package (http://www.python.org/sigs/distutils-sig/)
,Python/C API Reference Manual (http://docs.python.org/api/api.html)
and Extending and Embedding the Python Interpreter (http://docs.python.org/ext/ext.html)

For more more complex usage, you should check:
Pyrex: http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/
weave: http://www.scipy.org/Weave
and ShedSkin: http://sourceforge.net/projects/shedskin

Feedbacks are very welcome, please send them to my email.

Website: http://ezpyinline.sf.net

Author: __tim__ <timchen119.at.gmail.com>
License: The Artistic License (http://www.opensource.org/licenses/artistic-license.php)

Changelog:
2007-02-08 Version 0.1 public released.

'''

import os, string, re
import sys, os.path , shutil
from distutils.core import setup, Extension

#you could change this line to anywhere you wanna place.
EZPYINLINE_ROOTDIR = os.environ['HOME'] + "/.ezpyinline/"

#############################################################
# Utility Functions and Classes (from PyInline's c_util.py) #
#############################################################

class c_util:
    import re
    c_directive = '\s*#.*'
    c_cppcomment = '//.*'
    c_simplecomment = '/\*[^*]*\*+([^/*][^*]*\*+)*/'
    c_doublequote = r'(?:"(?:\\.|[^"\\])*")'
    c_singlequote = r'(?:\'(?:\\.|[^\'\\])*\')'
    c_comment = re.compile("(%s|%s)|(?:%s|%s|%s)" % (c_doublequote,
                                                     c_singlequote,
                                                     c_cppcomment,
                                                     c_simplecomment,
                                                     c_directive))

    const = re.compile('\s*const\s*')
    star = re.compile('\s*\*\s*')
    _c_pandn = "((?:(?:[\w*]+)\s+)+\**)(\w+)"
    c_pandm = re.compile(_c_pandn)
    _c_function = _c_pandn + "\s*\(([^\)]*)\)"
    c_function_def = re.compile("(?:%s|%s)|(%s)" % (c_doublequote,
                                                    c_singlequote,
                                                    _c_function + "\s*(?:\{|;)"))
    c_function_decl = re.compile(_c_function + "\s*;")

    trimwhite = re.compile("\s*(.*)\s*")

    def preProcess(code):
        return c_util.c_comment.sub(lambda(match): match.group(1) or "", code)
    preProcess = staticmethod(preProcess)

    def findFunctionDefs(code):
        functionDefs = []
        for match in c_util.c_function_def.findall(code):
            if match[0]:
                functionDefs.append({'return_type': c_util.trimWhite(match[1]),
                                     'name': c_util.trimWhite(match[2]),
                                     'rawparams': c_util.trimWhite(match[3])})
        return functionDefs
    findFunctionDefs = staticmethod(findFunctionDefs)

    _wsLeft = re.compile("^\s*")
    _wsRight = re.compile("\s*$")

    def trimWhite(str):
        str = c_util._wsLeft.sub("", str)
        str = c_util._wsRight.sub("", str)
        return str
    trimWhite = staticmethod(trimWhite)

#########################################################
# ezpyinline C Module                                   #
# most code are from PyInline,                          #
# Copyright (c)2001 Ken Simpson. All Rights Reserved.   #
#########################################################

class Builder:


    ptStringMap = {
        'unsigned': 'i',
        'unsigned int': 'i',
        'int': 'i',
        'long': 'l',
        'float': 'f',
        'double': 'd',
        'char': 'c',
        'short': 'h',
        'char*': 's',
        'PyObject*': 'O'}
    def __init__(self, **options):
        self._verifyOptions(options)
        self._options = options
        self._initDigest()
        self._initBuildNames()
        self._methods = []

    def __check_tempdir(self):
        try:
            if not os.path.isdir(self.__tempdir):
                os.mkdir(self.__tempdir)
        except:
            pass

    def _verifyOptions(self, options):
        pass

    def _initDigest(self):
        import md5, os, sys
        digester = md5.new()
        digester.update(self._options.get('code'))
        self._digest = digester.hexdigest()

    def _initBuildNames(self):
        #code function name
        self.__funcname = c_util.findFunctionDefs(self._options.get('code'))[0]['name']
        #every '.' in __pyfilename will replace to '_'
        self.__pyfilename = sys.argv[0].split("/")[-1].replace('.','_')
        #use ~/.py_inline/__funcname__pyfilename__md5digest/ as temp directory
        self._moduleName = "__%s__%s__%s" % (self.__funcname,self.__pyfilename,self._digest)

        self.__tempdir = EZPYINLINE_ROOTDIR

        self.__check_tempdir()

        self._buildDir = self.__tempdir + self._moduleName

        self._srcFileName = "%s.c" % self._moduleName
        self._moduleVersion = "1.0"
        self._homeDir = os.getcwd()

    def build(self):
        "Build a chunk of C source code."
        self._parse()

        try:
            return self._import()
        except ImportError:
            #tim: auto remove old function version in temp directory before compile
            self.__check_tempdir()

            import os,shutil
            [shutil.rmtree(self.__tempdir+x) for x in os.listdir(self.__tempdir) if x.startswith("__"+self.__funcname+"__"+self.__pyfilename) and x != self._moduleName]

            self._writeModule()
            self._compile()

            try:
                return self._import()
            except ImportError:
                raise BuildError("Build failed")

    def _import(self):
        "Import the new extension module into our client's namespace"
        from distutils.util import get_platform
        import sys, os
        
        # Add the module's lib directory to the Python path.
        plat_specifier = ".%s-%s" % (get_platform(), sys.version[0:3])
        build_platlib = os.path.join(self._buildDir,
                                     'build',
                                     'lib' + plat_specifier)
        sys.path.append(build_platlib)

        # Load the module.
        import imp
        fp, pathname, description = imp.find_module(self._moduleName)

        try:
            module = imp.load_module(self._moduleName, fp,
                                     pathname, description)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

        if self._options.has_key('targetmodule'):
            # Load each of the module's methods into the caller's
            # global namespace.
            setattr(self._options.get('targetmodule'), self._moduleName, module)
            for method in self._methods:
                setattr(self._options.get('targetmodule'), method['name'],
                        getattr(module, method['name']))
                
        return module

    def _parse(self):
        code = c_util.preProcess(self._options.get('code'))

        defs = c_util.findFunctionDefs(code)
        for d in defs:
            d['params'] = self._parseParams(d['rawparams'])
            self._methods.append(d)

    _commaSpace = re.compile(",\s*")
    _space = re.compile("\s+")
    _spaceStars = re.compile("(?:\s*\*\s*)+")
    _void = re.compile("\s*void\s*")
    _blank = re.compile("\s+")

    def _parseParams(self, params):
        "Return a tuple of tuples describing a list of function params"
        import re, string
        rawparams = self._commaSpace.split(params)
        if self._void.match(params) or\
           self._blank.match(params) or\
           params == '':
            return []

        return [self._parseParam(p) for p in rawparams]

    def _parseParam(self, p):
        param = {}
        
        # Grab the parameter name and its type.
        m = c_util.c_pandm.match(p)
        if not m:
            raise BuildError("Error parsing parameter %s" % p)

        type = self._parseType(m.group(1))
        param['type'] = type['text']
        param['const'] = type['const']
        param['pointers'] = type['pointers']
        param['name'] = m.group(2)

        return param

    def _parseType(self, typeString):
        type = {}
        # Remove const from the type.
        if c_util.const.search(typeString):
            typeString = c_util.const.sub(" ", typeString)
            type['const'] = 1
        else:
            type['const'] = 0

        # Reformat asterisks in the type.
        type['pointers'] = typeString.count('*')
        type['text'] = c_util.trimWhite(c_util.star.sub("", typeString) +\
                                        ("*" * type['pointers']))

        return type
        
    def _makeBuildDirectory(self):
        try:
            os.mkdir(self._buildDir)
        except OSError, e:
            # Maybe the build directory already exists?
            print "Couldn't create build directory %s" % self._buildDir

    def _writeModule(self):
        self._makeBuildDirectory()
        try:
            srcFile = open(os.path.join(self._buildDir, self._srcFileName),
                           "w")
        except IOError, e:
            raise BuildError("Couldn't open source file for writing: %s" % e)

        import time
        srcFile.write("// Generated by ezpyinline\n")
        srcFile.write("// At %s\n\n" %\
    	    time.asctime(time.localtime(time.time())))
        srcFile.write('#include "Python.h"\n\n')

        # First, write out the user's code.
        srcFile.write("/* User Code */\n")
        srcFile.write(self._options.get('code'))
        srcFile.write("\n\n")

        # Then add in marshalling methods.
        for method in self._methods:
            srcFile.write("static PyObject *\n")
            method['hashname'] = "_%s_%s" % (self._digest, method['name'])
            srcFile.write("%s(PyObject *self, PyObject *args)\n" %\
                          method['hashname'])
            self._writeMethodBody(srcFile, method)

        # Finally, write out the method table.
        moduleMethods = "%s_Methods" % self._moduleName
        srcFile.write("static PyMethodDef %s[] = {\n  " %\
                      moduleMethods)
        table = string.join(map(lambda(x): '{"%s", %s, METH_VARARGS}' %\
                         (x['name'], x['hashname']), self._methods), ",\n  ")
        srcFile.write(table + ",\n  ")
        srcFile.write("{NULL, NULL}\n};\n\n")

        # And finally an initialization method...
        srcFile.write("""
DL_EXPORT(void) init%s(void) {
  Py_InitModule("%s", %s);
}
""" % (self._moduleName, self._moduleName, moduleMethods))

        srcFile.close()

    def _writeMethodBody(self, srcFile, method):
        srcFile.write("{\n")

        # Don't write a return value for void functions.
        srcFile.write("  /* Return value */\n")
        if method['return_type'] != 'void':
            srcFile.write("  %s %s;\n\n" % (method['return_type'], "_retval"))
            
        srcFile.write("  /* Function parameters */\n")
        for param in method['params']:
            srcFile.write("  %s %s;\n" % (param['type'], param['name']));
        srcFile.write("\n")

        # Now marshal the input parameters, if there are any.
        if method['params']:
            ptString = self._buildPTString(method['params'])
            ptArgs = string.join(
                map(lambda(x): "&%s" % x['name'],
                    method['params']), ", ")
            srcFile.write('  if(!PyArg_ParseTuple(args, "%s", %s))\n' %\
                          (ptString, ptArgs))
            srcFile.write('    return NULL;\n');

        # And fill in the return value by calling the user's code
        # and then filling in the Python return object.
        retvalString = ""
        if method['return_type'] != 'void':
            retvalString = "_retval = "
            
        srcFile.write("  %s%s(%s);\n" %\
                      (retvalString,
                       method['name'],
                       string.join(map(lambda(x): '%s' % (x['name']),
                                method['params']),
                            ', ')))

        if method['return_type'] == 'void':
            srcFile.write("  /* void function. Return None.*/\n")
            srcFile.write("  Py_INCREF(Py_None);\n")
            srcFile.write("  return Py_None;\n")
        elif method['return_type'] == 'PyObject*':
            srcFile.write("  return _retval;\n")
        else:
            try:
                rt = self._parseType(method['return_type'])
                srcFile.write('  return Py_BuildValue("%s", _retval);\n' %\
                              self.ptStringMap[rt['text']])
            except KeyError:
                raise BuildError("Can't handle return type '%s' in function '%s'"%\
                                 (method['return_type'], method['name']))
        
        srcFile.write("}\n\n")

    def _compile(self):
        from distutils.core import setup, Extension
        os.chdir(self._buildDir)
        ext = Extension(self._moduleName,
                        [self._srcFileName],
                        library_dirs=self._options.get('library_dirs'),
                        libraries=self._options.get('libraries'),
                        define_macros=self._options.get('define_macros'),
                        undef_macros=self._options.get('undef_macros'))
        try:
            #tim: quiet compile 
            setup(name = self._moduleName,
                  version = self._moduleVersion,
                  ext_modules = [ext],
                  script_args = ["-q","build"] + (self._options.get('distutils_args') or []),
                  script_name="C.py",
                  package_dir=self._buildDir)
        except SystemExit, e:
            raise BuildError(e)
            
        os.chdir(self._homeDir)

    def _buildPTString(self,params):
        ptString = ""
        for param in params:
            if self.ptStringMap.has_key(param['type']):
                ptString += self.ptStringMap[param['type']]
            else:
                raise BuildError("Cannot map argument type '%s' for argument '%s'" %\
                                 (param['type'], param['name']))

        return ptString

################################
#from ezpyinline's __init__.py #
################################

class BuildError(Exception):
    pass

class PyInline:
    #tim: we'll try to compatible with PyInline
    #@staticmethod
    def build(**args):
        """
        Build a chunk of code, returning an object which contains
        the code's methods and/or classes.
        """
        # tim: since we only have C Builder now. just removed these.

        # Try to import a ezpyinline module for the specified language.
        #try:
        #    m = __import__("%s.%s" %(__name__, args['language']))
        #    m = getattr(m, args['language'])
        #except ImportError:
        #    raise BuildError("Failed to find module for language %s")

        # Create a Builder object to build the chunk of code.
        #b = m.Builder(**args)

        b = Builder(**args)

        # Build the code and return an object which contains whatever
        # resulted from the build.
        return b.build()
    build = staticmethod(build)

#the only public functions for ezpyinline.py, other stuffs are all in the class namespace.
def buildc(code):
    """
    A simple wrapper for just write C code and call PyInline.build().
    """
    return PyInline.build(code=code,language="C")

#An alias for easy usage.
CC=C=buildc

if __name__ == "__main__":
    print __doc__
