# TODO: Python2.x build
#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_with	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	cassandra
Summary:	A Python client driver for Apache Cassandra
Summary(pl.UTF-8):	Moduł Pythona dla klientów Apache Cassandra.
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	2.1.1
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/c/cassandra-driver/cassandra-driver-%{version}.tar.gz
# Source0-md5:	cb9f9e698cd131dfcbbcdc6339541aa3
Patch0:		%{name}-futures_already_in_py32.patch
URL:		http://github.com/datastax/python-driver
BuildRequires:	rpm-pythonprov
# remove BR: python-devel for 'noarch' packages.
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0

%if %{with python2}
BuildRequires:	python-PyYAML
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-futures
BuildRequires:	python-pytz
BuildRequires:	python-six

%endif
%if %{with python3}
# BuildRequires:	python3-futures  # Only 3.0 and 3.1
BuildRequires:	python3-PyYAML
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-mock
BuildRequires:	python3-modules
BuildRequires:	python3-pytz
BuildRequires:	python3-six
%endif
#Requires:		python-libs
Requires:	python-modules
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

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

# fix #!%{_bindir}/env python -> #!%{__python}:
#%{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{name}.py

%build
%if %{with python2}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

# in case there are examples provided
#%if %{with python2}
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
#cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
#%endif
#%if %{with python3}
#install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
#cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
#find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
#	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
#%endif

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
## change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
#%%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
#%%py_comp $RPM_BUILD_ROOT%{py_sitedir}
#%%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%{py_sitedir}/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE
# %{py3_sitedir}/%{module}
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/murmur3.cpython-*.so
%{py3_sitedir}/%{module}/__pycache__/
%dir %{py3_sitedir}/%{module}/io
%{py3_sitedir}/%{module}/io/*.py
%{py3_sitedir}/%{module}/io/libevwrapper.cpython-*.so
%{py3_sitedir}/%{module}/io/__pycache__
%{py3_sitedir}/cassandra_driver-%{version}-py*.egg-info
# %{_examplesdir}/python3-%{module}-%{version}

%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
