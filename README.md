<p align="center">
  <img src="http://ideiadofuturo.com.br/img/logo_ideia.png" width="120" title="supervisão"  alt="Supervisao Contabilidade e Consultoria">  
</p>


# Ideia do Futuro - IdFtools

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
wheel
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

## atualizando
```bash
pip install --upgrade pip
pip install --upgrade idftools
```

## importando

```python

from modules_idftools import idftools

# use as funções do seu pacote
utilities.some_function()
driversfactory.some_other_function()
certificate.another_function()
```

---

---

---

---

---

---


---
# criando e enviando para o PyPi
```bash
.venv/bin/python3 -m pip install wheel
```

```bash
rm -rf dist/
.venv/bin/python3 setup.py sdist bdist_wheel

twine upload --skip-existing dist/*
```






# comandos úteis

## GIT
 - lembre se trocar o nome do **branch** de acordo com a necessidade



### iniciar o repo
```bash
git init
git remote add origin https://github.com/eniodefarias/pypi-idftools.git
```


### puxar "git pull" da branch 
```bash    
git pull -f origin main
```

### trocar branch main
```bash    
git branch main ; git checkout main 
```

### gerar o venv

#### primeiro baixar o python
 - [www.python.org](https://www.python.org/downloads/release/python-380/)

#### no windows, no cmd do DOS:
```cmd    
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe -m venv .venv
```

#### no windows, no gitbash:
```bash    
/c/Users/$(whoami)/AppData/Local/Programs/Python/Python39/python.exe -m venv .venv
```

#### no linux, no shell
```bash    
/home/$(whoami)/.pyenv/shims/python3 -m venv .venv
```

### instalar os requirements.txt na mão
#### usando o gitbash
```bash     
cat requirements.txt| grep -v "#"|sort|uniq | xargs -n 1 .venv/Scripts/pip3.exe install ; .venv/Scripts/python.exe -m pip install --upgrade pip
```

#### usando o shell do linux
```bash    
cat requirements.txt| grep -v "#"|sort|uniq | xargs -n 1 .venv/bin/pip install ; .venv/bin/python3 -m pip install --upgrade pip
```

### atualizar modulos no Gitbash
```bash    
.venv/Scripts/python.exe -m pip install PyInstaller
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install --upgrade idftools
```

### enviar "git push" da branch
```bash    
git add . ; git add * ; git commit -m "update: ajuste" ; git push -f origin main
```

## executar:

### terminal gitbash
```bash     
.venv/Scripts/python.exe app.py
```

### terminal shell do linux:
```bash    
.venv/bin/python3 app.py
```

## compilar:
 - lembre-se de alterar o nome do executavel **".exe"** e script python **".py"** de acordo com a versão e script que vai compilar

### terminal do pycharm
```bash    
.venv/bin/python3  -m PyInstaller --onefile --paths .\venv\Lib\site-packages --icon=icone\logo_circle.ico -n app .\app.py ; rm app.exe ; mv dist/app.exe .
```

### terminal do gitbash
```bash
set UPX= --ultra-brute --best --compress-icons#0 ; time .venv/Scripts/python.exe -m PyInstaller --upx-dir=./ --noconfirm --onefile --paths .venv/Lib/site-packages --icon=icone/logo.ico -n  app app.py ; rm app.exe ; mv dist/app.exe . ; ls -latrh *.exe
```
    

---

<p align="center">
  <img src="http://ideiadofuturo.com.br/img/logo_ideia.png" width="120" title="supervisão"  alt="Supervisao Contabilidade e Consultoria">  
</p>