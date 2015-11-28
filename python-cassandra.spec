# TODO: Python2.x build
#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	cassandra
Summary:	A Python client driver for Apache Cassandra
Summary(pl.UTF-8):	Moduł Pythona dla klientów Apache Cassandra
Name:		python-%{module}
Version:	2.5.1
Release:	4
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/c/cassandra-driver/cassandra-driver-%{version}.tar.gz
# Source0-md5:	54f6ea0335e27f04fe13eb1036d01944
Patch0:		%{name}-futures_already_in_py32.patch
URL:		http://github.com/datastax/python-driver
BuildRequires:	libev-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
## BuildRequires:	python-futures
BuildRequires:	python-PyYAML
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-pytz
BuildRequires:	python-six
BuildRequires:	python-sure
Requires:	python-modules
%endif
%if %{with python3}
# BuildRequires:	python3-futures  # Only 3.0 and 3.1
BuildRequires:	python3-PyYAML
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-mock
BuildRequires:	python3-modules
BuildRequires:	python3-pytz
BuildRequires:	python3-six >= 1.6
BuildRequires:	python3-sure
%endif
Suggests:	python-blist

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python client driver for Apache Cassandra. This driver works
exclusively with the Cassandra Query Language v3 (CQL3) and
Cassandra's native protocol. Cassandra versions 1.2 through 2.1 are
supported. The driver supports Python 2.6, 2.7, 3.3, and 3.4.

%description -l pl.UTF-8
Interfejs klienta dla Apache Cassandra. Działa wyłacznie w oparciu
Cassandra Query Languages v3 (CQL3) i z natywnym protkołem Cassandry.
Wspiera Cassndry w wersjach od 1.2 w góre i działa z Pythonem 2.6,
2.7, 3.3, 3.4 .

%package -n python3-%{module}
Summary:	A Python client driver for Apache Cassandra
Summary(pl.UTF-8):	Moduł Pythona dla klientów Apache Cassandra
Group:		Libraries/Python
Requires:	python3-six >= 1.6
Suggests:	python3-blist


%description -n python3-%{module}
A Python client driver for Apache Cassandra. This driver works
exclusively with the Cassandra Query Language v3 (CQL3) and
Cassandra's native protocol. Cassandra versions 1.2 through 2.1 are
supported. The driver supports Python 2.6, 2.7, 3.3, and 3.4.

%description -n python3-%{module} -l pl.UTF-8
Interfejs klienta dla Apache Cassandra. Działa wyłacznie w oparciu
Cassandra Query Languages v3 (CQL3) i z natywnym protkołem Cassandry.
Wspiera Cassndry w wersjach od 1.2 w góre i działa z Pythonem 2.6,
2.7, 3.3, 3.4 .


%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation


%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n cassandra-driver-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/murmur3.so
%dir %{py_sitedir}/%{module}/cqlengine
%{py_sitedir}/%{module}/cqlengine/*.py[co]
%dir %{py_sitedir}/%{module}/io
%{py_sitedir}/%{module}/io/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/io/libevwrapper.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/cassandra_driver-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/murmur3.cpython-*.so
%{py3_sitedir}/%{module}/__pycache__/
%dir %{py3_sitedir}/%{module}/io
%{py3_sitedir}/%{module}/io/*.py
%attr(755,root,root) %{py3_sitedir}/%{module}/io/libevwrapper.cpython-*.so
%{py3_sitedir}/%{module}/io/__pycache__
%dir %{py3_sitedir}/%{module}/cqlengine
%{py3_sitedir}/%{module}/cqlengine/*.py
%{py3_sitedir}/%{module}/cqlengine/__pycache__
%{py3_sitedir}/cassandra_driver-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
