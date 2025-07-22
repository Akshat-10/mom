# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MOMOpenPoint(models.Model):
    _name = 'mom.open.point'
    _description = 'MOM Open Point'
    _order = 'sequence, name'
    
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Open Point', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    
    # Additional fields for better categorization
    category = fields.Selection([
        ('action', 'Action Item'),
        ('decision', 'Decision'),
        ('issue', 'Issue'),
        ('risk', 'Risk'),
        ('followup', 'Follow-up'),
        ('other', 'Other')
    ], string='Category', default='action')
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority', default='medium')
    
    # Statistics
    mom_count = fields.Integer(string='MOM Count', compute='_compute_mom_count')
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The open point name must be unique!')
    ]
    
    def _compute_mom_count(self):
        """Compute the number of MOMs using this open point."""
        for record in self:
            record.mom_count = self.env['mom.format.base'].search_count([('open_point_id', '=', record.id)])
    
    def action_view_moms(self):
        """View all MOMs for this open point."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Minutes of Meeting'),
            'res_model': 'mom.format.base',
            'view_mode': 'tree,form',
            'domain': [('open_point_id', '=', self.id)],
            'context': {
                'default_open_point_id': self.id,
            }
        }
