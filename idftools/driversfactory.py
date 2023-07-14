# -*- coding: utf-8 -*-
#coding: utf-8
import sys
sys.path.append("..")
import io, re, string, os
import time
#import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
import configparser
#from src.util.utilities2 import Utilities
from utilities import Utilities
import sys
import os
# import undetected_chromedriver as uc

from webdriver_manager.chrome import ChromeDriverManager

class DriverFactory:


    #HINT: set another dir to chrome:  https://stackoverflow.com/questions/45500606/set-chrome-browser-binary-through-chromedriver-in-python



    '''
    Retorna webdriver
    Parâmetros: chrome, firefox, phantomjs
    '''
    # def create_driver(self, type, headless=False):
    #     self.create_driver(type, headless, None)


    # def create_driver(self, type, headless=False, path_to_download=None, install_extension=None, largura=1440, altura=900):
    def create_driver(self, type, headless=False, path_to_download=None, install_extension=None, largura=800, altura=800, kiosk=False, nome_robo_exec='bot', robo_pid_exec='0', logger=None, cert_digital=False, path_cert_digital=None, senha_cert_digital=None, list_url_cert_digital=[], scale_factor=1):
        try:

            # print(f'cert_digital={cert_digital}')
            # print(f'path_cert_digital={path_cert_digital}')
            # print(f'path_cert_digital={senha_cert_digital}')

            # print('driver001')
            # print(f'driver001 type={type}')
            # print(f'driver001 headless={headless}')
            # print(f'driver001 path_to_download={path_to_download}')
            # print(f'driver001 install_extension={install_extension}')
            # print(f'driver001 largura={largura}')
            # print(f'driver001 altura={altura}')
            # print(f'driver001 kiosk={kiosk}')
            # print(f'driver001 nome_robo_exec={nome_robo_exec}')
            # print(f'driver001 robo_pid_exec={robo_pid_exec}')
            # print(f'driver001 logger={logger}')
            # print(f'driver001 util={util}')

            # util = Utilities()
            # util = Utilities(sys.argv[0], os.getpid(), test_config_dir_direto=True, logger=logger)

            # if util == '':
            #     util = Utilities(nome_robo_exec=nome_robo_exec, robo_pid_exec=robo_pid_exec, test_config_dir_direto=True, logger=logger)

            # print('driver002')
            # config = util.get_config()
            # config = configparser.ConfigParser()
            # config.read('config/config.ini')

            # print(f'path_to_download = {path_to_download}')
            # print('driver003')

            # try:
            #     dir_extensions = config['extensions_chrome']['dir_extensions']
            #     # print(f'create_driver: dir_extensions={dir_extensions}')
            # except Exception as e:
            #     # print(f'create_driver: DEU erro no dir_extensions: {e}')
            #     dir_extensions = ''
            #
            # try:
            #     extensions_to_install = config['extensions_chrome']['extensions_to_install']
            #     # print(f'create_driver: extensions_to_install={extensions_to_install}')
            #
            #
            # except Exception as e:
            #     # print(f'create_driver: DEU erro no extensions_to_install: {e}')
            #     extensions_to_install = ''

            if type == 'chrome' or type == '':
                # print('chrome 001')
                capabilities = {}

                # DesiredCapabilities
                # capabilities = DesiredCapabilities.chrome();
                # capabilities.setCapability("chrome.switches", Arrays.asList("--ignore-certificate-errors"))

                chrome_options = Options()
                chrome_options.add_argument('log-level=1')
                # chrome_options.add_argument(f'"{path_to_download}"')

                # chrome_options.add_argument("--user-data-dir=chrome-data")
                # chrome_options.add_argument("--user-data-dir="+path_to_download)

                chrome_options.add_argument("--ignore-certificate-errors")
                capabilities['acceptSslCerts'] = True
                capabilities['acceptInsecureCerts'] = True

                # chrome_options.add_argument('--profile-directory='+path_to_download)
                # chrome_options.add_argument("--incognito")

                # chrome_options.add_argument("--disable-extensions")
                # chrome_options.add_experimental_option("profile.default_content_settings.popups", 0)
                # chrome_options.add_experimental_option("download.prompt_for_download", "false")
                # chrome_options.add_experimental_option("download.default_directory", path_to_download)
                # chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
                # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
                # chrome_options.add_experimental_option("prefs", {"download.default_directory": r"C:\Users\xxx\downloads\Test", "download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled": True})
                # chrome_options.add_experimental_option("prefs", {"download.default_directory": path_to_download, "download.prompt_for_download": False, "download.directory_upgrade": True, "safebrowsing.enabled": True})

                chrome_options.add_argument('--allow-running-insecure-content')

                # chrome_options.add_argument('--safebrowsing-disable-download-protection')
                # chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')

                # chrome_options.add_argument("enable-automation")

                chrome_options.add_argument('disable-infobars')

                chrome_options.add_argument("--disable-login-animations")
                chrome_options.add_argument("--disable-notifications")
                chrome_options.add_argument("--disable-default-apps")

                chrome_options.add_argument("--no-sandbox")

                # chrome_options.add_argument("--dns-prefetch-disable")
                # chrome_options.add_argument("--dns-prefetch-disable")

                # chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

                # mobile_emulation = {"deviceName": "Nexus 5"}
                # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                # print('chrome 002')

                if cert_digital and len(list_url_cert_digital) > 0:
                    print('entrou no cert digital')
                    qtde_list_url_cert_digital = len(list_url_cert_digital)

                    chrome_options.add_argument("--ssl-client-certificate-file=" + path_cert_digital)
                    # chrome_options.add_argument("--ssl-client-certificates-dir=" + path_cert_digital)
                    chrome_options.add_argument("--ssl-version-min=tls1.2")
                    chrome_options.add_argument("--ssl-client-key-passphrase=" + senha_cert_digital)

                    chrome_options.add_experimental_option('prefs', {'required_client_certificate_for_user': path_cert_digital})

                    if qtde_list_url_cert_digital > 1:
                        chrome_options.add_argument("--auto-select-certificate-for-urls=" + ",".join(list_url_cert_digital))
                    elif qtde_list_url_cert_digital == 1:
                        url_um_cert = list_url_cert_digital[0]
                        chrome_options.add_argument("--auto-select-certificate-for-urls=" + url_um_cert)
                    else:
                        # self.logger.error(f'erro ao tentar abrir urls {list_url_cert_digital} com certificado digital')
                        print(f'erro ao tentar abrir urls {list_url_cert_digital} com certificado digital')
                else:
                    print('chrome normal')
                    # print('chrome 003')
                    # Configuração para ceitar qualquer certificados
                    # capabilities = DesiredCapabilities.CHROME.copy()

                    capabilities['acceptSslCerts'] = True
                    capabilities['acceptInsecureCerts'] = True  # print('create_driver: chrome 004')

                # time.sleep(5)

                if False:
                #if install_extension == True:
                    try:
                        list_extensions_to_install = extensions_to_install.split(';')
                        # print(f'create_driver: list_extensions_to_install: {list_extensions_to_install}')
                        qtde_extensions_to_install = len(list_extensions_to_install)
                        while qtde_extensions_to_install > 0:
                            valor_indice = qtde_extensions_to_install - 1
                            # print(f'create_driver: instalando Extensão local {list_extensions_to_install[valor_indice]}')
                            # chrome_options.add_extension('Save-to-Pocket_v3.0.0.11.crx')
                            chrome_options.add_extension(f'{dir_extensions}/{list_extensions_to_install[valor_indice]}')
                            # print(f'create_driver: Instalado! Extensão local {dir_extensions}/{list_extensions_to_install[valor_indice]}')
                            # time.sleep(2)
                            qtde_extensions_to_install -= 1

                    except Exception as e:
                        # print(f'create_driver: DEU erro if install_extension: {e}')
                        print('')

                # chrome_options.add_argument('window-size=800,800');
                # chrome_options.add_argument('window-size=1000,900');
                # chrome_options.add_argument(f'window-position=-{largura},1')
                chrome_options.add_argument(f'window-position=0,0')
                chrome_options.add_argument(f'window-size={largura},{altura}')

                if kiosk == True:
                    chrome_options.add_argument("--start-maximized")
                    chrome_options.add_argument("--kiosk")  ##esse é muito interessante para colocar no raspberry e na tv

                # chrome_options.add_experimental_option('useAutomationExtension', False)
                # chrome_options.add_experimental_option('excludeSwitches', ['load-extension', 'enable-automation'])

                # chrome_options.add_argument('--shm-size')  # enio 30/10/2020
                chrome_options.add_argument('--ignore-gpu-blocklist')  # enio 06/06/2023
                chrome_options.add_argument('--disable-gpu-driver-bug-workarounds')  # enio 06/06/2023
                chrome_options.add_argument('--disable-impl-side-painting')  # enio 30/10/2020
                chrome_options.add_argument('--disable-accelerated-2d-canvas')  # enio 30/10/2020
                chrome_options.add_argument('--disable-accelerated-jpeg-decoding')  # enio 30/10/2020
                chrome_options.add_argument('--no-sandbox')  # enio 30/10/2020
                chrome_options.add_argument('--test-type=ui')  # enio 30/10/2020

                chrome_options.add_argument('--force-device-scale-factor=1')

                chrome_options.add_argument(f'--force-device-scale-factor={scale_factor}')

                chrome_options.add_argument('--dns-prefetch-disable')
                chrome_options.add_argument('--always-authorize-plugins')
                chrome_options.add_argument('--aggressive-cache-discard')
                chrome_options.add_argument('--disable-cache')
                chrome_options.add_argument('--disable-application-cache')
                chrome_options.add_argument('--disable-offline-load-stale-cache')
                chrome_options.add_argument('--disk-cache-size=1000')
                chrome_options.add_argument('--no-proxy-server')

                chrome_options.add_argument('--disable-dev-shm-usage')  # 3nio
                chrome_options.add_argument("--ignore-certificate-errors")  #

                if headless == True:
                    # chrome_options.add_argument('window-size=1000,900');
                    # chrome_options.add_argument(f'window-size={largura},{altura}')
                    chrome_options.add_argument("headless")
                    # chrome_options.add_argument("disable-gpu") #
                    # chrome_options.add_argument("--test-type") #enio
                    # chrome_options.add_argument('--no-sandbox') #enio
                    # chrome_options.add_argument('--disable-dev-shm-usage') #3nio
                    # chrome_options.add_argument('--use-gl=swiftshader') #
                    # chrome_options.add_argument("--ignore-certificate-errors")#
                    # chrome_options.add_argument('--disable-popup-blocking')    #add enio
                    chrome_options.add_argument('--disable-gpu')  # add enio #  # chrome_options.add_argument('--disable-gpu-sandbox')  # enio 30/10/2020  # chrome_options.binary_location = config['drivers']['chrome_path']  # print('create_driver: chrome 005 headless true')

                prefs = {}
                # Add preferências para não exibit PDF viewer
                prefs["download.prompt_for_download"] = False
                prefs["plugins.always_open_pdf_externally"] = True
                prefs["profile.default_content_setting_values.notifications"] = 2

                prefs["profile.password_manager_enabled"] = False
                prefs["credentials_enable_service"] = False

                prefs["download.default_directory"] = path_to_download
                prefs["download.directory_upgrade"] = True
                prefs["safebrowsing.enabled"] = True

                if not path_to_download is None:
                    # print('chrome 006')
                    # print('create_driver: Iniciando chrome em path alternativo:' + path_to_download)
                    prefs['download.default_directory'] = path_to_download
                    prefs['download.prompt_for_download'] = False  # print('create_driver: chrome 007')

                # print('create_driver: chrome 008')
                chrome_options.add_experimental_option('prefs', prefs)

                # chromepath = os.path.abspath(config['drivers']['chrome_path'])

                # print(f'create_driver: chrome 009 chromepath={chromepath}')  # driver = webdriver.Chrome(chromepath, chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.  # print('create_driver: chrome 009b')  # driver = webdriver.Chrome(executable_path=chromepath,chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.

                # mobile_emulation = {"deviceName": "Nexus 5"}  # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

                # driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=chrome_options.to_capabilities())

                # print(f'create_driver: chrome 009c chromepath={chromepath} / chrome_options={chrome_options} / capabilities={capabilities}')

                # driver = webdriver.Chrome(executable_path=chromepath, chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.


                # chromepath = os.path.abspath(config['drivers']['chrome_path'])


                # print(f'create_driver: chrome 009 chromepath={chromepath}')
                #driver = webdriver.Chrome(chromepath, chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.
                # print('create_driver: chrome 009b')
                #driver = webdriver.Chrome(executable_path=chromepath,chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.



                # mobile_emulation = {"deviceName": "Nexus 5"}
                # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

                # driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=chrome_options.to_capabilities())

                # print(f'create_driver: chrome 009c chromepath={chromepath} / chrome_options={chrome_options} / capabilities={capabilities}')


                # driver = webdriver.Chrome(executable_path=chromepath, chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.

                chromepath = ChromeDriverManager().install()
                print(f'chromepath: {chromepath}')
                # time.sleep(1)
                # comando_perl = f'perl -pi -e "s/cdc_/abc_/g" {chromepath}'

                # saida_comando = os.popen(comando_perl)
                # print(f'saida_comando: {saida_comando}')

                pathc = os.path.abspath(chromepath)
                print(f'pathc={pathc}')
                try:
                    # replacement = "akl_roepstdlwoeproslP0weos".encode()
                    replacement = "akl_roepstdlwoeproslPOweos".encode()
                    print(f'replacement={replacement}')
                    # print(f'replacement: {replacement}')
                    with io.open(pathc, "r+b") as fh:
                        print('dentro do io')
                        for line in iter(lambda: fh.readline(), b""):
                            print(f'dentro for line: ')
                            if b"cdc_" in line:
                                print(f'dentro if cdc line:')
                                fh.seek(-len(line), 1);
                                newline = re.sub(b"cdc_.{22}", replacement, line);
                                fh.write(newline);
                                print("linha cdc_ encontrada e alterada com sucesso")
                except Exception as e:
                    print(f'ERROR: no cdc: {e}')
                print('criando driver')
                driver = webdriver.Chrome(executable_path=pathc, chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.
                print('depois driver')
                # driver = uc.drivera

                # driver.get('https://supervisao.com.vc/')

                # time.sleep(1)

                # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options, desired_capabilities=capabilities)  # Optional argument, if not specified will search path.

                # print('create_driver: chrome 0010 carregado driver')
                # try:
                #     print('\n\n\n------\n-------\nchrome position window: ini')
                #
                #     # driver.Manage().Window.Position = new System.Drawing.Point(2000, 1)
                #     # driver.Manage().Window.Maximize();
                #
                #     # time.sleep(2)
                #     # driver.set_window_position(300, 0)
                #     # time.sleep(2)
                #     # # driver.maximize_window()
                #     # time.sleep(2)
                #     # driver.set_window_position(-1200, 0)
                #     # time.sleep(2)
                #     # #driver.maximize_window()
                #     # # time.sleep(2)
                #     # # driver.set_window_position(100, 100)
                #     # # time.sleep(2)
                #     # driver.set_window_size(largura, altura)
                #     print('chrome position window: fim\n------\n-------\n\n\n')
                #     time.sleep(2)
                # except Exception as e:
                #     print(f'\n\n\n------\n-------\n\n\nerro chrome position window: {e}')
                #     time.sleep(20)

                #print('chrome 010')
                try:
                    # print('create_driver: chrome 0011a vai tentar if headless == True')
                    if False:
                        if headless == True:
                            # print('create_driver: chrome 0011b dentro if headless == True')
                            # print('create_driver: chrome 011 headless true')
                            driver.command_executor._commands["send_command"] = (
                                "POST",
                                '/session/$sessionId/chromium/send_command')
                            params = {
                                'cmd': 'Page.setDownloadBehavior',
                                'params': {
                                    'behavior': 'allow',
                                    'downloadPath': path_to_download
                                }
                            }
                            driver.execute("send_command", params)
                    # print('create_driver: chrome 0011c saiu if headless == True')


                    # print('create_driver: chrome 012')
                except Exception as e:
                    # print(f'create_driver: erro no if headless == True POST - {e}')
                    print('')

                # print('create_driver: chrome 0013 vai para return driver')
                return driver

            elif type == 'firefox':
                    #print('chrome 013')
                    # firefoxpath = config['drivers']['firefox_path']
                    firefoxpath = ''
                    driver = webdriver.Firefox(firefoxpath)
                    return driver

            elif type == 'phantomjs':
                    # phantomjspath = config['drivers']['phantomjs_path']
                    phantomjspath = ''
                    driver = webdriver.PhantomJS(phantomjspath)
                    return driver

        except Exception as e:
            print(f'create_driver: DEU erro ao criar driver {e}')
            print('')
