Name:           mapserver
%define fileversion 6.2.0
Version:        6.2.0
Release:        1
License:        BSD
Group:          Productivity/Scientific/Other
Source:         %{name}-%{fileversion}.tar.gz
Url:            http://www.mapserver.org
Summary:        Environment for building spatially-enabled internet applications
Requires:       php 
Requires:       postgresql 
Requires:       mysql 
Requires:       FastCGI 
Requires:       python 
Requires:       apache2
%if 0%{?suse_version} != 1010
BuildRequires:  xorg-x11-libXpm-devel
%endif
BuildRequires:  rpm 
BuildRequires:  gcc 
BuildRequires:  gcc-c++ 
BuildRequires:  pam
BuildRequires:  pam-devel 
BuildRequires:  postgresql-devel 
BuildRequires:  libexpat-devel 
BuildRequires:  mysql-devel 
BuildRequires:  giflib-devel 
BuildRequires:  libgeos-devel 
BuildRequires:  libproj-devel
BuildRequires:  libgdal-devel 
BuildRequires:  readline-devel 
BuildRequires:  freetype2-devel 
BuildRequires:  FastCGI-devel 
BuildRequires:  python-devel 
BuildRequires:  fribidi-devel 
BuildRequires:  cairo-devel
BuildRequires:  gd-devel >= 2.0.16
%if 0%{?suse_version} >= 1030
BuildRequires:  libcurl-devel
BuildRequires:  php-devel
%else
BuildRequires:  curl-devel
BuildRequires:  php5-devel
%endif
%if 0%{?suse_version} >= 1120
BuildRequires:  krb5-devel
%endif
BuildRequires:  zlib-devel 
BuildRequires:  libxml2-devel 
BuildRequires:  libxslt-devel 
BuildRequires:  libjpeg-devel 
BuildRequires:  libpng-devel 
BuildRequires:  libtiff-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  swig 
BuildRequires:  update-alternatives 
BuildRequires:  apache2-devel
%if 0%{?sles_version}
BuildRequires:  java-devel <= 1.5
BuildRequires:  java <= 1.5
%else
BuildRequires:  java-devel >= 1.5
BuildRequires:  java >= 1.5
%endif
%if 0%{?sles_version} == 10
%ifarch i586
BuildRequires:  java-1_5_0-ibm-alsa
%endif
BuildRequires:  krb5-devel
%endif
BuildRequires:  libgcj-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define _cgibindir /srv/www/cgi-bin

%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages, 
Mapserver can provide an interactive internet map based on 
custom GIS data.

%package -n php-mapserver
Summary:        PHP/Mapscript map making extensions to PHP
Group:          Development/Languages
Requires:       php-gd
Requires:       apache2
Requires:       apache2-mod_php5

%description -n php-mapserver
The PHP/Mapscript extension provides full map customization capabilities within the PHP scripting language.

%package perl
Summary:        Perl/Mapscript map making extensions to Perl
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       perl-base

%description perl
The Perl/Mapscript extension provides full map customization capabilities
within the Perl programming language.

%package python
Summary:        Python/Mapscript map making extensions to Python
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       python-base

%description python
The Python/Mapscript extension provides full map customization capabilities
within the Python programming language.

%package java
Summary:        Java/Mapscript map making extensions to Java
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description java
The Java/Mapscript extension provides full map customization capabilities
within the Java programming language.

%prep
%setup -q -n %{name}-%{fileversion}

%build -n %{name}-%{fileversion}
%configure XTRALIBS=-ldl \
   --with-gd \
   --with-zlib \
   --with-freetype=%{_bindir}/freetype-config \
   --with-fribidi-config \
   --with-gdal=%{_bindir}/gdal-config \
   --with-ogr=%{_bindir}/gdal-config \
   --with-geos=%{_bindir}/geos-config \
   --with-proj \
   --with-sos \
   --with-wms \
   --with-wfs \
   --with-wcs \
   --with-wmsclient \
   --with-wfsclient \
   --with-xpm \
   --with-png \
   --with-cairo \
   --with-postgis=%{_bindir}/pg_config \
   --with-mygis=%{_bindir}/mysql_config \
   --with-curl-config=%{_bindir}/curl-config \
   --with-xml2-config=%{_bindir}/xml2-config \
   --with-xslt-config=%{_bindir}/xslt-config \
   --with-php=%{_bindir}/php-config \
   --with-httpd=/usr/sbin/httpd2 \
   --with-fastcgi=/usr \
   --with-agg-svg-symbols=yes \
   --with-expat=/usr \
   --with-kml=yes \
   --with-xml-mapfile \
   --without-pdf \
   --without-eppl \
   --with-threads \
   --enable-python-mapscript \
   --disable-runpath

## WARNING !!!
# using %{?_smp_mflags} may break build

make
# temporary hack!
make mapscriptvars
#sed -i -e "s;libdir='%{_libdir}';libdir='%{buildroot}%{_libdir}';" libmapserver.la
#sed -i -e "s;libdir='%{python_sitearch}';libdir='%{buildroot}%{python_sitearch}';" mapscript/python/_mapscript.la
#sed -i -e "s;libdir='/usr/lib64/php/modules';libdir='%{buildroot}/usr/lib64/php/modules';" mapscript/php/php_mapscript.la

## build perl
cd mapscript/perl
perl Makefile.PL
make

## build python
#cd ../python
#python setup.py build

# build java
#touch ../mapscript.i
cd ../java
#JAVA_HOME=%{java_home} make
#sed -i -e "s;libdir='%{_libdir}';libdir='%{buildroot}%{_libdir}';" libjavamapscript.la
#make interface
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_cgibindir}
mkdir -p %{buildroot}/%{_sysconfdir}/php.d
mkdir -p %{buildroot}%{_libdir}/php5/extensions
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}%{python_sitearch}/

make DESTDIR=%{buildroot} install

cp %{buildroot}%{_bindir}/mapserv %{buildroot}%{_cgibindir}/mapserv
cp %{buildroot}%{_bindir}/legend %{buildroot}%{_cgibindir}/legend
cp %{buildroot}%{_bindir}/scalebar %{buildroot}%{_cgibindir}/scalebar
#install -p -m 755 shp2img %{buildroot}%{_bindir}
#install -p -m 755 shptree %{buildroot}%{_bindir}
#install -p -m 755 sortshp %{buildroot}%{_bindir}
#install -p -m 755 tile4ms %{buildroot}%{_bindir}

#install -p -m 755 mapscript/php/.libs/php_mapscript.so %{buildroot}/%{_libdir}/php5/extensions/



# install perl module
pushd mapscript/perl
make DESTDIR=%{buildroot} pure_vendor_install
popd

# install python module
#pushd mapscript/python

#python setup.py install --root %{buildroot}
#mv %{buildroot}/usr/local/%{_lib}/python%py_ver/site-packages/*mapscript* %{buildroot}/usr/%{_lib}/python%py_ver/site-packages/
#%if 0%{?suse_version} > 1110 || 0%{?sles_version} > 10
#    mv %{buildroot}/usr/local/%{_lib}/python%py_ver/site-packages/MapScript* %{buildroot}/usr/%{_lib}/python%py_ver/site-packages/
#%endif
#popd

# install java
mkdir -p %{buildroot}%{_javadir}
install -p -m 644 mapscript/java/mapscript.jar %{buildroot}%{_javadir}/

# install php config file
mkdir -p %{buildroot}%{_sysconfdir}/php5/conf.d/
cat > %{buildroot}%{_sysconfdir}/php5/conf.d/%{name}.ini <<EOF
; Enable %{name} extension module
extension=php_mapscript.so
EOF

# cleanup junks
for junk in {*.pod,*.bs,.packlist} ; do
find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done
# remove vera fonts, these are provided system wide
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}/tests/vera

# fix some exec bits
chmod 755 %{buildroot}%{perl_vendorarch}/auto/mapscript/mapscript.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README README.CONFIGURE README.WIN32 COMMITERS GD-COPYING HISTORY.TXT  
%doc INSTALL MIGRATION_GUIDE.txt
%doc symbols tests
%doc fonts
%{_bindir}/shp2img
%{_bindir}/shptree
%{_bindir}/sortshp
%{_bindir}/tile4ms
%{_bindir}/mapserv
%{_bindir}/legend
%{_bindir}/scalebar
%{_bindir}/mapserver-config
%{_bindir}/msencrypt
%{_bindir}/shptreetst
%{_bindir}/shptreevis
%{_cgibindir}/mapserv
%{_cgibindir}/legend
%{_cgibindir}/scalebar
%{_libdir}/libmapserver-6.*.so
%{_libdir}/libmapserver.la
%{_libdir}/libmapserver.so

%files -n php-mapserver
%defattr(-,root,root)
%doc mapscript/php/README
%doc mapscript/php/README.WIN32
%doc mapscript/php/examples
%config(noreplace) %{_sysconfdir}/php5/conf.d/%{name}.ini
%{_libdir}/php5/extensions/php_mapscript.so
%{_libdir}/php5/extensions/php_mapscript.la
%{_libdir}/php5/extensions/php_mapscript.so.0
%{_libdir}/php5/extensions/php_mapscript.so.0.0.0

%files perl
%defattr(-,root,root)
%doc mapscript/perl/examples
%dir %{perl_vendorarch}/auto/mapscript
%{perl_vendorarch}/auto/mapscript/*
%{perl_vendorarch}/mapscript.pm

%files python
%defattr(-,root,root)
%doc mapscript/python/README
%doc mapscript/python/examples
%doc mapscript/python/tests
%{python_sitearch}/*

%files java
%defattr(-,root,root)
%doc mapscript/java/README
%doc mapscript/java/examples
%doc mapscript/java/tests
%{_javadir}/*.jar

%changelog
