import os
import setuptools

version_file = open(os.path.join(".", 'VERSION'))

setuptools.setup(
    name="pmfp",
    version=version_file.read().strip(),
    author="Denis Rampnoux",
    description="A small agent to monitor process running for parental usage",
    packages=setuptools.find_packages(),
    install_requires=['psutil==5.8.0', 'schedule==1.1.0'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: System :: Monitoring",
        ],
    python_requires='>=3.7',
)

