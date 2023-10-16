# setup.py
from setuptools import setup
from pathlib import Path
import os

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
        with open('idftools/requirements.txt', 'w') as file:
            file.write('{}'.format(requirements))
            file.close()
except:
    requirements = ''



# print(f'requirements={requirements}')

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# print(f'long_description={long_description}')

setup(
    version="0.1.91",
    long_description=long_description,
    long_description_content_type='text/markdown',
    # install_requires=requirements,
    name="idftools",
    author_email="eniodefarias@gmail.com",
    author="eniodefarias",
    url="https://github.com/eniodefarias/pypi-idftools",
    description="Um pacote com alguns utilitarios uteis",
    py_modules=["idftools.utilities", "idftools.driversfactory", "idftools.certificate"],
    # package_dir={"": "idftools"}
    package_dir={"idftools": "idftools"},
    packages=["idftools"],
    # data_files=[('fonts', ['idftools/Roboto-Regular.ttf']), ('', ['idftools/logging.conf'])]
    # data_files=[('', ['requirements.txt', 'idftools/01-verify_registry_windows.exe', 'idftools/02-create_new_registry_windows_runas.exe'])],
    # data_files=[('', ['requirements.txt'])],
    # data_files=[('', [''])],
    include_package_data=True,
    package_data={'idftools': ['idftools/requirements.tx', 'idftools/Roboto-Regular.ttf', 'idftools/logging.conf', 'idftools/01-verify_registry_windows.exe', 'idftools/02-create_new_registry_windows_runas.exe']}
)



# .venv/bin/python3 setup.py sdist bdist_wheel
# twine upload --skip-existing dist/*