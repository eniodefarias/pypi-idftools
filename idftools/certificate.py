# -*- coding: utf-8 -*-
#coding: utf-8
import sys
sys.path.append("../../")
import os
import pandas as pd
import csv
import re
import json
import ssl
import time
import json
import re
import subprocess
import datetime
from colorama import Fore, Back, Style

if os.name == 'nt':
    from colorama import just_fix_windows_console
    just_fix_windows_console()
    from itertools import cycle
    import socket
    import winreg
    import wincertstore
    import base64
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509.oid import ExtensionOID

class Certificate:
    def __init__(self, dir_certificado):

        diretorio_local = os.path.dirname(os.path.abspath(__file__))
        self.criar_registro_chrome_winreg(diretorio_local)

        self.dir_certificado = dir_certificado
        #self.generator_json_wincertstore('./certificate/certificate_json.txt')
        # try:
        self.generator_json_wincertstore(f'{self.dir_certificado}/certificate_json.txt')
            # return True
        # except Exception as e:
        #     print(f'erro generator_json_wincertstore: {e}')
        #     return False

    def printa(self, tipo='', msg=''):
        msg = msg.replace('\n', '// ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        agora = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        if tipo == 'error':
            print(Fore.RED + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'debug':
            print(Fore.MAGENTA + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'warning':
            print(Fore.YELLOW + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'info':
            print(Fore.CYAN + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        elif tipo == 'critical':
            print(Back.RED + f'{agora} | {tipo} | {msg}' + Style.RESET_ALL)
        else:
            print(f'{agora} | {tipo} | {msg}')

    def somente_numeros(self, numerossujos):
        return re.sub('[^0-9]', '', str(numerossujos))

    def cnpj14digits(self, cnpj):
        return str('{:0>14}'.format(self.somente_numeros(cnpj)))

    def hex_string_readable(self, bytess):
        # print(f'bytes: {bytes}')
        return ["{:02X}".format(x) for x in bytess]

    def generator_json_wincertstore(self, filename):
        userwin = os.getlogin().upper()
        pc = socket.gethostname().upper()
        self.printa('info', f'_____________________________________\n"{userwin}" iniciando mapeamento dos certificados digitais da maquina "{pc}"\n')
        if os.name == 'nt':
            #f = open(filename, "w+")
            #f.close()

            valor = 'CNPJ;json_cert_digital' + '\n'
            with open(filename, 'w', encoding="utf-8") as file:
                file.write('{}'.format(valor))
                file.close()

            for storename in ("ROOT", "CA", "MY"):
                # for storename in ( 'MY',  ):
                # print(f'\n\n++++++++++++++++++ storename: {storename} ++++++++++++++++++')
                # with wincertstore.CertSystemStore(storename) as store:
                store = wincertstore.CertSystemStore(storename)
                # print(f'store: {store}')
                # time.sleep(1)
                # for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):

                for cert in store.itercerts(usage=wincertstore.CLIENT_AUTH) or store.itercerts(usage=wincertstore.SERVER_AUTH):
                    # print(f'\n------------------- cert: {cert} -----------------')
                    # if cert.get_name() == certName:
                    # if True:
                    pem = cert.get_pem()
                    encodedDer = ''.join(pem.split("\n")[1:-2])

                    cert_bytes = base64.b64decode(encodedDer)
                    cert_pem = ssl.DER_cert_to_PEM_cert(cert_bytes)
                    cert_details = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'), default_backend())

                    # fingerprint = hex_string_readable(cert_details.fingerprint(hashes.SHA1()))
                    # fingerprint_string = ''.join(fingerprint)

                    # if fingerprint_string.lower() == thumbPrint:
                    # if True:
                    issuer = cert_details.issuer.rfc4514_string()
                    subject = cert_details.subject.rfc4514_string()
                    list_Issuer = issuer.split(',')
                    list_Subjec = subject.split(',')
                    nome_cert = cert.get_name()

                    try:
                        repl_sub = str(list_Subjec).replace('[', '{').replace(']', '}').replace('=', '\':\'').replace('\'', '"')
                        repl_issuer = str(list_Issuer).replace('[', '{').replace(']', '}').replace('=', '\':\'').replace('\'', '"')
                        # print(f'repl_sub: {repl_sub}')
                        j_Subject = repl_sub
                        leitura_json = json.loads(j_Subject)
                        requerente_CN = leitura_json['CN']
                        # print(f'requerente_CN: {requerente_CN}')
                        list_CN = requerente_CN.split(':')
                        if len(list_CN) > 1:
                            # print(f'CNPJ: {list_CN[-1]}')
                            if self.cnpj_validate(self.cnpj14digits(list_CN[-1])):
                                cnpj = self.cnpj14digits(list_CN[-1])
                            elif self.cpf_validate(self.cpf11digits(list_CN[-1])):
                                cnpj = self.cpf11digits(list_CN[-1])


                            # print(f'cnpj: {cnpj}')
                        else:
                            cnpj = 'Null'
                    except Exception as e:
                        # print(f'erro: {e}')
                        cnpj = 'Error'

                    if len(list_Subjec) > 1 and len(list_Issuer) > 1 and cnpj != 'Error' and cnpj != 'Null':
                        self.printa('info', f'\n      CNPJ:"{cnpj}" =  adicionando "{cert.get_name()}" ao json ')
                        # print(cert.get_name())
                        self.printa('info', "              Issuer: ", issuer)
                        self.printa('info', "              Subject:", subject)

                        # print('')
                        # FRIENDLY
                        # print("     extensions: ", cert_details.extensions)

                        # print("     extensions: ", cert_details.extensions[''])

                        # print("     version: ", cert_details.version)
                        # print("     public_key: ", cert_details.public_key)
                        # print("     signature_algorithm_oid: ", cert_details.signature_algorithm_oid)
                        # print("     signature: ", cert_details.signature)

                        # print("     Thumbprint: ", fingerprint_string.lower())
                        # print("     Serial Number: ", hex(cert_details.serial_number).replace("0x", ""))
                        # print("     Issued (UTC): ", cert_details.not_valid_before)
                        # print("     Expiry (UTC): ", cert_details.not_valid_after)
                        # print(cert.get_name())
                        # print(cert.enhanced_keyusage_names())
                        # print(cert.enhanced_keyusage())
                        # print(cert.get_encoded())
                        # print(cert.get_encoded())
                        # print(cert.cert_type)
                        # print(cert.enhanced())
                        # print(cert.get_pem())
                        # time.sleep(1)

                        # san = cert_details.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
                        # names = san.get_values_for_type(x509.DNSName)
                        # print("     SAN(s): ", names)

                        # cert_usages = cert_details.extensions.get_extension_for_oid(ExtensionOID.EXTENDED_KEY_USAGE).value._usages
                        # print("     Usage(s): ", cert_usages)

                        emissor = '"ISSUER":' + repl_issuer
                        #emissor = '{' + repl_issuer + '}'
                        requerente = '"SUBJECT":' + repl_sub
                        #requerente = '{' + repl_sub + '}'

                        padrao_json = '{"pattern":"https://*","filter":{' + requerente + ',' + emissor + '}}'
                        #print(f'            padrao_json: {padrao_json}')

                        #leitura_json = json.loads(padrao_json)
                        #requerente_CN = leitura_json['filter']['SUBJECT']['CN']
                        #list_CN = requerente_CN.split(':')

                        #CNPJ = list_CN[-1]

                        linha_final = cnpj + ';' + padrao_json
                        with open(filename, 'a', encoding="utf-8") as f:
                            f.write(linha_final + '\n')
                            f.close()


                        #time.sleep(2)
                    else:
                        print(f' CNPJ:"{cnpj}" =  NÃO adiciona "{cert.get_name()}" ao json ')
                        # time.sleep(2)


            #linha_final2 = ''
            #with open(filename, 'a') as f:
            #    f.write(linha_final2 + '\n')
            #    f.close()
        else:

            # #### Linux

            os.system = 'certutil -d sql:$HOME/.pki/nssdb -L'
            os.system = 'certutil -d sql:$HOME/.pki/nssdb -K'
            # exemplo de saida:
            # certutil: Checking token "NSS Certificate DB" in slot "NSS User Private Key and Certificate Services"
            # < 0> rsa      03917ed9da81e37543a148f9763f0159f85858d9   teste02
            # < 1> rsa      af3a5a979251b275ce23a53077e0028fdfdf438f   enio ricardo de farias:05852252905 2022-11-11 18:00:19
            # < 2> rsa      124163b9a98ce709a472f11955278c211464ab38   MAK SERVICOS E PAVIMENTACOES LTDA13137265000188
            # < 3> rsa      5bd84f88a7a58cae9c7b0fc1f04329895bd03cf1   DEL FUEGO HAMBURGUERIA LTDA31537106000152
            # < 4> rsa      52bb7e8fdfe717b70145289b9e8f6c2990558adc   LUCIANO MORO67062300063
            # < 5> rsa      97f5a88874fc8e1619867fc20d7f3f35b4ffdc94   KUCHAK COMERCIAL DE ALIMENTOS EIRELI92607571000107

            comando_linux = '$HOME/.config/google-chrome/Default/Preferences'

            # #####################################


            self.printa('info', "This only works on a Windows System.")
            linha_final2 = '0001;ERROR: This only works on a Windows System.'
            with open(filename, 'w', encoding="utf-8") as file:
                file.write('{}\n'.format(linha_final2))
                file.close()

            #with open(filename, 'a') as f:
            #    f.write(linha_final2 + '\n')
            #    f.close()
        home_do_user_windows = os.path.expanduser('~')  # print::: 'C:\\Users\\eniod'
        #userwin=os.getlogin().upper()
        #pc=socket.gethostname().upper()

        self.printa('info', f'\n"{userwin}" terminou de coletar os Certificados digitais da maquina "{pc}" \n_____________________________________\n\n')

        #time.sleep(3)


    def generator_json_certutil_digital_certificate_windows(self, filename):
        #filename = 'teste.json'

        #print(f'filename: {filename}')

        comando = 'certutil -user -store My'
        result = subprocess.getoutput(comando)
        resultado = result.encode('utf-8').decode('utf-8')
        # .replace('\n', ' ').strip('\n').strip(' ').replace('  ', ' ')

        # print(f'xxxxxxxxxxxxxxxx\n{resultado}\nxxxxxxxxxxxxxxxxxxxx')

        xxxresultado = ''' 
        My "Pessoal"
        ================ Certificado 0 ================
        Número de Série: 6f8c4a4ff
        Emissor: CN=teste teste teste4-01, O=4teste, L=florianopolis, S=santa-catarina, C=BR
         NotBefore: 11/11/2022 09:55
         NotAfter: 08/11/2032 09:55
        Requerente: CN=teste teste one4-01, O=one4teste, L=florianopolis, S=santa-catarina, C=BR
        Assinatura coincide com Chave pública
        Certificado raiz: requerente coincide com o emissor
        Hash Cert(sha1): cf5438921
        Nenhuma informação de provedor de chave
        Não é possível localizar o certificado e a chave privada para decodificação.
    
        ================ Certificado 1 ================
        Número de Série: 720
        Emissor: CN=AC ONLINE BRASIL v5, OU=Autoridade Certificadora VALID - AC VALID v5, O=ICP-Brasil, C=BR
         NotBefore: 08/06/2022 10:39
         NotAfter: 08/06/2023 10:39
        Requerente: CN=MEDICINA DO TRABALHO LTDA, OU=15199, OU=VALID, OU=Pessoa Juridica A1, OU=AC ONLINE BRASIL, O=ICP-Brasil, L=GOVERNADOR VALADARES, S=MG, C=BR
        Certificado não raiz
        Hash Cert(sha1): c8954c
        Nenhuma informação de provedor de chave
        Não é possível localizar o certificado e a chave privada para decodificação.
    
        ================ Certificado 2 ================
        Número de Série: 62b5f
        Emissor: CN=AC ONLINE RFB v5, OU=Secretaria da Receita Federal do Brasil - RFB, O=ICP-Brasil, C=BR
         NotBefore: 11/03/2022 16:40
         NotAfter: 11/03/2023 16:40
        Requerente: CN=M3 SISTEMAS LTDA:0000145, OU=15199, OU=Presencial, OU=AR E-UTIL TECNOLOGIA E SEGURANCA, OU=RFB e-CNPJ A1, OU=Secretaria da Receita Federal do Brasil - RFB, O=ICP-Brasil, L=GOVERNADOR VALADARES, S=MG, C=BR
        Certificado não raiz
        Hash Cert(sha1): c8b4cb
        Nenhuma informação de provedor de chave
        Não é possível localizar o certificado e a chave privada para decodificação.
    
        ================ Certificado 3 ================
        Número de Série: 2b1b
        Emissor: CN=AC Certisign RFB G5, OU=Secretaria da Receita Federal do Brasil - RFB, O=ICP-Brasil, C=BR
         NotBefore: 11/11/2022 18:00
         NotAfter: 11/11/2023 18:00
        Requerente: CN=ENIOS:0505, OU=(em branco), OU=RFB e-CPF A1, OU=Secretaria da Receita Federal do Brasil - RFB, OU=0155475, OU=VideoConferencia, O=ICP-Brasil, C=BR
        Certificado não raiz
        Hash Cert(sha1): 9921ef162ce3
          Contêiner da chave = enio ricardo de farias:05 2022-11-11 18:00:19
          Nome de contêiner exclusivo: fc1c
          Provider = Microsoft Enhanced Cryptographic Provider v1.0
        Êxito no teste de criptografia
    
        ================ Certificado 4 ================
        Número de Série: 02145
        Emissor: CN=62596a
         NotBefore: 11/11/2022 03:38
         NotAfter: 11/11/2023 15:38
        Requerente: CN=62fd8d3c8c596a
        Assinatura coincide com Chave pública
        Certificado raiz: requerente coincide com o emissor
        Hash Cert(sha1): 4cd1b
          Contêiner da chave = ceb1
          Nome de contêiner exclusivo: 5d4c9c1c
          Provider = Microsoft Software Key Storage Provider
        A chave privada NÃO é exportável
        Teste de assinatura aprovado
    
        ================ Certificado 5 ================
        Número de Série: 5a3b
        Emissor: CN=47684
         NotBefore: 11/11/2022 03:38
         NotAfter: 11/11/2023 15:38
        Requerente: CN=479a3943b684
        Assinatura coincide com Chave pública
        Certificado raiz: requerente coincide com o emissor
        Hash Cert(sha1): 04ae2d3eb6f
          Contêiner da chave = 85574f2
          Nome de contêiner exclusivo: 0447d9c1c
          Provider = Microsoft Software Key Storage Provider
        A chave privada NÃO é exportável
        Teste de assinatura aprovado
        CertUtil: -store : comando concluído com êxito.
    
        Process finished with exit code 0
    
        '''

        resultadox = '''
        CertUtil: -store : comando concluído com êxito.
        '''

        resultado = resultado  # .replace('  ', ' ').replace('\n ', '').strip(' ')

        resultado = resultado.split('\n')

        # print(resultado)
        count = 1

        count_certificates = -1

        dict_certificados = {}

        for linha in resultado:
            # print(f'lendo linha ({count}): ->"{linha}"<- ')

            linha = linha.strip(' ').strip('\n')

            regex2 = r"CertUtil*"
            if re.match(regex2, linha):
                # print(f'ACABOU: linha ({count}): ->"{linha}"<- ')
                break

            else:
                regex = r"^==="
                if re.match(regex, linha):
                    count_certificates += 1
                    list_dados_certificado = []  # print(f'lendo linha ({count}): ->"{linha}"<- ')

                if count_certificates >= 0 and not re.match(regex, linha):
                    # print(f'if linha ({count}): ->"{linha}"<- ')
                    list_dados_certificado.append(linha)
                    dict_certificados[f'Certificado_{count_certificates}'] = list_dados_certificado

            count += 1

        len_dict = len(dict_certificados)
        self.printa('debug', f'len_dict: {len_dict}')

        # print(dict_certificados)

        if len_dict > 0:
            f = open(filename, "w+", encoding="utf-8")
            f.close()

        for dict_da_vez in dict_certificados:
            self.printa('debug', dict_da_vez)
            # nome_dic = dict_da_vez
            diciionario = dict_certificados[dict_da_vez]
            # print(diciionario)
            len_list_dict = len(diciionario)
            self.printa('debug', f'len_list_dict: {len_list_dict}')

            requerente = ''
            emissor = ''

            for valor_list in diciionario:
                valor_list = valor_list.replace('  ', ' ').replace('  ', ' ')
                # print(f'valor_list: {valor_list}')
                if 'Issuer:'.upper() in valor_list.upper() or 'Emissor:'.upper() in valor_list.upper():

                    repl = '"ISSUER":{"'

                    subs1 = 'Issuer: '
                    compiled1 = re.compile(re.escape(subs1), re.IGNORECASE)
                    valor_list = compiled1.sub(repl, valor_list)

                    subs2 = 'Emissor: '
                    compiled2 = re.compile(re.escape(subs2), re.IGNORECASE)
                    valor_list = compiled2.sub(repl, valor_list)

                    repl3_igual = '":"'
                    subs3_igual = '='
                    compiled3_igual = re.compile(re.escape(subs3_igual), re.IGNORECASE)
                    valor_list = compiled3_igual.sub(repl3_igual, valor_list)

                    repl4_virg = '", "'
                    subs4_virg = ', '
                    compiled4_virg = re.compile(re.escape(subs4_virg), re.IGNORECASE)
                    valor_list = compiled4_virg.sub(repl4_virg, valor_list)

                    valor_list = valor_list + '"}'

                    # print(f'ISSUER: -->{valor_list}<--')
                    emissor = valor_list



                elif 'Subject:'.upper() in valor_list.upper() or 'Requerente:'.upper() in valor_list.upper():
                    repl = '"SUBJECT":{"'

                    subs1 = 'Subject: '
                    compiled1 = re.compile(re.escape(subs1), re.IGNORECASE)
                    valor_list = compiled1.sub(repl, valor_list)

                    subs2 = 'Requerente: '
                    compiled2 = re.compile(re.escape(subs2), re.IGNORECASE)
                    valor_list = compiled2.sub(repl, valor_list)

                    repl3_igual = '":"'
                    subs3_igual = '='
                    compiled3_igual = re.compile(re.escape(subs3_igual), re.IGNORECASE)
                    valor_list = compiled3_igual.sub(repl3_igual, valor_list)

                    repl4_virg = '", "'
                    subs4_virg = ', '
                    compiled4_virg = re.compile(re.escape(subs4_virg), re.IGNORECASE)
                    valor_list = compiled4_virg.sub(repl4_virg, valor_list)

                    valor_list = valor_list + '"}'

                    # print(f'SUBJECT: {valor_list}')
                    requerente = valor_list

            # print(f'emissor    = {emissor}')
            # print(f'requerente = {requerente}')

            padrao_json = '{"pattern":"https://*","filter":{' + emissor + ',' + requerente + '}}'
            self.printa('debug', f'padrao_json: {padrao_json}')

            leitura_json = json.loads(padrao_json)
            requerente_CN = leitura_json['filter']['SUBJECT']['CN']
            list_CN = requerente_CN.split(':')

            CNPJ = list_CN[-1]

            linha_final = CNPJ + ';' + padrao_json
            with open(filename, 'a', encoding="utf-8") as f:
                f.write(linha_final + '\n')
                f.close()
            # print(f'requerente_CN: {requerente_CN}')
            self.printa('debug', f'linha_final: {linha_final}')

            self.printa('debug', '--------\n')

        self.printa('debug', '\n\nfim')

        # HINT: "ISSUER":{"CN":"AC ONLINE RFB v5", "O": "ICP-Brasil", "OU": "Secretaria da Receita Federal do Brasil - RFB"},
        #      "SUBJECT":{"CN":"M3 SISTEMAS DE INFORMATICA LTDA:07070596000145", "L": "GOVERNADOR VALADARES", "O": "ICP-Brasil"}

    def extract_json_infos(self, input_json):



        df = pd.json_normalize(input_json)
        df = df.sort_values(['IdCert', 'IdCli'])
        #print(f'----df------\n{df}\n----------')
        return df

    def delete_certificate(self):
        #x = 0
        #if x > 0:
        sub_key = r'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
        empty_json = ''
        try:
            path = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            # print(f'----path1------\n{path}\n----------')

            #winregg = winreg.OpenKey(path, sub_key, 0, winreg.KEY_ALL_ACCESS)
            #print(f'----winregg------\n{winregg}\n----------')

            with winreg.OpenKey(path, sub_key, 0, winreg.KEY_ALL_ACCESS) as key:
            #with winreg.OpenKey(path, sub_key) as key:
                # print(f'----key------\n{key}\n----------')
                #winreg.SetValueEx(key, '1', 0, winreg.REG_SZ, empty_json)
                winreg.SetValueEx(key, '1', 0, winreg.REG_SZ, '0')
                winreg.CloseKey(winreg.HKEY_LOCAL_MACHINE)

        except FileNotFoundError:
            self.printa('error', 'Arquivo não encontrado!')

    def select_certificate(self, df):
        #df = pd.json_normalize(input_json)
        df = df.sort_values(['IdCert', 'IdCli'])
        # print(f'----df2------\n{df}\n----------')
        self.delete_certificate()
        sub_key = r'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
        n_certificate = ''
        certificado_status = 'Certificado não instalado'
        try:
            with open(f'{self.dir_certificado}/certificate_json.txt', encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                # print(f'----csv_reader------\n{csv_reader}\n----------')
                for pos, value in df.iterrows():
                    # print(f'----pos------\n{pos}\n----------')
                    # print(f'----value------\n{value}\n----------')
                    #vvalue = self.cnpj14digits(value['IdCert'])
                    #nn_certificate = self.cnpj14digits(n_certificate)

                    # print(f'----n_certificate------\n{n_certificate}\n----------')
                    if value['IdCert'] != n_certificate:
                        # print(f'-------value[IdCert]-------\n{value["IdCert"]}\n-------')
                    #if vvalue != nn_certificate:
                        v=value
                        #value=self.cnpj14digits(value['IdCert'])
                        #print(f'----value v------\n{v}\n----------')
                        #n_certificate = self.cnpj14digits(value['IdCert'])
                        n_certificate = self.cnpj14digits(value['IdCert'])
                        # print(f'----n_certificate------\n{n_certificate}\n----------')

                        for row in csv_reader:
                            # print(f'----row------\n{row}\n----------')
                            #if self.cnpj14digits(n_certificate) == self.cnpj14digits(row[0]):

                            # print(f'----row[0]------\n{row[0]}\n----------')

                            if n_certificate == row[0] and row[0] != '':
                                # print(f'----n_certificate------\n{n_certificate}\n----------')
                                json_certificate = row[1]  # faz a troca aqui
                                # print(f'----json_certificate------\n{json_certificate}\n----------')
                                try:
                                    path = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                                    # print(f'----path------\n{path}\n----------')

                                    #key = winreg.OpenKey(path, sub_key, 0, winreg.KEY_ALL_ACCESS)
                                    #print(f'key: {key}')
                                    #valuex = winreg.QueryValueEx(key, '1')
                                    #print(f'valuex: {valuex}')

                                    #winreg.SetValueEx(key, '1', 0, winreg.REG_SZ, json_certificate)
                                    #winreg.SetValueEx(key, '1', 0, winreg.KEY_ALL_ACCESS, json_certificate)
                                    #winreg.CloseKey(winreg.HKEY_LOCAL_MACHINE)



                                    #print(f'fim json_certificate: {json_certificate}\n-----x-----x---x----x----')
                                    with winreg.OpenKey(path, sub_key, 0, winreg.KEY_ALL_ACCESS) as key:
                                    #with winreg.OpenKey(path, sub_key) as key:
                                        #print(f'----keyA------\n{key}\n----------')
                                        winreg.SetValueEx(key, '1', 0, winreg.REG_SZ, json_certificate)
                                        winreg.CloseKey(winreg.HKEY_LOCAL_MACHINE)
                                    certificado_status = 'Certificado OK'

                                    json_certificate_B = json_certificate.replace('{', '<br><br>{')
                                    linha_html = f'<html><body><center><h1>Abrindo certificado CNPJ: {row[0]}</h1></center><br><p>{json_certificate_B}</p></body></html>'
                                    ffile_html = f'{self.dir_certificado}/html.html'
                                    file_html = os.path.abspath(ffile_html)
                                    # print(f'file_html: {file_html}')
                                    with open(file_html, 'w', encoding="utf-8") as file:
                                        file.write('{}'.format(linha_html))
                                        file.close()

                                    break
                                #except FileNotFoundError:
                                except Exception as e:
                                    err = f'{e}'.replace('\n', ' ')
                                    self.printa('error', f'Erro Open001 no certificado: {err}')
                                    certificado_status = 'Erro no certificado: ' + err
                                    #return 'Arquivo não encontrado!'

                            else:
                                certificado_status = 'certificado Null'
        except Exception as e:
            err = f'{e}'.replace('\n', ' ')
            self.printa('error', f'Erro no certificado: {err}')
            certificado_status = 'Erro no certificado: ' + err

        return certificado_status

    def ler_arquivo_para_lista(self, filename):
        f = open(filename)
        lines = f.read().splitlines()
        #print(f'lendo lines={lines}')
        f.close()
        # time.sleep(0.2)
        return lines

    def select_certificate_direct(self, idcert):
        #df = pd.json_normalize(input_json)
        #df = df.sort_values(['IdCert', 'IdCli'])
        # print(f'----df2------\n{df}\n----------')
        self.delete_certificate()
        sub_key = r'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
        n_certificate = ''

        certificado_status = 'Certificado não instalado'
        certificado_status = False

        try:
            csv_file = os.path.abspath(f'{self.dir_certificado}/certificate_json.txt')
            csv_list = self.ler_arquivo_para_lista(csv_file)

            # if idcert in csv_list:

            for linha in csv_list:
                    l_linha = linha.split(';')
                    self.printa('debug', f'a1 - l_linha:{l_linha}')
                    comp_l_linha = len(l_linha)
                    self.printa('debug', f'a2 - comp_l_linha:{comp_l_linha}')
                    if comp_l_linha > 0:

                        # numero_documento = l_linha[0]
                        # testa se é cnpj ou cpf

                        if self.cnpj_validate(self.cnpj14digits(l_linha[0])):
                            cnpj_linha = self.cnpj14digits(l_linha[0])
                        elif self.cpf_validate(self.cpf11digits(l_linha[0])):
                            cnpj_linha = self.cpf11digits(l_linha[0])
                        else:
                            cnpj_linha = l_linha[0]
                        self.printa('debug', f'cnpj_linha = {cnpj_linha}')
                        self.printa('debug', f'idcert     = {idcert}')
                        json_linha = l_linha[1]
                        self.printa('debug', f'json_linha = {json_linha}')

                        if cnpj_linha == idcert:
                            self.printa('info', f'muito bem, achou o CNPJ {idcert} na lista de certificados!!!')
                            try:
                                path = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                                with winreg.OpenKey(path, sub_key, 0, winreg.KEY_ALL_ACCESS) as key:
                                    winreg.SetValueEx(key, '1', 0, winreg.REG_SZ, json_linha)
                                    winreg.CloseKey(winreg.HKEY_LOCAL_MACHINE)
                                certificado_status = 'Certificado OK'
                                json_certificate_B = json_linha.replace('{', '<br><br>{')
                                linha_html = f'<html><body><center><h1>Abrindo certificado CNPJ: {cnpj_linha}</h1></center><hr><p>{json_certificate_B}</p><hr></body></html>'
                                ffile_html = f'{self.dir_certificado}/html.html'
                                file_html = os.path.abspath(ffile_html)
                                with open(file_html, 'w', encoding="utf-8") as file:
                                    file.write('{}'.format(linha_html))
                                    file.close()
                                self.printa('info', f'excelente, configurou o reg com o certificado do CNPJ {idcert} !!!')
                                certificado_status = f'SUCESSO: {idcert}'
                                certificado_status = True
                                # return True
                                break
                            except Exception as e:
                                err = f'{e}'.replace('\n', ' ')
                                self.printa('error', f'Erro Open001 no certificado: {err}')
                                linha_html = f'<html><body><center><h1>erro certificado CNPJ: {cnpj_linha}</h1></center><hr><p>{err}</p><hr></body></html>'
                                ffile_html = f'{self.dir_certificado}/html.html'
                                file_html = os.path.abspath(ffile_html)
                                with open(file_html, 'w', encoding="utf-8") as file:
                                    file.write('{}'.format(linha_html))
                                    file.close()
                                certificado_status = 'ERRO no certificado: ' + err
                                certificado_status = False

                        else:
                            #certificado_status = 'certificado Null'
                            self.delete_certificate()
                            certificado_status = f'lendo certificado instalado {cnpj_linha} >> ainda nao localizou o registro certo {idcert} instalado no Windows'
                            certificado_status = False
                            #return False

                        self.printa('debug', f'lendo linhas de certificados: {certificado_status}')
            # else:
            #     certificado_status = f'ERRO: nao localizou o registro {idcert} instalado no Windows'
            #     raise Exception(f'{certificado_status}')

        except Exception as e:
            err = f'{e}'.replace('\n', ' ')
            self.printa('critical', f'Erro no certificado: {err}')
            certificado_status = 'ERRO no certificado: ' + err
            certificado_status = False
            # return False

        return certificado_status

    def cnpj_validate(self, cnpj: str) -> bool:

        # numbers = str(numbers_x)

        LENGTH_CNPJ = 14
        if len(cnpj) != LENGTH_CNPJ:
            # print(f' {cnpj} não1 é CNPJ\n\n')
            return False

        if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
            # print(f' {cnpj} não2 é CNPJ\n\n')
            return False

        cnpj_r = cnpj[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1:i] != str(dv % 10):
                # print(f' {cnpj} não3 é CNPJ\n\n')
                return False
        self.printa('info', f' {cnpj}  é CNPJ!!!!!!!!!\n\n')
        return True


    # def cpf_validate(self, numbers_x):
    def cpf_validate(self, numbers: str) -> bool:

        # numbers = str(numbers_x)
        self.printa('info', ('\n\nvalidando teste se é CPF')
        numbers = int(self.somente_numeros(numbers))
        #print(f'numbersA: "{numbers}"')
        numbers = self.cpf11digits(self.somente_numeros(numbers))
        #print(f'numbersB: "{numbers}"')

        self.printa('info', (f'    verificando e validando se {numbers} é um cpf')

        #  Obtém os números do CPF e ignora outros caracteres
        cpf = [int(char) for char in numbers if char.isdigit()]

        #  Verifica se o CPF tem 11 dígitos
        if len(cpf) != 11:
            # print(f' {numbers} não1 é CPF\n\n')
            return False

        #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
        #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
        #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
        if cpf == cpf[::-1]:
            # print(f' {numbers} não2 é CPF\n\n')
            return False

        #  Valida os dois dígitos verificadores
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                # print(f' {numbers} não3 é CPF\n\n')
                return False

        self.printa('info', f' {numbers} É CPF !!!!!\n\n')
        return True


    def cpf11digits(self, cpf):
        return str('{:0>11}'.format(self.somente_numeros(cpf)))   #cpf com 11 digito e somente numeros (deve ser passado como string)


    def criar_registro_chrome_winreg(self, dire):

        # self.logger.debug('b00 1 criar_registro_chrome_winreg')

        sub_key = r'1'

        #key_to_read = r'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'
        raiz_reg = r'HKEY_LOCAL_MACHINE'
        key_to_read = r'SOFTWARE\Policies\Google\Chrome\AutoSelectCertificateForUrls'

        # self.logger.debug('b00 2 criar_registro_chrome_winreg')
        # a = sys.argv[0]
        # pat = os.path.abspath(a)
        # dire = os.path.dirname(a)
        full = os.path.join(dire, '02-create_new_registry_windows_runas.exe')

        temp001 = 'TMP'

        try:
            temp1 = os.path.join(temp001, 'temp.txt')
            f = open(temp1, "w+")
            f.close()
            if self.test_if_exist(temp1):
                self.printa('debug', f'temp1 {temp1} existe')
            else:
                raise Exception(f'temp1 {temp1} NÂO existe')

        except:
            temp1 = os.path.join(dire, 'temp.txt')
            f = open(temp1, "w+")
            f.close()

        finally:
            temp = os.path.abspath(temp1)
            os.remove(temp)

        try:
            self.printa('info', f'primeiro verifica se o registro existe')
            # self.logger.debug('b2')
            key = winreg.HKEY_LOCAL_MACHINE
            reg = winreg.ConnectRegistry(None, key)
            k = winreg.OpenKey(reg, key_to_read)
            # self.logger.debug('b3')
            self.printa('debug', f'registro lido: {k}')

            # self.logger.debug('b4')
            valuex = winreg.QueryValueEx(k, sub_key)
            self.printa('debug', f'valuex: {valuex}')
            self.printa('info', f'\nOK. Registro já existe')
            # criar = winreg.CreateKeyEx(k, sub_keyB, reserved=0, access=winreg.KEY_WRITE)  # criar = winreg.CreateKeyEx(k, sub_keyB, reserved=0, access=winreg.KEY_ALL_ACCESS)  # criar = winreg.CreateKeyEx(k, sub_keyB, reserved=1, access=winreg.REG_SZ)  # criar = winreg.CreateKeyEx(k, sub_keyB, reserved=1, access=winreg.KEY_ALL_ACCESS)
            # self.logger.debug('b5')
            erro_hkey = False

        except Exception as e:
            # self.logger.debug('b6')
            self.printa('error', f'erro registro não encontrado: {e}')
            erro_hkey = True

        self.printa('debug', f'b7 - erro_hkey={erro_hkey}')

        if erro_hkey:
            try:
                self.printa('info', f'\nIniciando tentativa de criar o registro. È necessário ter permissão de ADMIN')
                # ASADMIN = 'asadmin'
                # user = sys.argv[-1]
                # userb = sys.argv[1:]
                # if sys.argv[-1] != ASADMIN:

                # fulli = f' open {full} '

                script = full
                paqms2 = f'-k "{raiz_reg}\\{key_to_read}" -s "{sub_key}" -t "REG_SZ" -v "0" -f "{temp}"'
                self.printa('debug', f'paqms2:     {paqms2}      ')
                params = ' '.join([paqms2])

                # HINT: http://timgolden.me.uk/pywin32-docs/shell__ShellExecuteEx_meth.html
                result = shell.ShellExecuteEx(lpVerb='runas', nShow=win32con.SW_SHOWNORMAL, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpFile=f'{script}', lpParameters=params)

                procHandle = result['hProcess']
                obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
                rc = win32process.GetExitCodeProcess(procHandle)
                f = open(temp)
                lines = f.read()
                self.printa('debug', f'lines: {lines}')
                f.close()
                linhas = lines.replace('\n', ' ').strip('\n').strip(' ')

                self.printa('info', f'Resultado: {linhas}')

            except Exception as e:
                self.printa('critical', f'erro ao criar registro usando system: {e}')

    def test_if_exist(self, file):
        from pathlib import Path
        import os

        #path = Path(os.path.abspath("README.mdx"))
        path = Path(os.path.abspath(file))
        self.printa('debug', f'path={path}')

        if path.exists():
            return True
        else:
            return False


# bot = Certificate()
