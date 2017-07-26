
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

Instructions to build RPMs for Mapserver 7.0
============================================

On a brand new "Enterprise Linux" installation (tested with official Dockerimage oraclelinux:latest) including EPEL repository and activated ol7_optional_latest:

    # activate ol7_optional_latest and EPEL
    yum-config-manager --enable ol7_optional_latest
    yum update -y
    yum install -y tar wget
    wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-10.noarch.rpm
    rpm -ivh epel-release-7-10.noarch.rpm

    # do the RPM build
    yum -y install git rpm-build rpmdevtools yum-utils
    rpmdev-setuptree
    git clone https://github.com/mapserver/packaging.git
    cd packaging/el/
    spectool -g -C ~/rpmbuild/SOURCES mapserver-7.0.spec
    yum-builddep -y mapserver-7.0.spec
    QA_RPATHS=$[ 0x0001|0x0002 ] rpmbuild -ba --target x86_64 mapserver-7.0.spec

