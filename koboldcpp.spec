%undefine _debugsource_packages

Name:		koboldcpp 
Version:	1.87.4
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
https://codeberg.org/FreeBSD/freebsd-ports/raw/branch/main/misc/koboldcpp/files/patch-Makefile

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
mkdir -p %{buildroot}%{_libdir}/%{name} %{buildroot}%{_bindir}
install -c -m 755 koboldcpp.py %{buildroot}%{_libdir}/%{name}/koboldcpp.py
ln -s %{_libdir}/%{name}/koboldcpp.py %{buildroot}%{_bindir}/koboldcpp
for lib in *.so; do
	install -c -m 755 ${lib} %{buildroot}%{_libdir}/%{name}/
done
for embd in *.embd; do
	install -c -m 644 ${embd} %{buildroot}%{_libdir}/%{name}/
done

%files
%{_bindir}/koboldcpp
%{_libdir}/%{name}
