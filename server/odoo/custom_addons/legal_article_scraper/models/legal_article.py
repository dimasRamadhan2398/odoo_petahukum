from odoo import models, fields, api

class LegalArticle(models.Model):
    _inherit = 'legal.article'

    is_scraped = fields.Boolean('Is Scraped News', default=False, help="Whether this article was scraped from an external news site")
    source_url = fields.Char('Source URL', help="The original URL if the article was scraped")
    source_site = fields.Char('Source Site', help="The name of the site this was scraped from")

    article_type = fields.Selection([
        ('blog', 'Our Blog'),
        ('news', 'External News')
    ], string="Article Type", default='blog', required=True)
