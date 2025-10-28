%undefine _debugsource_packages

Name:		koboldcpp 
Version:	1.100.1
Release:	1
License:	AGPL3.0
Summary:	Run GGUF models easily with a KoboldAI UI. One File. Zero Install. 
Group:		System/AI
Url:		https://github.com/LostRuins/koboldcpp
Source0:	https://github.com/LostRuins/koboldcpp/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(vulkan)

Requires:	tkinter
Requires:	python%{pyver}dist(customtkinter)

%patchlist
patch-Makefile

%description
KoboldCpp is an easy-to-use AI text-generation software for GGML and GGUF models, inspired by the original KoboldAI. 
It's a single self-contained distributable from Concedo, that builds off llama.cpp, and adds a versatile KoboldAI API endpoint, additional format support, 
Stable Diffusion image generation, speech-to-text, backward compatibility, as well as a fancy UI with persistent stories, editing tools, save formats, memory, 
world info, author's note, characters, scenarios and everything KoboldAI and KoboldAI Lite have to offer.

%prep
%autosetup -p1

%build
%make_build PRESET_CFLAGS="%{optflags}" PRESET_CXXFLAGS="%{optflags}" LLAMA_OPENBLAS=1 LLAMA_VULKAN=1 LDFLAGS="%{build_ldflags}"

%install
rm -rf %{buildroot}

# Main install location
install -d %{buildroot}/usr/share/koboldcpp

# Install Python launcher and shared libs
install -m644 *.so %{buildroot}/usr/share/koboldcpp/
install -m644 json_to_gbnf.py %{buildroot}/usr/share/koboldcpp/

# Resources
install -d %{buildroot}/usr/share/koboldcpp/embd_res
install -m644 embd_res/* %{buildroot}/usr/share/koboldcpp/embd_res/

install -d %{buildroot}/usr/share/koboldcpp/kcpp_adapters
install -m644 kcpp_adapters/* %{buildroot}/usr/share/koboldcpp/kcpp_adapters/

# Main Python script
install -m644 koboldcpp.py %{buildroot}/usr/share/koboldcpp/koboldcpp.py

# Wrapper executable
install -d %{buildroot}/usr/bin
echo '#!/bin/sh' > koboldcpp
echo 'exec python3 /usr/share/koboldcpp/koboldcpp.py "$@"' >> koboldcpp
install -m755 koboldcpp %{buildroot}/usr/bin/koboldcpp

%files
%{_bindir}/koboldcpp
#{_libdir}/%{name}
%{_datadir}/koboldcpp/
