
Instructions to build RPMs for Mapserver 6.4
============================================

On a brand new "Enterprise Linux" installation (only tested on CentOS & Red Hat 7) including EPEL repository:

    yum -y install git rpm-build rpmdevtools yum-utils
    rpmdev-setuptree
    git clone https://github.com/mapserver/packaging.git
    cd packaging/el
    spectool -g -C ~/rpmbuild/SOURCES mapserver-6.4.spec
    yum-builddep -y mapserver-6.4.spec
    rpmbuild -ba --target x86_64 mapserver-6.4.spec

