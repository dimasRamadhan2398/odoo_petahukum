{
    'name': 'Legal Article Scraper',
    'version': '1.0.0',
    'category': 'Legal/Articles',
    'summary': 'Scrape Indonesia legal news from legal news websites',
    'description': """
        Module to automatically scrape Indonesia legal news and store them in the legal.article model.
        Features:
        - Scrape legal news from popular Indonesia legal news websites
        - Automatically updated via scheduled action (cron)
        - Extends legal.article to distinguish between scraped news and internal blogs
    """,
    'author': 'Jules',
    'depends': ['base', 'legal_website'],
    'data': ['security/ir.model.access.csv', 'data/cron.xml', 'views/legal_article_extended_views.xml', 'views/website_templates_scraper.xml', 'views/scraper_views.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {'python': ['bs4', 'requests']},
    'assets': {'web.assets_frontend': ['legal_article_scraper/static/src/css/scraper.css']},
}
