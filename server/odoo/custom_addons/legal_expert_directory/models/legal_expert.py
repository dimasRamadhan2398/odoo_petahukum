# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LegalExpert(models.Model):
    _name = 'legal.expert'
    _description = 'Legal Expert'

    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')
    name = fields.Char(string='Name', related='user_id.name', store=True, readonly=False)
    profile_picture = fields.Image(string='Profile Picture', related='user_id.image_1920', store=True, readonly=False)

    role = fields.Selection([
        ('lbh', 'LBH'),
        ('lawyer', 'Lawyer'),
        ('notary', 'Notary'),
        ('judge', 'Judge'),
        ('prosecutor', 'Prosecutor'),
        ('police', 'Police'),
        ('other', 'Other Legal Expert'),
    ], string='Role', required=True, default='lawyer')

    experience = fields.Integer(string='Experience (Years)', default=0)
    ranking = fields.Float(string='Ranking', default=0.0)
    handled_client = fields.Integer(string='Handled Clients', default=0)
    availability = fields.Boolean(string='Availability', default=True)
    service_fee = fields.Float(string='Service Fee', default=0.0)
    description = fields.Text(string='Description')

    def name_get(self):
        result = []
        for expert in self:
            name = "%s (%s)" % (expert.name, dict(self._fields['role'].selection).get(expert.role))
            result.append((expert.id, name))
        return result
