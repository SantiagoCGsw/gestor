from fastapi import APIRouter, HTTPException
import requests
from models.news import NewsArticle
import certifi
import logging
from dotenv import load_dotenv
import os

# Carga las variables de entorno
load_dotenv()

# Obtén la clave API de NewsAPI desde .env
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Configura el logging para mostrar más detalles
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/news/", response_model=list[NewsArticle])
async def get_news(query: str = "productivity OR tasks"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY
    }
    
    try:
        logger.debug(f"Requesting URL: {url} with params: {params}")
        response = requests.get(url, params=params, verify=certifi.where())
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response text: {response.text}")
        
        response.raise_for_status()
        news_data = response.json()
        
        logger.debug(f"Parsed JSON: {news_data}")
        articles = news_data.get("articles", [])
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        return [NewsArticle(**article) for article in articles]
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    except ValueError as e:
        logger.error(f"JSON decode failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error parsing news data: {str(e)}")