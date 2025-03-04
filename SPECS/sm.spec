%global package_speccommit 6041ef4a60fa49d96a27c370aa7390f76b832bc2
%global package_srccommit v3.2.11

# -*- rpm-spec -*-

Summary: sm - XCP storage managers
Name:    sm
Version: 3.2.11
Release: 1%{?xsrel}%{?dist}
License: LGPL
URL:  https://github.com/xapi-project/sm
Source0: sm-3.2.11.tar.gz
Source1: update-cgrules.patch

%define __python python3

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pylint
BuildRequires: python3-coverage
BuildRequires: python3-bitarray

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: sm-fairlock = %{version}-%{release}
Requires: xenserver-multipath
Requires: xenserver-lvm2 >= 2.02.180-11.xs+2.0.2
Obsoletes: lvm2-sm-config <= 7:2.02.180-15.xs8
Requires: python3-bitarray
Requires(post): xs-presets >= 1.3
Requires(preun): xs-presets >= 1.3
Requires(postun): xs-presets >= 1.3
Conflicts: kernel < 4.19.19-5.0.0
Conflicts: blktap < 3.55.3
Requires: sg3_utils

%description
This package contains storage backends used in XCP

%prep
%autosetup -p1

%build
make
make -C misc/fairlock

%install
make -C misc/fairlock install DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}/
install -m 400 %SOURCE1 %{buildroot}%{_datadir}/%{name}/

# Mark processes that should be moved to the data path
%triggerin -- libcgroup-tools
# Do not apply patch if it was already applied
if ! patch --dry-run -RsN -d / -p1 < %{_datadir}/%{name}/update-cgrules.patch >/dev/null; then
    # Apply patch. Output NOT redirected to /dev/null so that error messages are displayed
    if ! patch -tsN -r - -d / -p1 < %{_datadir}/%{name}/update-cgrules.patch; then
        echo "Error: failed to apply patch:"
        cat %{_datadir}/%{name}/update-cgrules.patch
        false
    fi
fi

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
%systemd_post sr_health_check.timer
%systemd_post sr_health_check.service

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

systemctl enable sr_health_check.timer
systemctl start sr_health_check.timer

%preun
%systemd_preun make-dummy-sr.service
%systemd_preun mpcount.service
%systemd_preun sm-mpath-root.service
%systemd_preun xs-sm.service
%systemd_preun storage-init.service
%systemd_preun usb-scan.socket
%systemd_preun mpathcount.socket
%systemd_preun sr_health_check.timer
%systemd_preun sr_health_check.service
# Remove sm-multipath on upgrade or uninstall, to ensure it goes
[ ! -x /sbin/chkconfig ] || chkconfig --del sm-multipath || :
# only remove in case of erase (but not at upgrade)
if [ $1 -eq 0 ] ; then
    update-alternatives --remove multipath.conf /etc/multipath.xenserver/multipath.conf
fi
exit 0

%postun
%systemd_postun make-dummy-sr.service
%systemd_postun mpcount.service
%systemd_postun sm-mpath-root.service
%systemd_postun xs-sm.service
%systemd_postun storage-init.service
%systemd_postun sr_health_check.timer
%systemd_postun sr_health_check.service

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
/etc/xapi.d/xapi-pre-shutdown/*
/etc/xensource/master.d/02-vhdcleanup
/opt/xensource/bin/blktap2
/opt/xensource/bin/tapdisk-cache-stats
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
/opt/xensource/sm/lock_queue.py
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
/opt/xensource/sm/sr_health_check.py
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
%{_unitdir}/sr_health_check.timer
%{_unitdir}/sr_health_check.service
%{_unitdir}/SMGC@.service
%config /etc/udev/rules.d/65-multipath.rules
%config /etc/udev/rules.d/55-xs-mpath-scsidev.rules
%config /etc/udev/rules.d/58-xapi.rules
%config /etc/multipath.xenserver/multipath.conf
%dir /etc/multipath/conf.d
%config(noreplace) /etc/multipath/conf.d/custom.conf
%config /etc/udev/rules.d/69-dm-lvm-metad.rules
%config /etc/logrotate.d/SMlog
%config /etc/udev/rules.d/57-usb.rules
%doc CONTRIB LICENSE MAINTAINERS README.md
%{_datadir}/%{name}/update-cgrules.patch

%package testresults
Summary:  test results for SM package

%description testresults
The package contains the build time test results for the SM package

%files testresults
/.coverage
/coverage.xml
/htmlcov

%package test-plugins
Summary:  System test fake key lookup plugin

%description test-plugins
The package contains a fake key lookup plugin for system tests

%files test-plugins
/opt/xensource/sm/plugins/keymanagerutil.py*

%package fairlock
Summary: Fair locking subsystem

%description fairlock
This package provides the fair locking subsystem using by the Storage
Manager and some other packages

%files fairlock
%{python3_sitelib}/__pycache__/fairlock*pyc
%{python3_sitelib}/fairlock.py
%{_unitdir}/fairlock@.service
%{_libexecdir}/fairlock

%post fairlock
## On upgrade, shut down existing lock services so new ones will
## be started. There should be no locks held during upgrade operations
## so this is safe.
if [ $1 -gt 1 ];
then
    /usr/bin/systemctl list-units fairlock@* --all --no-legend | /usr/bin/cut -d' ' -f1 | while read service;
    do
        /usr/bin/systemctl stop "$service"
    done
fi

%changelog
* Tue Nov 19 2024 Mark Syms <mark.syms@cloud.com> - 3.2.11-1
- CP-42675: send messages to Xapi if GC has insufficient space
- CP-52620: enable read-through cache on persistent leaf

* Tue Nov 05 2024 Mark Syms <mark.syms@cloud.com> - 3.2.10-1
- CA-397084: SR scan tries to deactivate LV in use by tapdisk
- CA-399644: if we make progress do not abort the GC or evaluate criteria
- CA-400743: perform post snapshot rename in ioretry
- CA-401068: if iSCSI device path is not found scan the bus

* Wed Oct 09 2024 Mark Syms <mark.syms@cloud.com> - 3.2.9-3
- CP-51658: install stop gc helper script
- CA-399643 Use full paths when stopping fairlock on upgrade
- CA-396655: check xapi is enabled before starting multipath reporting
- CA-396658: check xapi is enabled before checking SR health
- CA-400106: disable leaf coalesce with VDI snapshot secondary

* Tue Sep 24 2024 Tim Smith <tim.smith@cloud.com> - 3.2.8-2
- CA-399643 Use full paths when stopping fairlock on upgrade

* Fri Sep 06 2024 Robin Newton <robin.newton@cloud.com> - 3.2.8-1
- CA-398958 Cope with concurrent read-only activations

* Wed Sep 04 2024 Mark Syms <mark.syms@cloud.com> - 3.2.7-1
- CA-398425: correctly check for multiple targets in iSCSI

* Wed Aug 21 2024 Mark Syms <mark.syms@cloud.com> - 3.2.6-1
- CA-395560: Log exception details when LUN refresh fails
- CA-396124: amend criteria under which the garbage collector aborts
- CA-397084: Log any user of LV at deactivate
- CP-51214: stop cgrules triggering errors on update

* Tue Jul 23 2024 Tim Smith <tim.smith@cloud.com> - 3.2.5-1
- CA-395554 Stop fairlock services on package upgrade

* Mon Jul 22 2024 Mark Syms <mark.syms@cloud.com> - 3.2.4-1
- Add missing sg3_utils dependency
- Update multipath config for Dell, IBM and Nimble arrays

* Thu Jul 04 2024 Mark Syms <mark.syms@cloud.com> - 3.2.3-1
- CA-393194: Fix pvremove failure

* Mon Jun 24 2024 Mark Syms <mark.syms@cloud.com> - 3.2.2-1
- CP-49689: remove reverse dependency on SR from xs_errors
- CP-49775 convert SMGC to systemd service
- CP-49720 Move LOCK_TYPE_RUNNING from cleanup.py to lock.py

* Wed May 29 2024 Mark Syms <mark.syms@cloud.com> - 3.2.1-1
- Use python3 rather than python3.6
- CA-390937: fix conflict between GC and SR detach
- CA-392989: improve diagnostics for tests

* Fri May 17 2024 Mark Syms <mark.syms@cloud.com> - 3.2.0-1
- CA-387861 Introduce fair locking subsystem
- CA-384942: use resolved CD path for error checking
- CA-392823: ensure no device mapper conflicts in LVHDSR detach

* Wed Mar 27 2024 Mark Syms <mark.syms@citrix.com> - 3.1.0-1
- CP-45750: Allow for alternative local storage SR types
- Release 3.0.13

* Tue Mar 26 2024 Mark Syms <mark.syms@citrix.com> - 3.0.13-2
- CA-388353: Fix context in cgrules patch triggerin script
- CA-379287 Cope with fs-encoded XMLRPC request on command line
- CP-383791 Fix handling of UTF-8 in srmetadata.py
- CP-45514: set ownership and permissions on backend
- CA-371791: Fix world readable permissions on EXTSR
- CA-384030 Ignore awkardly named images in ISO SRs
- CP-45927: set multipath checker for Equalogic 100E-00 to tur
- CA-377454: ensure that the iscsiadm running lock exists
- CA-384783 Probe for NFS4 when rpcinfo does not include it
- CA-253490 Add missing error codes
- CP-46807: reduce logs from scheduler set errors
- fix(NFSSR): ensure we can attach SR during attach_from_config call
- CP-39600: Rework LVM locking to use fair lock queue
- fix(ISOSR): type accepts 'nfs_iso' not 'nfs' as the docs claim
- CA-386281 CIFS username can be omitted in ISO SR
- CP-46863 Dump Multipath Status from Storage Manager
- CA-386479: ensure we login to all iSCSI Target Portal Groups
- CP-39600: remove stray print call
- CA-385069: Remove unnecessary LvmContext wrap
- CA-387770 Improve error message for readonly shares
- CA-388451: ensure that xapi sessions are logged out
- Always remove the RO/RW tag from VDIs in case of failure
- CA-387770 increase NFSSR and SMBSR test coverage
- CA-386316 Fix race condition between sr_detach and GC
- CP-47841: update multipath configuration for PURE Storage
- CA-387770: check for read-only shared fs at create
- CP-48018: Update to systemd to manage services
- CA-388933: rework GC Active lock to ensure GC starts

* Tue Sep 26 2023 Mark Syms <mark.syms@citrix.com> - 3.0.12-1
- Support IPv6 for NFS ISO SR
- CA-339581: Report NFS version incompatibilities for ISO SRs
- CA-381221: Increase NFS timeouts to the expected value

* Wed Sep 06 2023 Mark Syms <mark.syms@citrix.com> - 3.0.11-1
- CA-282738: fix bad exception thrown in mountOverSMB
- CA-372064: storage-init don't try to make Local storage if it already exists.
- CA-355289: if the SR is not plugged on GC startup wait a little while
- CP-40871: use returned sector count to calculate GC speed
- CP-40871: use VHD allocation size in checking canLiveCoalesce
- CA-379315 Use XE_SR_ERRORCODES in the LVM journaller
- Update multipath.conf with support for HP/HPE MSA storage appliances
- Fix use of vdi-ref when static vdis are used

* Tue Aug 01 2023 Mark Syms <mark.syms@citrix.com> - 3.0.10-1
- CA-379329: install and enable sr_health_check_timer

* Wed Jul 05 2023 Mark Syms <mark.syms@citrix.com> - 3.0.9-1
- FileSR: fix error code
- FileSR: get rid of unused loadLocked parameter in calls
- drivers: removed use code in .vdi() and associated loadLocked arg
- EXTSR: get rid of superfluous explicit line continuations
- CA-379434: extend wait for multipath to 30 seconds
- Support recent version of coverage tool (coverage 7.2.5)

* Wed Jun 21 2023 Mark Syms <mark.syms@citrix.com> - 3.0.8-1
- CA-374612: extend wait for multipath device arrival to 30 seconds
- CA-378768: set scheduler on multipath device

* Mon Jun 12 2023 Mark Syms <mark.syms@citrix.com> - 3.0.7-3
- Rebuild

* Thu Jun 01 2023 Mark Syms <mark.syms@citrix.com> - 3.0.7-2
- Rebuild

* Wed May 31 2023 Mark Syms <mark.syms@citrix.com> - 3.0.7-1
- Set schedulers correctly on 6.x kernel

* Thu May 18 2023 Mark Syms <mark.syms@citrix.com> - 3.0.6-3
- Rebuild

* Wed Apr 12 2023 Mark Syms <mark.syms@citrix.com> - 3.0.6-2
- Rebuild

* Wed Mar 29 2023 Mark Syms <mark.syms@citrix.com> - 3.0.6-1
- remove uninstall operations now unrelated to this package
- CA-375367 NFS timeout parameters not always set correctly
- CP-27709: filter error messages about ioctl not supported in trim
- CA-375968: multi session iSCSI updates
- Upstream changes to harmonise multipath configuration

* Tue Feb 21 2023 Mark Syms <mark.syms@citrix.com> - 3.0.4-2
- More python3 string fixes

* Mon Feb 20 2023 Mark Syms <mark.syms@citrix.com> - 3.0.4-1
- Python3 string fixes

* Fri Jan 27 2023 Mark Syms <mark.syms@citrix.com> - 3.0.3-1
- Include exportname in NBD data for attach

* Tue Jan 17 2023 Mark Syms <mark.syms@citrix.com> - 3.0.2-1
- CBT python3 fixes

* Thu Jan 12 2023 Mark Syms <mark.syms@citrix.com> - 3.0.1-1
- Check for open tapdisk NBD sockets before shutting down

* Tue Oct 25 2022  <mark.syms@citrix.com> - 3.0.0-1
- Migrate to Python3

* Wed Sep 21 2022 Tim Smith <tim.smith@citrix.com> - 2.46.16-1
- CA-370572: relinking is a transient property, do not copy to clones
- CA-370696 Do not attempt to validate device or NFS server paths

* Wed Aug 31 2022 Mark Syms <mark.syms@citrix.com> - 2.46.15-1
- CA-353437: give coalesce tracker grace iterations to make progress
- CA-353437: activate a FIST point in the coalesce tracker for test injection
- Add multipath configuration for Dell ME4

* Wed Aug 31 2022  <mark.syms@citrix.com> - 2.46.14-2
- CA-368585: Remove dependency on lvm2-sm-config

* Mon Aug 22 2022 Mark Syms <mark.syms@citrix.com> - 2.46.14-1
- CA-370037: report errors from NFS correctly

* Tue Aug 16 2022 Mark Syms <mark.syms@citrix.com> - 2.46.13-1
- Multipath fixes

* Mon Jul 25 2022 Mark Syms <mark.syms@citrix.com> - 2.46.12-1
- CA-368769: extend the timeout on tap-ctl close

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

