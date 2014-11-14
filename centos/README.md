CentOS
======

A simple spec file very close to that developed by Fedora but adapted for version 6.4.1 using CMake.

On a brand new CentOS 7 installation including EPEL repository:

    yum -y install git rpm-build rpmdevtools yum-utils
    rpmdev-setuptree
    git clone https://github.com/mapserver/packaging.git
    cd packaging/centos
    spectool -g -C ~/rpmbuild/SOURCES mapserver.spec
    yum-builddep -y mapserver.spec
    rpmbuild -ba --target x86_64 mapserver.spec

