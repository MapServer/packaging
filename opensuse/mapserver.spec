Name:           mapserver
%define fileversion 6.4.0
Version:        6.4.0
Release:        1
License:        BSD-3-Clause
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
BuildRequires:  autoconf
BuildRequires:  cmake >= 2.4 
BuildRequires:  pam
BuildRequires:  pam-devel 
BuildRequires:  postgresql-devel 
BuildRequires:  libexpat-devel 
BuildRequires:  mysql-devel 
BuildRequires:  giflib-devel 
BuildRequires:  libgeos-devel 
BuildRequires:  libproj-devel
BuildRequires:  libgdal-devel
BuildRequires:  openjpeg2-devel
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
Group:          Development/Languages/PHP
Requires:       php-gd
Requires:       apache2
Requires:       apache2-mod_php5

%description -n php-mapserver
The PHP/Mapscript extension provides full map customization capabilities within the PHP scripting language.

%package perl
Summary:        Perl/Mapscript map making extensions to Perl
Group:          Development/Languages/Perl
Requires:       %{name} = %{version}-%{release}
Requires:       perl-base

%description perl
The Perl/Mapscript extension provides full map customization capabilities
within the Perl programming language.

%package python
Summary:        Python/Mapscript map making extensions to Python
Group:          Development/Languages/Python
Requires:       %{name} = %{version}-%{release}
Requires:       python-base

%description python
The Python/Mapscript extension provides full map customization capabilities
within the Python programming language.

%package java
Summary:        Java/Mapscript map making extensions to Java
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}

%description java
The Java/Mapscript extension provides full map customization capabilities
within the Java programming language.

%package	devel
Summary:        Mapserver development files
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}-%{release}

%description	devel
The Mapserver development package provides necessary files to build
against the C Mapserver library.

%prep
%setup -q -n %{name}-%{fileversion}

%build -n %{name}-%{fileversion}

cd ..
mkdir temp
cd temp

cmake -D CMAKE_INSTALL_PREFIX=%{_prefix} \
      -D CMAKE_PREFIX_PATH="%{_includedir}/fastcgi;%{_includedir}/pgsql" \
      -D CMAKE_BUILD_TYPE="Release" \
      -D WITH_CAIRO=TRUE \
      -D WITH_CLIENT_WFS=TRUE \
      -D WITH_CLIENT_WMS=TRUE \
      -D WITH_CURL=TRUE \
      -D WITH_FCGI=TRUE \
      -D WITH_FRIBIDI=TRUE \
      -D WITH_GD=TRUE \
      -D WITH_GDAL=TRUE \
      -D WITH_GEOS=TRUE \
      -D WITH_GIF=TRUE \
      -D WITH_ICONV=TRUE \
      -D WITH_JAVA=TRUE \
      -D WITH_KML=TRUE \
      -D WITH_LIBXML2=TRUE \
      -D WITH_OGR=TRUE \
      -D WITH_MYSQL=TRUE \
      -D WITH_PERL=TRUE \
      -D CUSTOM_PERL_SITE_ARCH_DIR="%{perl_vendorarch}" \
      -D WITH_PHP=TRUE \
      -D WITH_POSTGIS=TRUE \
      -D WITH_PROJ=TRUE \
      -D WITH_PYTHON=TRUE \
      -D WITH_SOS=TRUE \
      -D WITH_THREAD_SAFETY=TRUE \
      -D WITH_WCS=TRUE \
      -D WITH_WMS=TRUE \
      -D WITH_WFS=TRUE \
      -D WITH_XMLMAPFILE=TRUE ../%{name}-%{fileversion}/

## WARNING !!!
# using %{?_smp_mflags} may break build

make %{?jobs:-j%{jobs}}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_cgibindir}
mkdir -p %{buildroot}/%{_sysconfdir}/php.d
mkdir -p %{buildroot}%{_libdir}/php5/extensions
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}%{python_sitearch}/
mkdir -p %{buildroot}/%{_includedir}/mapserver
cp *.h %{buildroot}/%{_includedir}/mapserver/

cd ../temp
%makeinstall
cd ../%{name}-%{fileversion}
 
cp %{buildroot}%{_bindir}/mapserv %{buildroot}%{_cgibindir}/mapserv
cp %{buildroot}%{_bindir}/legend %{buildroot}%{_cgibindir}/legend
cp %{buildroot}%{_bindir}/scalebar %{buildroot}%{_cgibindir}/scalebar

%ifarch x86_64
mv %{buildroot}/usr/lib/*.so* %{buildroot}%{_libdir}/
%endif

# # install perl module
# pushd mapscript/perl
# make DESTDIR=%{buildroot} pure_vendor_install
# popd
#
 
# # install java
# mkdir -p %{buildroot}%{_javadir}
# install -p -m 644 mapscript/java/mapscript.jar %{buildroot}%{_javadir}/

# install php config file
mkdir -p %{buildroot}%{_sysconfdir}/php5/conf.d/
cat > %{buildroot}%{_sysconfdir}/php5/conf.d/%{name}.ini <<EOF
; Enable %{name} extension module
extension=php_mapscript.so
EOF

# # cleanup junks
# for junk in {*.pod,*.bs,.packlist} ; do
# find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
# done

# remove vera fonts, these are provided system wide
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}/tests/vera

# # fix some exec bits
# chmod 755 %{buildroot}%{perl_vendorarch}/auto/mapscript/mapscript.so

%clean
rm -rf %{buildroot}

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COMMITERS GD-COPYING HISTORY.TXT  
%doc MIGRATION_GUIDE.txt
%doc symbols tests
%doc fonts
%{_bindir}/shp2img
%{_bindir}/shptree
%{_bindir}/sortshp
%{_bindir}/tile4ms
%{_bindir}/mapserv
%{_bindir}/legend
%{_bindir}/scalebar
%{_bindir}/msencrypt
%{_bindir}/shptreetst
%{_bindir}/shptreevis
%{_cgibindir}/mapserv
%{_cgibindir}/legend
%{_cgibindir}/scalebar
%{_libdir}/*.so.*

%files -n php-mapserver
%defattr(-,root,root)
%doc mapscript/php/README
%doc mapscript/php/examples
%config(noreplace) %{_sysconfdir}/php5/conf.d/%{name}.ini
%{_libdir}/php5/extensions/php_mapscript.so

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
#%{_javadir}/*.jar

%files devel
%defattr(-,root,root)
%dir %{_includedir}/mapserver
%{_includedir}/mapserver/*
%{_libdir}/libmapserver.so
%{_libdir}/libjavamapscript.so

%changelog
