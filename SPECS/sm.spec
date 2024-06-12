%global package_speccommit 634fbf9dda9f0157f2fdac9867484d76b2fd9a08
%global usver 2.30.8
%global xsver 12
%global xsrel %{xsver}%{?xscount}%{?xshash}
# Series applies on top of v2.29.0 and includes all later tags to 2.30.7
# after that tag the commits are in the patchqueue here.
%global package_srccommit v2.29.0
# -*- rpm-spec -*-


Summary: sm - XCP storage managers
Name:    sm
Version: 2.30.8
Release: %{?xsrel}%{?dist}
Group:   System/Hypervisor
License: LGPL
URL:  https://github.com/xapi-project/sm
Source0: sm-2.29.0.tar.gz
Patch0: ca-343115-ensure-device
Patch1: ca-350522-backport
Patch2: ca-350871-log-if-lvhd-snapshot
Patch3: ca-350871-add-lock-context
Patch4: cp-35625-extract-calls-to
Patch5: cp-35625-use-link-instead-of
Patch6: cp-35625-extract-calls-to-1
Patch7: xsi-915-improve-performance-of
Patch8: ca-352165-check-that-device
Patch9: merge-pull-request-530-from
Patch10: ca-354228-reinstate-load-calls
Patch11: ca-355401-make-post-attach
Patch12: ca-355289-ensure-xapi-is
Patch13: ca-356645-use-self.session-is
Patch14: ca-359453-check-shared-file
Patch15: ca-359453-add-fist-fault
Patch16: ca-359453-use-rename-not-link
Patch17: cp-38316-dell-requested-that
Patch18: ca-352880-when-deleting-an-hba
Patch19: ca-369613-report-errors
Patch20: ca-369395-default-multipath
Patch21: ca-370037-don-t-lose-exception
Patch22: ca-370037-correctly-format
Patch23: added-dell-me4-multipath
Patch24: ca-370696-do-not-attempt-to
Patch25: ca-344254-add-tests-for
Patch26: ca-344254-simplify-test
Patch27: ca-353437-give-coalesce
Patch28: ca-353437-activate-a-fist
Patch29: ca-372641-fix-_expand_size-for
Patch30: ca-372772-fix-miscalculation
Patch31: ca-375968-multi-session-iscsi
Patch32: ca-379329-check-for-missing
Patch33: cp-45514-set-ownership-and
Patch34: ca-379315-use-xe_sr_errorcodes
Patch35: ca-375367-nfs-timeout
Patch36: ca-381221-increase-nfs
Patch37: cp-45927-change-equalogic
Patch38: run_unittests_directly
Patch39: ca-380360-report-error
Patch40: add-unittests-for-multisession
Patch41: ca-386479-ensure-we-login-to
Patch42: ca-387770-improve-error
Patch43: ca-388451-ensure-that-xapi
Patch44: cp-47841-update-multipath
Patch45: move_mocks_dir
Patch46: fix-nfssr-ensure-we-can-attach
Patch47: ca-387770-check-for-read-only
Patch48: ca-389576_handle_ioerror
BuildRequires: python-devel xen-devel systemd pylint python-nose python-coverage python2-mock python2-bitarray
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: xenserver-multipath
Requires: xenserver-lvm2 >= 2.02.180-11.xs+2.0.2
Requires: python2-bitarray
Requires(post): xs-presets >= 1.3
Requires(preun): xs-presets >= 1.3
Requires(postun): xs-presets >= 1.3
Conflicts: kernel < 4.19.19-5.0.0

%description
This package contains storage backends used in XCP

%prep
%autosetup -p1

%build
DESTDIR=$RPM_BUILD_ROOT make

%install
DESTDIR=$RPM_BUILD_ROOT make install

%clean
rm -rf $RPM_BUILD_ROOT

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
if [ $1 -eq 0 ]; then
    [ ! -d /etc/lvm/master ] || rm -Rf /etc/lvm/master || exit $?
    cp -f /etc/lvm/lvm.conf.orig /etc/lvm/lvm.conf || exit $?
elif [ $1 -eq 1 ]; then
    true;
fi

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
/opt/xensource/sm/DummySR.pyc
/opt/xensource/sm/DummySR.pyo
/opt/xensource/sm/EXTSR
/opt/xensource/sm/EXTSR.py
/opt/xensource/sm/EXTSR.pyc
/opt/xensource/sm/EXTSR.pyo
/opt/xensource/sm/FileSR
/opt/xensource/sm/FileSR.py
/opt/xensource/sm/FileSR.pyc
/opt/xensource/sm/FileSR.pyo
/opt/xensource/sm/HBASR
/opt/xensource/sm/HBASR.py
/opt/xensource/sm/HBASR.pyc
/opt/xensource/sm/HBASR.pyo
/opt/xensource/sm/ISCSISR
/opt/xensource/sm/RawISCSISR.py
/opt/xensource/sm/RawISCSISR.pyc
/opt/xensource/sm/RawISCSISR.pyo
/opt/xensource/sm/BaseISCSI.py
/opt/xensource/sm/BaseISCSI.pyc
/opt/xensource/sm/BaseISCSI.pyo
/opt/xensource/sm/ISOSR
/opt/xensource/sm/ISOSR.py
/opt/xensource/sm/ISOSR.pyc
/opt/xensource/sm/ISOSR.pyo
/opt/xensource/sm/OCFSSR.py
/opt/xensource/sm/OCFSSR.pyc
/opt/xensource/sm/OCFSSR.pyo
/opt/xensource/sm/OCFSoISCSISR.py
/opt/xensource/sm/OCFSoISCSISR.pyc
/opt/xensource/sm/OCFSoISCSISR.pyo
/opt/xensource/sm/OCFSoHBASR.py
/opt/xensource/sm/OCFSoHBASR.pyc
/opt/xensource/sm/OCFSoHBASR.pyo
/opt/xensource/sm/LUNperVDI.py
/opt/xensource/sm/LUNperVDI.pyc
/opt/xensource/sm/LUNperVDI.pyo
/opt/xensource/sm/LVHDSR.py
/opt/xensource/sm/LVHDSR.pyc
/opt/xensource/sm/LVHDSR.pyo
/opt/xensource/sm/LVHDoHBASR.py
/opt/xensource/sm/LVHDoHBASR.pyc
/opt/xensource/sm/LVHDoHBASR.pyo
/opt/xensource/sm/LVHDoISCSISR.py
/opt/xensource/sm/LVHDoISCSISR.pyc
/opt/xensource/sm/LVHDoISCSISR.pyo
/opt/xensource/sm/LVHDoFCoESR.py
/opt/xensource/sm/LVHDoFCoESR.pyc
/opt/xensource/sm/LVHDoFCoESR.pyo
/opt/xensource/sm/LVMSR
/opt/xensource/sm/LVMoHBASR
/opt/xensource/sm/LVMoISCSISR
/opt/xensource/sm/LVMoFCoESR
/opt/xensource/sm/NFSSR
/opt/xensource/sm/NFSSR.py
/opt/xensource/sm/NFSSR.pyc
/opt/xensource/sm/NFSSR.pyo
/opt/xensource/sm/SMBSR
/opt/xensource/sm/SMBSR.py
/opt/xensource/sm/SMBSR.pyc
/opt/xensource/sm/SMBSR.pyo
/opt/xensource/sm/SHMSR.py
/opt/xensource/sm/SHMSR.pyc
/opt/xensource/sm/SHMSR.pyo
/opt/xensource/sm/SR.py
/opt/xensource/sm/SR.pyc
/opt/xensource/sm/SR.pyo
/opt/xensource/sm/SRCommand.py
/opt/xensource/sm/SRCommand.pyc
/opt/xensource/sm/SRCommand.pyo
/opt/xensource/sm/VDI.py
/opt/xensource/sm/VDI.pyc
/opt/xensource/sm/VDI.pyo
/opt/xensource/sm/XE_SR_ERRORCODES.xml
/opt/xensource/sm/blktap2.py
/opt/xensource/sm/blktap2.pyc
/opt/xensource/sm/blktap2.pyo
/opt/xensource/sm/cleanup.py
/opt/xensource/sm/cleanup.pyc
/opt/xensource/sm/cleanup.pyo
/opt/xensource/sm/devscan.py
/opt/xensource/sm/devscan.pyc
/opt/xensource/sm/devscan.pyo
/opt/xensource/sm/fjournaler.py
/opt/xensource/sm/fjournaler.pyc
/opt/xensource/sm/fjournaler.pyo
/opt/xensource/sm/flock.py
/opt/xensource/sm/flock.pyc
/opt/xensource/sm/flock.pyo
/opt/xensource/sm/ipc.py
/opt/xensource/sm/ipc.pyc
/opt/xensource/sm/ipc.pyo
/opt/xensource/sm/iscsilib.py
/opt/xensource/sm/iscsilib.pyc
/opt/xensource/sm/iscsilib.pyo
/opt/xensource/sm/fcoelib.py
/opt/xensource/sm/fcoelib.pyc
/opt/xensource/sm/fcoelib.pyo
/opt/xensource/sm/journaler.py
/opt/xensource/sm/journaler.pyc
/opt/xensource/sm/journaler.pyo
/opt/xensource/sm/lcache.py
/opt/xensource/sm/lcache.pyc
/opt/xensource/sm/lcache.pyo
/opt/xensource/sm/lock.py
/opt/xensource/sm/lock.pyc
/opt/xensource/sm/lock.pyo
/opt/xensource/sm/lvhdutil.py
/opt/xensource/sm/lvhdutil.pyc
/opt/xensource/sm/lvhdutil.pyo
/opt/xensource/sm/lvmanager.py
/opt/xensource/sm/lvmanager.pyc
/opt/xensource/sm/lvmanager.pyo
/opt/xensource/sm/lvmcache.py
/opt/xensource/sm/lvmcache.pyc
/opt/xensource/sm/lvmcache.pyo
/opt/xensource/sm/lvutil.py
/opt/xensource/sm/lvutil.pyc
/opt/xensource/sm/lvutil.pyo
/opt/xensource/sm/metadata.py
/opt/xensource/sm/metadata.pyc
/opt/xensource/sm/metadata.pyo
/opt/xensource/sm/srmetadata.py
/opt/xensource/sm/srmetadata.pyc
/opt/xensource/sm/srmetadata.pyo
/opt/xensource/sm/mpath_cli.py
/opt/xensource/sm/mpath_cli.pyc
/opt/xensource/sm/mpath_cli.pyo
/opt/xensource/sm/mpath_dmp.py
/opt/xensource/sm/mpath_dmp.pyc
/opt/xensource/sm/mpath_dmp.pyo
/opt/xensource/sm/mpath_null.py
/opt/xensource/sm/mpath_null.pyc
/opt/xensource/sm/mpath_null.pyo
/opt/xensource/sm/mpathcount.py
/opt/xensource/sm/mpathcount.pyc
/opt/xensource/sm/mpathcount.pyo
/opt/xensource/sm/mpathutil.py
/opt/xensource/sm/mpathutil.pyc
/opt/xensource/sm/mpathutil.pyo
/opt/xensource/sm/mpp_mpathutil.py
/opt/xensource/sm/mpp_mpathutil.pyc
/opt/xensource/sm/mpp_mpathutil.pyo
/opt/xensource/sm/nfs.py
/opt/xensource/sm/nfs.pyc
/opt/xensource/sm/nfs.pyo
/opt/xensource/sm/refcounter.py
/opt/xensource/sm/refcounter.pyc
/opt/xensource/sm/refcounter.pyo
/opt/xensource/sm/resetvdis.py
/opt/xensource/sm/resetvdis.pyc
/opt/xensource/sm/resetvdis.pyo
/opt/xensource/sm/scsiutil.py
/opt/xensource/sm/scsiutil.pyc
/opt/xensource/sm/scsiutil.pyo
/opt/xensource/sm/scsi_host_rescan.py
/opt/xensource/sm/scsi_host_rescan.pyc
/opt/xensource/sm/scsi_host_rescan.pyo
/opt/xensource/sm/sysdevice.py
/opt/xensource/sm/sysdevice.pyc
/opt/xensource/sm/sysdevice.pyo
/opt/xensource/sm/udevSR
/opt/xensource/sm/udevSR.py
/opt/xensource/sm/udevSR.pyc
/opt/xensource/sm/udevSR.pyo
/opt/xensource/sm/util.py
/opt/xensource/sm/util.pyc
/opt/xensource/sm/util.pyo
/opt/xensource/sm/cifutils.py
/opt/xensource/sm/cifutils.pyc
/opt/xensource/sm/cifutils.pyo
/opt/xensource/sm/verifyVHDsOnSR.py
/opt/xensource/sm/verifyVHDsOnSR.pyc
/opt/xensource/sm/verifyVHDsOnSR.pyo
/opt/xensource/sm/vhdutil.py
/opt/xensource/sm/vhdutil.pyc
/opt/xensource/sm/vhdutil.pyo
/opt/xensource/sm/trim_util.py
/opt/xensource/sm/trim_util.pyc
/opt/xensource/sm/trim_util.pyo
/opt/xensource/sm/xs_errors.py
/opt/xensource/sm/xs_errors.pyc
/opt/xensource/sm/xs_errors.pyo
/opt/xensource/sm/wwid_conf.py
/opt/xensource/sm/wwid_conf.pyc
/opt/xensource/sm/wwid_conf.pyo
/opt/xensource/sm/pluginutil.py
/opt/xensource/sm/pluginutil.pyc
/opt/xensource/sm/pluginutil.pyo
/opt/xensource/sm/constants.py
/opt/xensource/sm/constants.pyc
/opt/xensource/sm/constants.pyo
/opt/xensource/sm/cbtutil.py
/opt/xensource/sm/cbtutil.pyc
/opt/xensource/sm/cbtutil.pyo
/opt/xensource/sm/multipath-root-setup
/opt/xensource/sm/sr_health_check.py
/opt/xensource/sm/sr_health_check.pyc
/opt/xensource/sm/sr_health_check.pyo
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
%config /etc/udev/rules.d/65-multipath.rules
%config /etc/udev/rules.d/55-xs-mpath-scsidev.rules
%config /etc/udev/rules.d/58-xapi.rules
%config /etc/multipath.xenserver/multipath.conf
%config /etc/udev/rules.d/69-dm-lvm-metad.rules
%config /etc/logrotate.d/SMlog
%config /etc/udev/rules.d/57-usb.rules
%doc CONTRIB LICENSE MAINTAINERS README.md

%changelog
* Wed Mar 13 2024 Mark Syms <mark.syms@citrix.com> - 2.30.8-12
- CA-389576: in Python 2.7 IOError is not a subclass of OSError

* Mon Feb 26 2024 Mark Syms <mark.syms@citrix.com> - 2.30.8-11
- CA-387770 Improve error message for readonly shares
- CA-388451: Ensure that xapi sessions are logged out
- CP-47841: update multipath confiugration for PURE FlashArray
- Backport fix for NFS attach from config
- CA-387770: Backport Check for R/O FS at create

* Fri Jan 19 2024 Mark Syms <mark.syms@citrix.com> - 2.30.8-10
- Backport fix for CA-386479, log into all iSCSI targets

* Fri Oct 27 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-9
- Backport fix for CP-45927, set Equalogic path checker

* Thu Oct 19 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-8
- Backport fix for CA-375367
- Backport fix for CA-379315
- Backport fix for CA-381221

* Thu Sep 28 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-7
- CP-45514: set ownership and perms on backeend device

* Fri Aug 04 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-6
- Fixes for CA-379329, monitor for missing iSCSI sessions

* Fri Jun 30 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-5
- CA-375968: multi session iSCSI updates

* Fri Jun 30 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-4
- Rebuild

* Mon Jun 26 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-3
- Backport fix for CA-378768

* Wed Nov 23 2022 Mark Syms <mark.syms@citrix.com> - 2.30.8-2
- CA-353437: give coalesce tracker grace iterations to make progress
- CA-372641: fix _expand_size for multipath
- CA-372772: fix miscalculation of seek offset

* Fri Sep 23 2022 Tim Smith <tim.smith@citrix.com> - 2.30.8-1
- CA-369613: report errors correctly from multipath
- CA-369395: default multipath handle to dmp if not set
- CA-370037: improvements to exception handling
- Added Dell ME4 multipath config
- CA-370696 Do not attempt to validate device or NFS server paths

* Fri Apr 29 2022 Mark Syms <mark.syms@citrix.com> - 2.30.7-1
- CA-352880: when deleting an HBA SR remove the kernel devices

* Fri Oct 22 2021 Mark Syms <mark.syms@citrix.com> - 2.30.6-1
- CA-359453: use rename not link if links not supported
- CP-38316: update path checker for Equalogic at vendors request

* Thu Oct  7 2021 Mark Syms <mark.syms@citrix.com> - 2.30.5-1
- CA-355401: make post attach scan best effort and report errors
- CA-355289: ensure xapi is initialised before starting GC
- CA-356645: use "self.session is None" not "self.session == None"

* Wed May 19 2021 Mark Syms <mark.syms@citrix.com> - 2.30.4-1
- CA-354228: Reinstate load calls in _pathrefresh

* Fri Mar 26 2021 Ben Sims <ben.sims@citrix.com> - 2.30.3-1
- CA-349759: don't call srUpdate within a lock
- CA-352165: Check that 'device' exists in the dconf before using it
- XSI-915: Improve performance of LVHDoHBA
- CP-35625: Extract calls to unlink to helper and log
- CP-35625: use link instead of rename to improve crash consistency
- CP-35625: Extract calls to rename into helper and log.
- CA-350871: Add lock context manager for LVM operations to allow for
  higher level controlDon't take locks for readonly operations
- CA-350871: Log if LVHD snapshot pauses VM for more than 60secs
- CA-350437: simplify 02vhd-cleanup to only handle LVM refcounts

* Wed Sep 30 2020 Tim Smith <tim.smith@citrix.com> - 2.29.1-1
- CA-343115: ensure device symlinks are created correctly even when path count
  not required

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


%package rawhba
Group:   System/Hypervisor
Summary: rawhba SR type capability
#Requires: sm = @SM_VERSION@-@SM_RELEASE@

%description rawhba
This package adds a new rawhba SR type. This SR type allows utilization of
Fiber Channel raw LUNs as separate VDIs (LUN per VDI)

%files rawhba
/opt/xensource/sm/RawHBASR.py
%exclude /opt/xensource/sm/RawHBASR
/opt/xensource/sm/RawHBASR.pyc
/opt/xensource/sm/RawHBASR.pyo
/opt/xensource/sm/B_util.py
/opt/xensource/sm/B_util.pyc
/opt/xensource/sm/B_util.pyo
/opt/xensource/sm/enable-borehamwood

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
