#
# Conditional build:
%bcond_with	tests	# perform "make test" (requires running esd)
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Audio
%define		pnam	ESD
Summary:	Audio::ESD Perl module - interface to Enlightened Sound Daemon
Summary(pl.UTF-8):	Moduł Perla Audio::ESD - interfejs do ESD ("Oświeconego" Demona Dźwięku)
Name:		perl-Audio-ESD
Version:	0.02
Release:	5
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	71f71b5e4d47028482e2ae18ae010c2a
BuildRequires:	esound-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides a Perl interface to the Enlightened Sound Daemon,
which is used on many Linux systems to mix sound output streams from
multiple desktop applications. It allows you to open input, output,
monitoring, and filtering streams which function like normal Perl
filehandles, as well as to control various parameters on the ESD
server.

%description -l pl.UTF-8
Ten moduł udostępnia perlowy interfejs do ESD - "Oświeconego" Demona
Dźwięku, który jest używany na wielu systemach linuksowych do
mieszania strumieni dźwiękowych z wielu aplikacji. Pozwala na
otworzenie strumieni wejściowego, wyjściowego, monitorującego i
filtrującego, które działają jak normalne perlowe uchwyty plików, a
także na kontrolę różnych parametrów serwera ESD.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
# typemap missing...
cat > typemap <<EOF
my_esd_t		T_IV
esd_server_info_t *	T_PTROBJ
esd_info_t *		T_PTROBJ
EOF

%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/Audio/ESD.pm
%dir %{perl_vendorarch}/auto/Audio/ESD
# is this empty file required ?
%{perl_vendorarch}/auto/Audio/ESD/autosplit.ix
%{perl_vendorarch}/auto/Audio/ESD/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Audio/ESD/*.so
%{_mandir}/man3/*
