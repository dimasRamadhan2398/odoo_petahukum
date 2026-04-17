from odoo import http
from odoo.http import request
from odoo.addons.legal_website.controllers.main import LegalWebsiteController
import math
import logging

_logger = logging.getLogger(__name__)

class LegalScraperWebsiteController(LegalWebsiteController):

    @http.route('/legal/articles', type='http', auth='public', website=True)
    def legal_articles(self, page=1, category=None, tag=None, search=None, type=None, **kw):
        """Override list articles to add type filter"""
        domain = [('website_published', '=', True)]

        if search:
            domain += ['|', ('name', 'ilike', search), ('content', 'ilike', search)]

        if category:
            domain += [('category_id', '=', int(category))]

        if tag:
            domain += [('tag_ids', 'in', [int(tag)])]

        if type:
            domain += [('article_type', '=', type)]

        # Pagination
        items_per_page = 9
        try:
            page_num = int(page)
        except ValueError:
            page_num = 1

        offset = (page_num - 1) * items_per_page

        Article = request.env['legal.article'].sudo()

        total_articles = Article.search_count(domain)
        articles = Article.search(domain, limit=items_per_page, offset=offset)

        total_pages = math.ceil(total_articles / items_per_page) if total_articles else 1

        categories = request.env['legal.category'].sudo().search([])
        tags = request.env['legal.tag'].sudo().search([])

        values = {
            'articles': articles,
            'categories': categories,
            'tags': tags,
            'current_page': page_num,
            'total_pages': total_pages,
            'current_category': int(category) if category else None,
            'current_tag': int(tag) if tag else None,
            'search_query': search,
            'current_type': type,
        }

        return request.render('legal_website.legal_articles', values)
