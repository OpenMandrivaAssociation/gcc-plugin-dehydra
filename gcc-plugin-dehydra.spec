%define name gcc-plugin-dehydra
%define _gcc gcc
%define gccdir %(%{_gcc} -print-file-name=plugin)
%define _gcc45 gcc4.5
%define gcc45dir %(%{_gcc45} -print-file-name=plugin)

Name:		%{name}
Version:	0.0.hg563
Release:	6
License:	GPLv2
Summary:	GCC Dehydra Plugin
Group:		Development/C++
URL:		http://hg.mozilla.org/rewriting-and-analysis/dehydra/
Source0:	%{name}-%{version}.tar.bz2
Requires:	%{_gcc}-c++
Suggests:	%{name}-doc
Suggests:	%{name}-treehydra
Requires:	%{_gcc}-plugin-devel
Requires:	gmp-devel
Requires:	ppl-devel
Requires:	ppl_c-devel
Requires:	mpfr-devel
Requires:	libmpc-devel
Requires:	spidermonkey-mozillacentral
BuildRequires:	%{_gcc}-c++
BuildRequires:	%{_gcc45}-c++
BuildRequires:	%{_gcc}-plugin-devel
BuildRequires:	%{_gcc45}-plugin-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libstdc++-4.5-devel
BuildRequires:  gmp-devel
BuildRequires:  ppl-devel
BuildRequires:  ppl_c-devel
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
BuildRequires:	spidermonkey-mozillacentral-devel

%description
Dehydra is a lightweight, scriptable, general purpose static analysis
tool capable of application-specific analyses of C++ code. In the
simplest sense, Dehydra can be thought of as a semantic grep tool. It
presents a wealth of semantic information that can be queried with
concise JavaScripts. It is also useful to find bugs in source code as it
allows for much more error checking than C++ is capable of by itself.
Dehydra is built as a GCC plugin, thus it is easy to use for projects
that already support GCC.

Dehydra is also useful for generating language bindings and is used to
bootstrap Treehydra, a heavy-duty static analysis GCC plugin.

%files
%{gccdir}/gcc_dehydra.so
%{gccdir}/*.js
%{gccdir}/libs/*.js
%{gccdir}/libs/unstable/*.js

%package	-n gcc-plugin-treehydra
Summary:	GCC Treehydra Plugin
Group:		Development/C++
URL:		https://developer.mozilla.org/en/Treehydra
Suggests:	%{name}-doc
Requires:	%{_gcc}-c++
Requires:	%{_gcc}-plugin-devel
Requires:	gmp-devel
Requires:	ppl-devel
Requires:	ppl_c-devel
Requires:	mpfr-devel
Requires:	libmpc-devel
Requires:	%{name}
Requires:	spidermonkey-mozillacentral

%description	-n gcc-plugin-treehydra 
Treehydra is a GCC plugin that provides a low level JavaScript binding
to GCC's GIMPLE AST representation. Treehydra is intended for precise
static analyses.

Most of Treehydra is generated by Dehydra. A Dehydra script walks the
GCC tree node structure using the GTY attributes present in GCC.
Treehydra is included in Dehydra source, and is built when a
plugin-enabled CXX is detected.

%files	-n gcc-plugin-treehydra
%{gccdir}/gcc_treehydra.so

%package -n gcc4.5-plugin-dehydra
Summary:	GCC 4.5 Dehydra Plugin
Group:		Development/C++
Requires:	%{_gcc45}-c++
Suggests:	%{name}-doc
Suggests:	%{name}-treehydra
Requires:	%{_gcc45}-plugin-devel
Requires:	gmp-devel
Requires:	ppl-devel
Requires:	ppl_c-devel
Requires:	mpfr-devel
Requires:	libmpc-devel
Requires:	spidermonkey-mozillacentral

%description -n gcc4.5-plugin-dehydra
Dehydra is a lightweight, scriptable, general purpose static analysis
tool capable of application-specific analyses of C++ code. In the
simplest sense, Dehydra can be thought of as a semantic grep tool. It
presents a wealth of semantic information that can be queried with
concise JavaScripts. It is also useful to find bugs in source code as it
allows for much more error checking than C++ is capable of by itself.
Dehydra is built as a GCC plugin, thus it is easy to use for projects
that already support GCC.

Dehydra is also useful for generating language bindings and is used to
bootstrap Treehydra, a heavy-duty static analysis GCC plugin.

%files -n gcc4.5-plugin-dehydra
%{gcc45dir}/gcc_dehydra.so
%{gcc45dir}/*.js
%{gcc45dir}/libs/*.js
%{gcc45dir}/libs/unstable/*.js


%package	-n gcc4.5-plugin-treehydra
Summary:	GCC 4.5 Treehydra Plugin
Group:		Development/C++
URL:		https://developer.mozilla.org/en/Treehydra
Suggests:	%{name}-doc
Requires:	%{_gcc45}-c++
Requires:	%{_gcc45}-plugin-devel
Requires:	gmp-devel
Requires:	ppl-devel
Requires:	ppl_c-devel
Requires:	mpfr-devel
Requires:	libmpc-devel
Requires:	%{name}
Requires:	spidermonkey-mozillacentral

%description	-n gcc4.5-plugin-treehydra 
Treehydra is a GCC plugin that provides a low level JavaScript binding
to GCC's GIMPLE AST representation. Treehydra is intended for precise
static analyses.

Most of Treehydra is generated by Dehydra. A Dehydra script walks the
GCC tree node structure using the GTY attributes present in GCC.
Treehydra is included in Dehydra source, and is built when a
plugin-enabled CXX is detected.

%files	-n gcc4.5-plugin-treehydra
%{gcc45dir}/gcc_treehydra.so

%package doc
Summary:	GCC Dehydra Plugin Documentation
BuildArch:	noarch

%description doc
This package provides HTML documentation for the GCC Dehydra
Plugin, a GCC plugin aimed at tying together JavaScript and GCC
to be able to use JavaScript script from inside the compiler.

%files doc
%doc README

%prep
%setup -q -n %{name}-%{version}

%autopatch -p1

%build
sed -ri -e 's/\$\(GCC_PLUGIN_HEADERS\)/\$\(GCC_PLUGIN_HEADERS\) \$\(GCC_PLUGIN_HEADERS\)\/c-family/g' Makefile.in

%{__mkdir} ../%{_gcc} ../%{_gcc45}
%{__cp} -r * ../%{_gcc}
%{__cp} -r * ../%{_gcc45}

%{__mv} ../%{_gcc} %{_gcc}
%{__mv} ../%{_gcc45} %{_gcc45}

pushd %{_gcc}
export CC=gcc
export CXX=g++
../configure --js-name=mozjscentral --js-lib=%{_libdir} --js-headers=/usr/include/jscentral/
%make
popd

pushd %{_gcc45}
export CC=gcc4.5
export CXX=g++4.5
../configure --js-name=mozjscentral --js-lib=%{_libdir} --js-headers=/usr/include/jscentral/
%make
popd

%install
pushd %{_gcc}
for plugin in gcc_dehydra.so gcc_treehydra.so; do
	%{__install} -m755 -D $plugin %{buildroot}/%{gccdir}/$plugin
done;

for lib in *.js libs/*.js libs/unstable/*.js; do
	%{__install} -m644 -D $lib %{buildroot}/%{gccdir}/$lib
done;
popd

pushd %{_gcc45}
for plugin in gcc_dehydra.so gcc_treehydra.so; do
	%{__install} -m755 -D $plugin %{buildroot}/%{gcc45dir}/$plugin
done;

for lib in *.js libs/*.js libs/unstable/*.js; do
	%{__install} -m644 -D $lib %{buildroot}/%{gcc45dir}/$lib
done;
popd

%clean
rm -fr %{buildroot}
