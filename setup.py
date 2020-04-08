import setuptools
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.install_scripts import install_scripts
from setuptools.command.build_ext import build_ext as build_ext_orig
from subprocess import check_call
from distutils.sysconfig import get_python_lib
import os
import platform
import pathlib
import atexit

with open("README.md", "r") as fh:
    long_description = fh.read()

class PostInstallCommand(install_scripts):
    def run(self):
        post_install_script(self.build_dir)
        install_scripts.run(self)
        
def post_install_script(s):
    current_dir = os.getcwd()
    site_p = pathlib.Path(s).parent
    print(site_p)
    raw_build_dir = ""
    build_dir_sub_lib = ""
    if platform.system() == "Darwin":
        build_dir_sub_lib = "/wheel/magent"
    else:
        build_dir_sub_lib = "/magent"
    for sub in site_p.iterdir():
        f = str(sub)
        print("sub builds ",f)
        raw_build_dir = f+build_dir_sub_lib
        break
    
    if raw_build_dir != "":
        os.chdir(str(raw_build_dir))
        check_call("bash build.sh".split())
        os.chdir(str(current_dir))
    else:
        print("pre-built src not available, cannot build.")


setuptools.setup(
    name="magent",
    version="0.1.3",
    author="PettingZoo Team",
    author_email="justinkterry@gmail.com",
    description="Multi-Agent Reinforcement Learning environments with very large numbers of agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PettingZoo-Team/MAgent",
    keywords=["Reinforcement Learning", "game", "RL", "AI"],
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'pygame>=2.0.0.dev6'
    ],
    python_requires='>=3.5',
    data_files = [("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    cmdclass = {
        'install_scripts': PostInstallCommand,
    },
)



