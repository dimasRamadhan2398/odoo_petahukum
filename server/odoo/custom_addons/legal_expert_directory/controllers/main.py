# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class LegalExpertDirectory(http.Controller):

    @http.route(['/legal/experts', '/legal/experts/page/<int:page>'], type='http', auth="public", website=True)
    def experts_directory(self, page=1, **kw):
        domain = []
        if kw.get('role'):
            domain.append(('role', '=', kw.get('role')))

        LegalExpert = request.env['legal.expert'].sudo()
        experts = LegalExpert.search(domain)

        roles = dict(LegalExpert._fields['role'].selection)

        values = {
            'experts': experts,
            'roles': roles,
            'current_role': kw.get('role', ''),
        }
        return request.render('legal_expert_directory.website_expert_directory', values)
