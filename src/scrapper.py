from bs4 import BeautifulSoup, Comment
import re
import requests


def get_soup_from_file(file):

    # import the html file located in the data/ folder and asign it the name page
    with open(file, 'r') as page:

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')

    return soup

def get_soup_from_internet(url):
    
    if "https://annas-archive" not in url:
        return "Not valid url"

    response = requests.get(url).text

    if len(response) != 0:
        soup = BeautifulSoup(response, 'html.parser')
        return soup

    else:
        return None


def get_books(pagina):

    if pagina == "Not valid url":
        return pagina

    elif pagina is None:
        return "error in response"

    a = pagina.find_all(id=re.compile("^link-index-"))

    if len(a) == 0:
        return "No books found"

    result = {}
    for i in range(51):
        try:
            ## Titulo del libro, en <h3> de cada div, innerHTML
            titulo = a[i].find("h3").get_text()

            ## autores en div con esta class abajo, innerHTML
            autores = a[i].find(attrs={"class": "truncate italic"}).get_text()

            href = a[i].find("a")["href"]
            ## src de la imagen


            try:
                imagen = a[i].find("img")["src"]

            except:
                imagen = None

            index = str(i)

            result_piece = {
                "titulo": titulo,
                "autores": autores,
                "imagen": imagen,
                "href": href
            }

            result[index] = result_piece

        except:

            comment = a[i].find(text=lambda text: isinstance(text, Comment))
            soup_comment = BeautifulSoup(comment, "html.parser")


            ## Titulo del libro, en <h3> de cada div, innerHTML
            titulo = soup_comment.find("h3").get_text()

            ## autores en div con esta class abajo, innerHTML
            autores = soup_comment.find(attrs={"class": "truncate italic"}).get_text()


            href = soup_comment.find("a")["href"]

            ## src de la imagen
            try:
                imagen = soup_comment.find("img")["src"]

            except:
                imagen = None

            index = str(i)

            result_piece = {
                "titulo": titulo,
                "autores": autores,
                "imagen": imagen,
                "href": href
            }

            result[index] = result_piece

    return result
