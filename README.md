Pineal
======

![screenshot](http://i.imgur.com/3lBNKan.png)

Engine and DSL for graphical live-coding.
Built on top of [OpenFrameworks](http://openframeworks.cc/) using an embedded
Python interpreter and the magic metaprogramming powers of [Hy](http://hylang.org).


Example
-------

```hy
(background 0 0 0)

(-@> (cube 1.8)
	 (no-fill)
	 (color 1 1 1)
	 (line-width 1)
	 (turn-z 64)
	 (turn-y 16)
	 (rotate-y (-> (time 0.5)
                   (% 2pi))))

```

Instructions
------------

- Compile and run the application.
- Send the code via OSC to the path `/code`, port 7172.

The script `scripts/watch.py` automatically sends the content of a file every
time it is changed:

```
python scripts/watch.py bin/data/test.pn 7172 /code
```


Dependencies
------------

- [OpenFrameworks](http://openframeworks.cc/)
- [OfxAubio](https://github.com/aubio/ofxAubio) plugin for audio analysis, if you
  are on Linux check [my fork](https://github.com/edne/ofxAubio) (waiting for the
  pull-request to be accepted).
- [Hy](http://hylang.org)

To run `watch.py`:
```
pip install liblo watchdog
```


Documentation
-------------
References are available on [Readthedocs](http://pineal.readthedocs.org/en/latest/)


Contributing
------------
- Fork.
- Make a branch with the name of your new feature.
- Use the [Of code style](https://github.com/openframeworks/openFrameworks/wiki/oF-code-style).
- Document everything that will be exposed to the final user, adding or editing a
  `.rst` file in the `docs/` folder.
- `scripts/test.sh` builds the project, runs it and sends via OSC the code from
  `bin/data/test.pn` updating it every time the file is changed.
- Make a pull-request.


Internals Overview
------------------
If you want to contribute.

The pineal DSL is composed by 2 parts: functions (C++) and macros (Hy).
The macros are in `bin/py/dsl.hy` and are used to language keywords. The functions
are in `src/dsl_wrapper.h` **BUT** the file is generated automatically by
`scripts/generate.hy` using .h files in the `src/dsl/` folder, exposing the
ones marked with `PINEAL("function_name")`.


License
-------
This project is released under the terms of [GNU AGPL](http://www.gnu.org/licenses/agpl-3.0.html), see [LICENSE](LICENSE) file for details


Warning
-------
This project is **heavily in development**. You can use it, I use it in
"production" (coding at parties). But be prepared to continuous and unexpected
changes in syntax (it's getting even more functional) and new features that
randomly appear or disappear.

