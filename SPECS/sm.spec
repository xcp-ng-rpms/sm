%global package_speccommit d1db94566be4ff4dcc574ff44b508e48e849dbe6
%global package_srccommit v3.0.3
# -*- rpm-spec -*-

Summary: sm - XCP storage managers
Name:    sm
Version: 3.0.3
Release: 1.4%{?xsrel}%{?dist}
Group:   System/Hypervisor
License: LGPL
URL:  https://github.com/xapi-project/sm
Source0: sm-3.0.3.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define __python python3.6

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python36-pylint
BuildRequires: python3-coverage
BuildRequires: python36-bitarray
BuildRequires: python3-future

# XCP-ng: python36-mock for %%check
BuildRequires: python36-mock

# XCP-ng: gcc must be explicitly required in our build system
BuildRequires: gcc

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: xenserver-multipath
Requires: xenserver-lvm2 >= 2.02.180-11.xs+2.0.2
Obsoletes: lvm2-sm-config <= 7:2.02.180-15.xs8
Requires: python36-bitarray
Requires(post): xs-presets >= 1.3
Requires(preun): xs-presets >= 1.3
Requires(postun): xs-presets >= 1.3
Conflicts: kernel < 4.19.19-5.0.0

Obsoletes: sm-additional-drivers

# XCP-ng patches
# Generated from our sm repository
# git format-patch v3.0.3..3.0.3-8.3
Patch1001: 0001-Update-xs-sm.service-s-description-for-XCP-ng.patch
Patch1002: 0002-Add-TrueNAS-multipath-config.patch
Patch1003: 0003-feat-drivers-add-CephFS-and-GlusterFS-drivers.patch
Patch1004: 0004-feat-drivers-add-XFS-driver.patch
Patch1005: 0005-feat-drivers-add-ZFS-driver-to-avoid-losing-VDI-meta.patch
Patch1006: 0006-feat-drivers-add-LinstorSR-driver.patch
Patch1007: 0007-feat-tests-add-unit-tests-concerning-ZFS-close-xcp-n.patch
Patch1008: 0008-Added-SM-Driver-for-MooseFS.patch
Patch1009: 0009-Avoid-usage-of-umount-in-ISOSR-when-legacy_mode-is-u.patch
Patch1010: 0010-MooseFS-SR-uses-now-UUID-subdirs-for-each-SR.patch
Patch1011: 0011-Fix-is_open-call-for-many-drivers-25.patch
Patch1012: 0012-Remove-SR_CACHING-capability-for-many-SR-types-24.patch
Patch1013: 0013-Fix-code-coverage-regarding-MooseFSSR-and-ZFSSR-29.patch
Patch1014: 0014-py3-simple-changes-from-futurize-on-XCP-ng-drivers.patch
Patch1015: 0015-py3-futurize-fix-of-xmlrpc-calls-for-CephFS-GlusterF.patch
Patch1016: 0016-py3-use-of-integer-division-operator.patch
Patch1017: 0017-test_on_slave-allow-to-work-with-SR-using-absolute-P.patch
Patch1018: 0018-py3-switch-interpreter-to-python3.patch
Patch1019: 0019-Support-recent-version-of-coverage-tool.patch
Patch1020: 0020-Fix-blktap-error-mapping-in-python3.patch
Patch1021: 0021-feat-LinstorSR-import-all-8.2-changes.patch
Patch1022: 0022-feat-LinstorSR-is-now-compatible-with-python-3.patch

%description
This package contains storage backends used in XCP

%prep
%autosetup -p1

%build
DESTDIR=$RPM_BUILD_ROOT make

%install
DESTDIR=$RPM_BUILD_ROOT make install

# Mark processes that should be moved to the data path
%triggerin -- libcgroup-tools
( patch -tsN -r - -d / -p1 || : )>/dev/null << 'EOF'
--- /etc/cgrules.conf
+++ /etc/cgrules.conf
@@ -7,4 +7,6 @@
 #@student    cpu,memory    usergroup/student/
 #peter        cpu        test1/
 #%        memory        test2/
+*:tapdisk    cpu,cpuacct    vm.slice/
+%        blkio        vm.slice/
 # End of file
EOF

%pre
# Remove sm-multipath on install or upgrade, to ensure it goes
[ ! -x /sbin/chkconfig ] || chkconfig --del sm-multipath || :

%post
%systemd_post make-dummy-sr.service
%systemd_post mpcount.service
%systemd_post sm-mpath-root.service
%systemd_post xs-sm.service
%systemd_post storage-init.service
%systemd_post usb-scan.socket
%systemd_post mpathcount.socket

# On upgrade, migrate from the old statefile to the new statefile so that
# storage is not reinitialized.
if [ $1 -gt 1 ] ; then
    grep -q ^success /etc/firstboot.d/state/10-prepare-storage 2>/dev/null && touch /var/lib/misc/ran-storage-init || :
fi

rm -f /etc/lvm/cache/.cache
touch /etc/lvm/cache/.cache

# We try to be "update-alternatives" ready.
# If a file exists and it is not a symlink we back it up
if [ -e /etc/multipath.conf -a ! -h /etc/multipath.conf ]; then
   mv -f /etc/multipath.conf /etc/multipath.conf.$(date +%F_%T)
fi
update-alternatives --install /etc/multipath.conf multipath.conf /etc/multipath.xenserver/multipath.conf 90

# XCP-ng: enable linstor-monitor by default.
# However it won't start without linstor-controller.service
systemctl enable linstor-monitor.service

%preun
%systemd_preun make-dummy-sr.service
%systemd_preun mpcount.service
%systemd_preun sm-mpath-root.service
%systemd_preun xs-sm.service
%systemd_preun storage-init.service
%systemd_preun usb-scan.socket
%systemd_preun mpathcount.socket
# Remove sm-multipath on upgrade or uninstall, to ensure it goes
[ ! -x /sbin/chkconfig ] || chkconfig --del sm-multipath || :
# only remove in case of erase (but not at upgrade)
if [ $1 -eq 0 ] ; then
    update-alternatives --remove multipath.conf /etc/multipath.xenserver/multipath.conf
fi
exit 0

# XCP-ng
%systemd_preun linstor-monitor.service

%postun
%systemd_postun make-dummy-sr.service
%systemd_postun mpcount.service
%systemd_postun sm-mpath-root.service
%systemd_postun xs-sm.service
%systemd_postun storage-init.service
if [ $1 -eq 0 ]; then
    [ ! -d /etc/lvm/master ] || rm -Rf /etc/lvm/master || exit $?
    cp -f /etc/lvm/lvm.conf.orig /etc/lvm/lvm.conf || exit $?
elif [ $1 -eq 1 ]; then
    true;
fi

# XCP-ng
%systemd_postun linstor-monitor.service

%check
tests/run_python_unittests.sh
cp .coverage %{buildroot}
cp coverage.xml %{buildroot}
cp -r htmlcov %{buildroot}/htmlcov

%files
%defattr(-,root,root,-)
/etc/udev/scripts/xs-mpath-scsidev.sh
/etc/xapi.d/plugins/coalesce-leaf
/etc/xapi.d/plugins/lvhd-thin
/etc/xapi.d/plugins/nfs-on-slave
/etc/xapi.d/plugins/on-slave
/etc/xapi.d/plugins/tapdisk-pause
/etc/xapi.d/plugins/testing-hooks
/etc/xapi.d/plugins/intellicache-clean
/etc/xapi.d/plugins/trim
/etc/xensource/master.d/02-vhdcleanup
/opt/xensource/bin/blktap2
/opt/xensource/bin/tapdisk-cache-stats
/opt/xensource/bin/xe-getarrayidentifier
/opt/xensource/bin/xe-get-arrayid-lunnum
/opt/xensource/bin/xe-getlunidentifier
/opt/xensource/debug/tp
/opt/xensource/libexec/check-device-sharing
/opt/xensource/libexec/dcopy
/opt/xensource/libexec/local-device-change
/opt/xensource/libexec/make-dummy-sr
/opt/xensource/libexec/usb_change
/opt/xensource/libexec/kickpipe
/opt/xensource/libexec/set-iscsi-initiator
/opt/xensource/libexec/storage-init
/opt/xensource/sm/DummySR
/opt/xensource/sm/DummySR.py
/opt/xensource/sm/EXTSR
/opt/xensource/sm/EXTSR.py
/opt/xensource/sm/FileSR
/opt/xensource/sm/FileSR.py
/opt/xensource/sm/HBASR
/opt/xensource/sm/HBASR.py
/opt/xensource/sm/ISCSISR
/opt/xensource/sm/RawISCSISR.py
/opt/xensource/sm/BaseISCSI.py
/opt/xensource/sm/ISOSR
/opt/xensource/sm/ISOSR.py
/opt/xensource/sm/LUNperVDI.py
/opt/xensource/sm/LVHDSR.py
/opt/xensource/sm/LVHDoHBASR.py
/opt/xensource/sm/LVHDoISCSISR.py
/opt/xensource/sm/LVHDoFCoESR.py
/opt/xensource/sm/LVMSR
/opt/xensource/sm/LVMoHBASR
/opt/xensource/sm/LVMoISCSISR
/opt/xensource/sm/LVMoFCoESR
/opt/xensource/sm/NFSSR
/opt/xensource/sm/NFSSR.py
/opt/xensource/sm/SMBSR
/opt/xensource/sm/SMBSR.py
/opt/xensource/sm/SHMSR.py
/opt/xensource/sm/SR.py
/opt/xensource/sm/SRCommand.py
/opt/xensource/sm/VDI.py
/opt/xensource/sm/XE_SR_ERRORCODES.xml
/opt/xensource/sm/blktap2.py
/opt/xensource/sm/cleanup.py
/opt/xensource/sm/devscan.py
/opt/xensource/sm/fjournaler.py
/opt/xensource/sm/flock.py
/opt/xensource/sm/ipc.py
/opt/xensource/sm/iscsilib.py
/opt/xensource/sm/fcoelib.py
/opt/xensource/sm/journaler.py
/opt/xensource/sm/lcache.py
/opt/xensource/sm/lock.py
/opt/xensource/sm/lvhdutil.py
/opt/xensource/sm/lvmanager.py
/opt/xensource/sm/lvmcache.py
/opt/xensource/sm/lvutil.py
/opt/xensource/sm/metadata.py
/opt/xensource/sm/srmetadata.py
/opt/xensource/sm/mpath_cli.py
/opt/xensource/sm/mpath_dmp.py
/opt/xensource/sm/mpath_null.py
/opt/xensource/sm/mpathcount.py
/opt/xensource/sm/mpathutil.py
/opt/xensource/sm/mpp_mpathutil.py
/opt/xensource/sm/nfs.py
/opt/xensource/sm/refcounter.py
/opt/xensource/sm/resetvdis.py
/opt/xensource/sm/scsiutil.py
/opt/xensource/sm/scsi_host_rescan.py
/opt/xensource/sm/sysdevice.py
/opt/xensource/sm/udevSR
/opt/xensource/sm/udevSR.py
/opt/xensource/sm/util.py
/opt/xensource/sm/cifutils.py
/opt/xensource/sm/verifyVHDsOnSR.py
/opt/xensource/sm/vhdutil.py
/opt/xensource/sm/trim_util.py
/opt/xensource/sm/xs_errors.py
/opt/xensource/sm/wwid_conf.py
/opt/xensource/sm/pluginutil.py
/opt/xensource/sm/constants.py
/opt/xensource/sm/cbtutil.py
/opt/xensource/sm/multipath-root-setup
%dir /opt/xensource/sm/plugins
/opt/xensource/sm/plugins/__init__.py*
/sbin/mpathutil
/etc/rc.d/init.d/sm-multipath
%{_unitdir}/make-dummy-sr.service
%{_unitdir}/xs-sm.service
%{_unitdir}/sm-mpath-root.service
%{_unitdir}/usb-scan.service
%{_unitdir}/usb-scan.socket
%{_unitdir}/mpathcount.service
%{_unitdir}/mpathcount.socket
%{_unitdir}/storage-init.service
%config /etc/udev/rules.d/65-multipath.rules
%config /etc/udev/rules.d/55-xs-mpath-scsidev.rules
%config /etc/udev/rules.d/58-xapi.rules
%config /etc/multipath.xenserver/multipath.conf
%config /etc/udev/rules.d/69-dm-lvm-metad.rules
%config /etc/logrotate.d/SMlog
%config /etc/udev/rules.d/57-usb.rules
%doc CONTRIB LICENSE MAINTAINERS README.md
# XCP-ng
/etc/systemd/system/linstor-satellite.service.d/override.conf
/etc/systemd/system/var-lib-linstor.service
/etc/xapi.d/plugins/linstor-manager
/opt/xensource/bin/linstor-kv-tool
/opt/xensource/libexec/fork-log-daemon
/opt/xensource/libexec/linstor-monitord
/opt/xensource/libexec/safe-umount
/opt/xensource/sm/CephFSSR
/opt/xensource/sm/CephFSSR.py
/opt/xensource/sm/GlusterFSSR
/opt/xensource/sm/GlusterFSSR.py
/opt/xensource/sm/linstorjournaler.py
/opt/xensource/sm/LinstorSR
/opt/xensource/sm/LinstorSR.py
/opt/xensource/sm/linstorvhdutil.py
/opt/xensource/sm/linstorvolumemanager.py
/opt/xensource/sm/MooseFSSR
/opt/xensource/sm/MooseFSSR.py
/opt/xensource/sm/XFSSR
/opt/xensource/sm/XFSSR.py
/opt/xensource/sm/ZFSSR
/opt/xensource/sm/ZFSSR.py
%{_unitdir}/linstor-monitor.service

%changelog
* Mon Jul 31 2023 Benjamin Reis <benjamin.reis@vates.fr> - 3.0.3-1.4
- Drop 0006-Re-add-the-ext4-driver-for-users-who-need-to-transit.patch

* Thu Jul 20 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 3.0.3-1.3
- LINSTOR driver support for XCP-ng 8.3
- Add 0021-Fix-blktap-error-mapping-in-python3.patch
- Add 0022-feat-LinstorSR-import-all-8.2-changes.patch
- Add 0023-feat-LinstorSR-is-now-compatible-with-python-3.patch

* Thu May 04 2023 Yann Dirson <yann.dirson@vates.fr> - 3.0.3-1.1
- Rebase on sm 3.0.3
- Patches for python3 compat.
- Switch interpreter to python3 in drivers.
- Use python36-bitarray not python3-bitarray.
- Use python36-pylint not python3-pylint.
- BuildRequires: python36-mock for %check.
- *** Upstream changelog ***
- * Fri Jan 27 2023 Mark Syms <mark.syms@citrix.com> - 3.0.3-1
- - Include exportname in NBD data for attach
- * Tue Jan 17 2023 Mark Syms <mark.syms@citrix.com> - 3.0.2-1
- - CBT python3 fixes
- * Thu Jan 12 2023 Mark Syms <mark.syms@citrix.com> - 3.0.1-1
- - Check for open tapdisk NBD sockets before shutting down
- * Tue Oct 25 2022  <mark.syms@citrix.com> - 3.0.0-1
- - Migrate to Python3

* Thu Dec 15 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.46.16-1.1
- Rebase on sm 2.46.16
- *** Upstream changelog ***
- * Wed Sep 21 2022 Tim Smith <tim.smith@citrix.com> - 2.46.16-1
- - CA-370572: relinking is a transient property, do not copy to clones
- - CA-370696 Do not attempt to validate device or NFS server paths
- * Wed Aug 31 2022 Mark Syms <mark.syms@citrix.com> - 2.46.15-1
- - CA-353437: give coalesce tracker grace iterations to make progress
- - CA-353437: activate a FIST point in the coalesce tracker for test injection
- - Add multipath configuration for Dell ME4
- * Wed Aug 31 2022  <mark.syms@citrix.com> - 2.46.14-2
- - CA-368585: Remove dependency on lvm2-sm-config
- * Mon Aug 22 2022 Mark Syms <mark.syms@citrix.com> - 2.46.14-1
- - CA-370037: report errors from NFS correctly
- * Tue Aug 16 2022 Mark Syms <mark.syms@citrix.com> - 2.46.13-1
- - Multipath fixes
- * Mon Jul 25 2022 Mark Syms <mark.syms@citrix.com> - 2.46.12-1
- - CA-368769: extend the timeout on tap-ctl close

* Mon Sep 19 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.46.11-1.2
- Re-enable tests, test file coverage rate is now 100%

* Thu Sep 01 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.46.11-1.1
- Rebase on CH 8.3 Preview
- Remove patches merged upstream
- Keep other patches still necessary.

* Wed Jun 22 2022 Mark Syms <mark.syms@citrix.com> - 2.46.11-1
- Remove use of eval
- Raise explicit error in case of NFS mount failure

* Wed May  4 2022 Mark Syms <mark.syms@citrix.com> - 2.46.10-2
- Add requires for lvm2-sm-config

* Fri Mar 18 2022 Mark Syms <mark.syms@citrix.com> - 2.46.10-1
- CA-365359: cope with on_slave.is_open passing server=None
- Fix timeout_call: alarm must be reset in case of success
- timeout_call returns the result of user function now

* Mon Dec 13 2021 Mark Syms <mark.syms@citrix.com> - 2.46.9-1
- CP-38670: add dependency on python-monotonic
- Update product identification for QNAP iSCSI storage

* Thu Oct 07 2021 Mark Syms <mark.syms@citrix.com> - 2.46.8-1
- CA-359453: fallback to rename in snapshot if hardlinks are not supported
- CP-38316: Update pathchecker for EQL to be readsector0

* Mon Oct 04 2021 Mark Syms <mark.syms@citrix.com> - 2.46.7-1
- CP-38283: Support explicit NFS 4.0 version choice
- CP-38283: allow any NFS 4.x version
- CA-359621: fix regression in error handler

* Tue Sep 28 2021 Mark Syms <mark.syms@citrix.com> - 2.46.6-1
- CA-359304: ignore relinking and activating tags in update_sm_config

* Wed Sep  8 2021 Mark Syms <mark.syms@citrix.com> - 2.46.5-2
- Dummy build

* Tue Sep 07 2021 Mark Syms <mark.syms@citrix.com> - 2.46.5-1
- CA-327302: report signals in CommandException
- CA-352880: when deleting an HBA SR remove the kernel devices

* Mon Aug 09 2021 Mark Syms <mark.syms@citrix.com> - 2.46.4-1
- CA-356761: ensure that children are always reloaded on relink
- CA-334762: Fix VDI import with storage driver domains
- CA-356983: ignore more rules on td/nbd devices

* Thu Jul 15 2021 Mark Syms <mark.syms@citrix.com> - 2.46.3-1
- CA-356645: use "self.session is None" not "self.session == None"
- CP-37498: Fix all E711 errors in SM

* Tue Jul 13 2021 Mark Syms <mark.syms@citrix.com> - 2.46.2-1
- CA-356234: don't run repair if parent is raw
- CA-356102: retry LV commands when 'Incorrect checksum in metadata' reported
- CA-356411: correct check for session

* Wed Jun 16 2021 Mark Syms <mark.syms@citrix.com> - 2.46.1-1
- CA-355401: make post attach scan best effort and report errors
- CA-355289: ensure xapi is initialised before starting GC
- If not NFS ACLs provided, assume everyone (external contributor)

* Mon May 24 2021 Mark Syms <mark.syms@citrix.com> - 2.46.0-1
- CA-354692: check for device parameter in create/probe calls

* Tue May 18 2021 Mark Syms <mark.syms@citrix.com> - 2.45.0-1
- Remove OCFS SRs
- CA-354228: Reinstate load calls in _pathrefresh

* Wed Apr 14 2021 Mark Syms <mark.syms@citrix.com> - 2.44.0-2
- CP-36641: Fix build dependencies

* Tue Mar 02 2021 Mark Syms <mark.syms@citrix.com> - 2.44.0-1
- CA-352165: check for device key in dconf before referencing

* Tue Feb 23 2021 Mark Syms <mark.syms@citrix.com> - 2.43.0-1
- CA-351674: Reduce the frequency and cost of pathrefresh calls

* Tue Feb 16 2021 Mark Syms <mark.syms@citrix.com> - 2.42.0-1
- Support IPv6 in NFS

* Wed Feb 03 2021 Mark Syms <mark.syms@citrix.com> - 2.41.0-1
- Remove deprecated rawhba package

* Mon Jan 25 2021 Mark Syms <mark.syms@citrix.com> - 2.40.0-1
- CA-350871: optimise locking in LVHDSR snapshot

* Wed Jan 06 2021 Mark Syms <mark.syms@citrix.com> - 2.39.0-1
- New release
- PEP8 housekeeping cleanup
- CA-350437: simplify 02vhd-cleanup to only handle LVM refcounts

* Thu Dec 10 2020 Mark Syms <mark.syms@citrix.com> - 2.38.0-1
- New release

* Fri Dec 04 2020 Mark Syms <mark.syms@citrix.com> - 2.37.0-1
- Improved logging

* Mon Nov 30 2020 Mark Syms <mark.syms@citrix.com> - 2.36.0-2
- Enable sonarqube

* Wed Nov 25 2020 Mark Syms <mark.syms@citrix.com> - 2.36.0-1
- CA-349188: only check for the initator name, alias is optional

* Fri Nov 06 2020 Mark Syms <mark.syms@citrix.com> - 2.35.0-1
- EMC-75: add config for new DellEMC PowerStore array
- Add TrueNAS ALUA support

* Tue Oct 13 2020 Mark Syms <mark.syms@citrix.com> - 2.34.0-1
- Stage 1 futurize on SM
- CA-346583: make set-iscsi-initiator idempotent
- CA-346590: log when activating flag removed

* Wed Sep 30 2020 Mark Syms <mark.syms@citrix.com> - 2.33.0-1
- CA-333441 create directory for set-iscsi-initiator
- CA-344254: address race between GC and VDI activate

* Tue Sep 15 2020 Mark Syms <mark.syms@citrix.com> - 2.32.0-1
- Use object member session instead of creating a new one
- CA-344254: add unit tests for blktap2.activate
- CA-344254: add tests for coalesce

* Tue Sep 01 2020 Mark Syms <mark.syms@citrix.com> - 2.31.0-1
- CP-32998 - Use cgclassify to move tapdisk into pre configured vm.slice and vm-blktap.slice
- CA-343115: ensure device symlinks are created correctly even when path count not required

* Mon Jul 13 2020 Mark Syms <mark.syms@citrix.com> - 2.30.0-1
- CA-340203: remove name header from mpath map list
- CP-34042: Add unit tests for mpath utils and remove dead code
- CP-33617 Initial set of unit tests for mpathcount.py
- Add unit tests for blktap2.TapCtl
- CP-33629 - Unit tests for HBA
- CA-341777: pass args in the correct order

* Fri May 29 2020 Mark Syms <mark.syms@citrix.com> - 2.29.0-1
- CA-339329 firstboot scripts shouldn't sync DB when upgrading

* Wed May 20 2020 Mark Syms <mark.syms@citrix.com> - 2.28.0-1
- CA-338619: log the hostname when asking slaves
- CA-332978: Ensure that multipath reconnects after failure
- CA-332978: Only force reload multipath on start

* Tue Apr 21 2020 Mark Syms <mark.syms@citrix.com> - 2.27.0-1
- CA-337772: remove dead code handling qcow files.
- CP-33292: add read caching capability flags

* Tue Apr 07 2020 Mark Syms <mark.syms@citrix.com> - 2.26.0-1
- CA-337352: just idempotently unlink NBD symlinks on deactivate

* Wed Mar 25 2020 Mark Syms <mark.syms@citrix.com> - 2.25.0-1
- CA-331454: Handle interrupted SMGC during hotfix application

* Fri Mar 13 2020 Mark Syms <mark.syms@citrix.com> - 2.24.0-1
- CA-335092: after an update we use the new SM but the NBD link won't be there

* Wed Mar 11 2020 marksy <mark.syms@citrix.com> - 2.23.0-1
- CA-335771: call tap-ctl close with a timeout

* Mon Mar 09 2020 Mark Syms <mark.syms@citrix.com> - 2.22.0-1
- Filter out USB storage from HBA device, since USB storage is already managed by udev SM
- CA-335351: ensure async tasks are cleaned up
- CP-31856 - Return nbd socket as parameter to XAPI
- CA-335178: If we don't need tap we dont have NBD
- CA-335178: Fix unitialized variable
- CA-335721: Add missing case blktap2 for cached devices.

* Wed Jan  8 2020 Mark Syms <mark.syms@citrix.com> - 2.21.0-1
- CA-333441: add script to update iSCSI IQN and restart daemons

* Mon Jan 06 2020 Mark Syms <mark.syms@citrix.com> - 2.20.0-1
- CP-31089: Move storage firstboot scripts out of xenserver-firstboot
- CA-332890: trigger mpath count when multipath dm device added/removed
- CA-331453: Ensure all v1 GC processes are killed upon master promotion.
- CA-332806: Lock speedfile and use atomic write to prevent corruption during abort.
- Fix xe-mount-iso-sr command name in error message

* Thu Dec 12 2019 Mark Syms <mark.syms@citrix.com> - 2.19.0-1
- CA-332806 - Fix type mismatch when processing speed file
- CA-332801: use slightly longer timeout for testing connectivity

* Tue Dec 10 2019 Mark Syms <mark.syms@citrix.com> - 2.18.0-1
- CP-32433: refine the conditions under which mpath count will trigger
- CP-32433: kick the multipath and usb scanners at start
- CA-324971: lock LVM commands to avoid concurrency clashes
- CP-32204: Dynamic limits to leaf coalesce using storage speed estimate.

* Wed Nov  6 2019 Mark Syms <mark.syms@citrix.com> - 2.17.0-1
- CA-329845 - Remove usage of credentials file for CIF
- CA-329841 - Sanitise chaps incoming usage

* Tue Oct 29 2019 Mark Syms <mark.syms@citrix.com> - 2.16.0-1
- LUNperVDI supports multipathed LUN

* Fri Oct 11 2019 Mark Syms <mark.syms@citrix.com> - 2.15.0-1
- CA-328536: If we give up on leaf-coalesce make sure we do so until process exits

* Wed Sep 25 2019 Mark Syms <mark.syms@citrix.com> - 2.14.0-1
- CP-32203: report VHD sizes when abandoning leaf coalesce
- CA-327382: reap child processes

* Mon Sep 02 2019 Mark Syms <mark.syms@citrix.com> - 2.13.0-1
- CP-32027: remove snapwatchd

* Wed Aug 07 2019 Mark Syms <mark.syms@citrix.com> - 2.12.0-1
- CA-324815: lock the SR in GC before deleting orphans.

* Tue Aug 06 2019 Mark Syms <mark.syms@citrix.com> - 2.11.0-1
- CA-323702: fcntl locks are per process, so need to reference count.

* Mon Jul 22 2019 Mark Syms <mark.syms@citrix.com> - 2.10.0-1
- CA-315318: optimise mpathcount, we only need to call once per SCSI ID
- CA-315318: refine udev trigger conditions for mpath count

* Tue Jul 09 2019 Mark Syms <mark.syms@citrix.com> - 2.9.0-1
- CA-323050: check that at least one iSCSI session established
- CA-323394: Stop tapdisk process inheriting fds from sm process
- CP-23299: add test for HFX-651

* Mon Jun 03 2019 Mark Syms <mark.syms@citrix.com> - 2.8.0-1
- Avoid exceptions from LV existance checks
- CA-314822: use scanLocked in should_prempt to avoid SR contents changing during scan

* Wed May 08 2019 Mark Syms <mark.syms@citrix.com> - 2.7.0-1
- CA-316157: Check if any garbage collection needs to be done before going quiet
- CA-309979 Fix Storage Manager initialisation
- CA-315152: gc_force needs to take gc_active lock not running

* Tue Apr 16 2019 Mark Syms <mark.syms@citrix.com> - 2.6.0-1
- CA-314717 Explicit stdout and stderr for scan services

* Tue Apr 09 2019 Mark Syms <mark.syms@citrix.com> - 2.5.0-1
- CA-312605: Allow config of pause in _gcLoop.

* Mon Apr 01 2019 Mark Syms <mark.syms@citrix.com> - 2.4.0-1
- CA-313960: ensure that mpathcount trigger correctly

* Fri Mar 22 2019 Mark Syms <mark.syms@citrix.com> - 2.3.0-1
- CA-311551: do not trigger mpath count for nbd devices
- CA-298641: be more benign on removing host tag
- CA-273708: improve VHD scan for file-based SR
- CA-312608: Set scheduler to noop for tdX devices

* Fri Feb 15 2019 Mark Syms <mark.syms@citrix.com> - 2.2.0-1
- Update MAINTAINERS file
- CA-247723: wait for udevadm settle in LVM create

* Wed Feb 06 2019 Mark Syms <mark.syms@citrix.com> - 2.0.0-1
- Update NFS unit tests to make intent clearer
- Properly strip output of scsi_id
- NFS 4.1 Support
- CA-262506: Remove sec=ntlm from SMBSR mount option
- cifs.conf: Remove cifs.conf
- CP-30167: handle changed blkback kthread notification

* Wed Jan 23 2019 Mark Syms <mark.syms@citrix.com> - 1.37.0-1
- CA-285844: update mpathcount so that it can remove multipath information as well as add it
- CA-293816: convert OSError to CommandException
- CA-293816: make _clonecleanup safer
- CA-293816: stop and rollback earlier in case of errors

* Tue Jan 08 2019 Mark Syms <mark.syms@citrix.com> - 1.36.0-1
- Update MAX_VHD_SIZE to 2088960MiB (2040GiB).

* Wed Nov 28 2018 Mark Syms <mark.syms@citrix.com> - 1.35.0-1
- CA-303252 Generalise the pipe kicker
- CA-303252 Make the multipath count a kickable socket service
- CA-302773: move import of plugins until we need it.

* Mon Nov 26 2018 Tim Smith <tim.smith@citrix.com> - 1.34.0-2.0
- CA-303252 update mpathcount to use the kickpipe trigger

* Wed Nov 21 2018 Mark Syms <mark.syms@citrix.com> - 1.34.0-1
- Revert "CP-27709: suppress error if blkdiscard fails on full provisioned lun"

* Fri Nov 16 2018 Mark Syms <mark.syms@citrix.com> - 1.33.0-1
- CP-27709: suppress error if blkdiscard fails on full provisioned lun
- CP-29603: load plugins for key discovery
- CP-29688:encryption key lookup plugin
- CP-29688: Install the test plugin
- CP-29689: Integrate encryption key lookup into Storage Manager
- CP-29755: Implement VDI.create for encrypted VDIs
- If key_hash is present in sm_config then assign to variable
- CP-29778: detect encrypted VHDs during SR scan
- keymanagerutil: generate completely random keys & store them in base64
- Added alphanumeric key generator and removed key field from json
- CA-302505: Add key_hash to sm_config of snapshots if it exists
- CA-302770: Added key_hash key to sm_config_keep
- CP-29955: pass VDI UUID too to key lookup plugin
- CP-29955: Log failures in key lookup plugins

* Fri Nov 09 2018 Mark Syms <mark.syms@citrix.com> - 1.32.0-1
- CA-286144: add usb-scan systemd units
- CA-302514 increase default NFS timeouts

* Thu Nov  1 2018 Mark Syms <mark.syms@citrix.com> - 1.31.0-1.0
- CA-297628: Tweak mpath_dmp.py for using device-mapper-multipath-0.4.9
- Add versioned dependency for LVM2

* Tue Oct 30 2018 Liang Dai <liang.dai1@citrix.com> - 1.30.0-1
- CA-294319: CLI command sr-create failed: Error code: SR_BACKEND_FAILURE_77

* Mon Oct 15 2018 Mark Syms <mark.syms@citrix.com> - 1.29.0-1
- Remove obsolete 39-multipath.rules file from install rules
- CA-296534: if we give up on snapshot-coalesce, don't fall through to live coalesce

* Tue Oct 09 2018 Mark Syms <mark.syms@citrix.com> - 1.28.0-1
- CP-28924: Declare thin provisioning capability for file based SRs

* Mon Oct 01 2018 Mark Syms <mark.syms@citrix.com> - 1.27.0-1
- CA-292588 Add debug to header checking
- CA-297698 improve assert message

* Fri Sep 07 2018 Mark Syms <mark.syms@citrix.com> - 1.26.0-1
- CA-247723: Use fuser to report on who has the device open
- CA-295775 Fix handling of multipath events
- CA-295775 Escape from systemd-udevd's control group

* Tue Aug 14 2018 Mark Syms <mark.syms@citrix.com> - 1.25.0-1
- CA-294975: ensure chap settings are removed from discovery db when not used
- CA-295846: call vgs with --readonly
- CA-295861: extract processname correctly when there are no arguments

* Wed Jul 25 2018 Mark Syms <mark.syms@citrix.com> - 1.24.0-2.0
- Remove obsolete LVM config overrides, now in LVM package

* Mon Jul 16 2018 Mark Syms <mark.syms@citrix.com> - 1.24.0-1
- CA-292144 Avoid having an invalid leaf while taking a snapshot

* Fri Jun 29 2018 Mark Syms <mark.syms@citrix.com> - 1.23.0-1
- CA-292268: Retry tap-ctl.Spawn on failure
- Blacklist nbd devices

* Mon Jun 25 2018 Mark Syms <mark.syms@citrix.com> - 1.22.0-1
- CA-247723: extend timeout and log lsof if still busy afterwards

* Mon Jun 18 2018 Mark Syms <mark.syms@citrix.com> - 1.21.0-1
- CA-290491: do not leaf coalesce VDIs with allow_caching=true
- Add LIO-ORG iscsi device configuration
- Add RBD devices to blacklist
- CA-292103: do not scan for and clear signatures in new volumes

* Fri May 25 2018 marksy <mark.syms@citrix.com> - 1.20.0-1.0
- CA-247723: check lsof when EBUSY on device
- CA-287511: add ENOENT to acceptable IO retry errors in VDI load to avoid race
- CA-247723: refactor open exclusive and allow a single shot retry to counter new device tool race
- CA-277616: add retry into pathexists to diagnose underlying issue
- CA-288738: add dependency on multipathd.service
- CA-289543: get mpathcount to return the GFS2 multipath count
- CP-27874: Failed iSCSI paths are not reconnected to automatically
- CA-286622: fix logging issue
- CA-288100: in case the VDI is removed in between
- CA-288222: deactivate LV on slaves before changing the LVM layout
- CA-289979: Refine ENOENT error handling while deleting VDI

* Fri May 25 2018 marksy <mark.syms@citrix.com> - 1.19.0-1.0
- Release 1.19.0

* Tue Apr 17 2018 marksy <mark.syms@citrix.com> - 1.18.0-1.31
- CA-287884: reuse existing session in _get_pool_config
- CA-287883: Refresh CBT log LV on slave after snapshot

* Tue Apr 10 2018 marksy <mark.syms@citrix.com> - 1.18.0-1.30
- CA-283724: Don't attach CBT log when VDI attached in RO mode
- CA-274386: Ensure that get_supported_nfs_versions always returns a list
- CA-287504: Import Rackspace fix to Delete LUN on detach of RawISCSI
- CA-247723: add log trace for error on exclusive open to track reason
- CA-287286: correct error logging message read not write
- CA-277128: Remove broken RRD code from SM

* Tue Mar 27 2018 marksy <mark.syms@citrix.com> - 1.18.0-1.29
- CA-274822: SR-detach fails with parameter errors(add extra logs)
- CA-268337: have resetvdis.py request the GC abort before acquiring locks
- update series with upstream commit ids

* Fri Feb 16 2018 marksy <mark.syms@citrix.com> - 1.18.0-1.28
- Actually remove the patches which are now on github
- CA-267460: Make device multipath eligibility check more robust
- CA-273731: call _testHost before trying to mount ISO SR NFS share
- CA-283272: Skip multipath validity check if device is not up yet
- CA-283207: Modify mpathcount script to work for GFS2 SRs

* Tue Jan 30 2018 Mark Syms <mark.syms@citrix.com> - 1.18.0-1.27
- Release version 1.18.0

* Tue Jan 30 2018 marksy <mark.syms@citrix.com> - 1.17.1-1.26
- Move patches to github, update series and context in patches
- Merge CBT upstream, move patches and make minor corrections
- Update series with upstream commit ids
- Rationalise installation of pip packages
- Move the rest of Inverness patches to GH and update series references

* Wed Jan 10 2018 marksy <mark.syms@citrix.com> - 1.17.1-1.25
- CA-274584: this fixes reboot issues with iscsi sessions
- CA-276751: Make sure there are no left-overs in wwids file
- CA-277346: Fix flawed parsing of /proc/<pid>/cmdline, split on NUL

* Tue Dec 12 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.24
- CA-261907: cleanup refcounts when deleting unused volume
- CA-276601: update patch with correct ticket number

* Wed Dec 06 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.23
- CA-270011: Handle snapshotting a snapshot in a CBT chain
- Redo unit tests helpers for CBT chain setup and verification
- CA-274115: Handle RAW VDIs when getting block tracking status
- CA-257740: fix HA broken for NFS

* Tue Oct 31 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.22
- CA-268695: Do not strip bitmap strings
- CA-269654: Make tapdisk-unpause CBT aware
- CA-269988: Remove VDI from MGT metadata on data-destroy
- CA-269652: Live disk is not paused before bitmap coalesce on snapshot delete

* Wed Oct 25 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.21
- CA-267339: Race conditions when activating-deactiving cbtlog files
- CA-267032: add ESRCH to list of acceptable errors in pid search
- CP-24532: trigger pusb scan
- CP-24548: set usb path for VDI
- CP-25157: refine document of get_usb_node

* Thu Oct 19 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.20
- CA-269013: Check SR capability before querying CBT status
- CA-264210: Intellicache only supports a single base disk with deltas
- CA-269653: Make CBT changes only for user created snapshots

* Mon Oct 16 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.19
- CA-269166: remove bare print from error path

* Thu Oct 12 2017 marksy <mark.syms@citrix.com> - 1.17.1-1.18
- CA-255945: fix race on mkdir
- CP-24279: Use autospec=True on mocks for unit test
- CA-267352: Update local state of VDI after XAPI update
- CP-23681: [Unit test] Test snapshot creation on CBT VDI when OOS
- CP-23549: Make VDI._db_update use current CBT state of disk
- CP-25002: Update XAPI db with CBT state on snapshot

* Tue Oct 03 2017 marksy <mark.syms@citrix.com> - 1.17.1-xs.1+1.17
- CP-24893: test coverage improvements for refcount
- Reenable CP-23549__Update_VDI_CBT_status_on_SR_scan

* Wed Sep 27 2017 marksy <mark.syms@citrix.com> - 1.17.1-xs.1+1.16
- CP-23557: Extend ISOSR unit tests for SMB protocol
- CP-23535: Extend tap-ctl create to consdier CBT parameters
- CA-265461: Exclude source vdi whilst calculating changed blocks
- CP-22030: Unit tests for export-changed-blocks API
- CP-23547: On cbt error disable CBT and generate error for XenCenter
- CP-23405: Support calculation of changed blocks for resized VDIs
- CP-24536: Add support for CBT-specific messages to xapi and SM
- CP-24566: Change export_changed_blocks to list_changed_blocks
- CP-24593: Remove changes unrelated to CBT from patch introduced for CP-23919
- CP-24592: Resize in VDI should remain unimplemented

%package testresults
Group:    System/Hypervisor
Summary:  test results for SM package

%description testresults
The package contains the build time test results for the SM package

%files testresults
/.coverage
/coverage.xml
/htmlcov

%package test-plugins
Group:    System/Hypervisor
Summary:  System test fake key lookup plugin

%description test-plugins
The pckage contains a fake key lookup plugin for system tests

%files test-plugins
/opt/xensource/sm/plugins/keymanagerutil.py*
