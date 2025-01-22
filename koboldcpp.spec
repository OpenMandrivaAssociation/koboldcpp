Name:		koboldcpp 
Version:	1.82.2
Release:	1
License:	AGPL3.0
Summary:	Run GGUF models easily with a KoboldAI UI. One File. Zero Install. 
Group:		System/AI
Url:		https://github.com/LostRuins/koboldcpp
Source0:	https://github.com/LostRuins/koboldcpp/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: pkgconfig(python)
BuildRequires: pkgconfig(vulkan)

Requires: tkinter
Requires: python3dist(customtkinter)


%description
KoboldCpp is an easy-to-use AI text-generation software for GGML and GGUF models, inspired by the original KoboldAI. 
It's a single self-contained distributable from Concedo, that builds off llama.cpp, and adds a versatile KoboldAI API endpoint, additional format support, 
Stable Diffusion image generation, speech-to-text, backward compatibility, as well as a fancy UI with persistent stories, editing tools, save formats, memory, 
world info, author's note, characters, scenarios and everything KoboldAI and KoboldAI Lite have to offer.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install

%files
