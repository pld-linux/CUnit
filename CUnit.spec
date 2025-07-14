# NOTE: due to its nature, base package is development tool, so there is no separate -devel
#
# Conditional build:
%bcond_with	examples	# build examples (seems broken)
#
Summary:	Automated testing framework for C
Summary(pl.UTF-8):	Szkielet automatycznych testów dla C
Name:		CUnit
Version:	2.1
Release:	4
License:	LGPL v2+
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/cunit/%{name}-%{version}-3.tar.bz2
# Source0-md5:	b5f1a9f6093869c070c6e4a9450cc10c
Patch0:		%{name}-curses.patch
Patch1:		%{name}-libs.patch
Patch2:		%{name}-FHS.patch
Patch3:		format.patch
URL:		http://cunit.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
Requires:	%{name}-libs = %{version}-%{release}
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

%description -l pl.UTF-8
CUnit to lekki system do pisania, administrowania i uruchamiania
testów jednostkowych w C. Udostępnia programistom C podstawową
funkcjonalność testującą z elastycznym wyborem interfejsów
użytkownika.

CUnit jest budowany jako biblioteka statyczna, którą linkuje się z
kodem testowym użytkownika. Używa prostego szkieletu do tworzenia
struktur testowych i udostępnia bogaty zbiór zapewnień (assertions)
do testowania popularnych typów danych.

%package libs
Summary:	Shared CUnit library
Summary(pl.UTF-8):	Biblioteka współdzielona CUnit
Group:		Libraries

%description libs
Shared CUnit library.

%description libs -l pl.UTF-8
Biblioteka współdzielona CUnit.

%package static
Summary:	Static CUnit library
Summary(pl.UTF-8):	Biblioteka statyczna CUnit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static CUnit library.

%description static -l pl.UTF-8
Biblioteka statyczna CUnit.

%package examples
Summary:	CUnit examples
Summary(pl.UTF-8):	Przykłady do CUnita
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description examples
CUnit examples.

%description examples -l pl.UTF-8
Przykłady do CUnita.

%prep
%setup -q -n %{name}-%{version}-3
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-curses \
	%{?debug:--enable-debug} \
	%{?with_examples:--enable-examples --enable-test}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcunit.la

rm -rf docs
%{__mv} $RPM_BUILD_ROOT%{_docdir}/CUnit docs

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO docs
%attr(755,root,root) %{_libdir}/libcunit.so
%{_includedir}/CUnit
%{_datadir}/CUnit
%{_pkgconfigdir}/cunit.pc
%{_mandir}/man3/CUnit.3*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcunit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcunit.so.1

%files static
%defattr(644,root,root,755)
%{_libdir}/libcunit.a

%if %{with examples}
%files examples
%dir %{_libexecdir}/CUnit
%dir %{_libexecdir}/CUnit/Examples
%dir %{_libexecdir}/CUnit/Examples/Automated
%attr(755,root,root) %{_libexecdir}/CUnit/Examples/Automated/AutomatedTest
%{_libexecdir}/CUnit/Examples/Automated/README
%dir %{_libexecdir}/CUnit/Examples/Basic
%attr(755,root,root) %{_libexecdir}/CUnit/Examples/Basic/BasicTest
%{_libexecdir}/CUnit/Examples/Basic/README
%dir %{_libexecdir}/CUnit/Examples/Console
%attr(755,root,root) %{_libexecdir}/CUnit/Examples/Console/ConsoleTest
%{_libexecdir}/CUnit/Examples/Console/README
%dir %{_libexecdir}/CUnit/Examples/Curses
%attr(755,root,root) %{_libexecdir}/CUnit/Examples/Curses/CursesTest
%{_libexecdir}/CUnit/Examples/Curses/README
%dir %{_libexecdir}/CUnit/Test
%attr(755,root,root) %{_libexecdir}/CUnit/Test/test_cunit
%endif
