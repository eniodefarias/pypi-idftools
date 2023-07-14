# I.d.F. tools

 - [https://pypi.org/project/idftools/](https://pypi.org/project/idftools/)

## pre-requirements.txt
```text
webdriver_manager
wincertstore
undetected_chromedriver
winreg
pywin32
pyautogui
subprocess
database
json
cv2
intertools
cryptography
openpyxl
PyInstaller
pip
pandas
winreg
csv
configparser
sys
os
selenium
pyautogui
time
datetime
pytz
openpyxl
numpy
subprocess
os
sys
re
sys
os
anticaptchaofficial
psycopg2-binary
Pillow
opencv-python
img2pdf
xlsxwriter
```

### dica para instalar os pre-requirements.txt na mão
#### usando o gitbash
```bash
cat pre-requirements.txt| grep -v "#" |sort|uniq | xargs -n 1 .venv/Scripts/pip3.exe install; .venv/Scripts/pip3.exe --upgrade pip ; .venv/Scripts/python.exe -m pip install --upgrade pip
```
#### usando o shell do linux
```bash
cat pre-requirements.txt| grep -v "#" |sort|uniq | xargs -n 1 .venv/bin/pip install; .venv/bin/pip --upgrade pip ; .venv/bin/python3 -m pip install --upgrade pip
```



## instalando

```bash
pip install idftools
```

## importando
```python
import idftools

# use as funções do seu pacote
idftools.utilities.some_function()
idftools.driversfactory.some_other_function()
idftools.certificate.another_function()
```
