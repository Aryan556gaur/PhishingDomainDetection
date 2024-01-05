from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filename:str)->List[str]:
    requirements=[]
    with open(filename) as file:
        requirements = file.readlines()
        
        requirements = [i.replace("\n","") for i in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name="PhishingDomainDetection",
    version='0.0.1',
    author='Aryan',
    author_email='aryangaur556@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)