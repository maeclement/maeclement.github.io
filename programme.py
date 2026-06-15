# Section des imports de bibliothèques
import json
import csv
import datetime
import os

# Section des définitions des fonctions
def ouvrirFichierSource(titre,chemin):
    with open(chemin+titre, "r",encoding="utf-8-sig") as fichier:
        base = json.load(fichier)
        fichier.close()
    return base


def nomTraduitEnCSV(titre):
    '''
    Crée le nom du fichier de la future base de données en format csv en fonction de fichier json initial
    exemple :
    nomFichier.json -> nomFichier.csv
    '''
    if titre[-5:]==".json":
        titreCSV=titre[:-5]+".csv"
    else:
        titreCSV="dataConverties.csv"
    return titreCSV


def validation(ligne,numLigne,writer):
    try:
        Nom_Station=(ligne["fields"]["nom_station"])
        Lattitude=(ligne["geometry"]["coordinates"][0])
        Longitude=(ligne["geometry"]["coordinates"][1])
        Date_de_prélèvement=datetime.datetime.strptime((ligne["fields"]["date_fin"])[:10],"%Y-%m-%d" ).strftime("%d/%m/%Y")
        Nom_Polluant=(ligne["fields"]["nom_poll"])
        Unité=(ligne["fields"]["unite"]) 
        Valeur=(ligne["fields"]["valeur"])

        # Création de ligne à intégrer
        New_Base[numLigne]={"Nom Station":Nom_Station,
                            "Lattitude":Lattitude,
                            "Longitude":Longitude,
                            "Date de prélèvement":Date_de_prélèvement,
                            "Nom_Polluant":Nom_Polluant,
                            "Valeur":Valeur,
                            "Unité":Unité}
        
        # Convertir la ligne pour qu'elle soit lue et intégrée, colonne par colonne dans le csv
        writer.writerow({"Nom Station":Nom_Station,
                         "Lattitude":Lattitude,
                         "Longitude":Longitude,
                         "Date de prélèvement":Date_de_prélèvement,
                         "Nom_Polluant":Nom_Polluant,
                         "Valeur":Valeur,
                         "Unité":Unité})
        return ligne
    except KeyError:
        # Informe que la ligne traitées contenait une erreur (valeur introuvable)
        try :
            print("Ligne "+str(numLigne)+ " non conforme ({"+Nom_Station+"}, {"+str(Date_de_prélèvement)+"} )")     
        except  UnboundLocalError:
            print("Ligne "+str(numLigne)+ " non conforme et champs mal renseignés")


def afficherBilan(New_Base,numLigne):
    '''
    Procédure qui permet d'écrire le bilan du programme
    '''
    print("\nVoici au dessus, toutes les lignes avec des erreurs : n'apparaissent pas dans le fichier CSV\n" ,100*"_")
    print("\nBILAN de ce qui vient de se produire :\n")
    print("     ->",numLigne," lignes traitées à partir du fichier :",titre)
    print("\n    Ainsi :\n")
    print("     ->",len(New_Base),"/",numLigne," lignes intégrées au fichier :",nomTraduitEnCSV(titre),"\n",
          "        ->",round((len(New_Base)/numLigne),3)*100,"%\n",
          "        ->",len(base)-len(New_Base)," lignes initialement incorrectes\n")


# Section qui nomme le titre du document recherché et son chemin d'accès
titre="concentrations-polluants-dans-lair-ambiant.json"

# Chemin pour atteindre le fichier nommé {titre} à partir du programme.py(fichier actuel) executé
chemin=".\\DATA\\"      

# Dossier où enregistrer le fichier.csv,
# -> changer "DATA" par vide "" si vous voulez que le nouveau fichier s'enregistre dans le dossier général
destination="DATA" 
if destination!="":
    destination+="\\"

try:
    # Ouverture du fichier pour copier ses données
    base=ouvrirFichierSource(titre,chemin)      
    print("fichier ouvert, ses données sont copiées \n(il y a ",len(base)," datas)")

    New_Base={}     # Initialisation de ce qui sera notre json de data correctes à convertir en csv

    # Essai d'ouvrir le fichier csv
    try:     
        with open(destination+nomTraduitEnCSV(titre), 'w', newline='', encoding="utf-8-sig") as csvfile:
            fieldnames = ["Nom Station","Lattitude","Longitude","Date de prélèvement","Nom_Polluant","Valeur","Unité"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=";")
            writer.writeheader()

            # Initialisation des numLigne pour le bilan
            numLigne = 0

            # Boucle qui lit toutes les données et vérifie si elles sont correctes
            for ligne in base:
                numLigne+=1
                validation(ligne,numLigne,writer)
        csvfile.close()

        # Bilan informationnel dans le terminal
        afficherBilan(New_Base,numLigne)

    # Erreur de permission : s'affiche le fichier csv est déjà ouvert par l'utilisateur
    except PermissionError:
        print("Erreur de permission ; le fichier en '.csv' est déjà ouvert sur votre ordinateur ce qui bloque sa modification. \n-> le fermer puis relancer le programme")


except  FileNotFoundError:
    print("Fichier non trouvé, nom ou emplacement incorrect")

    if chemin!="":
        print("\nDans le DOSSIER ",chemin,"vous recherchiez le fichier :\n ",titre)
        try:
            os.chdir(chemin)
            print("\nVoici les noms des dossiers et fichiers existants ici :")
            for i in os.listdir():
                print(" ",i)
        except:
            pass
    else:
        print("\nVoici tous les documents du dossier où vous vous trouvez :\n")
        print("     (Rappel du nom de fichier recherché :\n",titre)
        for i in os.listdir():
            print(" ",i)