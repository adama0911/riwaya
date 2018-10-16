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

# Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.

#os.environ['MOZ_HEADLESS'] = '1'

# Select your Firefox binary.
binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)

# Start selenium with the configured binary.
driver = webdriver.Firefox(firefox_binary=binary)

print("Firefox has been launched ...")

# Visit this webpage. 
#driver.get("https://intoli.com/blog/running-selenium-with-headless-firefox/")


############################### LANCEMENT PAGE AUTHENTIFICATION WARI ###########################################
driver.get("https://www.warime.com/callmoney/checking.zul")

window_before = driver.window_handles[0]

print("warime has been launched ...")

# Grab the heading element from the response.

#heading_element = driver.find_element_by_xpath('//*[@id="heading-breadcrumbs"]')

#heading_element = driver.find_element_by_xpath('//*[@placeholder="Identifiant"]')

#heading_element = driver.find_element_by_xpath('//*[@class="panel-title"][1]')

heading_element = driver.find_element_by_tag_name('title')

driver.get_screenshot_as_file('main-page.png')

# Print the title in the terminal.
if heading_element:
    print(heading_element.get_property('textContent'))
else:
    print("Heading element not found!")

################################# SAISIE PARAMETRES D'ACCES ET VALIDATION POUR CONNEXION ############################################

heading_element_2 = driver.find_element_by_xpath('//*[@placeholder="Identifiant"]')

if heading_element_2:
    print(heading_element_2.get_property('placeholder'))
    heading_element_2.clear()
    heading_element_2.send_keys("AARRY409")
    print("Connexion: find element => Login input ----------------------------------[OK]")
else:
    print("Connexion: find element => Login input ----------------------------------[NO]")

heading_element_3 = driver.find_element_by_xpath('//*[@placeholder="Mot de Passe"]')

if heading_element_3:
    heading_element_3.clear()
    heading_element_3.send_keys("DAKAR2018")
    driver.get_screenshot_as_file('main-page-post-saisie.png')
    heading_element_3.send_keys(Keys.RETURN)
    print("Connexion: find element => Password input ----------------------------------[OK]")
else:
    print("Connexion: find element => Password input ----------------------------------[NO]")



##########################  TRAITEMENT REPONSE WARI APRES TENTATIVE DE CONNEXION ############################################

try:
    element_mask = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']//descendant::span[text()='Paramètres de connexion incorrects']"))
    )
    error = driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']//descendant::span[text()='Paramètres de connexion incorrects']")
    print(error.text)
except TimeoutException:
    element_mask = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "z-modal-mask"))
    )

    print("Modal Connexion : showing --------------------------------------[OK]")

    driver.get_screenshot_as_file('main-page-post-validation.png')

    secondLevel_PWD_element = driver.find_element_by_xpath("//div[@class='z-window z-window-noheader z-window-highlighted z-window-shadow']//descendant::input")
    
    if secondLevel_PWD_element:
        secondLevel_PWD_element.clear()
        secondLevel_PWD_element.send_keys("SERVICE2020")
        print("Modal Connexion: find element => Password input ----------------------------------[OK]")
    else:
        print("Modal Connexion: find element => Password input ----------------------------------[NO]")  


    driver.get_screenshot_as_file('modal-pwd-second-level.png')
   
    secondLevel_PWD_validBTN = driver.find_element_by_xpath('//div[@class="z-div"]/button')

    if secondLevel_PWD_validBTN:
        print("Modal Connexion: find element => Validation Button ----------------------------------[OK]")
        secondLevel_PWD_validBTN.click()
    else:
        print("Modal Connexion: find element => Validation Button ----------------------------------[NO]")

    try:
        element_mask = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']//descendant::div[@class='z-messagebox-icon z-messagebox-information z-div z-div']"))
        )
        print("----------------Votre Compte sera bloquer apres 3 essaies--------------------------")
        
        print("Modal Connexion: ===================================================================[NO]")
        print("---------------------------Connexion is bad ! ----------------------")

    except TimeoutException:
        second_element_mask = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='z-listcell-content'][text()='Guichetier de  Distributeur']"))
        )
        print("Connexion: ===================================================================[OK]")
        driver.get_screenshot_as_file('modal-pwd-second-level-post-validation.png')

        guichetierChoice = driver.find_element_by_xpath("//div[@class='z-listcell-content'][text()='Guichetier de  Distributeur']")

        if guichetierChoice:
            print("Modal choice guichetier: find element => guichetier  Button ----------------------------------[OK]")
            guichetierChoice.click()
        else:
            print("Modal choice guichetier: find element => guichetier  Button ----------------------------------[NO]")

        second_element_mask = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@class='z-row z-grid-odd']//descendant::div[@class='z-listcell-content']"))
        )
        

        driver.get_screenshot_as_file('modal-post-choix-typeCompte.png')
        
        distribToChoose = driver.find_element_by_xpath("//tr[@class='z-row z-grid-odd']//descendant::div[@class='z-listcell-content']")

        if distribToChoose:
            print("Modal choice guichetier: Location element => location  Button ----------------------------------[OK]")
            distribToChoose.click()
        else:
            print("Modal choice guichetier: Location element => location  Button ----------------------------------[NO]")


        home_element_mask = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='messagebox-btn z-button'][text()='OK']"))
        )
        
        driver.get_screenshot_as_file('modal-ok-page-principale.png')
        
        #geolocBTN = driver.find_element_by_xpath("//div[@class='z-window-header z-window-header-move']/div[@class='z-window-icon z-window-close']/i[@class='z-icon-times']")

        #geolocBTN.click()

        geoloc = driver.find_element_by_xpath("//button[@class='messagebox-btn z-button']")
    
        if geoloc:
            geoloc.click()
            print("Modal Geolocation: Location's permissions => Ok  Button ----------------------------------[OK]")
        else:
            print("Modal Geolocation: Location's permissions => Ok  Button ----------------------------------[NO]")

        
        full_home_element_mask = WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH,"//div[@class='z-window-header z-window-header-move']/div[@class='z-window-icon z-window-close']/i[@class='z-icon-times']")))

        
        driver.get_screenshot_as_file('full-page-principale.png')

        #deconnectBTN = driver.find_element_by_xpath("//i[@class='z-icon-power-off fa-3x']")

        #deconnectBTN.click()

        # retour_login_page_element_mask = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mot de Passe']"))
        # )

        driver.get_screenshot_as_file('de-retour-page-connexion.png')

        # get Menu buttons
        warim_menu_items = driver.find_elements_by_xpath("//a[@class='btn btn-success z-toolbarbutton']")

        """
        =========================================================================
        -------------- Jeux Et Medias ------------------------------------------------------
        """
        warim_menu_items[9].click()

        envoi_element_mask = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[1]"))
        )

        pays = "Senegal"
        driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[1]/option[text()='"+ pays +"']").click()

        partenaire = "Cash Chrono"
        driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[2]/option[text()='"+ partenaire +"']").click()

        section = "Depot"
        driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[3]/option[text()='"+ section +"']").click()

        if section=="Valider Ticket":
            inputs = driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
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
            driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::select[4]/option[text()='"+ tirage +"']").click()
        elif section=="Depot":
            numero_de_telephone  = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[1]")
            numero_de_telephone.send_keys("232323")
           
            montant_du_depot  = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[@class='z-doublebox']")
            montant_du_depot.send_keys("232323")
        

        rechercher = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']//descendant::button[text()='Recherche']")
        print(rechercher.text)  

        """
        =========================================================================
        -------------- Abonnement TV------------------------------------------------------
        """

        # warim_menu_items[3].click()

        # envoi_element_mask = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='z-div'][1]//descendant::select[1]"))
        # )

        # print(' ---------here -----')
        # #Choisir un pays de destination
        # pays = "Senegal"
        # driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='z-div'][1]//descendant::select[1]/option[text()='"+ pays +"']").click()
        # #Selectionnez un facturier

        # facturier = "CANAL"

        # driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='z-div'][1]//descendant::select[2]/option[text()='"+ facturier +"']").click()

        # envoi_element_mask = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[1]"))
        # )

        # if( facturier=="CANAL"):
        #     inputs = driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
        #     inputs[0].send_keys("2323")
        #     inputs[1].send_keys("2323")

        # if( facturier=="Excaf"):
        #     inputs = driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
        #     #Num Abonne *
        #     num_abonne = "2323"
        #     inputs[0].send_keys(num_abonne)
        #     #Formule Abonnement *
        #     formule_abonnement = "2323"
        #     inputs[1].send_keys(formule_abonnement)
        #     #Montant
        #     montant = "500"
        #     inputs[2].send_keys(montant)
        #     #Nom *
        #     nom  = "Goudiaby"
        #     inputs[3].send_keys(nom)
        #     #Prenom *
        #     prenom  = "adama"
        #     inputs[4].send_keys(prenom)
        #     #Numero de Telephone *
        #     tel  = "77665533"
        #     inputs[5].send_keys(tel)

        # if( facturier=="DSTV"):
        #     envoi_element_mask = WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located((By.XPATH,"//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input[@class='z-datebox-input']"))
        #     )

        #     time.sleep(5)
        #     inputs = driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::input")
        #     #Numero de Police *
        #     num_police = "2323"
        #     inputs[0].send_keys(num_police)
        #     #Montant*
        #     montant = "2000"
        #     inputs[1].send_keys(montant)
        #     #Nom
        #     nom = "Goudiaby"
        #     inputs[2].send_keys(nom)
        #     #Date Echeance
        #     date_echeance  = "10 oct. 2018"
        #     inputs[3].send_keys(date_echeance)
        #     #Numero Abonne
        #     numero_abonne  = "123"
        #     inputs[4].send_keys(numero_abonne)
        #     #Prenom
        #     prenom  = "Adama"
        #     inputs[5].send_keys(prenom)
        #     #Numero Facture
        #     numero_facture  = "234"
        #     inputs[6].send_keys(numero_facture)
        #     #Numero Abonne
        #     numero_de_telephon  = "776543212"
        #     inputs[7].send_keys(numero_de_telephon)
        #     #pays
        #     pays  = "Senegal"
        #     inputs[8].send_keys(pays)

            
        # #Num Abonne suivi des cinq derniers chiffres du numero de la carte 

        # recherche = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div//descendant::button")

        # print(recherche.text)
        # # print(len(select_items))
        """
        =========================================================================
        --------------Envoi------------------------------------------------------
        """

        #warim_menu_items[5].click() #click in "envoi" tag

        # envoi_element_mask = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@class='z-auxheader-content']"))
        # )

        # #Get html elements 

        # select_items_envoi = driver.find_elements_by_xpath("//select[@class='z-select']")
        # inputs_items_envoi = driver.find_elements_by_xpath("//input[@class='z-textbox']")
        # montant_envoyeur = driver.find_element_by_xpath("//input[@class='z-doublebox']")
        # inputs_dates_cni_envoyeur = driver.find_elements_by_xpath("//input[@class='z-datebox-input']")
        # radios_mode = driver.find_elements_by_xpath("//input[@type='radio']")
        

        # #----------------Choisir un pays de destination-----------------    

        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Senegal']").click()
        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Senegal']").send_keys(Keys.RETURN)
    
        # #--------------------Envoyeur-----------------
        #     #  set "nom"
        # nom_envoyeur = "Goudiaby"
        # inputs_items_envoi[0].clear()
        # inputs_items_envoi[0].send_keys(nom_envoyeur)
        #     # set "prenom"
        # prenom_envoyeur  =   "Adama"
        # inputs_items_envoi[1].clear()
        # inputs_items_envoi[1].send_keys(prenom_envoyeur)
        #     # set "adresse"
        # adresse_envoyeur = "Grand yoff"
        # inputs_items_envoi[2].clear()
        # inputs_items_envoi[2].send_keys(adresse_envoyeur)
        #     # set "cellulaire"
        # cellulaire_envoyeur = "776537639"
        # inputs_items_envoi[3].clear()
        # inputs_items_envoi[3].send_keys(cellulaire_envoyeur)
        # #-------------Information Piece-----------
        #     # set "type de piece"
        # type_piece = "Passeport"
        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='"+ type_piece +"']").click()
        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Passeport']").send_keys(Keys.RETURN)

        #     # set "Pays"
        # pays = "Barbade"
        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='"+ pays +"']").click()
        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='Samoa']").send_keys(Keys.RETURN)
        #     #set "date de délivrance"
        # date_de_delivrance = "11/09/2018"
        # inputs_dates_cni_envoyeur[0].send_keys(date_de_delivrance)
        #     #set "date de validité"
        # date_de_validite = "11/09/2018"
        # inputs_dates_cni_envoyeur[1].send_keys(date_de_validite)
        #     #set  "Numero CNI"
        # numero_cni = "1234567890987"
        # inputs_items_envoi[4].clear()
        # inputs_items_envoi[4].send_keys(numero_cni)
        #     #set  "Montant"
        # montant = "50"
        # montant_envoyeur.clear()
        # montant_envoyeur.send_keys(montant)
        #     #set  "Choix du motif"
        # motif = "Aide scolaire"
        # driver.find_element_by_xpath("//select[@class='z-select'][1]/option[text()='"+ motif +"']").click()

        #     #set "mode de d'envoi"
        # mode_de_envoi = "Espèce"
        # if(mode_de_envoi=="Espèce"):
        #     radios_mode[6].click()
        # elif(mode_de_envoi=="Carte"):
        #         radios_mode[7].click()
        #         driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::select[1]//descendant::option[text()='Wari']").click()
        #         numero_carte = driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::select[1]//following::input")
        #         numero_carte.send_keys("1234")
        #         driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::select[2]//descendant::option[text()='Compte courant']").click()            
        # elif(mode_de_envoi=="Wari pass"):
        #         radios_mode[8].click()
        #         wari_secure = driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-textbox']")
        #         wari_secure.send_keys("1234")
        # elif(mode_de_envoi=="Voucher"):
        #         radios_mode[9].click()	
        #         partenaire = driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-combobox-input']")
        #         partenaire.send_keys("1234")
        #         Code_voucher = driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-combobox-input']//following::input")
        #         Code_voucher.send_keys("1234")
        #         Cellulaire = driver.find_element_by_xpath("//div[@class='z-vlayout-inner'][2]/div/div[@class='z-grid-body']/table//descendant::input[@class='z-combobox-input']//following::input//following::input")
        #         Cellulaire.send_keys("1234")
        # elif(mode_de_envoi=="Wallet"):
        #         radios_mode[10].click()
        #         """
        #             is not reachable by keyboard
        #         """
        #     # partenaire

        # #--------------------Receveur-----------------
        #     # nom
        # nom_receveur = "Ndiaye"
        # inputs_items_envoi[5].clear()
        # inputs_items_envoi[5].send_keys(nom_receveur)
        #     # prenom
        # prenom_reecveur = "Naby"
        # inputs_items_envoi[6].clear()
        # inputs_items_envoi[6].send_keys(prenom_reecveur)
        #     # adresse
        # adresse_receveur  = "PA"
        # inputs_items_envoi[7].clear()
        # inputs_items_envoi[7].send_keys(adresse_receveur)
        #     # cellulaire
        # cellulaire_receveur = "772220594"
        # inputs_items_envoi[8].clear()
        # inputs_items_envoi[8].send_keys(cellulaire_receveur)

        #     # mode de reception
        # mode_de_reception = "Compte"
        # if(mode_de_reception=="Espèce"):
        #     radios_mode[2].click()
        # elif(mode_de_reception=="Wallet"):
        #     radios_mode[3].click()
        #     #Partenaire
        #     partenaire = driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']")
        #     partenaire.clear()
        #     partenaire.send_keys("3434")
        #     partenaire.send_keys(Keys.RETURN)
        #     #celulllaire
        #     cellulaire = driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']//following::input")
        #     cellulaire.clear()
        #     cellulaire.send_keys("+221775645645")
        #     cellulaire.send_keys(Keys.RETURN)
        # elif(mode_de_reception=="Compte"):
        #         radios_mode[4].click()
        #         #Partenaire
        #         partenaire = driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']")
        #         partenaire.clear()
        #         partenaire.send_keys("3434")
        #         partenaire.send_keys(Keys.RETURN)
        #         #numero compte
        #         """
        #             is not reachable by keyboard
        #         """
        #         numero_compte = driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::input[@class='z-combobox-input']//following::input")
        #         driver.execute_script("arguments[0].setAttribute('value', '12345')", numero_compte)
        #         print(numero_carte.get_property("value"))
        #         # driver.execute_script("arguments[0].setAttribute('value', arguments[1])", numero_compte, '23232');
        #         # numero_compte.send_keys(Keys.RETURN)
        # elif(mode_de_reception=="Carte"):
        #         radios_mode[5].click()
        #         #Type Carte
        #         T_Carte = "Wari"
        #         driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::select[1]/option[text()='"+T_Carte +"']").click()
        #         #Numero Carte
        #         numero_carte = driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::select[1]//following::input")
        #         numero_carte.send_keys("2323")
        #         #Type compte
        #         t_compte = "Compte courant"
        #         driver.find_element_by_xpath("//div[@class='z-window-content']//descendant::div[@class='z-hlayout-inner'][2]//descendant::div[@class='z-grid-body'][2]//descendant::select[2]/option[text()='"+ t_compte +"']").click()


        # time.sleep(2)

        # driver.find_element_by_xpath("//button[@class='z-button'][text()='Executer']").click()
        
        # element_mask = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, "//button[@class='z-button'][text()='Valider']"))
        # )

        # driver.find_element_by_xpath("//button[@class='z-button'][text()='Valider']").click()
        
        # time.sleep(5)


        # #-------- Success


        # if driver.window_handles[1]:
        #     window_after = driver.window_handles[1]

        #     driver.switch_to_window(window_after)
        #         #conde envoi
        #     code_envoi =  driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr/th").text
        #     print(code_envoi)
        #     numero =  driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr//following::tr/th").text
        #     print(numero)

        #     iostream = open("code_envoi.txt","w")
        #     iostream.write(code_envoi)
        #     iostream.close()

        #     # montant_envoyer =  driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr//following::tr//following::tr/td").text
        #     # print(montant_envoyer)
        #     # commissions_ttc =  driver.find_element_by_xpath("//body/fieldset//descendant::legend[text()='Transaction']//following::table/tbody/tr//following::tr//following::tr//following::tr/td").text
        #     # print(commissions_ttc)
        #     #body = driver.find_element_by_xpath("//body")
        #     driver.close()
        #     driver.switch_to_window(window_before)
        #-------- Unsuccess

        # else:
        #     element_mask = WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']"))
        #     )

        #     #error =  driver.find_element_by_xpath("//span[@class='z-label'][text()='Solde insuffisant.']")

        #     driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()
            
        #     #print(error.text)

        """
        =========================================================================
        --------------Retrait------------------------------------------------------
        """
        # warim_menu_items[6].click()
        # element_mask = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, "//input[@type='radio'][1]"))
        # )
        # retrait_radios = driver.find_elements_by_xpath("//input[@type='radio']")
        
        # typeretrait="Retrait avec moyen de paiement (carte,voucher, wari pass etc.)"

        # if(typeretrait=="Code Wari"):
        #     retrait_radios[0].click()

        #     element_mask = WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located((By.XPATH, "//input[@class='z-textbox']"))
        #     )
        #     code = "500042807"
        #     driver.find_element_by_xpath("//input[@class='z-textbox']").send_keys(code)
            
        #     retrait_or_remboursement = "Retrait"

        #     if(retrait_or_remboursement=="Retrait"):
        #         retrait_radios[2].click()
        #         driver.find_element_by_xpath("//button[@class='z-button'][text()='Rechercher']").click()
            
        #         try:
        #             element_mask = WebDriverWait(driver, 5).until(
        #                 EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/div[@class='z-hlayout z-valign-middle']/div[@class='z-hlayout-inner']//descendant::span"))
        #             )
        #             error_text =  driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/div[@class='z-hlayout z-valign-middle']/div[@class='z-hlayout-inner']//descendant::span").text
        #             print(error_text)
        #             ok_error = driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']/div[@class='z-window-content']/table//descendant::button")
        #             ok_error.click()
        #         except TimeoutException:
        #             element_mask = WebDriverWait(driver, 5).until(
        #                 EC.presence_of_element_located((By.XPATH, "//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::textarea"))
        #             )

        #             inputs_retireur =  driver.find_elements_by_xpath("//input[@class='z-textbox']")


        #             #Nom retireur
        #             nom_retireur = "Goudiaby"
        #             inputs_retireur[1].send_keys(nom_retireur)
        #             #Prenom retireur
        #             prenom_retireur = "Adama"
        #             inputs_retireur[2].send_keys(prenom_retireur)

        #             inputs_envoyeur = driver.find_elements_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::input")
        #             inputs_receveur = driver.find_elements_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::input")

        #             print("----------------------infos envoyeur-------------------")
                    
        #             #nom envoyeur
        #             nom_envoyeur = inputs_envoyeur[0].get_property("value")
        #             print(nom_envoyeur)
        #             #prenom envoyeur
        #             prenom_envoyeur = inputs_envoyeur[1].get_property("value")
        #             print(nom_envoyeur)
        #             #cellulaire envoyeur
        #             cellulaire_envoyeur = inputs_envoyeur[2].get_property("value")
        #             print(cellulaire_envoyeur)
        #             #montant envoyeur
        #             montant_envoyeur = inputs_envoyeur[3].get_property("value")
        #             print(montant_envoyeur)
        #             #adresse envoyeur
        #             adresse_envoyeur = driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][1]//descendant::textarea").get_property("value")
        #             print(adresse_envoyeur)

        #             print("----------------------infos Receveur-------------------")

        #             #nom receveur
        #             nom_receveur = inputs_receveur[1].get_property("value")
        #             print(nom_receveur)
        #             # #prenom receveur
        #             prenom_receveur = inputs_receveur[2].get_property("value")
        #             print(prenom_receveur)
        #             #cellulaire receveur
        #             cellulaire_receveur = inputs_receveur[3].get_property("value")
        #             print(cellulaire_receveur)
        #             #Tel receveur
        #             numero_piece = "1234567890987"
        #             tel_receveur = inputs_receveur[4].send_keys(numero_piece)
        #             #type de piece
        #             type_piece= "Passeport"
        #             driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::select[1]/option[text()='"+ type_piece +"']").click()
        #             #adresse receveur
        #             adresse_receveur = driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::textarea").get_property("value")
        #             print(adresse_receveur)
        #             #pays receveur
        #             pays_receveur= "Sénégal"
        #             driver.find_element_by_xpath("//div[@class='z-groupbox-content']/div/div[@class='z-groupbox'][2]//descendant::select[2]/option[text()='"+ pays_receveur +"']").click()
        #             #Date de délivrance
        #             date_de_delivrance = "20/09/2017"
        #             inputs_receveur[5].send_keys(date_de_delivrance)
        #             #Date de validité
        #             date_de_validite  = "20/09/2021"
        #             inputs_receveur[6].send_keys(date_de_validite)

        #             # last_id_file = open("lastid.txt","r")
        #             # number_last_file = int(last_id_file.read())
        #             # last_id_file.close()
        #             # last_id_file = open("lastid.txt","w")
        #             # last_file_name   = str(number_last_file) + ".txt"
        #             # next_file_name   = str(number_last_file + 1) + ".txt"

        #             # print(last_file_name)

        #             # last_id_file.write(str(number_last_file + 1))

        #             # next_file_request = open("./request_files/"+next_file_name,'w')
        #             # next_file_response = open("./response_files/"+next_file_name,'w')

        #             # datas = "2"+ "[" + prenom_envoyeur + "[" + nom_envoyeur + "[" + adresse_envoyeur + "[" + cellulaire_envoyeur + "[" + montant_envoyeur + "[" + prenom_receveur + "[" + nom_receveur + "[" + type_piece +"["+ tel + "[" + pays_receveur + "[" + date_de_delivrance + "[" + date_de_validite

        #             # next_file_request.write(datas)

        #             # next_file_request.close()
        #             # next_file_response.close()
        #             # last_id_file.close()

        #             btn_validation_retrait = driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Valider']")
        #             btn_validation_retrait.click()
                    
        #             time.sleep(5)


        #             if driver.window_handles[1]:
        #                 window_after = driver.window_handles[1]
        #                 driver.switch_to_window(window_after)

        #                 #conde envoi
        #                 code_retrait =  driver.find_element_by_xpath("//body/fieldset[2]//descendant::legend[text()='Transaction']//following::table/tbody/tr/th//following::th").text
        #                 print(code_retrait)
                        
        #                 driver.close()
        #                 driver.switch_to_window(window_before)

        #             btn_annulation_retrait = driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Annuler']")
        #             print(btn_annulation_retrait.text)


        #     if(retrait_or_remboursement=="Remboursement"):
        #         retrait_radios[3].click()

        #         driver.find_element_by_xpath("//button[@class='z-button'][text()='Rechercher']").click()
            
        #         time.sleep(5)

        #         inputs_envoyeur = driver.find_elements_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::input")
        #         inputs_receveur = driver.find_elements_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][2]//descendant::input")

        #         print("----------------------infos envoyeur-------------------")
                
        #         #nom envoyeur
        #         nom_envoyeur = inputs_envoyeur[0].get_property("value")
        #         print(nom_envoyeur)
        #         #prenom envoyeur
        #         prenom_envoyeur = inputs_envoyeur[1].get_property("value")
        #         print(prenom_envoyeur)
        #         #cellulaire envoyeur
        #         cellulaire_envoyeur = inputs_envoyeur[2].get_property("value")
        #         print(cellulaire_envoyeur)
        #         #montant envoyeur
        #         montant_envoyeur = inputs_envoyeur[3].get_property("value")
        #         print(montant_envoyeur)
        #         #adresse envoyeur
        #         adresse_envoyeur = driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::textarea").get_property("value")
        #         print(adresse_envoyeur)
        #         #numero cni
        #         numero_piece = inputs_envoyeur[4].get_property("value")
        #         print(numero_piece)
        #         #Date de délivrance
        #         date_de_delivrance = "20/09/2018"
        #         inputs_envoyeur[5].send_keys(date_de_delivrance)
        #         #Date de validité
        #         date_de_validite  = "20/09/2018"
        #         inputs_envoyeur[6].send_keys(date_de_validite)
        #         #pays envoyeur
        #         pays_envoyeur= "Sénégal"
        #         driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::select[2]/option[text()='"+ pays_envoyeur +"']").click()
        #         #type de piece
        #         type_piece= "Passeport"
        #         driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][1]//descendant::select[1]/option[text()='"+ type_piece +"']").click()

        #         print("----------------------infos Receveur-------------------")

        #         #nom receveur
        #         nom_receveur = inputs_receveur[0].get_property("value")
        #         print(nom_receveur)
        #         # #prenom receveur
        #         prenom_receveur = inputs_receveur[1].get_property("value")
        #         print(prenom_receveur)
        #         #cellulaire receveur
        #         cellulaire_receveur = inputs_receveur[2].get_property("value")
        #         print(cellulaire_receveur)
        #         #adresse receveur
        #         adresse_receveur = driver.find_element_by_xpath("//div[@class='z-groupbox-content']//descendant::div[@class='z-groupbox'][2]//descendant::textarea").get_property("value")
        #         print(adresse_receveur)


        #         # last_id_file = open("lastid.txt","r")
        #         # number_last_file = int(last_id_file.read())
        #         # last_id_file.close()
        #         # last_id_file = open("lastid.txt","w")
        #         # last_file_name   = str(number_last_file) + ".txt"
        #         # next_file_name   = str(number_last_file + 1) + ".txt"


        #         # last_id_file.write(str(number_last_file + 1))

        #         # next_file_request = open("./request_files/"+next_file_name,'w')
        #         # next_file_response = open("./response_files/"+next_file_name,'w')

        #         # datas = "2"+ "[" + prenom_envoyeur + "[" + nom_envoyeur + "[" + adresse_envoyeur + "[" + cellulaire_envoyeur + "[" + montant_envoyeur + "[" + prenom_receveur + "[" + nom_receveur + "[" + type_piece +"["+ tel + "[" + pays_receveur + "[" + date_de_delivrance + "[" + date_de_validite

        #         # next_file_request.write(datas)

        #         # next_file_request.close()
        #         # next_file_response.close()
        #         # last_id_file.close()

        #         btn_validation_retrait = driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Valider']")
        #         print(btn_validation_retrait.text)
        #         btn_annulation_retrait = driver.find_element_by_xpath("//div[@class='z-window-content']/div[@class='z-div']//descendant::button[text()='Annuler']")
        #         print(btn_annulation_retrait.text)
                
        # elif(typeretrait=="Retrait avec moyen de paiement (carte,voucher, wari pass etc.)"):
        #     retrait_radios[1].click()
               
                                    
        #     element_mask = WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//descendant::input[@type='text']"))
        #     )

        #     inputs =  driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::input")

        #     print(len(inputs))
        #     print("Yes")
        #     # Nom
        #     monNom = "Goudiaby"
        #     # el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//descendant::input")
        #     inputs[0].clear()
        #     inputs[0].send_keys(monNom)
        #     # Prenom
        #     monPrenom = "Adama"
        #     #el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//descendant::input")
        #     inputs[1].clear()
        #     inputs[1].send_keys(monPrenom)

        #     # Cellulaire
        #     monCellulaire = "779807654"
        #     #el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//descendant::input")
        #     inputs[2].clear()
        #     inputs[2].send_keys(monCellulaire)

        #     # Montant
        #     monCellulaire = "1000"
        #     #el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//descendant::input")
        #     inputs[3].clear()
        #     inputs[3].send_keys(monCellulaire)

        #     # Type de pièce
        #     Typ_de_piece = "Passeport"
        #     el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//descendant::select/option[text()='"+Typ_de_piece+"']")
        #     el.click()
        #     el.send_keys(Keys.RETURN)

        #     # NumeroPiece
        #     Numeropiece = "2324657679546"
        #     #el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input")
        #     inputs[4].clear()
        #     inputs[4].send_keys(Numeropiece)

        #     element_mask = WebDriverWait(driver, 5).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button"))
        #     )

        #     driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()
        #     # pays
        #     pays = "Afghanistan"
        #     el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select/option[text()='"+pays+"']")
        #     el.click()
        #     el.send_keys(Keys.RETURN)

        #     # NumeroPiece
        #     date_de_delivrance = "03/06/2010"
        #     #el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input")
        #     inputs[5].clear()
        #     inputs[5].send_keys(date_de_delivrance)


        #     # NumeroPiece
        #     date_de_validite  = "03/06/2025"
        #     #el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input")
        #     inputs[6].clear()
        #     inputs[6].send_keys(date_de_validite)

        #     element_mask = WebDriverWait(driver, 5).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button"))
        #     )
            
        #     driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()

        #     els =   driver.find_elements_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::input[@type='radio']")

        #     time.sleep(2)

        #     moyen_paiement = "Wari pass"
            
            
        #     if moyen_paiement=="Carte":
        #         els[0].click()
        #         wari_secure = "zejz"
        #         el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-textbox']")
        #         el.send_keys(wari_secure)
                
        #         element_mask = WebDriverWait(driver, 5).until(
        #             EC.presence_of_element_located((By.XPATH, "//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button"))
        #         )
                
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-highlighted z-window-shadow']//descendant::button").click()

        #         valid = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
        #         print(valid.text)
                
        #         annu  = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
        #         print(annu.text)
        #     elif moyen_paiement=="Carte":
        #         els[1].click()
        #         time.sleep(2)
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select[1]/option[text()='Wari']").click()                
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select[1]//following::input").send_keys("3434343")        
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::select[1]//following::input//following::select/option[text()='Compte courant']").click()        

        #         valid = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
        #         print(valid.text)
                
        #         annu  = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
        #         print(annu.text)
        #     elif moyen_paiement=="Voucher":
        #         els[2].click()
        #         time.sleep(2)
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']").send_keys("Wari")                
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']//following::input").send_keys("3434343")        
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']//following::input//following::input").send_keys("3434343")        
                
        #         valid = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
        #         print(valid.text)
                
        #         annu  = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
        #         print(annu.text)
        #     elif moyen_paiement=="Wallet":
        #         els[3].click()
        #         time.sleep(2)
        #         driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::input[@class='z-combobox-input']").send_keys("Wari")
        #         el = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::tr[@class='z-row z-grid-odd']//following-sibling::tr//following-sibling::tr//descendant::input[@class='z-textbox']")
                
        #         driver.execute_script("arguments[0].setAttribute('value', '12345')", el)

        #         print(el.get_property("value"))

        #         valid = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Valider']")
        #         print(valid.text)

        #         annu  = driver.find_element_by_xpath("//div[@class='z-window z-window-noborder z-window-noheader z-window-embedded']/div/div[@class='cm-grid z-div']//descendant::table//descendant::table//descendant::table/tbody//descendant::tr[1]//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//following::tr//descendant::button[text()='Annuler']")
        #         print(annu.text)


        #     # nom = driver.find_element_by_xpath("//input[@class='z-textbox z-textbox-invalid'][1]")
        #     # print(nom.get_property("class"))
        	


    except TimeoutException:
        print("Connexion: ===================================================================[NO]")  

    ############################ EN SUSPENS ##############

    #    second_element_mask = WebDriverWait(driver,10).until(
    #        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".z-listcell-content"), "Guichetier de  Distributeur")
    #    )                                                        


    #    second_element_mask = WebDriverWait(driver, 10).until(
    #        EC.presence_of_element_located((By.CSS_SELECTOR, ".z-window-header.z-window-header-move"))
    #    )


    #    element_span = driver.find_element_by_xpath('//span[@class="z-label"]')
    #    element_span = driver.find_element_by_xpath('html/body/div/div/div/div/div/table/tbody/tr/td/div/span')

    #    print( element_span.get_property('textContent') )    

    #    element_btn = driver.find_element_by_xpath('//button[@class="messagebox-btn z-button"]')
    #    print( element_btn.get_property('textContent') )
    #    element_btn.send_keys(Keys.RETURN)

    finally:
        time.sleep(60000)
        driver.quit()
        print("Connexion: ===================================================================[NO]")


   