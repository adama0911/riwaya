import os
import sys
import time
import datetime

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


FILE_FOLD= "./files_fold/"
REQUESTS_FOLD= FILE_FOLD + "requests_fold/"
RESPONCES_FOLD= FILE_FOLD + "responses_fold/"
HANDLE_FOLD= FILE_FOLD + "handle_fold/"
NEXT_REAUEST_FILE= FILE_FOLD + "./nextRequestFile.txt"
LOGS_FOLD= "./logs/"

class Connexion:
    
    def __init__(self,driver):
        self.driver = driver
        self.m_login = ""
        self.m_pwdLevel1  = ""
        self.m_pwdLevel2  = ""

        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//title"))
            )
            self.driver.get_screenshot_as_file('modal-ok-page-principale.png')
            print("Load Website------------------------------------------------[OK]")
        except TimeoutException:
            print("Load Website------------------------------------------------[NO]")

    def login(self):
        log = self.driver.find_element_by_xpath('//*[@placeholder="Identifiant"]')

        if log:
            log.clear()
            log.send_keys(self.m_login)
            print("Connexion: find element => Login input ---------------------[OK]")
        else:
            print("Connexion: find element => Login input ---------------------[NO]")
            return 1

        psw = self.driver.find_element_by_xpath('//*[@placeholder="Mot de Passe"]')

        if psw:
            psw.clear()
            psw.send_keys(self.m_pwdLevel1)
            self.driver.get_screenshot_as_file('main-page-post-saisie.png')
            psw.send_keys(Keys.RETURN)
            print("Connexion: find element => Password input ------------------[OK]")
        else:
            print("Connexion: find element => Password input ------------------[NO]")
            return 1

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']//descendant::span[text()='Paramètres de connexion incorrects']"))
            )
            error = self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']//descendant::span[text()='Paramètres de connexion incorrects']")
            print("Login Level 1: find element => Password input ------------------[NO]")
            print(error.text) 
            return 0
        except TimeoutException:
            print("Login Level 1: find element => Password input ------------------[OK]")
            self.driver.get_screenshot_as_file('main-page-post-validation.png')
            pwd = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noheader z-window-highlighted z-window-shadow']//descendant::input")

            if pwd:
                pwd.clear()
                pwd.send_keys(self.m_pwdLevel2)
                print("Login Level 2: find element => Password input ----------[OK]")
                self.driver.get_screenshot_as_file('modal-pwd-second-level.png')
            else:
                print("Login Level 2: find element => Password input ----------[NO]")  

            validation_btn = self.driver.find_element_by_xpath('//div[@class="z-div"]/button')

            if validation_btn:
                print("Login Level 2: find element => Validation Button -------[OK]")
                validation_btn.click()
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']//descendant::div[@class='z-messagebox-icon z-messagebox-information z-div z-div']"))
                    )
                    
                    print("Login Level 2:--------------------------------------[NO]")

                    print("----------------Votre Compte sera bloquer apres 3 essaies--------------------------")
                    
                    print("---------------------------Connexion is bad ! ----------------------")
                    
                    return 1
                except TimeoutException:
                    print("Login Level 2:--------------------------------------[OK]")
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='z-listcell-content'][text()='Guichetier de  Distributeur']"))
                    )

                    print("Connexion: =========================================[OK]")
                    self.driver.get_screenshot_as_file('modal-pwd-second-level-post-validation.png')
                    return 0
                
            else:
                print("Login Level 2: find element => Validation Button -------[NO]")
                return 1
    
    def logout (self):
        return 0

    def choiceGuichetier(self):
        
        guichetierChoice = self.driver.find_element_by_xpath("//div[@class='z-listcell-content'][text()='Guichetier de  Distributeur']")

        if guichetierChoice:
            print(" choiceGuichetier: find element => guichetier  Button ----------------------------------[OK]")
            guichetierChoice.click()
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//tr[@class='z-row z-grid-odd']//descendant::div[@class='z-listcell-content']"))
                )
                self.driver.get_screenshot_as_file('modal-post-choix-typeCompte.png')
                print(" choiceGuichetier:----------------------------------[OK]")
                return 0

            except TimeoutException:
                print(" choiceGuichetier:----------------------------------[NO]")
                return 1

        else:
            print("Modal choice guichetier: find element => guichetier  Button ----------------------------------[NO]")
            return 1

    def chooseDistrib (self):

        distribToChoose = self.driver.find_element_by_xpath("//tr[@class='z-row z-grid-odd']//descendant::div[@class='z-listcell-content']")

        if distribToChoose:
            print("ChooseDistrib: Location element => location  Button ----------------------------------[OK]")
            distribToChoose.click()
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='messagebox-btn z-button'][text()='OK']"))
                )
                print("ChooseDistrib: ----------------------------------[OK]")
                self.driver.get_screenshot_as_file('modal-ok-page-principale.png')
                return 0
            except TimeoutException:
                print("ChooseDistrib: ----------------------------------[NO]")
                return 1
        else:
            print("ChooseDistrib: Location element => location  Button ----------------------------------[NO]")
            return 1
    
    def geolocalisation (self):
        geoloc = self.driver.find_element_by_xpath("//button[@class='messagebox-btn z-button']")
    
        if geoloc:
            geoloc.click()
            print("geolocalisation: Location's permissions => Ok  Button ----------------------------------[OK]")
        
            try:
                WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((By.XPATH,"//div[@class='z-window-header z-window-header-move']/div[@class='z-window-icon z-window-close']/i[@class='z-icon-times']")))
                print("geolocalisation: ----------------------------------[OK]")
                return 0
            except TimeoutException:
                print("geolocalisation: ----------------------------------[NO]")
                return 1

        else:
            print("geolocalisation: Location's permissions => Ok  Button -------[NO]")
            return 1
        
        
class Client:
      
      def __init__(self):
          self.m_nom=""
          self.m_prenom=""
          self.m_addresse=""
          self.m_cellulaire=""
          self.m_typePiece=""
          self.m_numeroPiece=""
          self.m_numeroPiece=""
          self.m_pays=""
          self.m_dateDelivrance=""
          self.m_dateValidite=""


class Envoyeur(Client):
    
    def __init__(self):
        self.m_montant="50"
        self.m_motif=""
        self.m_modePaiement=""

class Beneficiaire(Client):
    def __init__(self):
        self.m_modeReception=""

class Operations:

    def __init__(self,driver):
        self.driver = driver
        self.m_menuItems = self.driver.find_elements_by_xpath("//a[@class='btn btn-success z-toolbarbutton' or @class='btn z-toolbarbutton btn-primary' or @class='btn z-toolbarbutton btn-success']")
        self.m_caissier = Client()
        self.requestNumber= 0
        self.request = ""
        self.response= ""
        self.requesthandle= ""
        self.responsehandle= ""
        
    def jeuxEtMedia(self):
        self.m_menuItems[9].click()

        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[1]"))
            )

            print("jeuxEtMedia: Loaded ---------------------------------[OK] ")
            pays = "Senegal"
            self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[1]/option[text()='"+ pays +"']").click()

            partenaire = "Cash Chrono"
            self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[2]/option[text()='"+ partenaire +"']").click()

            section = "Depot"
            self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[3]/option[text()='"+ section +"']").click()

            if section=="Valider Ticket":
                inputs = self.driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
                #Numero de Telephone *
                numero_de_telephone = "774356654"
                inputs[0].send_keys(numero_de_telephone)

                #Saisir 5 numero en 1 et 50
                num1 = "1"
                inputs[1].send_keys(num1)
                num2 = "2"
                inputs[2].send_keys(num2)
                num3 = "3"
                inputs[3].send_keys(num3)
                num4 = "4"
                inputs[4].send_keys(num4)
                num5 = "5"
                inputs[5].send_keys(num5)

                tirage = "2 Tirage"
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[4]/option[text()='"+ tirage +"']").click()
            elif section=="Depot":
                numero_de_telephone  = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[1]")
                numero_de_telephone.send_keys("232323")
            
                montant_du_depot  = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[@class='z-doublebox']")
                montant_du_depot.send_keys("232323")
            

            rechercher = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']//descendant::button[text()='Recherche']")
            print(rechercher.text)


        except TimeoutException:
            print("jeuxEtMedia: Loaded ---------------------------------[NO] ")

    def abonnemantTV(self):
        self.m_menuItems[3].click()

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='z-div'][1]//descendant::select[1]"))
        )

        #Choisir un pays de destination
        pays = "Senegal"
        self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='z-div'][1]//descendant::select[1]/option[text()='"+ pays +"']").click()
        #Selectionnez un facturier

        facturier = "CANAL"

        self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='z-div'][1]//descendant::select[2]/option[text()='"+ facturier +"']").click()

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[1]"))
        )

        if( facturier=="CANAL"):
            inputs = self.driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
            inputs[0].send_keys("2323")
            inputs[1].send_keys("2323")

        if( facturier=="Excaf"):
            inputs = self.driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
            #Num Abonne *
            num_abonne = "2323"
            inputs[0].send_keys(num_abonne)
            #Formule Abonnement *
            formule_abonnement = "2323"
            inputs[1].send_keys(formule_abonnement)
            #Montant
            montant = "500"
            inputs[2].send_keys(montant)
            #Nom *
            nom  = "Goudiaby"
            inputs[3].send_keys(nom)
            #Prenom *
            prenom  = "adama"
            inputs[4].send_keys(prenom)
            #Numero de Telephone *
            tel  = "77665533"
            inputs[5].send_keys(tel)

        if( facturier=="DSTV"):
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[@class='z-datebox-input']"))
            )

            time.sleep(5)
            inputs = self.driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
            #Numero de Police *
            num_police = "2323"
            inputs[0].send_keys(num_police)
            #Montant*
            montant = "2000"
            inputs[1].send_keys(montant)
            #Nom
            nom = "Goudiaby"
            inputs[2].send_keys(nom)
            #Date Echeance
            date_echeance  = "10 oct. 2018"
            inputs[3].send_keys(date_echeance)
            #Numero Abonne
            numero_abonne  = "123"
            inputs[4].send_keys(numero_abonne)
            #Prenom
            prenom  = "Adama"
            inputs[5].send_keys(prenom)
            #Numero Facture
            numero_facture  = "234"
            inputs[6].send_keys(numero_facture)
            #Numero Abonne
            numero_de_telephon  = "776543212"
            inputs[7].send_keys(numero_de_telephon)
            #pays
            pays  = "Senegal"
            inputs[8].send_keys(pays)

            
        #Num Abonne suivi des cinq derniers chiffres du numero de la carte 

        recherche = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::button")

        print(recherche.text)
        # print(len(select_items))
    
    def envoi(self,envoyeur,beneficiaire,resquestNumber):

        self.m_menuItems[6].click()
        time.sleep(1)
        self.m_menuItems[5].click() #click in "envoi" tag

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='z-auxheader-content']"))
        )

        #Get html elements 

        self.driver.find_elements_by_xpath("//select[@class='z-select']")
        inputs_items_envoi = self.driver.find_elements_by_xpath("//input[@class='z-textbox']")
        montant_envoyeur = self.driver.find_element_by_xpath("//input[@class='z-doublebox']")
        inputs_dates_cni_envoyeur = self.driver.find_elements_by_xpath("//input[@class='z-datebox-input']")
        radios_mode = self.driver.find_elements_by_xpath("//input[@type='radio']")
        

        #----------------Choisir un pays de destination-----------------    

        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Senegal']").click()
        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Senegal']").send_keys(Keys.RETURN)
    

        inputs_items_envoi[0].clear()
        inputs_items_envoi[0].send_keys(envoyeur.m_nom)

            # set "prenom"
        inputs_items_envoi[1].clear()
        inputs_items_envoi[1].send_keys(envoyeur.m_prenom)
            # set "adresse"
        inputs_items_envoi[2].clear()
        inputs_items_envoi[2].send_keys(envoyeur.m_addresse)
            # set "cellulaire"
        inputs_items_envoi[3].clear()
        inputs_items_envoi[3].send_keys(envoyeur.m_cellulaire)
        #-------------Information Piece-----------
            # set "type de piece"
        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='"+ envoyeur.m_typePiece +"']").click()
        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Passeport']").send_keys(Keys.RETURN)

            # set "Pays"
        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='"+ envoyeur.m_pays +"']").click()
        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Samoa']").send_keys(Keys.RETURN)
            #set "date de délivrance"
        inputs_dates_cni_envoyeur[0].send_keys(envoyeur.m_dateDelivrance)
            #set "date de validité"
        inputs_dates_cni_envoyeur[1].send_keys(envoyeur.m_dateValidite)
            #set  "Numero CNI"
        inputs_items_envoi[4].clear()
        inputs_items_envoi[4].send_keys(envoyeur.m_numeroPiece)
            #set  "Montant"
        montant_envoyeur.clear()
        montant_envoyeur.send_keys(envoyeur.m_montant)
            #set  "Choix du motif"
        self.driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='"+ envoyeur.m_motif +"']").click()

            #set "mode de d'envoi"
        if(envoyeur.m_modePaiement=="Espèce"):
            radios_mode[6].click()
        elif(envoyeur.m_modePaiement=="Carte"):
                radios_mode[7].click()
                self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::select[1]//descendant::option[text()='Wari']").click()
                numero_carte = self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::select[1]//following::input")
                numero_carte.send_keys("1234")
                self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::select[2]//descendant::option[text()='Compte courant']").click()            
        elif(envoyeur.m_modePaiement=="Wari pass"):
                radios_mode[8].click()
                wari_secure = self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-textbox']")
                wari_secure.send_keys("1234")
        elif(envoyeur.m_modePaiement=="Voucher"):
                radios_mode[9].click()	
                partenaire = self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-combobox-input']")
                partenaire.send_keys("1234")
                Code_voucher = self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-combobox-input']//following::input")
                Code_voucher.send_keys("1234")
                Cellulaire = self.driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-combobox-input']//following::input//following::input")
                Cellulaire.send_keys("1234")
        elif(envoyeur.m_modePaiement=="Wallet"):
                radios_mode[10].click()
                """
                    is not reachable by keyboard
                """
            # partenaire

        #--------------------Receveur-----------------
            # nom
        inputs_items_envoi[5].clear()
        inputs_items_envoi[5].send_keys(beneficiaire.m_nom)
            # prenom
        inputs_items_envoi[6].clear()
        inputs_items_envoi[6].send_keys(beneficiaire.m_prenom)
            # adresse
        inputs_items_envoi[7].clear()
        inputs_items_envoi[7].send_keys(beneficiaire.m_addresse)
            # cellulaire
        inputs_items_envoi[8].clear()
        inputs_items_envoi[8].send_keys(beneficiaire.m_cellulaire)

            # mode de reception
        if(beneficiaire.m_modeReception=="Espèce"):
            radios_mode[2].click()
        elif(beneficiaire.m_modeReception=="Wallet"):
            radios_mode[3].click()
            #Partenaire
            partenaire = self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']")
            partenaire.clear()
            partenaire.send_keys("3434")
            partenaire.send_keys(Keys.RETURN)
            #celulllaire
            cellulaire = self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']//following::input")
            cellulaire.clear()
            cellulaire.send_keys("+221775645645")
            cellulaire.send_keys(Keys.RETURN)
        elif(beneficiaire.m_modeReception=="Compte"):
            radios_mode[4].click()
            #Partenaire
            partenaire = self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']")
            partenaire.clear()
            partenaire.send_keys("3434")
            partenaire.send_keys(Keys.RETURN)
            #numero compte
            """
                is not reachable by keyboard
            """
            numero_compte = self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']//following::input")
            self.driver.execute_script("arguments[0].setAttribute('value', '12345')", numero_compte)
            print(numero_carte.get_property("value"))
            # self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", numero_compte, '23232');
            # numero_compte.send_keys(Keys.RETURN)
        elif(beneficiaire.m_modeReception=="Carte"):
            radios_mode[5].click()
            #Type Carte
            T_Carte = "Wari"
            self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::select[1]/option[text()='"+T_Carte +"']").click()
            #Numero Carte
            numero_carte = self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::select[1]//following::input")
            numero_carte.send_keys("2323")
            #Type compte
            t_compte = "Compte courant"
            self.driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::select[2]/option[text()='"+ t_compte +"']").click()


        time.sleep(2)

        self.driver.find_element_by_xpath("//button[@class='z-button'][text()='Executer']").click()
        
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='z-button'][text()='Valider']"))
        )

        self.driver.find_element_by_xpath("//button[@class='z-button'][text()='Valider']").click()
        
        time.sleep(5)


        #-------- Success


        if self.driver.window_handles[1]:
            window_before = self.driver.window_handles[0]
            window_after = self.driver.window_handles[1]

            self.driver.switch_to_window(window_after)
                #conde envoi
            code_envoi =  self.driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr/th").text
            print(code_envoi)
            codet = code_envoi.split(' ')
            code = ""+ codet[0]+codet[1]+codet[2]
            self.response = ""+code
            # self.saveResponse(resquestNumber,str(resquestNumber)+'['+code)
            # numero =  self.driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr//following::tr/th").text
            # print(numero)

            # montant_envoyer =  self.driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr//following::tr//following::tr/td").text
            # print(montant_envoyer)
            # commissions_ttc =  self.driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr//following::tr//following::tr//following::tr/td").text
            # print(commissions_ttc)
            # body = self.driver.find_element_by_xpath("//body")
            self.driver.close()
            self.driver.switch_to_window(window_before)
            print("-------------"+ self.response + "-----------------")
            return ""+ code

        #-------- Unsuccess

        else:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']"))
            )

            #error =  self.driver.find_element_by_xpath("//span[@class='z-label'][text()='Solde insuffisant.']")

            self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()
            
            #print(error.text)
  
    def retraitSuite(self,typeRetrait,code,retrait_or_remboursement,resquestNumber,benefInfoSup):
        envoyeur  = Envoyeur()
        beneficiaire  = Beneficiaire()
        self.m_menuItems[5].click()
        time.sleep(1)
        self.m_menuItems[6].click()

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Quel est le code Wari :']"))
        )
        retrait_radios = self.driver.find_elements_by_xpath("//input[@type='radio']")
        
        typeretrait="Code Wari"

        if(typeretrait=="Code Wari"):
            retrait_radios[0].click()

            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//input[@class='z-textbox']"))
            )
            code_re = code
            self.driver.find_element_by_xpath("//input[@class='z-textbox']").send_keys(code_re)
            
            retrait_or_remboursement = "Retrait"

            if(retrait_or_remboursement=="Retrait"):
                retrait_radios[2].click()
                self.driver.find_element_by_xpath("//button[@class='z-button'][text()='Rechercher']").click()
            
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/div[@class='z-hlayout z-valign-middle']/div[@class='z-hlayout-inner']//descendant::span"))
                    )
                    error_text =  self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/div[@class='z-hlayout z-valign-middle']/div[@class='z-hlayout-inner']//descendant::span").text
                    print(error_text)
                    ok_error = self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/table//descendant::button")
                    ok_error.click()
                except TimeoutException:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::textarea"))
                    )

                    inputs_retireur =  self.driver.find_elements_by_xpath("//input[@class='z-textbox']")


                    self.m_caissier.m_nom= "Goudiaby"
                    self.m_caissier.m_prenom= "Adama"

                    #Nom retireur
                    nom_retireur = "Goudiaby"
                    inputs_retireur[1].send_keys(nom_retireur)
                    #Prenom retireur
                    prenom_retireur = "Adama"
                    inputs_retireur[2].send_keys(prenom_retireur)

                    inputs_envoyeur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::input")
                    inputs_receveur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::input")

                    print("----------------------infos envoyeur-------------------")
                    
                    #nom envoyeur

                    envoyeur.m_nom = inputs_envoyeur[0].get_property("value")
                    #prenom envoyeur
                    envoyeur.m_prenom = inputs_envoyeur[1].get_property("value")
                    #cellulaire envoyeur
                    envoyeur.m_cellulaire = inputs_envoyeur[2].get_property("value")
                    #montant envoyeur
                    envoyeur.m_montant = inputs_envoyeur[3].get_property("value")
                    #adresse envoyeur
                    envoyeur.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::textarea").get_property("value")

                    print("----------------------infos Receveur-------------------")

                    #nom receveur
                    beneficiaire.m_nom = inputs_receveur[1].get_property("value")
                    # #prenom receveur
                    beneficiaire.m_prenom = inputs_receveur[2].get_property("value")
                    #cellulaire receveur
                    beneficiaire.m_cellulaire = inputs_receveur[3].get_property("value")
                    #adresse receveur
                    beneficiaire.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::textarea").get_property("value")
                    
                    #Tel receveur
                    print(benefInfoSup)
                    beneficiaire.m_numeroPiece = benefInfoSup[1]
                    inputs_receveur[4].send_keys(beneficiaire.m_numeroPiece)
                    #type de piece
                    beneficiaire.m_typePiece= benefInfoSup[0]
                    self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::select[1]/option[text()='"+ beneficiaire.m_typePiece +"']").click()
                    #pays receveur
                    beneficiaire.m_pays= benefInfoSup[2]
                    self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::select[2]/option[text()='"+ beneficiaire.m_pays +"']").click()
                    #Date de délivrance
                    beneficiaire.m_dateDelivrance = benefInfoSup[3]
                    inputs_receveur[5].send_keys(beneficiaire.m_dateDelivrance)
                    #Date de validité
                    beneficiaire.m_dateValidite  = benefInfoSup[4]
                    inputs_receveur[6].send_keys(beneficiaire.m_dateValidite)


                    btn_validation_retrait = self.driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Valider']")
                    btn_annulation_retrait = self.driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Annuler']")

                    btn_validation_retrait.click()
                    
                    time.sleep(5)


                    if self.driver.window_handles[1]:
                        window_before = self.driver.window_handles[0]
                        window_after = self.driver.window_handles[1]
                        self.driver.switch_to_window(window_after)

                        #conde envoi
                        code_retrait =  self.driver.find_element_by_xpath("//body/fieldset[2]//descendant::legend[text()='Transaction']//following::table/tbody/tr/th//following::th").text
                        print(code_retrait)
               
                        
                        #self.saveResponse(resquestNumber,'2['+ str(resquestNumber)+'['+code_re[0]+code_re[1]+code_re[2])
                        self.driver.close()
                        self.driver.switch_to_window(window_before)
                        resp = "2["+ str(resquestNumber)+ "[" + code_retrait
                        self.response = "" + resp
                        return resp

                    return 1

            if(retrait_or_remboursement=="Remboursement"):
                retrait_radios[3].click()

                self.driver.find_element_by_xpath("//button[@class='z-button'][text()='Rechercher']").click()
            
                time.sleep(5)

                inputs_envoyeur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::input")
                inputs_receveur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][2]//descendant::input")

                print("----------------------infos envoyeur-------------------")
                
                #nom envoyeur
                envoyeur.m_nom = inputs_envoyeur[0].get_property("value")
                #prenom envoyeur
                envoyeur.m_prenom = inputs_envoyeur[1].get_property("value")
                #cellulaire envoyeur
                envoyeur.m_cellulaire = inputs_envoyeur[2].get_property("value")
                #montant envoyeur
                envoyeur.montant = inputs_envoyeur[3].get_property("value")
                #adresse envoyeur
                envoyeur.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::textarea").get_property("value")
                #numero cni
                beneficiaire.m_numeroPiece = benefInfoSup[1]
                envoyeur.m_numeroPiece = inputs_envoyeur[4].get_property("value")
                #Date de délivrance
                envoyeur.m_dateDelivrance = benefInfoSup[3]
                inputs_envoyeur[5].send_keys(envoyeur.m_dateDelivrance)
                #Date de validité
                envoyeur.m_dateValidite = benefInfoSup[4]
                inputs_envoyeur[6].send_keys(envoyeur.m_dateValidite)
                #pays envoyeur
                envoyeur.m_pays= benefInfoSup[2]
                self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::select[2]/option[text()='"+ envoyeur.m_pays +"']").click()
                #type de piece
                envoyeur.m_typePiece= benefInfoSup[0]
                self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::select[1]/option[text()='"+ envoyeur.m_typePiece +"']").click()

                print("----------------------infos Receveur-------------------")

                #nom receveur
                beneficiaire.m_nom = inputs_receveur[0].get_property("value")
                # #prenom receveur
                beneficiaire.m_prenom = inputs_receveur[1].get_property("value")
                #cellulaire receveur
                beneficiaire.m_cellulaire = inputs_receveur[2].get_property("value")
                #adresse receveur
                beneficiaire.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][2]//descendant::textarea").get_property("value")


                btn_validation_retrait = self.driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Valider']")
                print(btn_validation_retrait.text)
                btn_annulation_retrait = self.driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Annuler']")
                print(btn_annulation_retrait.text)
                
      
    def retrait (self,typeRetrait,code,retrait_or_remboursement,resquestNumber):
        envoyeur  = Envoyeur()
        beneficiaire  = Beneficiaire()

        self.m_menuItems[5].click()
        time.sleep(1)
        self.m_menuItems[6].click()

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Quel est le code Wari :']"))
        )

        retrait_radios = self.driver.find_elements_by_xpath("//input[@type='radio']")
        
        typeretrait="Code Wari"

        if(typeretrait=="Code Wari"):
            retrait_radios[0].click()

            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//input[@class='z-textbox']"))
            )
            code_re = code
            self.driver.find_element_by_xpath("//input[@class='z-textbox']").send_keys(code_re)
            
            retrait_or_remboursement = "Retrait"

            if(retrait_or_remboursement=="Retrait"):
                retrait_radios[2].click()
                self.driver.find_element_by_xpath("//button[@class='z-button'][text()='Rechercher']").click()
            
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/div[@class='z-hlayout z-valign-middle']/div[@class='z-hlayout-inner']//descendant::span"))
                    )
                    error_text =  self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/div[@class='z-hlayout z-valign-middle']/div[@class='z-hlayout-inner']//descendant::span").text
                    print(error_text)
                    ok_error = self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/table//descendant::button")
                    ok_error.click()
                except TimeoutException:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::textarea"))
                    )

                    inputs_retireur =  self.driver.find_elements_by_xpath("//input[@class='z-textbox']")


                    self.m_caissier.m_nom= "Goudiaby"
                    self.m_caissier.m_prenom= "Adama"

                    #Nom retireur
                    nom_retireur = "Goudiaby"
                    inputs_retireur[1].send_keys(nom_retireur)
                    #Prenom retireur
                    prenom_retireur = "Adama"
                    inputs_retireur[2].send_keys(prenom_retireur)

                    inputs_envoyeur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::input")
                    inputs_receveur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::input")

                    print("----------------------infos envoyeur-------------------")
                    
                    #nom envoyeur

                    envoyeur.m_nom = inputs_envoyeur[0].get_property("value")
                    #prenom envoyeur
                    envoyeur.m_prenom = inputs_envoyeur[1].get_property("value")
                    #cellulaire envoyeur
                    envoyeur.m_cellulaire = inputs_envoyeur[2].get_property("value")
                    #montant envoyeur
                    envoyeur.m_montant = inputs_envoyeur[3].get_property("value")
                    #adresse envoyeur
                    envoyeur.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::textarea").get_property("value")

                    print("----------------------infos Receveur-------------------")

                    #nom receveur
                    beneficiaire.m_nom = inputs_receveur[1].get_property("value")
                    # #prenom receveur
                    beneficiaire.m_prenom = inputs_receveur[2].get_property("value")
                    #cellulaire receveur
                    beneficiaire.m_cellulaire = inputs_receveur[3].get_property("value")
                    #adresse receveur
                    beneficiaire.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::textarea").get_property("value")

                    data = "2["+ envoyeur.m_prenom+"[" + envoyeur.m_nom+"["+ envoyeur.m_cellulaire+"["+ envoyeur.m_addresse+"["+  envoyeur.m_montant  +"["+beneficiaire.m_prenom+"["+ beneficiaire.m_nom+"["+ beneficiaire.m_addresse+"["+ beneficiaire.m_cellulaire
                    
                    self.requesthandle = data + "]" + "2" +"["+ typeretrait + "[" + code + "[" + retrait_or_remboursement
                    #self.saveretrait(resquestNumber,data)
                    
            if(retrait_or_remboursement=="Remboursement"):
                retrait_radios[3].click()

                self.driver.find_element_by_xpath("//button[@class='z-button'][text()='Rechercher']").click()
            
                time.sleep(5)

                inputs_envoyeur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::input")
                inputs_receveur = self.driver.find_elements_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][2]//descendant::input")

                print("----------------------infos envoyeur-------------------")
                
                #nom envoyeur
                envoyeur.m_nom = inputs_envoyeur[0].get_property("value")
                #prenom envoyeur
                envoyeur.m_prenom = inputs_envoyeur[1].get_property("value")
                #cellulaire envoyeur
                envoyeur.m_cellulaire = inputs_envoyeur[2].get_property("value")
                #montant envoyeur
                envoyeur.montant = inputs_envoyeur[3].get_property("value")
                #adresse envoyeur
                envoyeur.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::textarea").get_property("value")
                #numero cni
                envoyeur.m_numeroPiece = inputs_envoyeur[4].get_property("value")
                #Date de délivrance
                envoyeur.m_dateDelivrance = "20/09/2018"
                inputs_envoyeur[5].send_keys(envoyeur.m_dateDelivrance)
                #Date de validité
                envoyeur.m_dateValidite = "20/09/2018"
                inputs_envoyeur[6].send_keys(envoyeur.m_dateValidite)
                #pays envoyeur
                envoyeur.m_pays= "Sénégal"
                self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::select[2]/option[text()='"+ envoyeur.m_pays +"']").click()
                #type de piece
                envoyeur.m_typePiece= "Passeport"
                self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::select[1]/option[text()='"+ envoyeur.m_typePiece +"']").click()

                print("----------------------infos Receveur-------------------")

                #nom receveur
                beneficiaire.m_nom = inputs_receveur[0].get_property("value")
                # #prenom receveur
                beneficiaire.m_prenom = inputs_receveur[1].get_property("value")
                #cellulaire receveur
                beneficiaire.m_cellulaire = inputs_receveur[2].get_property("value")
                #adresse receveur
                beneficiaire.m_addresse = self.driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][2]//descendant::textarea").get_property("value")


                btn_validation_retrait = self.driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Valider']")
                print(btn_validation_retrait.text)
                btn_annulation_retrait = self.driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Annuler']")
                print(btn_annulation_retrait.text)
                
        elif(typeretrait=="Retrait avec moyen de paiement (carte,voucher, wari pass etc.)"):
            retrait_radios[1].click()
               
            client = Envoyeur()      
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//descendant::input[@type='text']"))
            )

            inputs =  self.driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::input")

            print(len(inputs))
            print("Yes")
            # Nom
            client.m_nom = "Goudiaby"
            # el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//descendant::input")
            inputs[0].clear()
            inputs[0].send_keys(client.m_nom)
            # Prenom
            client.m_prenom = "Adama"
            #el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//descendant::input")
            inputs[1].clear()
            inputs[1].send_keys(client.m_prenom)

            # Cellulaire
            client.m_cellulaire = "779807654"
            #el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//descendant::input")
            inputs[2].clear()
            inputs[2].send_keys(client.m_cellulaire)

            # Montant
            client.m_montant = "1000"
            #el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//descendant::input")
            inputs[3].clear()
            inputs[3].send_keys(client.m_montant)

            # Type de pièce
            client.m_typePiece = "Passeport"
            el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//descendant::select/option[text()='"+client.m_typePiece+"']")
            el.click()
            el.send_keys(Keys.RETURN)

            # NumeroPiece
            client.m_numeroPiece = "2324657679546"
            #el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input")
            inputs[4].clear()
            inputs[4].send_keys(client.m_numeroPiece)

            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button"))
            )

            self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()
            # pays
            client.m_pays = "Afghanistan"
            el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select/option[text()='"+client.m_pays+"']")
            el.click()
            el.send_keys(Keys.RETURN)

            # NumeroPiece
            client.m_dateDelivrance = "03/06/2010"
            #el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input")
            inputs[5].clear()
            inputs[5].send_keys(client.m_dateDelivrance)


            # NumeroPiece
            client.m_numeroPiece  = "03/06/2025"
            #el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input")
            inputs[6].clear()
            inputs[6].send_keys(client.m_numeroPiece)

            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button"))
            )
            
            self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()

            els =   self.driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::input[@type='radio']")

            time.sleep(2)

            client.m_modePaiement = "Wari pass"
            
            
            if client.m_modePaiement=="Carte":
                els[0].click()
                wari_secure = "zejz"
                el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-textbox']")
                el.send_keys(wari_secure)
                
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button"))
                )
                
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()

                valid = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
                print(valid.text)
                
                annu  = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
                print(annu.text)
            elif client.m_modePaiement=="Carte":
                els[1].click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select[1]/option[text()='Wari']").click()                
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select[1]//following::input").send_keys("3434343")        
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select[1]//following::input//following::select/option[text()='Compte courant']").click()        

                valid = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
                print(valid.text)
                
                annu  = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
                print(annu.text)
            elif client.m_modePaiement=="Voucher":
                els[2].click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']").send_keys("Wari")                
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']//following::input").send_keys("3434343")        
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']//following::input//following::input").send_keys("3434343")        
                
                valid = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
                print(valid.text)
                
                annu  = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
                print(annu.text)
            elif client.m_modePaiement=="Wallet":
                els[3].click()
                time.sleep(2)
                self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']").send_keys("Wari")
                el = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::tr[@class='z-row z-grid-odd']//following-sibling::tr//following-sibling::tr//descendant::input[@class='z-textbox']")
                
                self.driver.execute_script("arguments[0].setAttribute('value', '12345')", el)

                print(el.get_property("value"))

                valid = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
                print(valid.text)

                annu  = self.driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
                print(annu.text)


            # nom = self.driver.find_element_by_xpath("//input[@class='z-textbox z-textbox-invalid'][1]")
            # print(nom.get_property("class"))

    def getRequest(self,request,nextRequest_number):
        opp = request
        self.request = ''.join(opp)
        if(opp[0]=='1'):
            envoyeur = Envoyeur()
            beneficiaire = Beneficiaire()

            envoyeur.m_nom= opp[1]
            envoyeur.m_prenom= opp[2]
            envoyeur.m_addresse= opp[3]
            envoyeur.m_cellulaire= opp[4]
            envoyeur.m_typePiece= opp[5]
            envoyeur.m_pays= opp[6]
            envoyeur.m_dateDelivrance= opp[7]
            envoyeur.m_dateValidite= opp[8]
            envoyeur.m_montant= opp[9]
            envoyeur.m_motif= opp[10]
            envoyeur.m_modePaiement= opp[11]
            envoyeur.m_numeroPiece= opp[12]

            beneficiaire.m_nom= opp[13]
            beneficiaire.m_prenom= opp[14]
            beneficiaire.m_addresse= opp[15]
            beneficiaire.m_cellulaire= opp[16]
            beneficiaire.m_modeReception= opp[17]
            
            return [envoyeur,beneficiaire,nextRequest_number]
        elif(opp[0]=='2'):
            print('hé heé heeé')
            typeRetrait = opp[1]
            code    =   opp[2]
            retrait_or_remboursement    =   opp[3]
            return [typeRetrait,code,retrait_or_remboursement,nextRequest_number]
                
        return 1
    
    def getResponseHandleRetrait (self):
        numberNextRequest_file = open("nextRequest.txt",'r')
        nextRequest_number = int(numberNextRequest_file.read())
        numberNextRequest_file.close()
        print(nextRequest_number)
        path = "./handle_retrait_response/"+ str(nextRequest_number)+ ".txt"
        print(path)
        with open(path,"r") as f:
            # Indented - do whatever you want with the file
            request = f.read()
            f.close()

            opp = request.split('[')
            return [opp[0],opp[1],opp[2],opp[3],opp[4]]

        return 1

    def saveretrait(self,numberRequest,data):
        with open("./handle_retrait/"+ str(numberRequest) +".txt","w") as fResp:
            fResp.write(data)
            fResp.close()
            return 0
        return 1
    
    def saveResponse (self,numberRequest,responce):
        
        with open("./response_files/"+ str(numberRequest) +".txt","w") as fResp:
            fResp.write(responce)
            fResp.close()

            with open("nextRequest.txt",'w') as fNumb:
                num = int(numberRequest) + 1
                fNumb.write(str(num))
                fNumb.close()
                return 0
        return 1



def connexion(driver):
    con = Connexion(driver)
    con_stat = con.login()
    if con_stat==0:
        cg_stat = con.choiceGuichetier()
        if  cg_stat==0:
            cd_stat = con.chooseDistrib()
            if cd_stat==0:
                geo_stat = con.geolocalisation()
                if geo_stat==0:
                    return con.driver
    return 1

def envoiyer (opp,request,nextRequest_number):
    c = opp.getRequest(request,nextRequest_number)
    if(c != 1):
        env = c[0]
        ben = c[1]
        resquestNumber = c[2]
        opp.envoi(env,ben,resquestNumber)
    else:
        print("Pas de nouvelle transation")

def retirer (opp,request,nextRequest_number):
    c = opp.getRequest(request,nextRequest_number)
    if(c != 1):
        typeRetrait = c[0]
        code = c[1]
        retrait_or_remboursement = c[2]
        numberRequest = c[3]
        stat_retrait = opp.retrait(typeRetrait,code,retrait_or_remboursement,numberRequest)
        if(stat_retrait == 0):
            return 0
    else:
        print("Pas de nouvelle transation")
        return 1

def retirerSuite(opp,request,nextRequest_number,benefInfoSup):
    c = opp.getRequest(request,nextRequest_number)
    print(benefInfoSup)
    if(c != 1):
        typeRetrait = c[0]
        code = c[1]
        retrait_or_remboursement = c[2]
        numberRequest = c[3]
        opp.retraitSuite(typeRetrait,code,retrait_or_remboursement,numberRequest,benefInfoSup)

def jeuxEtMedia(opp):
    opp.jeuxEtMedia()

def abonnementTv(opp):
    opp.abonnemantTV()

    opp.jeuxEtMedia()
    
"""
if __name__=="__main__":

    if connexion()==0:
        print("Kon yes---------------------------")
        ser = "retrait"
        opp = Operations()
        if ser=="jeux et media":
            jeuxEtMedia(opp)
        elif ser=="retrait":
            retirer(opp)
        elif ser=="envoi":
            envoiyer(opp)
        elif ser=="abonnemant tv":
            abonnementTv(opp)

        time.sleep(60000)
"""