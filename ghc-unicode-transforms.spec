#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	unicode-transforms
Summary:	Unicode normalization
Name:		ghc-%{pkgname}
Version:	0.3.6
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/unicode-transforms
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	84c76482be51c0e3b90b27999e629f0e
URL:		http://hackage.haskell.org/package/unicode-transforms
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-bitarray >= 0.0.1
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-bitarray-prof >= 0.0.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-bitarray >= 0.0.1
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Fast Unicode 12.1.0 normalization in Haskell (NFC, NFKC, NFD, NFKD).

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-bitarray-prof >= 0.0.1

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc Changelog.md NOTES.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/UTF8
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/UTF8/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/UTF8/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Properties
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Properties/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Properties/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/UTF8/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Unicode/Properties/*.p_hi
%endif
