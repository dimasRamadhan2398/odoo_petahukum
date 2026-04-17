import requests
from bs4 import BeautifulSoup
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class LegalArticleScraper(models.AbstractModel):
    _name = 'legal.article.scraper'
    _description = 'Legal Article Scraper'

    @api.model
    def scrape_detik_hukum(self):
        """Scrape legal news from Detik.com"""
        url = 'https://www.detik.com/search/searchall?query=hukum'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            articles = soup.find_all('article')
            _logger.info(f"Found {len(articles)} articles to process from Detik")

            # Create a default category for News if it doesn't exist
            Category = self.env['legal.category']
            news_category = Category.search([('name', 'ilike', 'News')], limit=1)
            if not news_category:
                news_category = Category.create({
                    'name': 'Legal News',
                    'description': 'Scraped legal news'
                })

            Article = self.env['legal.article']

            # Filter valid news articles
            valid_articles = []
            for art in articles:
                a_tag = art.find('a')
                h2_tag = art.find('h2')
                if a_tag and h2_tag:
                    link = a_tag.get('href')
                    if link and ('/hukum-dan-kriminal/' in link or '/berita/' in link) and 'foto-news' not in link:
                        valid_articles.append((h2_tag.text.strip(), link))

            for title, link in valid_articles[:10]: # Process up to 10 recent articles
                # Check if article already exists
                existing = Article.search([('source_url', '=', link)], limit=1)
                if existing:
                    continue

                # Scrape article content
                try:
                    art_response = requests.get(link + '?single=1', headers=headers, timeout=15)
                    art_soup = BeautifulSoup(art_response.content, 'html.parser')

                    # Detik's article body class
                    content_div = art_soup.select_one('.detail__body-text') or art_soup.select_one('.itp_bodycontent')

                    if content_div:
                        # Clean up content
                        for unwanted in content_div.select('script, style, .detail__vid, .baca-juga, iframe, table, .paragrap, .pic_artikel'):
                            unwanted.extract()

                        # Wrap in a div to preserve styling but scope it
                        content = f'<div class="scraped-content">{str(content_div)}</div>'
                    else:
                        content = f"<p>Read full article at <a href='{link}'>{link}</a></p>"

                    # Try to get better title from article page
                    art_title_tag = art_soup.select_one('.detail__title') or art_soup.select_one('h1')
                    if art_title_tag:
                        title = art_title_tag.text.strip()

                    # Create article
                    Article.create({
                        'name': title,
                        'content': content,
                        'category_id': news_category.id,
                        'is_scraped': True,
                        'source_url': link,
                        'source_site': 'Detik News',
                        'article_type': 'news',
                        'website_published': True,
                    })
                    _logger.info(f"Successfully scraped article: {title}")

                except Exception as e:
                    _logger.error(f"Error scraping article {link}: {str(e)}")

        except Exception as e:
            _logger.error(f"Error scraping Detik: {str(e)}")

    @api.model
    def run_all_scrapers(self):
        """Cron job entry point"""
        _logger.info("Starting legal article scrapers...")
        self.scrape_detik_hukum()
        _logger.info("Finished legal article scrapers.")
