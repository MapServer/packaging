Overview
========

This is [MapServer](http://mapserver.org)'s packaging repository. It holds 
or provides references to MapServer packaging scripts for various platforms, 
distributions, and package formats (rpms, debs, etc.).

The repository is organized in a directory for each distribution holding 
packaging information for [MapServer](https://github.com/mapserver/mapserver) 
and possibly [MapCache](https://github.com/mapserver/mapcache) and 
[TinyOWS](https://github.com/mapserver/tinyows).

This repository is meant for reference and does not replace any authoritative 
configuration shipped within distributions.

Here is an alphabetically ordered list of packaging support known of.

CentOS
======

See directory [centos](packaging/tree/master/centos)

Debian/Ubuntu
=============

Packaging for Debian and Ubuntu is [maintained externally]
(http://anonscm.debian.org/gitweb/?p=pkg-grass/mapserver.git)

Enterprise Linux
================

See directory [el](packaging/tree/master/el)

Homebrew support
================

```
$ brew install https://raw.github.com/mapserver/packaging/master/homebrew/mapserver.rb
```

MS4W - MapServer for Windows
============================

The MS4W packaging for Windows is [maintained externally] 
(http://maptools.org/ms4w/)

openSUSE
========

See directory [opensuse](packaging/tree/master/opensuse) or [externally]
(https://build.opensuse.org/package/files?package=mapserver&project=Application:Geo)
