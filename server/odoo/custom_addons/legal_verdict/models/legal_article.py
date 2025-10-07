# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import html2plaintext
import logging

_logger = logging.getLogger(__name__)

class LegalArticle(models.Model):
    _name = 'legal.article'
    _description = 'Legal Article'
    _order = 'create_date desc'
    _inherit = ['website.seo.metadata', 'website.published.mixin']

    name = fields.Char('Judul Artikel', required=True, translate=True)
    content = fields.Html('Konten Artikel', required=True, translate=True)
    summary = fields.Text('Ringkasan', translate=True)
    # format_id = fields.Many2one('legal.format', 'Bentuk', required=True)
    category_id = fields.Many2one('legal.category', 'Kategori', required=True)
    tag_ids = fields.Many2many('legal.tag', string='Tags')
    # type_id = fields.Many2one('legal.type', string='Type', required=True)
    author_id = fields.Many2one('res.users', 'Penulis', default=lambda self: self.env.user)
    publish_date = fields.Datetime('Tanggal Publikasi', default=fields.Datetime.now)
    publish_place = fields.Char('Tempat Penetapan', translate=True)
    view_count = fields.Integer('Jumlah View', default=0)
    
    # SEO fields
    website_meta_title = fields.Char('Meta Title')
    website_meta_description = fields.Text('Meta Description')
    website_meta_keywords = fields.Char('Meta Keywords')
    
    @api.model
    def create(self, vals):
        if 'summary' not in vals and 'content' in vals:
            content_text = html2plaintext(vals['content'])
            vals['summary'] = content_text[:200] + '...' if len(content_text) > 200 else content_text
        return super().create(vals)
    
    def increment_view_count(self):
        self.sudo().write({'view_count': self.view_count + 1})

class LegalCategory(models.Model):
    _name = 'legal.category'
    _description = 'Legal Category'
    _order = 'sequence, name'
    
    name = fields.Char('Nama Kategori', required=True, translate=True)
    description = fields.Text('Deskripsi', translate=True)
    sequence = fields.Integer('Urutan', required=True, default=10)
    color = fields.Integer('Warna')
    article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')
    
    @api.depends('name')
    def _compute_article_count(self):
        for category in self:
            category.article_count = self.env['legal.article'].search_count([
                ('category_id', '=', category.id),
                ('website_published', '=', True)
            ])

class LegalTag(models.Model):
    _name = 'legal.tag'
    _description = 'Legal Tag'
    
    name = fields.Char('Nama Tag', required=True, translate=True)
    color = fields.Integer('Warna')
    article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')
    
    @api.depends('name')
    def _compute_article_count(self):
        for tag in self:
            tag.article_count = self.env['legal.article'].search_count([
                ('tag_ids', 'in', tag.id),
                ('website_published', '=', True)
            ])

# class LegalType(models.Model):
#     _name = 'legal.type'
#     _description = 'Legal Type'

#     name = fields.Char('Tipe Hukum', required=True, translate=True)
#     color = fields.Integer('Warna')
#     article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')

#     @api.depends('name')
#     def _compute_article_count(self):
#         for type in self:
#             type.article_count = self.env['legal.article'].search_count([
#                 ('type_id', 'in', type.id),
#                 ('website_published', '=', True)
#             ])

# class LegalTeu(models.Model):
#     _name = 'legal.teu'
#     _description = 'Legal T.E.U.'

#     name = fields.Char('T.E.U.', required=True, translate=True)
#     color = fields.Integer('Warna')
#     article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')

#     @api.depends('name')
#     def _compute_article_count(self):
#         for teu in self:
#             teu.article_count = self.env['legal.article'].search_count([
#                 ('teu_id', 'in', teu.id),
#                 ('website_published', '=', True)
#             ])

# class LegalNumber(models.Model):
#     _name = 'legal.number'
#     _description = 'Legal Number'

#     name = fields.Char('Nomor', required=True, translate=True)
#     color = fields.Integer('Warna')
#     article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')

#     @api.depends('name')
#     def _compute_article_count(self):
#         for number in self:
#             number.article_count = self.env['legal.article'].search_count([
#                 ('number_id', 'in', number.id),
#                 ('website_published', '=', True)
#             ])

# class LegalFormat(models.Model):
#     _name = 'legal.format'
#     _description = 'Legal Format'
#     _order = 'sequence, name'
    
#     name = fields.Char('Nama Bentuk', required=True, translate=True)
#     description = fields.Text('Deskripsi', translate=True)
#     sequence = fields.Integer('Urutan', required=True, default=10)
#     color = fields.Integer('Warna')
#     article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')
    
#     @api.depends('name')
#     def _compute_article_count(self):
#         for format in self:
#             format.article_count = self.env['legal.article'].search_count([
#                 ('format_id', '=', format.id),
#                 ('website_published', '=', True)
#             ])

# class LegalYear(models.Model):
#     _name = 'legal.year'
#     _description = 'Legal Year'

#     name = fields.Char('Tahun', required=True, translate=True)
#     color = fields.Integer('Warna')
#     article_count = fields.Integer('Jumlah Artikel', compute='_compute_article_count')

#     @api.depends('name')
#     def _compute_article_count(self):
#         for year in self:
#             year.article_count = self.env['legal.article'].search_count([
#                 ('year_id', 'in', year.id),
#                 ('website_published', '=', True)
#             ])


