from setuptools import setup, find_packages

setup(
    name="blocklist-py",
    version="0.0.1",
    description=(
        "module to create and format blocklists for use in pihole"
    ),
    url="https://github.com/dhoessl/blocklist-py.git",
    author="Dominic Hößl",
    author_email="dhoessl@dhoessl.de",
    license="GPL-v3",
    packages=find_packages(exclude=["docs", "docs.*"]),
    package_data={},
    include_package_data=True,
    install_requires=["loguru", "requests", "pyyaml"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ]
)
