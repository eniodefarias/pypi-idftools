# -*- coding: utf-8 -*-
#coding: utf-8
import sys
sys.path.append("../")

#from _winreg import *
import time
import subprocess
import winreg
import os
import sys
#use python -m pip install pywin32
import win32com.shell.shell as shell
import win32api, win32con, win32event, win32process
#from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
#import pywin32.shell.shell as shell

#registry = registry.Registry('system')
#print(f'registry: {registry}')

#sub_key = r'Teste4'
#key_to_read = r'SOFTWARE\Barrier'




sub_key = r'1'

#key_to_read = r'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
#key_to_read = r'HKEY_LOCAL_MACHINE\SOFTWARE\PoPoPo\Google\Chrome\AutoSelectCertificateForUrls'
key_to_read = r'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
raiz_reg = r'HKEY_LOCAL_MACHINE'
key_to_read = r'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'

#key_to_write = r'SOFTWARE\Barrier\teste'

a = sys.argv[0]
pat = os.path.abspath(a)
dire = os.path.dirname(a)


#dire = os.path.dirname(direa, 'bin')



full = os.path.join(dire, '02-create_new_registry_windows_runas.exe')
temp1 = os.path.join(dire, 'temp.txt')

temp = os.path.abspath(temp1)

try:
    print(f'\nIniciando tentativa de criar o registro')
    ASADMIN = 'asadmin'
    user = sys.argv[-1]
    # print(f'user: {user}')
    userb = sys.argv[1:]
    # print(f'userb: {userb}')
    if sys.argv[-1] != ASADMIN:
        # script = os.path.abspath(sys.argv[0])
        # script = f'"reg add HKEY_LOCAL_MACHINE\\{key_to_read} /v {sub_key} /t REG_SZ /d 1 /f"'
        # script = f'"'
        fulli = f' open {full} '
        # script = os.path.abspath(sys.argv[0])
        # script = r'C:\Windows\notepad.exe'
        #    -k "HKEY_LOCAL_MACHINE\SOFTWARE\TesteA\TesteB\TesteD" -s "Teste004" -t "REG_SZ" -v "x"
        # script = f'{full} -k \"{key_to_read}\" -s \"{sub_key}\" -t \"REG_SZ\" -v \"1\" '

        script = full
        # paqms2 = '-k "HKEY_LOCAL_MACHINE\SOFTWARE\TesteA" -s "sub_key" -t "REG_SZ" -v "1" '
        # temp2 = f'{temp}'.replace(' ', '/ ')
        ##paqms2 = f'-k "{raiz_reg}\\{key_to_read}" -s "{sub_key}" -t "REG_SZ" -v "0" -f "{temp}"'
        paqms2 = f'-k "{raiz_reg}\\{key_to_read}" -s "{sub_key}" -t "REG_SZ" -v "0" -f "{temp}"'
        print(f'paqms2:     {paqms2}      ')
        # script = f'{full}'
        # print(f'script:    {script}')
        # params = ' '.join([script] + sys.argv[1:]  + [ASADMIN])
        # params = ' '.join([script] + sys.argv[1:] + [paqms2])
        # params = ' '.join([script] + [paqms2])
        params = ' '.join([paqms2])
        # params = ' '
        # print(f'params:    {params}')
        # result = shell.ShellExecuteEx(lpVerb='runas', nShow=win32con.SW_SHOWNORMAL, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpFile=sys.executable, lpParameters=fulli)
        # result = shell.ShellExecuteEx(lpVerb='runas', lpExpandConstant=f'{full}', nShow=win32con.SW_SHOWNORMAL, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpFile=sys.executable, lpParameters=fulli)

        # commando = f'reg add HKEY_LOCAL_MACHINE\\{key_to_read} /v {sub_key} /t REG_SZ /d 1 /f'

        # HINT: http://timgolden.me.uk/pywin32-docs/shell__ShellExecuteEx_meth.html
        result = shell.ShellExecuteEx(lpVerb='runas', nShow=win32con.SW_SHOWNORMAL, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpFile=f'{script}', lpParameters=params)
        # result = shell.ShellExecuteEx(lpVerb='runas', nShow=win32con.SW_SHOWNORMAL, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpFile=f'{pat}', lpParameters=params)

        procHandle = result['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        # print(f'obj: {obj}')
        rc = win32process.GetExitCodeProcess(procHandle)
        # print(f'rc: {rc}')
        # result = shell.ShellExecuteEx(0, "open", "cmd.exe", f"/C {script}", 0, lpVerb='runas', lpFile=sys.executable)
        # result = shell.ShellExecuteEx(0, "open", "cmd.exe", f"/C {script}", 0, SW_SHOW)

        # result = subprocess.call(['runas', '/user:Administrator', script])

        # sys.exit(0)
        # time.sleep(4)
        f = open(temp)
        lines = f.read()
        print(f'lines: {lines}')
        f.close()
        linhas = lines.replace('\n', ' ').strip('\n').strip(' ')

        print(f'Resultado: {linhas}')

        # os.popen(f'reg add HKEY_LOCAL_MACHINE\\{key_to_read} /v {sub_key} /t REG_SZ /d 1 /f')
        # os.system(f'reg add HKEY_LOCAL_MACHINE\\{key_to_read} /v {sub_key} /t REG_SZ /d 1 /f')
        # os.system(f'{full}')
        time.sleep(5)

except Exception as e:
    print(f'erro ao criar registro usando system: {e}')
    time.sleep(5)






try:
    key = winreg.HKEY_LOCAL_MACHINE
    reg = winreg.ConnectRegistry(None, key)
    #print(f'----path1------\n{reg}\n----------')


    #k = winreg.OpenKey(reg, key_to_read, 0, winreg.KEY_READ)
    k = winreg.OpenKey(reg, key_to_read)
    print(f'registro lido: {k}')



    #value = winreg.QueryValue(key, key_to_read)
    #print(f'value: {value}')

    valuex = winreg.QueryValueEx(k, sub_key)
    print(f'valuex: {valuex}')
    print(f'\nOK. Registro já existe')
    #sub_keyB = r'Teste'
    #criar = winreg.CreateKeyEx(k, sub_keyB, reserved=0, access=winreg.KEY_WRITE)
    #criar = winreg.CreateKeyEx(k, sub_keyB, reserved=0, access=winreg.KEY_ALL_ACCESS)
    #criar = winreg.CreateKeyEx(k, sub_keyB, reserved=1, access=winreg.REG_SZ)
    #criar = winreg.CreateKeyEx(k, sub_keyB, reserved=1, access=winreg.KEY_ALL_ACCESS)

    #print(f'criar: {criar}')




except Exception as e:
    # do things to handle the exception here
    print(f'erro registro lido: {e}')
    time.sleep(5)










time.sleep(7)









    #verify_registry_windows