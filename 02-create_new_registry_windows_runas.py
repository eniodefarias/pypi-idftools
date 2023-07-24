# -*- coding: utf-8 -*-
#coding: utf-8
import sys
sys.path.append("../")

#import subprocess
#import winreg
#import os
#import sys
            #HINT: use python -m pip install pywin32
#import win32com.shell.shell as shell
import time
import argparse

#from subprocess import Popen, PIPE
import subprocess
import os
#import decode


def reg():
    try:
        msg_erros = []
        error_block = False

        retorno = 'ERRO DESCONHECIDO'

        afullpath = sys.argv[0]
        #print(f'afullpath: {afullpath}')
        pat = os.path.abspath(afullpath)
        #print(f'pat: {pat}')
        dire = os.path.dirname(afullpath)
        #print(f'dire: {dire}')
        #subinacl = os.path.join(dire, 'subinacl.exe')
        #print(f'subinacl: {subinacl}')
        chrome_regedit1 = os.path.join(dire, 'chrome_regedit.txt')
        chrome_regedit = os.path.abspath(chrome_regedit1)

        parser = argparse.ArgumentParser(description='argumentos')

        try:
            #print('   Inicia captura do argumento Key')
            parser.add_argument('--filename', '-f', dest="arg_filename", type=str, help="filename, é o arquivo temporario", required=True)
        except Exception as e:
            erro = f'erro ao pegar argumento Filename: {e}'
            time.sleep(2)
            #print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True

        try:
            #print('   Inicia captura do argumento Key')
            parser.add_argument('--key', '-k', dest="arg_key", type=str, help="key, é o caminho completo de onde está a chave. Ex: HKEY_LOCAL_MACHINE\SOFTWARE\Teste", required=True)
        except Exception as e:
            erro = f'erro ao pegar argumento Key: {e}'
            time.sleep(2)
            #print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True

        try:
            ##print('   Inicia captura do argumento da Chave')
            parser.add_argument('--subkey', '-s', dest="arg_subkey", type=str, help="subkey, é o nome da chave", required=True)
        except Exception as e:
            erro = f'erro ao pegar argumento Subkey: {e}'
            time.sleep(2)
            #print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True


        try:
            ##print('   Inicia captura do argumento do Tipo')
            parser.add_argument('--type', '-t', dest="arg_type", type=str, help="type, é o tipo da chave. Ex: REG_SZ", required=True)
        except Exception as e:
            erro = f'erro ao pegar argumento Type: {e}'
            time.sleep(2)
            #print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True


        try:
            ##print('   Inicia captura do argumento do Valor')
            parser.add_argument('--value', '-v', dest="arg_value", type=str, help="value, é o valor da chave. Ex: 1", required=True)
        except Exception as e:
            erro = f'erro ao pegar argumento Value: {e}'
            time.sleep(2)
            #print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True

        try:
            args = parser.parse_args()
            chave = args.arg_key
            subchave = args.arg_subkey
            tipo = args.arg_type
            valor = args.arg_value
            arquivo = args.arg_filename

            comando = f'reg add "{chave}" /v "{subchave}" /t {tipo} /d "{valor}" /f'
            print(f'executando criação de registro:   {comando}')
            time.sleep(2)



            #HINT:   echo HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls [1 5 7 11 14 17 21] > rreg.txt
            comando3 = f'{chave} [1 5 7 11 14 17 21]'
            with open(chrome_regedit, 'w') as file:
                file.write('{}'.format(comando3))
                file.close()


            comando2 = f'regini {chrome_regedit}'


            #comando2 = f'{subinacl} /{subchave} {chave} /GRANT=All_Users=F'
            #comando2 = f'{subinacl} /{subchave} {chave}  /GRANT=S-1-5-11=F'

            #print(f'\n\n{comando2}\n\n')
            #time.sleep(10)

            #comando2='subinacl.exe /subkeyreg HKEY_LOCAL_MACHINE\SOFTWARE\POLICIES\MICROSOFT /grant=Everyone=f'

            ##print(f'   montando comando do registro:     "{comando}"    ')
            #print(f'   Executando o comando:     "{comando}"    \n')
            #time.sleep(3)

        except Exception as e:
            comando = ''
            erro = f'erro ao mapear argumentos: {e}'
            print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True
            time.sleep(2)

        try:
            #os.popen(f'reg add HKEY_LOCAL_MACHINE\\{key_to_read} /v {sub_key} /t REG_SZ /d 1 /f')
            #resultado = os.popen(f'{comando}')
            #resultado = os.system(f'{comando}')
            #retorno = resultado

            #output = Popen(["date"], stdout=PIPE)
            #output = Popen([f'{comando}'], stdout=PIPE)
            #response = output.communicate()
            #retorno = response

            #result = subprocess.check_output(comando, shell=True)
            #result = subprocess.check_output([comando], stderr=subprocess.STDOUT)

            #os.system('chcp 850 ')
            result = subprocess.getoutput(comando)
            resultado1 = result.encode('utf-8').decode('utf-8').replace('\n', ' ').strip('\n').strip(' ').replace('  ', ' ')

            result2 = subprocess.getoutput(comando2)
            resultado2 = result2.encode('utf-8').decode('utf-8').replace('\n', ' ').strip('\n').strip(' ').replace('  ', ' ')

            resultado = f'(reg: {resultado1});(subinacl.exe: {resultado2})'


            #retorno = result.encode('Windows-1252').decode('Windows-1252')
            #retorno = result.encode('Windows-1252').decode('utf-8')


            ##print("result::: ", result)
            #retorno = result.encode('UTF-8')
            #retorno = result.decode('ascii')
            #retorno = result.encode('utf-8')
                #.encode('iso8859-1').decode('uft-8')

            #result_bytes = subprocess.check_output(comando, text=False)
            #result = result_bytes.decode("gb2312")
            #retorno = result

            if 'ERRO' in resultado or 'ERROR' in resultado:
                erro = 'erro ao executar o comando do registro: {}'
                msg_erros.append(f'{erro}')
                #err = str(msg_erros).replace('"', '').replace('\'', '')
                #error_block = True
                retorno = '{"Type": "Command", "Status": "ERROR", "Descriptions": "' + resultado + '"}'
            else:
                retorno = '{"Type": "Command", "Status": "SUCCESS", "Descriptions": "' + resultado + '"}'

            ##print(' ####################### ')
            print(f'   Resultado do comando:    "{retorno}"    ')
            time.sleep(2)
            ##print(' ####################### ')

        except Exception as e:
            erro = f'erro ao executar o comando {comando}: {e}'
            #print(f'   Abort: ERROR: {erro}')
            msg_erros.append(f'{erro}')
            error_block = True

        if error_block is True:
            err = str(msg_erros).replace('"','').replace('\'','')
            retorno = '{"Type": "Reg", "Status": "ERROR", "Descriptions": "' + err + '"}'
            ##print(f'   {retorno}')

    except Exception as e:
        err = f'Erro desconhecido: {e}'.replace('"', '').replace('\'', '')
        retorno = '{"Type": "System", "Status": "ERROR", "Descriptions": "' + err + '"}'
        ##print(f'   {retorno}')

    #print('\n\n\n')
    #print(f'{retorno}\n')
    #time.sleep(10)
    #time.sleep(2)

    with open(arquivo, 'w') as file:
        file.write('{}'.format(retorno))
        file.close()
    return retorno

a = reg()
#reg()
print(a)
time.sleep(5)

#HINT: .\create_new_registry_windows_runas.exe -k "HKEY_LOCAL_MACHINE\SOFTWARE\TesteB\TesteC" -s "Teste001" -t "REG_SZ" -v "0"