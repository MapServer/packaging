Name:      tinyows
Version:   1.1.0
Release:   1%{?dist}
Summary:   WFS-T and FE implementation server

Group:     Applications/Publishing
License:   MIT
URL:       http://www.tinyows.org
Source0:   http://tinyows.org/tracdocs/release/%{name}-%{version}.tar.bz2
Source1:   no_date_footer.html
Source2:   tinyows-config.xml
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  httpd

BuildRequires: ctags indent doxygen valgrind
BuildRequires: flex flex-devel
BuildRequires: libxml2-devel >= 2.9 fcgi-devel
BuildRequires:	postgresql-devel >= 8.4 postgis 

%description
TinyOWS server implements latest WFS-T standard versions,
as well as related standards such as Filter Encoding (FE).

%prep
%setup -q -n %{name}-%{version}
# clean SVN
# find . -type d -name .svn -exec rm -rf '{}' +

%build

%configure --enable-api \
    --with-fastcgi \
    --with-shp2pgsql=/usr/bin/shp2pgsql

# fix datadir lookup path
sed -i -e 's|/usr/tinyows/|%{_datadir}/%{name}/|' src/ows_define.h

# WARNING
# disable %{?_smp_mflags}
# it breaks compile
make

# disable timestamp inside docs
sed -i -e 's|HTML_FOOTER|HTML_FOOTER=no_date_footer.html\n\#|g' doc/Doxyfile
make doxygen

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -p -m 0755 tinyows %{buildroot}%{_bindir}/
install -d %{buildroot}%{_datadir}/%{name}
cp -pR schema %{buildroot}%{_datadir}/%{name}/
install -d %{buildroot}%{_sysconfdir}/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/config.xml
pushd %{buildroot}%{_datadir}/%{name}/
   ln -s ../../../%{_sysconfdir}/%{name}/config.xml config.xml
popd

%clean
rm -rf %{buildroot}

%check

make %{?_smp_mflags} test-valgrind || true

%files
%defattr(-,root,root,-)
%doc LICENSE README VERSION
%doc doc/doxygen
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/config.xml
%{_datadir}/%{name}

