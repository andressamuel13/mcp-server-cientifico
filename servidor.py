import os
from fastmcp import FastMCP
import feedparser
from config import FEEDS_CIENCIA  # Importamos el diccionario con tus URLs

mcp = FastMCP("servidor-noticias-ciencia")

@mcp.tool()
def buscar_noticias(tema: str, limite: int = 5) -> list[dict] | str:
    """Busca las últimas noticias científicas o papers según el tema especificado."""
    
    # 1. Normalizar el tema ingresado a minúsculas
    tema_lower = tema.lower()
    
    # 2. Verificar si el tema existe en nuestro diccionario de config.py
    if tema_lower not in FEEDS_CIENCIA:
        return f"El tema '{tema}' no está configurado. Vías disponibles: {list(FEEDS_CIENCIA.keys())}"
    
    # 3. Obtener la URL correspondiente y hacer la petición con feedparser
    url = FEEDS_CIENCIA[tema_lower]
    feed = feedparser.parse(url)
    
    # 4. Validar si el feed devolvió entradas/artículos
    if feed.entries:
        lista_noticias = []
        
        # Iteramos sobre los artículos reales usando [:limite] para no exceder el número pedido
        for entrada in feed.entries[:limite]:
            noticia = {
                "titulo": entrada.get("title", "Sin título"),
                "autor": entrada.get("author", "Autor no especificado"),
                "fecha": entrada.get("published", "Fecha desconocida"),
                "resumen": entrada.get("summary", "Sin resumen"),
                "url": entrada.get("link", "#")
            }
            lista_noticias.append(noticia)
            
        return lista_noticias
    else:
        return "No se encontraron noticias o hubo un problema al conectar con la fuente."

if __name__ == "__main__":
    puerto = os.environ.get("PORT")

    if puerto:
        mcp.run(transport="http", host="0.0.0.0", port=int(puerto))
    else:
        mcp.run(transport="stdio")