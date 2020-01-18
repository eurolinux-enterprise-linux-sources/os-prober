Name:           os-prober
Version:        1.58
Release:        5%{?dist}
Summary:        Probes disks on the system for installed operating systems

Group:          System Environment/Base
# For more information about licensing, see copyright file.
License:        GPLv2+ and GPL+
URL:            http://kitenet.net/~joey/code/os-prober/
Source0:        http://ftp.de.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.gz
# move newns binary outside of os-prober subdirectory, so that debuginfo
# can be automatically generated for it
Patch0:         os-prober-newnsdirfix.patch
Patch1:         os-prober-no-dummy-mach-kernel.patch
# Sent upstream
Patch2:         os-prober-mdraidfix.patch
Patch3:         os-prober-yaboot-parsefix.patch
Patch4:         os-prober-usrmovefix.patch
Patch5:         os-prober-remove-basename.patch
Patch6:         os-prober-disable-debug-test.patch
Patch7:         os-prober-btrfsfix.patch
Patch8:         os-prober-bootpart-name-fix.patch
Patch9:         os-prober-mounted-partitions-fix.patch
Patch10:        os-prober-factor-out-logger.patch
# To be sent upstream
Patch11:        os-prober-factored-logger-efi-fix.patch
Patch12:	os-prober-man.patch

Requires:       udev coreutils util-linux
Requires:       grep /bin/sed /sbin/modprobe

%description
This package detects other OSes available on a system and outputs the results
in a generic machine-readable format. Support for new OSes and Linux
distributions can be added easily. 

%prep
%setup -q
%patch0 -p1 -b .newnsdirfix
%patch1 -p1 -b .macosxdummyfix
%patch2 -p1 -b .mdraidfix
%patch3 -p1 -b .yaboot-parsefix
%patch4 -p1
%patch5 -p1 -b .remove-basename
%patch6 -p1 -b .disable-debug-test
%patch7 -p1
%patch8 -p1 -b .bootpart-name-fix
%patch9 -p1 -b .mounted-partitions-fix
%patch10 -p1 -b .factor-out-logger
%patch11 -p1 -b .factor-out-logger-efi-fix
%patch12 -p1 -b .man

find -type f -exec sed -i -e 's|usr/lib|usr/libexec|g' {} \;
sed -i -e 's|grub-probe|grub2-probe|g' os-probes/common/50mounted-tests \
     linux-boot-probes/common/50mounted-tests

%build
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
install -m 0755 -d %{buildroot}%{_bindir}
install -m 0755 -d %{buildroot}%{_var}/lib/%{name}
install -d 0755 -d %{buildroot}%{_mandir}/man1/

install -m 0755 -p os-prober linux-boot-prober %{buildroot}%{_bindir}
install -m 0755 -Dp newns %{buildroot}%{_libexecdir}/newns
install -m 0644 -Dp common.sh %{buildroot}%{_datadir}/%{name}/common.sh
install -m 0644 -Dp *.1 %{buildroot}%{_mandir}/man1/

%ifarch m68k
ARCH=m68k
%endif
%ifarch ppc ppc64
ARCH=powerpc
%endif
%ifarch sparc sparc64
ARCH=sparc
%endif
%ifarch %{ix86} x86_64
ARCH=x86
%endif

for probes in os-probes os-probes/mounted os-probes/init \
              linux-boot-probes linux-boot-probes/mounted; do
        install -m 755 -d %{buildroot}%{_libexecdir}/$probes 
        cp -a $probes/common/* %{buildroot}%{_libexecdir}/$probes
        if [ -e "$probes/$ARCH" ]; then 
                cp -a $probes/$ARCH/* %{buildroot}%{_libexecdir}/$probes 
        fi
done
if [ "$ARCH" = x86 ]; then
        install -m 755 -p os-probes/mounted/powerpc/20macosx \
            %{buildroot}%{_libexecdir}/os-probes/mounted
fi

%files
%doc README TODO debian/copyright debian/changelog
%{_bindir}/*
%{_datadir}/%{name}
%{_libexecdir}/*
%{_mandir}/man1/*
%{_var}/lib/%{name}

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.58-5
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 Peter Jones <pjones@redhat.com> - 1.58-4
- Add man pages.
  Resolves: rhbz#948848

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.58-3
- Mass rebuild 2013-12-27

* Tue Jun 18 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-2
- Fix a bug in EFI detection because of redirecting result output

* Sun May 05 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-1
- Update to upstream version 1.58, with UEFI support

* Sat Feb 02 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.57-2
- Fix a bug in recent btrfs patch when an extended partition is examined. 
  (H.J. Lu) (bug #906847)
- Fix naming of /boot partitions according to their fstab entry (bug #893472)
- Don't generate .btrfsfix files which will be included in final rpm
- Fix wrong boot partition set by linux-boot-prober when / and /boot are
  mounted (bug #906886)
- Factor out 'logger', so that it is run once and logs are piped to it (John
  Reiser) (bug #875356)

* Tue Jan 22 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.57-1
- Update to 1.57 (#890409)
- Use shell string processing rather than 'basename' (#875356)
- Make it possible to disable logging debug messages by assigning a value to
  OS_PROBER_DISABLE_DEBUG environment variable (Gene Czarcinski) (#893997).
- Detect multi btrfs pools/volumes (Gene Czarcinski) (#888341)

* Thu Oct 11 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.56-1
- Update to 1.56 with a bug fix and applied one of my patches

* Mon Aug 27 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.55-1
- Update to new upstream version: 1.55

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 02 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.53-3
- Consider usrmoved distribtions in fallback linux detector (bug #826754)
- Remove patch backup files from final rpm package (by not creating a backup!)

* Fri May 25 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.53-2
- Add support for OSes installed on Linux mdraid partitions, bug #752402
- Add Fedora's grub2 config path, fixes generating menu entries for other
  installed Fedora's
- Fixed bug in parsing yaboot.conf: accept spaces around '=' for append, 
  bug #825041

* Fri May 11 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.53-1
- Updated to 1.53 for a bugfix
- Fixed directory name in upstream tarbal

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 1.52-3
- Don't detect our Mac boot blocks as OS X.
  Resolves: rhbz#811412

* Sun Apr 29 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.52-2
- use correct directory name for setup

* Sun Apr 29 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.52-1
- Updated to 1.52, supports win 8

* Wed Mar 28 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.51-1
- Update to latest upstream version, 1.51

* Sat Jan 21 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.48-3
- Remove dmraid and lvm2 dependency. bug #770393

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.48-1
- Updated to 1.48 release

* Thu May 19 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.47-1
- Updated to the new upstream version 1.47

* Wed May 04 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.46-2
- Removed obsolete parts (build tag, defattr, etc)
- Added a patch to move newns outside of os-prober subdirectory
- Added required utilities as package requires

* Sat Apr 30 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.46-1
- Updated to 1.46 release

* Tue Feb 22 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.42-2
- Remove executable permission from common.sh

* Thu Feb 17 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.42-1
- Initial version
