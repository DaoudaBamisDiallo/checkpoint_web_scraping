# ----------importation des packages-------------------
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin 
import pandas as pd

# les fonctions du prohramme
'''
    1: recuperer les contenue d'une page wikipédia
    2: Recuperer le titre
    3: Recuperer le titre des articles ainsi que le contenu de leurs paragraphes
    4: Recuperer tous les autres liens de rédirection
    5: Fonction principale du programme

'''
#---1: recuperer les contenue de la page wikipédia
def get_containte_page(url : str):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except AttributeError as e:
        print(f"Aucun noeud <'p.instock.availability'> n'a été trouvé dans cette page {e}.")

    soup = BeautifulSoup(response.content,'html.parser')

    return soup

#--2: Recuperer le titre
def get_title_article(tree :  str):
    try:
        title_article = tree.find('h1').get_text()
    except AttributeError as e:
        print(f"Aucun noeud <'p.instock.availability'> n'a été trouvé dans cette page {e}.")
    return title_article

#--2: Recuperer le titre
def get_paragraphe(tree :  str):
    try:
        # recuper tous les divs de qui ont la classe mx-heading
        divs=tree.select(".mw-heading.mw-heading2")
    
        # Liste pour stocker tous les <p> qui suivent immédiatement un <div>

        articles={}
        titles=[]
        paragraphs=[]
        # Parcourir chaque <div>
        for div in divs:
            # selection du paragraphe qui suit le div
            p = div.find_next_sibling('p')
            if p:
                # ajoute du titre  et du contenu de l'article
                titles.append(div.find("h2").text)
                paragraphs.append(p.text)

        # ajoute dans le dictionnaire   
        articles['title']=titles
        articles["Containte"]=paragraphs
    except AttributeError as e:
        print(f"Aucun noeud <'div '> n'a été trouvé dans cette page {e}.")
    # creation d'une dataframe pandans
    data = pd.DataFrame(articles)
    data.to_csv("articles_page.csv",index=False)
    # returne le dictionnaire
    return pd.read_csv("articles_page.csv", delimiter=",")

# recuperation de toutes les lien sur la page
def get_links(url: str,tree : str):
    # selection de toutes les balises a
    a_links = tree.select(".mw-body-content a")
    # recuperation et ajoute de l'url obsolution
    all_links={}
    href_link=[]
    title_href=[]
    for link in a_links:
    
        if link.get("href"):
            href_link.append(urljoin(url,link.get("href")))
            title_href.append(link.get('title'))

    all_links["Url"]=href_link
    all_links["Title"]=title_href
        # creation d'une dataframe pandans
    data = pd.DataFrame(all_links)
    data.to_csv("links_page.csv",index=False)
    # returne le dictionnaire
    return pd.read_csv("links_page.csv", delimiter=",")

#----------------- FONCTION PRINCIPAL----------------------
def main(url_base:str):
     
    URL= "https://fr.wikipedia.org/index.html"
    # Récuperation et analyse de la page
    page = get_containte_page(url=url_base)
    
    # affichage du titre de la page
    print("\n---------------------------TITRE DE LA PAGE---------------------------\n")
    print(get_title_article(tree=page))
    # # liste des articles
    data_articles=get_paragraphe(tree=page)
    print("\n---------------------------LISTE DES ARTICLES---------------------------\n")
    print(data_articles.head(100))
    # affichage des url de la page
    print("\n---------------------------URL RELATIVES DE LA PAGE---------------------------\n")
    links_page=get_links(url=URL,tree=page)
    print(links_page.head(100))
#----------execution du programmme-----------
if __name__=="__main__":
    try :
        url="https://fr.wikipedia.org/wiki/Bourse_(%C3%A9conomie)"
        url="https://fr.wikipedia.org/wiki/Science_des_donn%C3%A9es"
        url=input("Entrer votre un URL wikipédia  : ")

        main(url_base=url)
    except:
        print("Desolé nous n'avons pu acceder à cet url , veillez bien saisir votre URL et réessayez")
   