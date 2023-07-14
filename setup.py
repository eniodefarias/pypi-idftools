# setup.py
from setuptools import setup
from pathlib import Path

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except:
    requirements = ''

print(f'requirements={requirements}')

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

print(f'long_description={long_description}')

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    name="idftools",
    author_email="eniodefarias@gmail.com",
    author="eniodefarias",
    version="0.1.4",
    url="https://github.com/eniodefarias/pypi-idftools",
    description="Um pacote com alguns utilitarios uteis",
    py_modules=["utilities", "driversfactory", "certificate"],
    package_dir={"": "idftools"}
)

# .venv/bin/python3 setup.py sdist bdist_wheel
# twine upload --skip-existing dist/*