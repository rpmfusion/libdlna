Version: 0.2.3
Summary: Open-source implementation of DLNA (Digital Living Network Alliance) standards
Name: libdlna
Release: 6%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://libdlna.geexbox.org/
Source: http://libdlna.geexbox.org/releases/%{name}-%{version}.tar.bz2
Patch0: libdlna-pkgconfig.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ffmpeg-devel

%description
Libdlna aims at being the reference open-source implementation of 
DLNA (Digital Living Network Alliance) standards.

%package devel
Group: Development/Libraries
Summary: Include files needed for development with libdlna
Requires: libdlna = %{version}-%{release}
Requires: pkgconfig
Requires: ffmpeg-devel

%description devel
The libdlna-devel package contains the files necessary for development with
the libdlna libraries.

%prep
%setup -q
%patch0 -p1
# adjust includes for the header move in latest ffmpeg <sigh>
sed -i -e 's|ffmpeg/avcodec.h|ffmpeg/libavcodec/avcodec.h|g' \
  -e 's|ffmpeg/avformat.h|ffmpeg/libavformat/avformat.h|g' \
  -e 's|postproc/postprocess.h|ffmpeg/libpostproc/postprocess.h|g' \
  -e 's|ffmpeg/swscale.h|ffmpeg/libswscale/swscale.h|g' \
  ext/ffmpeg/*.c ext/ffmpeg/*.h ext/libpostproc/*.c


%build
export CFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix} --libdir=%{_libdir} --includedir=%{_includedir} --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog AUTHORS README
%{_libdir}/libdlna.so.*

%files devel
%defattr(0644,root,root,0755)
%{_includedir}/dlna.h
%{_libdir}/libdlna.so
%{_libdir}/pkgconfig/libdlna.pc

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2.3-6
- rebuild

* Sun Feb 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2.3-5
- rebuild for new ffmpeg

* Thu Jan 03 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.2.3-4
- add requires ffmpeg-devel for devel package

* Fri Dec 14 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.2.3-3
- Modify libdlna-pkgconfig.patch

* Fri Dec 14 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.2.3-2
- Modify configure to fix pkgconfig for lib64
- Modify configure to use -O2 instead of -O3

* Sun Nov 18 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.2.3-1
- Initial build
