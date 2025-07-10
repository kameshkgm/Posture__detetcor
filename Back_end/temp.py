import pkg_resources

required_packages = {
    "certifi": "2025.7.9",
    "charset-normalizer": "3.4.2",
    "click": "8.1.8",
    "colorama": "0.4.6",
    "Flask": "2.2.5",
    "Flask-Cors": "5.0.0",
    "git-filter-repo": "2.47.0",
    "idna": "3.10",
    "importlib-metadata": "6.7.0",
    "itsdangerous": "2.1.2",
    "jinja2": "3.1.6",
    "MarkupSafe": "2.1.5",
    "numpy": "1.21.6",
    "opencv-python": "3.4.2.16",
    "requests": "2.31.0",
    "typing-extensions": "4.7.1",
    "urllib3": "2.0.7",
    "Werkzeug": "2.2.3",
    "zipp": "3.15.0",
    "Keras": "2.2.4",
    "Keras-Applications": "1.0.6",
    "Keras-Preprocessing": "1.0.5",
    "scipy": "1.0.0",
    "tensorflow": "1.15.4",
    "opencv-contrib-python": "3.4.2.16",
}

for pkg, ver in required_packages.items():
    try:
        installed_ver = pkg_resources.get_distribution(pkg).version
        if installed_ver == ver:
            print(f"{pkg}=={ver} is installed.")
        else:
            print(f"{pkg} version mismatch: installed {installed_ver}, required {ver}")
    except pkg_resources.DistributionNotFound:
        print(f"{pkg} is NOT installed.")
