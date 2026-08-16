# Vendored ggml/llama.cpp/sd.cpp/tts — KoboldCpp has no USE_SYSTEM_GGML
# and compiles ggml into per-ISA backend DSOs plus ggml v1/v2/v3 for
# old .bin models. System ggml is not a drop-in.

%undefine _debugsource_packages

Name:		koboldcpp
Version:	1.119
Release:	2
License:	AGPL-3.0-only AND MIT
Summary:	Run GGUF models with a KoboldAI UI
Group:		Sciences/Other
URL:		https://github.com/LostRuins/koboldcpp
Source0:	https://github.com/LostRuins/koboldcpp/archive/refs/tags/v%{version}/koboldcpp-%{version}.tar.gz
# Distro optflags; do not let the Makefile strip (-s) debuginfo.
Patch0:		0001-makefile-optflags.patch

BuildRequires:	make
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	glslc
BuildRequires:	python

Requires:	python
Requires:	python%{pyver}dist(customtkinter)

%description
KoboldCpp runs GGUF and legacy GGML models with a KoboldAI-style
web UI: stories, memory, world info, image generation, speech-to-text
and TTS. Tensor kernels are compiled from the bundled llama.cpp tree
into several plugins (CPU instruction-set variants and Vulkan).
System ggml cannot be used — there is no upstream option and the
loader expects those plugins next to the script.

  koboldcpp --model /var/lib/koboldcpp/model.gguf

%prep
%autosetup -p1 -n koboldcpp-%{version}
# Bundled glslc-linux is an x86_64 blob; use the system compiler.
rm -f glslc-linux glslc.exe
ln -s %{_bindir}/glslc glslc-linux
find . -name '.gitignore' -delete 2>/dev/null || true

%build
export CC=clang
export CXX=clang++
# Drop -march/-mtune/-mcpu and x86 ISA flags so failsafe/noavx2
# plugins stay portable. Makefile adds -mavx2/-msse3 per backend.
# -fno-lto: link-time opt would recompile every plugin for the
# same CPU target and collapse the variants.
kcpp_cflags=$(printf '%s' '%{optflags}' | sed -E \
	-e 's/ -m(arch|tune|cpu)=[^ ]+//g' \
	-e 's/ -m(mmx|sse[0-9.a]*|ssse3|avx[0-9]*|sha|aes|fma|f16c|clflushopt|fsgsbase|rdrnd|rdseed|popcnt|adx|bmi2?|fxsr|xsave[a-z]*|mwaitx|clzero|fpmath=[^ ]+)//g')
kcpp_ldflags=$(printf '%s' '%{?build_ldflags}' | sed -E \
	-e 's/ -m(arch|tune|cpu)=[^ ]+//g' \
	-e 's/ -m(mmx|sse[0-9.a]*|ssse3|avx[0-9]*|sha|aes|fma|f16c|clflushopt|fsgsbase|rdrnd|rdseed|popcnt|adx|bmi2?|fxsr|xsave[a-z]*|mwaitx|clzero|fpmath=[^ ]+)//g')
# LLAMA_PORTABLE: explicit ISA flags instead of -march=native.
# Vulkan/failsafe/noavx2 backends are no-ops on non-x86.
%make_build \
	PRESET_CFLAGS="$kcpp_cflags -fno-lto" \
	PRESET_CXXFLAGS="$kcpp_cflags -fno-lto" \
	LLAMA_PORTABLE=1 \
	LLAMA_VULKAN=1 \
	LDFLAGS="$kcpp_ldflags -fno-lto"

%install
inst=%{buildroot}%{_libdir}/%{name}
mkdir -p "$inst" %{buildroot}%{_bindir}
install -m 0755 koboldcpp.py "$inst/koboldcpp.py"
sed -i '1s|^#!/usr/bin/env python3|#!/usr/bin/python|' "$inst/koboldcpp.py"
# Imported as "from json_to_gbnf import SchemaConverter"
install -m 0644 json_to_gbnf.py "$inst/json_to_gbnf.py"
ln -s %{_libdir}/%{name}/koboldcpp.py %{buildroot}%{_bindir}/koboldcpp

# Backend plugins (CPU ISA + Vulkan). CUDA/HIP targets are no-ops
# unless LLAMA_CUBLAS / LLAMA_HIPBLAS is set.
for lib in koboldcpp_default.so koboldcpp_failsafe.so \
	koboldcpp_noavx2.so koboldcpp_vulkan.so \
	koboldcpp_vulkan_noavx2.so koboldcpp_vulkan_failsafe.so; do
	[ -f "$lib" ] && install -m 0755 "$lib" "$inst/"
done

cp -a embd_res "$inst/"
cp -a kcpp_adapters "$inst/"

%check
python ./koboldcpp.py --version | grep -F '%{version}'

%files
%license LICENSE.md MIT_LICENSE_GGML_SDCPP_LLAMACPP_ONLY.md
%doc README.md
%{_bindir}/koboldcpp
%{_libdir}/%{name}/
