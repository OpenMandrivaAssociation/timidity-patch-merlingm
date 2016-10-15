#
# NOTE:
#
# 1. When big change is involved (e.g. timidity.cfg change location),
# so that new timidity binray and old patch RPM won't work together,
# increment this number by 1 for all timidity related RPMs
#
# 2. Current config is hand merged from freepats.cfg and crude.cfg,
# so if new version is available, please merge both config, and make
# sure all patch files listed in config file do exist.
#
%define patch_pkg_version 2

Name:		timidity-patch-merlingm
Version:	32
Release:	1
Summary:	Patch set for MIDI audio synthesis
Group:		Sound
License:	Public Domain
URL:		http://www.soundfonts.gonet.biz/search.php?name=Merlin%20GM%20v32&grupo=0&goto=1
Source0:	http://www.soundfonts.gonet.biz/download2.php?rec=78&arq=./sf2/merlin_gmv32.sfArk
BuildArch:	noarch
Provides:	timidity-instruments = %{patch_pkg_version}
Obsoletes:	timidity-instruments <= 1.0-19mdk
BuildRequires:	sfarkxtc

%description
A freely distributable set of soundfonts following the General MIDI standard 

%prep

%install
mkdir -p %{buildroot}%{_datadir}/timidity/merlingm
cd %{buildroot}%{_datadir}/timidity/merlingm
cp %{SOURCE0} .
sfarkxtc *.sfArk merlin_gmv32.sf2
rm *.sfArk

mkdir -p %{buildroot}%{_sysconfdir}/timidity
cat >%{buildroot}%{_sysconfdir}/timidity/timidity-merlingm.cfg <<EOF
dir %{_datadir}/timidity/merlingm

soundfont merlin_gmv32.sf2
EOF

%post
%{_sbindir}/update-alternatives --install %{_sysconfdir}/timidity/timidity.cfg timidity.cfg %{_sysconfdir}/timidity/timidity-merlingm.cfg 30

%postun
if [ "$1" = "0" ]; then
  %{_sbindir}/update-alternatives --remove timidity.cfg %{_sysconfdir}/timidity/timidity-merlingm.cfg
fi

%triggerpostun -- TiMidity++ <= 2.13.2-1mdk
%{_sbindir}/update-alternatives --install %{_sysconfdir}/timidity/timidity.cfg timidity.cfg %{_sysconfdir}/timidity/timidity-merlingm.cfg 30

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/timidity/timidity-merlingm.cfg
%{_datadir}/timidity/merlingm
