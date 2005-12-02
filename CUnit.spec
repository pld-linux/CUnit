Summary:	Automated testing framework for C
Summary(pl):	Szkielet automatycznych testów dla C
Name:		CUnit
Version:	2.0
Release:	0.5
License:	LGPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/cunit/%{name}-%{version}-2.tar.gz
# Source0-md5:	d493ba42f06bf9156225f5026ff65f86
Patch0:		%{name}-curses.patch
Patch1:		%{name}-libs.patch
Patch2:		%{name}-FHS.patch
URL:		http://cunit.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CUnit is a lightweight system for writing, administering, and running
unit tests in C. It provides C programmers a basic testing
functionality with a flexible variety of user interfaces.

CUnit is built as a static library which is linked with the user's
testing code. It uses a simple framework for building test structures,
and provides a rich set of assertions for testing common data types.
In addition, several different interfaces are provided for running
tests and reporting results.

%description -l pl
CUnit to lekki system do pisania, administrowania i uruchamiania
testów jednostkowych w C. Udostêpnia programistom C podstawow±
funkcjonalno¶æ testuj±c± z elastycznym wyborem interfejsów
u¿ytkownika.

CUnit jest budowany jako biblioteka statyczna, któr± linkuje siê z
kodem testowym u¿ytkownika. U¿ywa prostego szkieletu do tworzenia
struktur testowych i udostêpnia bogaty zbiór zapewnieñ (assertions)
do testowania popularnych typów danych.

%prep
%setup -q -n %{name}-%{version}-2
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-debug} \
	--enable-curses
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf html headers
# can't package %doc %{_docdir}/%{name}-%{version} as rpm fails:
# error: magic_file(ms, "/home/builder/tmp/cunit-2.0-root-builder/usr/share/doc/cunit-2.0/headers")
# failed: mode 040755 cannot open `/home/builder/tmp/cunit-2.0-root-builder/usr/share/doc/cunit-2.0/headers' (No such file or directory)
# rpmbuild: rpmfc.c:1564: rpmfcClassify: Assertion `ftype != ((void *)0)' failed.
mv -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{html,headers} .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%doc html headers
%{_includedir}/CUnit
# maybe attempt to make .so too?
%{_libdir}/libcunit.a
%{_datadir}/CUnit

# dunno, worth to package these at all?
%dir %{_libdir}/CUnit
%dir %{_libdir}/CUnit/Examples
%dir %{_libdir}/CUnit/Examples/Automated
%attr(755,root,root) %{_libdir}/CUnit/Examples/Automated/AutomatedTest
%{_libdir}/CUnit/Examples/Automated/README

%dir %{_libdir}/CUnit/Examples/Basic
%attr(755,root,root) %{_libdir}/CUnit/Examples/Basic/BasicTest
%{_libdir}/CUnit/Examples/Basic/README

%dir %{_libdir}/CUnit/Examples/Console
%attr(755,root,root) %{_libdir}/CUnit/Examples/Console/ConsoleTest
%{_libdir}/CUnit/Examples/Console/README

%dir %{_libdir}/CUnit/Examples/Curses
%attr(755,root,root) %{_libdir}/CUnit/Examples/Curses/CursesTest
%{_libdir}/CUnit/Examples/Curses/README

%dir %{_libdir}/CUnit/Test
%attr(755,root,root) %{_libdir}/CUnit/Test/test_cunit

%{_mandir}/man3/CUnit.3*
