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
Release: %{?xsrel}.1.0.linstor.3%{?dist}
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
BuildRequires: gcc
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: xenserver-multipath
Requires(post): xenserver-multipath
Requires: xenserver-lvm2 >= 2.02.180-11.xs+2.0.2
Requires: python2-bitarray
Requires(post): xs-presets >= 1.3
Requires(preun): xs-presets >= 1.3
Requires(postun): xs-presets >= 1.3
Conflicts: kernel < 4.19.19-5.0.0

Obsoletes: sm-additional-drivers

# To remove after stable release of LINSTOR.
Provides: sm-linstor

# XCP-ng patches
# Generated from our sm repository
# git format-patch v2.30.8-12-xcpng..2.30.8-8.2
# Note: the v2.30.8-12-xcpng tag was manually created by us on our fork because
# the upstream sm doesn't provide maintenance updates anymore
# To create this tag in the sources, you must create a 2.30.8-8.2 branch from the
# previous -xcpng tag then cherry pick each upstream commit referenced in the changelog
# of the upstream spec file.
# To ensure you have all changes, you can use:
# `diff -urq <sources> <upstream sources>`.
# After that we can create the tag: `git tag -a v2.30.8-12-xcpng -m "v2.30.8-12-xcpng"`,
# push the commits and tag.
Patch1001: 0001-backport-of-ccd121cc248d79b749a63d4ad099e6d5f4b8b588.patch
Patch1002: 0002-Update-xs-sm.service-s-description-for-XCP-ng.patch
Patch1003: 0003-Add-TrueNAS-multipath-config.patch
Patch1004: 0004-feat-drivers-add-CephFS-GlusterFS-and-XFS-drivers.patch
Patch1005: 0005-feat-drivers-add-ZFS-driver-to-avoid-losing-VDI-meta.patch
Patch1006: 0006-Re-add-the-ext4-driver-for-users-who-need-to-transit.patch
Patch1007: 0007-feat-drivers-add-LinstorSR-driver.patch
Patch1008: 0008-feat-tests-add-unit-tests-concerning-ZFS-close-xcp-n.patch
Patch1009: 0009-If-no-NFS-ACLs-provided-assume-everyone.patch
Patch1010: 0010-Added-SM-Driver-for-MooseFS.patch
Patch1011: 0011-Avoid-usage-of-umount-in-ISOSR-when-legacy_mode-is-u.patch
Patch1012: 0012-MooseFS-SR-uses-now-UUID-subdirs-for-each-SR.patch
Patch1013: 0013-Fix-is_open-call-for-many-drivers-25.patch
Patch1014: 0014-Remove-SR_CACHING-capability-for-many-SR-types-24.patch
Patch1015: 0015-Remove-SR_PROBE-from-ZFS-capabilities-37.patch
Patch1016: 0016-Fix-vdi-ref-when-static-vdis-are-used.patch
Patch1017: 0017-Tell-users-not-to-edit-multipath.conf-directly.patch
Patch1018: 0018-Add-custom.conf-multipath-configuration-file.patch
Patch1019: 0019-Install-etc-multipath-conf.d-custom.conf.patch
Patch1020: 0020-Backport-NFS4-only-support.patch
Patch1021: 0021-Backport-probe-for-NFS4-when-rpcinfo-does-not-includ.patch
Patch1022: 0022-feat-LargeBlock-backport-of-largeblocksr-51-55.patch
Patch1023: 0023-feat-LVHDSR-add-a-way-to-modify-config-of-LVMs-56.patch
Patch1024: 0024-Fix-timeout_call-alarm-must-be-reset-in-case-of-succ.patch
Patch1025: 0025-timeout_call-returns-the-result-of-user-function-now.patch
Patch1026: 0026-Always-remove-the-pause-tag-from-VDIs-in-case-of-fai.patch
Patch1027: 0027-fix-LinstorSR-repair-volumes-only-if-an-exclusive-co.patch
Patch1028: 0028-feat-LinstorSR-Improve-LINSTOR-performance.patch
Patch1029: 0029-feat-LinstorSR-robustify-scan-to-avoid-losing-VDIs-i.patch
Patch1030: 0030-feat-LinstorSR-display-a-correctly-readable-size-for.patch
Patch1031: 0031-feat-linstor-monitord-scan-all-LINSTOR-SRs-every-12-.patch
Patch1032: 0032-fix-LinstorSR-call-correctly-method-in-_locked_load-.patch
Patch1033: 0033-feat-LinstorSR-integrate-minidrbdcluster-daemon.patch
Patch1034: 0034-feat-LinstorSR-ensure-heartbeat-and-redo_log-VDIs-ar.patch
Patch1035: 0035-feat-LinstorSR-protect-sr-commands-to-avoid-forgetti.patch
Patch1036: 0036-fix-LinstorJournaler-ensure-uri-is-not-None-during-l.patch
Patch1037: 0037-feat-LinstorSR-add-an-option-to-disable-auto-quorum-.patch
Patch1038: 0038-fix-LinstorVolumeManager-add-a-workaround-to-create-.patch
Patch1039: 0039-feat-LinstorSR-add-optional-ips-parameter.patch
Patch1040: 0040-feat-LinstorSR-add-a-helper-log_drbd_erofs-to-trace-.patch
Patch1041: 0041-fix-LinstorSR-try-to-restart-the-services-again-if-t.patch
Patch1042: 0042-fix-LinstorSR-robustify-linstor-manager-to-never-inc.patch
Patch1043: 0043-fix-LinstorSR-prevent-starting-controller-during-fai.patch
Patch1044: 0044-feat-LinstorVolumeManager-increase-peer-slots-limit-.patch
Patch1045: 0045-feat-LinstorVolumeManager-add-a-fallback-to-find-con.patch
Patch1046: 0046-fix-var-lib-linstor.mount-ensure-we-always-mount-dat.patch
Patch1047: 0047-feat-LinstorVolumeManager-add-a-fallback-to-find-nod.patch
Patch1048: 0048-feat-LinstorSR-explain-on-which-host-plugins-command.patch
Patch1049: 0049-fix-LinstorSR-create-diskless-path-if-necessary-duri.patch
Patch1050: 0050-feat-LinstorSR-use-HTTP-NBD-instead-of-DRBD-directly.patch
Patch1051: 0051-fix-LinstorSR-find-controller-when-XAPI-unreachable-.patch
Patch1052: 0052-fix-LinstorSR-use-IPs-instead-of-hostnames-in-NBD-se.patch
Patch1053: 0053-fix-LinstorVolumeManager-ensure-we-always-use-IPs-in.patch
Patch1054: 0054-feat-linstor-manager-add-methods-to-add-remove-host-.patch
Patch1055: 0055-feat-LinstorVolumeManager-support-SR-creation-with-d.patch
Patch1056: 0056-feat-LinstorSR-add-a-config-var-to-disable-HTTP-NBD-.patch
Patch1057: 0057-feat-LinstorSr-ensure-LVM-group-is-activated-during-.patch
Patch1058: 0058-feat-linstor-manager-add-method-to-create-LinstorSR-.patch
Patch1059: 0059-fix-LinstorSR-always-set-vdi_path-in-generate_config.patch
Patch1060: 0060-fix-minidrbdcluster-supports-new-properties-like-for.patch
Patch1061: 0061-fix-LinstorSR-enabled-disable-minidrbcluster-with-fi.patch
Patch1062: 0062-fix-linstor-manager-change-linstor-satellite-start-b.patch
Patch1063: 0063-Fix-is_open-call-for-LinstorSR.patch
Patch1064: 0064-fix-linstorvhdutil-fix-boolean-params-of-check-call.patch
Patch1065: 0065-feat-linstor-manager-robustify-exec_create_sr.patch
Patch1066: 0066-fix-cleanup-print-LINSTOR-VDI-UUID-if-error-during-i.patch
Patch1067: 0067-feat-cleanup-raise-and-dump-DRBD-openers-in-case-of-.patch
Patch1068: 0068-feat-linstorvhdutil-trace-DRBD-openers-in-case-of-ER.patch
Patch1069: 0069-fix-linstorvolumemanager-compute-correctly-size-in-a.patch
Patch1070: 0070-feat-LinstorSR-use-DRBD-openers-instead-of-lsof-to-l.patch
Patch1071: 0071-feat-LinstorSR-support-cProfile-to-trace-calls-when-.patch
Patch1072: 0072-fix-LinstorJournaler-reset-namespace-when-get-is-cal.patch
Patch1073: 0073-fix-linstorvhdutil-fix-coalesce-with-VM-running-unde.patch
Patch1074: 0074-fix-linstorvolumemanager-_get_volumes_info-doesn-t-r.patch
Patch1075: 0075-fix-linstorvolumemanager-remove-double-prefix-on-kv-.patch
Patch1076: 0076-feat-LinstorSR-add-linstor-kv-dump-helper-to-print-k.patch
Patch1077: 0077-fix-LinstorSR-disable-VHD-key-hash-usage-to-limit-ex.patch
Patch1078: 0078-fix-minidrbdcluster-ensure-SIGINT-is-handled-correct.patch
Patch1079: 0079-feat-minidrbdcluster-stop-resource-services-at-start.patch
Patch1080: 0080-feat-linstor-manager-add-new-healthCheck-function-to.patch
Patch1081: 0081-fix-LinstorSR-fix-xha-conf-parsing-return-host-ip-no.patch
Patch1082: 0082-fix-LinstorSR-start-correctly-HA-servers-HTTP-NBD-af.patch
Patch1083: 0083-fix-linstorvolumemanager-use-an-array-to-store-diskf.patch
Patch1084: 0084-feat-linstorvolumemanager-support-snaps-when-a-host-.patch
Patch1085: 0085-fix-linstorvolumemanager-support-offline-hosts-when-.patch
Patch1086: 0086-fix-linstorvolumemanager-define-_base_group_name-mem.patch
Patch1087: 0087-feat-linstorvhdutil-modify-logic-of-local-vhdutil-ca.patch
Patch1088: 0088-fix-linstorvolumemanager-robustify-failed-snapshots.patch
Patch1089: 0089-fix-linstorvolumemanager-use-a-namespace-for-volumes.patch
Patch1090: 0090-feat-linstor-kv-dump-rename-to-linstor-kv-tool-add-r.patch
Patch1091: 0091-fix-LinstorSR-handle-correctly-localhost-during-star.patch
Patch1092: 0092-fix-cleanup.py-call-repair-on-another-host-when-EROF.patch
Patch1093: 0093-fix-LinstorSR-avoid-introduction-of-DELETED-volumes.patch
Patch1094: 0094-feat-linstor-kv-tool-remove-all-volumes-supports-jou.patch
Patch1095: 0095-fix-linstorvhdutil-due-to-bad-refactoring-check-call.patch
Patch1096: 0096-feat-linstorvhdutil-ensure-we-use-VHD-parent-to-find.patch
Patch1097: 0097-feat-linstorvolumemanager-force-DRBD-demote-after-fa.patch
Patch1098: 0098-fix-linstorvhdutil-ensure-we-retry-creation-in-all-s.patch
Patch1099: 0099-fix-linstorvhdutil-don-t-retry-local-vhdutil-call-wh.patch
Patch1100: 0100-feat-fork-log-daemon-ignore-SIGTERM.patch
Patch1101: 0101-feat-LinstorSR-wait-for-http-disk-server-startup.patch
Patch1102: 0102-fix-LinstorSR-handle-inflate-resize-actions-correctl.patch
Patch1103: 0103-fix-linstor-manager-add-a-static-iptables-rule-for-D.patch
Patch1104: 0104-feat-LinstorSR-sync-with-last-http-nbd-transfer-vers.patch
Patch1105: 0105-fix-LinstorSR-don-t-check-VDI-metadata-while-listing.patch
Patch1106: 0106-fix-LinstorSR-don-t-check-metadata-when-destroying-s.patch
Patch1107: 0107-fix-linstorvhdutil-handle-correctly-generic-exceptio.patch
Patch1108: 0108-fix-minidrbdcluster-robustify-to-unmount-correctly-L.patch
Patch1109: 0109-fix-minidrbdcluster-handle-correctly-KeyboardInterru.patch
Patch1110: 0110-feat-LinstorSR-use-drbd-reactor-instead-of-minidrbdc.patch
Patch1111: 0111-fix-LinstorSR-ensure-vhdutil-calls-are-correctly-exe.patch
Patch1112: 0112-fix-LinstorSR-replace-bad-param-in-detach_thin-impl.patch
Patch1113: 0113-fix-linstorvolumemanager-remove-usage-of-realpath.patch
Patch1114: 0114-fix-linstorvhdutil-avoid-parent-path-resolution.patch
Patch1115: 0115-fix-LinstorSR-create-parent-path-during-attach.patch
Patch1116: 0116-fix-LinstorSR-retry-if-we-can-t-build-volume-cache.patch
Patch1117: 0117-fix-linstorvolumemanager-reduce-peer-slots-param-to-.patch
Patch1118: 0118-fix-LinstorSR-attach-a-valid-XAPI-session-is_open-is.patch
Patch1119: 0119-fix-LinstorSR-ensure-we-always-have-a-DRBD-path-to-s.patch
Patch1120: 0120-fix-LinstorSR-remove-hosts-ips-param.patch
Patch1121: 0121-fix-LinstorSR-compute-correctly-SR-size-using-pool-c.patch
Patch1122: 0122-fix-blktap2-ensure-we-can-import-this-module-when-LI.patch
Patch1123: 0123-fix-LinstorSR-ensure-volume-cache-can-be-recreated.patch
Patch1124: 0124-fix-linstor-manager-remove-dead-useless-code-in-add-.patch
Patch1125: 0125-fix-LinstorSR-Ensure-we-always-have-a-device-path-du.patch
Patch1126: 0126-fix-LinstorSR-always-use-lock.acquire-during-attach-.patch
Patch1127: 0127-fix-LinstorSR-mare-sure-hostnames-are-unique-at-SR-c.patch
Patch1128: 0128-fix-LinstorSR-ensure-we-can-attach-non-special-stati.patch
Patch1129: 0129-fix-LinstorSR-ensure-we-can-detach-when-deflate-call.patch
Patch1130: 0130-fix-LinstorSR-assume-VDI-is-always-a-VHD-when-the-in.patch
Patch1131: 0131-fix-LinstorSR-remove-SR-lock-during-thin-attach-deta.patch
Patch1132: 0132-fix-LinstorSR-ensure-database-is-mounted-during-scan.patch
Patch1133: 0133-fix-LinstorSR-restart-drbd-reactor-in-case-of-failur.patch
Patch1134: 0134-fix-linstorvolumemanager-retry-in-case-of-failure-du.patch
Patch1135: 0135-fix-linstorvolumemanager-avoid-diskless-creation-whe.patch
Patch1136: 0136-fix-LinstorSR-remove-diskless-after-VDI.detach-calls.patch
Patch1137: 0137-fix-LinstorSR-robustify-_load_vdi_info-in-cleanup.py.patch
Patch1138: 0138-fix-LinstorSR-ensure-detach-never-fails-on-plugin-fa.patch
Patch1139: 0139-fix-LinstorSR-ensure-we-coalesce-only-volumes-with-a.patch
Patch1140: 0140-fix-LinstorSR-don-t-try-to-repair-persistent-volumes.patch
Patch1141: 0141-fix-linstorvhdutil-format-correctly-message-if-vhd-u.patch
Patch1142: 0142-fix-LinstorSR-wait-during-attach-to-open-DRBD-path.patch
Patch1143: 0143-fix-LinstorSR-support-different-volume-sizes-in-clea.patch
Patch1144: 0144-fix-LinstorSR-remove-useless-IPS_XHA_CACHE-var.patch
Patch1145: 0145-fix-LinstorSR-ensure-we-can-deflate-on-any-host-afte.patch
Patch1146: 0146-fix-LinstorSR-ensure-we-always-use-real-DRBD-VHD-siz.patch
Patch1147: 0147-feat-linstor-kv-tool-If-no-controller-uri-option-is-.patch
Patch1148: 0148-fix-linstorvolumemanager-robustify-SR-destroy-46.patch
Patch1149: 0149-feat-linstor-manager-extend-API-with-createNodeInter.patch
Patch1150: 0150-fix-LinstorSR-support-VDI.resize-on-thick-volumes.patch
Patch1151: 0151-fix-linstorvolumemanager-format-correctly-exception-.patch
Patch1152: 0152-fix-LinstorSR-ensure-we-can-skip-coalesces-if-device.patch
Patch1153: 0153-feat-linstor-manager-add-methods-to-modify-destroy-l.patch
Patch1154: 0154-fix-LinstorSR-force-a-defined-volume-prefix-if-we-ca.patch
Patch1155: 0155-fix-LinstorSR-explicit-error-message-when-a-group-is.patch
Patch1156: 0156-fix-LinstorSR-make-sure-VDI.delete-doesn-t-throw-und.patch
Patch1157: 0157-fix-LinstorSR-add-drbd-in-the-blacklist-of-multipath.patch
Patch1158: 0158-fix-linstorvolumemanager-create-cloned-volumes-on-ho.patch
Patch1159: 0159-fix-linstorvolumemanager-don-t-align-volumes-on-LVM-.patch
Patch1160: 0160-fix-linstorvolumemanager-assert-with-message-after-l.patch
Patch1161: 0161-fix-linstorvolumemanager-retry-resize-if-volume-is-n.patch
Patch1162: 0162-fix-LinstorSR-create-DRBD-diskless-if-necessary-for-.patch
Patch1163: 0163-fix-LinstorSR-fix-bad-call-to-vhdutil.inflate-bad-ex.patch
Patch1164: 0164-fix-LinstorSR-activate-VG-if-attach-from-config-is-a.patch
Patch1165: 0165-feat-LinstorSR-use-a-specific-resource-group-for-DB-.patch
Patch1166: 0166-feat-linstor-manager-add-getNodePreferredInterface-h.patch
Patch1167: 0167-fix-linstorvolumemanager-blocks-deletion-of-default-.patch
Patch1168: 0168-feat-linstorvolumemanager-change-logic-of-get_resour.patch
Patch1169: 0169-feat-linstor-manager-add-error-codes-to-healthCheck-.patch
Patch1170: 0170-fix-LinstorSR-fix-bad-exception-reference-during-sna.patch
Patch1171: 0171-fix-tapdisk-pause-ensure-LINSTOR-VHD-chain-is-availa.patch
Patch1172: 0172-fix-LVHDoISCSISR-disable-restart-of-ISCSI-daemon.patch
Patch1173: 0173-fix-linstorvhdutil-retry-check-on-another-machine-in.patch
Patch1174: 0174-fix-LinstorSR-explicit-errors-when-database-path-is-.patch
Patch1175: 0175-fix-LinstorSR-Misc-fixes-on-destroy.patch
Patch1176: 0176-fix-LinstorSR-open-non-leaf-volumes-in-RO-mode-creat.patch

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

# XCP-ng: enable linstor-monitor by default.
# However it won't start without linstor-controller.service
systemctl enable linstor-monitor.service

# XCP-ng: We must reload the multipathd configuration without restarting the service to prevent
# the opening of /dev/drbdXXXX volumes. Otherwise if multipathd opens a DRBD volume,
# it blocks its access to other hosts.
# This command is also important if our multipath conf is modified for other drivers.
if [ $1 -gt 1 ]; then
    multipathd reconfigure
fi

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

# XCP-ng
%systemd_preun linstor-monitor.service

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

# XCP-ng
%systemd_postun linstor-monitor.service

%check
tests/run_python_unittests.sh
cp .coverage %{buildroot}
cp coverage.xml %{buildroot}
cp -r htmlcov %{buildroot}/htmlcov

%files
%defattr(-,root,root,-)
/etc/systemd/system/drbd-reactor.service.d/override.conf
/etc/systemd/system/linstor-satellite.service.d/override.conf
/etc/systemd/system/var-lib-linstor.service
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
/opt/xensource/bin/linstor-kv-tool
/opt/xensource/bin/tapdisk-cache-stats
/opt/xensource/bin/xe-getarrayidentifier
/opt/xensource/bin/xe-get-arrayid-lunnum
/opt/xensource/bin/xe-getlunidentifier
/opt/xensource/debug/tp
/opt/xensource/libexec/check-device-sharing
/opt/xensource/libexec/dcopy
/opt/xensource/libexec/local-device-change
/opt/xensource/libexec/make-dummy-sr
/opt/xensource/libexec/safe-umount
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
# XCP-ng: we don't replace this file if it has local modifications
# Doing so may break production for very little benefit:
# If there are changes, this means they need them, and anything
# we may add to the file is likely to be irrelevant for their setup.
%config(noreplace) /etc/multipath.xenserver/multipath.conf
# XCP-ng: Add directory and file for custom multipath config.
%dir /etc/multipath/conf.d
%config(noreplace) /etc/multipath/conf.d/custom.conf
%config /etc/udev/rules.d/69-dm-lvm-metad.rules
%config /etc/logrotate.d/SMlog
%config /etc/udev/rules.d/57-usb.rules
%doc CONTRIB LICENSE MAINTAINERS README.md
# XCP-ng
/etc/xapi.d/plugins/linstor-manager
/opt/xensource/sm/CephFSSR
/opt/xensource/sm/CephFSSR.py
/opt/xensource/sm/CephFSSR.pyc
/opt/xensource/sm/CephFSSR.pyo
/opt/xensource/sm/EXT4SR
/opt/xensource/sm/EXT4SR.py
/opt/xensource/sm/EXT4SR.pyc
/opt/xensource/sm/EXT4SR.pyo
/opt/xensource/sm/GlusterFSSR
/opt/xensource/sm/GlusterFSSR.py
/opt/xensource/sm/GlusterFSSR.pyc
/opt/xensource/sm/GlusterFSSR.pyo
/opt/xensource/sm/LargeBlockSR
/opt/xensource/sm/LargeBlockSR.py
/opt/xensource/sm/LargeBlockSR.pyc
/opt/xensource/sm/LargeBlockSR.pyo
/opt/xensource/sm/LinstorSR
/opt/xensource/sm/LinstorSR.py
/opt/xensource/sm/LinstorSR.pyc
/opt/xensource/sm/LinstorSR.pyo
/opt/xensource/sm/MooseFSSR
/opt/xensource/sm/MooseFSSR.py
/opt/xensource/sm/MooseFSSR.pyc
/opt/xensource/sm/MooseFSSR.pyo
/opt/xensource/sm/XFSSR
/opt/xensource/sm/XFSSR.py
/opt/xensource/sm/XFSSR.pyc
/opt/xensource/sm/XFSSR.pyo
/opt/xensource/sm/ZFSSR
/opt/xensource/sm/ZFSSR.py
/opt/xensource/sm/ZFSSR.pyc
/opt/xensource/sm/ZFSSR.pyo
/opt/xensource/sm/linstorjournaler.py
/opt/xensource/sm/linstorjournaler.pyc
/opt/xensource/sm/linstorjournaler.pyo
/opt/xensource/sm/linstorvhdutil.py
/opt/xensource/sm/linstorvhdutil.pyc
/opt/xensource/sm/linstorvhdutil.pyo
/opt/xensource/sm/linstorvolumemanager.py
/opt/xensource/sm/linstorvolumemanager.pyc
/opt/xensource/sm/linstorvolumemanager.pyo
/opt/xensource/libexec/fork-log-daemon
/opt/xensource/libexec/linstor-monitord
%{_unitdir}/linstor-monitor.service

%changelog
* Fri Jun 28 2024 Ronan Abhamon <ronan.abhamon@vates.fr> 2.30.8-12.1.0.linstor.3
- Add 0176-fix-LinstorSR-open-non-leaf-volumes-in-RO-mode-creat.patch

* Mon Jun 17 2024 Ronan Abhamon <ronan.abhamon@vates.fr> 2.30.8-12.1.0.linstor.2
- Reload automatically multipathd config after each update

* Wed Jun 12 2024 Ronan Abhamon <ronan.abhamon@vates.fr> 2.30.8-12.1.0.linstor.1
- Add "Provides": sm-linstor (necessary for the "Requires" of xcp-ng-linstor)
- Add LINSTOR patches

* Wed Jun 12 2024 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.8-12.1
- Add 0023-feat-LVHDSR-add-a-way-to-modify-config-of-LVMs-56.patch
- Sync with hotfix XS82ECU1065
- Sync patches with our latest 2.30.8-8.2 branch
- - *** Upstream changelog ***
- * Wed Mar 13 2024 Mark Syms <mark.syms@citrix.com> - 2.30.8-12
- - CA-389576: in Python 2.7 IOError is not a subclass of OSError
- * Mon Feb 26 2024 Mark Syms <mark.syms@citrix.com> - 2.30.8-11
- - CA-387770 Improve error message for readonly shares
- - CA-388451: Ensure that xapi sessions are logged out
- - CP-47841: update multipath confiugration for PURE FlashArray
- - Backport fix for NFS attach from config
- - CA-387770: Backport Check for R/O FS at create

* Mon May 06 2024 Damien Thenot <damien.thenot@vates.tech> - 2.30.8-10.2
- Add LargeBlockSR for 8.2

* Tue Feb 06 2024 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.8-10.1
- Sync with hotfix XS82ECU1060
- Sync patches with our latest 2.30.8-8.2 branch
- - *** Upstream changelog ***
- * Fri Jan 19 2024 Mark Syms <mark.syms@citrix.com> - 2.30.8-10
- - Backport fix for CA-386479, log into all iSCSI targets

* Tue Dec 19 2023 Benjamin Reis <benjamin.reis@vates.fr> - 2.30.8-9.2
- Add 0020-Backport-NFS4-only-support.patch
- Add 0021-Backport-probe-for-NFS4-when-rpcinfo-does-not-includ.patch

* Mon Dec 11 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.8-9.1
- Sync with hotfix XS82ECU1056
- Sync patches with our latest 2.30.8-8.2 branch
- *** Upstream changelog ***
- * Fri Oct 27 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-9
- - Backport fix for CP-45927, set Equalogic path checker
- * Thu Oct 19 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-8
- - Backport fix for CA-375367
- - Backport fix for CA-379315
- - Backport fix for CA-381221

* Fri Oct 13 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.8-7.1
- Sync with hotfix XS82ECU1051
- Sync patches with our latest 2.30.8-8.2 branch
- *** Upstream changelog ***
- * Thu Sep 28 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-7
- - CP-45514: set ownership and perms on backeend device
- * Fri Aug 04 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-6
- - Fixes for CA-379329, monitor for missing iSCSI sessions
- * Fri Jun 30 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-5
- - CA-375968: multi session iSCSI updates
- * Fri Jun 30 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-4
- - Rebuild
- * Mon Jun 26 2023 Mark Syms <mark.syms@citrix.com> - 2.30.8-3
- - Backport fix for CA-378768

* Fri Aug 25 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.30.8-2.3
- Do not overwrite multipath.conf if users made changes
- Add warning to multipath.conf to prevent future modifications
  (for users which haven't modified it yet, that is, the vast majority)
- Add /etc/multipath/conf.d/custom.conf for user customization
- Add 0017-Tell-users-not-to-edit-multipath.conf-directly.patch
- Add 0018-Add-custom.conf-multipath-configuration-file.patch
- Add 0019-Install-etc-multipath-conf.d-custom.conf.patch

* Tue Aug 22 2023 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 2.30.8-2.2
- Fix issues when running quicktest on ZFS and LVMoISCSI
- Add 0015-Remove-SR_PROBE-from-ZFS-capabilities-37.patch
- Add 0016-Fix-vdi-ref-when-static-vdis-are-used.patch

* Tue Apr 25 2023 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.8-2.1
- Sync with hotfix XS82ECU1022
- Sync patches with our latest 2.30.8-8.2 branch
- *** Upstream changelog ***
- * Wed Nov 23 2022 Mark Syms <mark.syms@citrix.com> - 2.30.8-2
- - CA-353437: give coalesce tracker grace iterations to make progress
- - CA-372641: fix _expand_size for multipath
- - CA-372772: fix miscalculation of seek offset
- * Fri Sep 23 2022 Tim Smith <tim.smith@citrix.com> - 2.30.8-1
- - CA-369613: report errors correctly from multipath
- - CA-369395: default multipath handle to dmp if not set
- - CA-370037: improvements to exception handling
- - Added Dell ME4 multipath config
- - CA-370696 Do not attempt to validate device or NFS server paths

* Fri Jul 08 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.7-1.3
- Fix regression caused by is_open patch (LVHDSR + XCP-ng drivers)

* Thu Jun 30 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.7-1.2
- Add 0013-Fix-is_open-call-for-many-drivers-25.patch
- Add 0014-Remove-SR_CACHING-capability-for-many-SR-types-24.patch

* Wed Jun 15 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.7-1.1
- Sync with hotfix XS82ECU1009
- Sync patches with our latest 2.30.7-8.2 branch
- Add 0012-MooseFS-SR-uses-now-UUID-subdirs-for-each-SR.patch
- Use subdirectory for each SR on the MooseFS server
- *** Upstream changelog ***
- * Fri Apr 29 2022 Mark Syms <mark.syms@citrix.com> - 2.30.7-1
- - CA-352880: when deleting an HBA SR remove the kernel devices

* Thu May 05 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.6-1.2
- Add 0011-Avoid-usage-of-umount-in-ISOSR-when-legacy_mode-is-u.patch
- Keep folder mounted when ISO SR is used with legacy_mode=True

* Tue Jan 04 2022 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.6-1.1
- Sync with CH 8.2.1
- Sync patches with our latest 2.30.6-8.2 branch
- *** Upstream changelog ***
- * Fri Oct 22 2021 Mark Syms <mark.syms@citrix.com> - 2.30.6-1
- - CA-359453: use rename not link if links not supported
- - CP-38316: update path checker for Equalogic at vendors request
- * Thu Oct  7 2021 Mark Syms <mark.syms@citrix.com> - 2.30.5-1
- - CA-355401: make post attach scan best effort and report errors
- - CA-355289: ensure xapi is initialised before starting GC
- - CA-356645: use "self.session is None" not "self.session == None"

* Tue Jun 22 2021 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.4-1.1
- Sync with hotfix XS82E028
- Sync patches with our latest 2.30.4-8.2 branch
- *** Upstream changelog ***
- * Wed May 19 2021 Mark Syms <mark.syms@citrix.com> - 2.30.4-1
- - CA-354228: Reinstate load calls in _pathrefresh

* Thu May 27 2021 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.3-1.4
- Remove 0009-Fix-regression-added-by-XSI-915.patch
- Add 0001-backport-of-ccd121cc248d79b749a63d4ad099e6d5f4b8b588 to use upstream fix instead

* Tue May 18 2021 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.3-1.3
- Update 0009-Fix-regression-added-by-XSI-915.patch (fix regression in the patch itself)

* Thu May 06 2021 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.3-1.2
- Add experimental MooseFS driver

* Thu Apr 29 2021 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.30.3-1.1
- Sync with hotfix XS82E023
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
- Sync patches with our latest 2.30.3-8.2 branch
- 0009-Fix-regression-added-by-XSI-915.patch added

* Thu Feb 25 2021 Benjamin Reis <benjamin.reis@vates.fr> - 2.29.1-1.3
- Add: 0008-If-no-NFS-ACLs-provided-assume-everyone.patch
- Fix crash when attempting to access non existent ACL (happened on QNAP devices)

* Fri Nov 06 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.1-1.2
- Sync patches with our latest 2.29.1-8.2 branch before XCP-ng 8.2 final release
- 0006-feat-drivers-add-LinstorSR-driver.patch updated
- 0007-feat-tests-add-unit-tests-concerning-ZFS-close-xcp-n.patch added

* Wed Nov 04 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.1-1.1
- Sync with hotfix XS82E006
- CA-343115: ensure device symlinks are created correctly even when path count not required

* Fri Sep 18 2020 Ronan Abhamon <ronan.abhamon@vates.fr> - 2.29.0-1.7
- Update ZFS patch (use location instead of device in configuration)

* Wed Aug 19 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.0-1.6
- Add linstor-monitor daemon to detect master changes

* Mon Aug 17 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.0-1.5
- Re-enable linstor patch
- Re-add support for ext4 driver since sm-additional-drivers is gone
- Patches reordered after the 2.29.0-8.2 branch rebase

* Mon Aug 17 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.0-1.4
- Temporarily disable linstor patch

* Thu Aug 13 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.0-1.3
- Add experimental XFS, CephFS, Gluster and ZFS drivers
- Add experimental Linstor driver and related required code changes
- Patches now produced from our maintenance branch of the sm git repo
- Obsolete sm-additional-drivers

* Tue Jul 07 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.0-1.2
- Re-add cleanup support for ext4 driver (not removing it from 8.2)
- Add cleanup support for gluster and cephfs drivers
- Rename sm-2.29.0-partial-xfs-support.XCP-ng.patch...
- ... to sm-2.29.0-fix-cleanup-for-additional-drivers.XCP-ng.patch
- That patch is temporary, until sm is fixed to let drivers define...
- ... their type themselves.

* Tue Jun 30 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 2.29.0-1.1
- Rebase on CH 8.2
- Remove backported patches
- Keep sm-2.2.3-rebrand-xs-sm-service.XCP-ng.patch
- Rediff sm-2.29.0-add-TrueNAS-multipath-config.XCP-ng.patch
- Remove support for the experimental `ext4` SR type
- Rename patch to sm-2.29.0-partial-xfs-support.XCP-ng.patch

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
