# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MOMFormatLine(models.Model):
    _name = 'mom.format.line'
    _description = 'MOM Format Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    # Sequence and basic fields
    sequence = fields.Integer(string='Sequence', default=10)
    serial_no = fields.Integer(string='Serial No.', copy=False, compute='_compute_serial_no', store=True)
    mom_format_id = fields.Many2one('mom.format.base', string='MOM Format', required=True, ondelete='cascade')
    
    # Main fields
    open_point_id = fields.Many2one('mom.open.point', string='Open Point', required=True)
    responsibility_id = fields.Many2one('res.partner', string='Responsibility (Supplier)')
    target_date = fields.Date(string='Target Date', required=True)
    actual_completion_date = fields.Date(string='Actual Completion Date')
    
    # Status field
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # Additional fields
    remarks = fields.Text(string='Remarks')
    create_date = fields.Datetime(string='Created on Date', readonly=True)
    
    # Attendees and Champion
    attendee_ids = fields.Many2many('hr.employee', 'mom_line_attendee_rel', 'mom_line_id', 'employee_id', string='Attendees')
    conducted_by_id = fields.Many2one('hr.employee', string='Conducted By/Champion')
    
    @api.model
    def default_get(self, fields_list):
        """Override default_get to populate attendee_ids and conducted_by_id from parent MOM format."""
        defaults = super(MOMFormatLine, self).default_get(fields_list)
        
        # Check if we're creating from a MOM format context
        mom_format_id = self.env.context.get('mom_format_id') or self.env.context.get('default_mom_format_id')
        if not mom_format_id and 'mom_format_id' in defaults:
            mom_format_id = defaults['mom_format_id']
            
        if mom_format_id:
            mom_format = self.env['mom.format.base'].browse(mom_format_id)
            if mom_format.exists():
                if 'attendee_ids' in fields_list and mom_format.attendee_ids:
                    defaults['attendee_ids'] = [(6, 0, mom_format.attendee_ids.ids)]
                if 'conducted_by_id' in fields_list and mom_format.conducted_by_id:
                    defaults['conducted_by_id'] = mom_format.conducted_by_id.id
        
        return defaults
    
    # Approval fields
    approve_date = fields.Datetime(string='Approve Date', readonly=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True)
    
    # Company
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    
    # State History Tracking
    state_history = fields.Text(string='State History', readonly=True, copy=False)
    
    @api.onchange('mom_format_id')
    def _onchange_mom_format_id(self):
        """Auto-fill attendee_ids and conducted_by_id when mom format is selected."""
        if self.mom_format_id:
            # Only set if fields are empty
            if not self.attendee_ids and self.mom_format_id.attendee_ids:
                self.attendee_ids = self.mom_format_id.attendee_ids
            if not self.conducted_by_id and self.mom_format_id.conducted_by_id:
                self.conducted_by_id = self.mom_format_id.conducted_by_id
    
    @api.depends('mom_format_id', 'sequence')
    def _compute_serial_no(self):
        """Compute serial number based on sequence order within the mom format."""
        for record in self:
            if record.mom_format_id:
                # Get all records for the same mom format, ordered by sequence and id
                all_records = self.search([('mom_format_id', '=', record.mom_format_id.id)], order='sequence, id')
                # Assign serial numbers based on the order
                for idx, rec in enumerate(all_records, 1):
                    if rec.serial_no != idx:
                        rec.serial_no = idx
    
    @api.model
    def create(self, vals):
        """Create MOM format line, initialize state_history, and update serial numbers."""
        if 'serial_no' not in vals or not vals.get('serial_no'):
            if 'mom_format_id' in vals and vals['mom_format_id']:
                # Find the next sequence number
                existing_records = self.search([('mom_format_id', '=', vals['mom_format_id'])], order='sequence desc', limit=1)
                next_sequence = existing_records.sequence + 10 if existing_records else 10
                vals['sequence'] = next_sequence
                # Serial number will be computed later
            else:
                vals['sequence'] = 10
        
        # Initialize state_history
        if 'state_history' not in vals:
            vals['state_history'] = ''
        
        # Auto-fill attendee_ids and conducted_by_id from mom format
        if 'mom_format_id' in vals and vals['mom_format_id']:
            mom_format = self.env['mom.format.base'].browse(vals['mom_format_id'])
            if mom_format:
                # Only set if not already provided or if empty
                if ('attendee_ids' not in vals or not vals.get('attendee_ids')) and mom_format.attendee_ids:
                    vals['attendee_ids'] = [(6, 0, mom_format.attendee_ids.ids)]
                if ('conducted_by_id' not in vals or not vals.get('conducted_by_id')) and mom_format.conducted_by_id:
                    vals['conducted_by_id'] = mom_format.conducted_by_id.id
        
        res = super(MOMFormatLine, self).create(vals)
        if res.mom_format_id:
            # Recompute serial numbers for all records in the mom format
            all_records = self.search([('mom_format_id', '=', res.mom_format_id.id)], order='sequence, id')
            all_records._compute_serial_no()
        # Update state history for the 'created' event
        res._update_state_history('created', res.state or 'draft')
        return res
    
    def unlink(self):
        """Delete MOM format line and update remaining serial numbers."""
        mom_format_ids = self.mapped('mom_format_id.id')
        res = super(MOMFormatLine, self).unlink()
        for mom_id in mom_format_ids:
            remaining_records = self.search([('mom_format_id', '=', mom_id)], order='sequence, id')
            remaining_records._compute_serial_no()
        return res
    
    def write(self, vals):
        """Override write to handle sequence changes and update state history."""
        old_mom_ids = {rec.id: rec.mom_format_id.id for rec in self if rec.mom_format_id}
        old_states = {rec.id: rec.state for rec in self}
        
        res = super(MOMFormatLine, self).write(vals)
        
        if 'state' in vals:
            for record in self:
                old_state = old_states.get(record.id)
                new_state = vals.get('state')
                if old_state != new_state:
                    record._update_state_history(old_state, new_state)
        
        # If mom_format_id or sequence is changed, update serial numbers
        if 'mom_format_id' in vals or 'sequence' in vals:
            mom_ids = set()
            for record in self:
                if record.mom_format_id:
                    mom_ids.add(record.mom_format_id.id)
            if 'mom_format_id' in vals:
                for old_mom_id in set(old_mom_ids.values()):
                    if old_mom_id and old_mom_id not in mom_ids:
                        remaining_records = self.search([('mom_format_id', '=', old_mom_id)], order='sequence, id')
                        remaining_records._compute_serial_no()
            for mom_id in mom_ids:
                all_records = self.search([('mom_format_id', '=', mom_id)], order='sequence, id')
                all_records._compute_serial_no()
        
        return res
    
    def _update_state_history(self, old_state, new_state):
        """Update state history with plain text formatting and ensure each entry is on a new line."""
        for record in self:
            timestamp = fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user = self.env.user
            
            state_display = {
                'draft': 'Draft',
                'in_progress': 'In Progress',
                'completed': 'Completed',
                'approved': 'Approved',
                'cancelled': 'Cancelled',
                'created': 'Created'
            }
            
            old_state_name = state_display.get(old_state, old_state)
            new_state_name = state_display.get(new_state, new_state)
            
            if old_state == 'created':
                history_entry = f"{timestamp} - Record created in {new_state_name} state by {user.name}"
            else:
                history_entry = f"{timestamp} - State changed from {old_state_name} to {new_state_name} by {user.name}"
            
            # Append the new entry with a newline
            if record.state_history:
                record.state_history = record.state_history + "\n" + history_entry
            else:
                record.state_history = history_entry
    
    def action_approve(self):
        """Approve the MOM format line record."""
        for record in self:
            if record.state != 'completed':
                raise UserError(_('You can only approve completed records.'))
            record.write({
                'state': 'approved',
                'approve_date': fields.Datetime.now(),
                'approved_by_id': self.env.user.id,
            })
        return True
    
    def action_complete(self):
        """Mark the MOM format line as completed."""
        for record in self:
            if not record.actual_completion_date:
                raise UserError(_('Please set the actual completion date before marking as completed.'))
            record.state = 'completed'
        return True
    
    def action_cancel(self):
        """Cancel the MOM format line record."""
        for record in self:
            if record.state == 'approved':
                raise UserError(_('You cannot cancel an approved record.'))
            record.state = 'cancelled'
        return True
    
    def action_reset_to_draft(self):
        """Reset the record to draft state."""
        for record in self:
            record.write({
                'state': 'draft',
                'approve_date': False,
                'approved_by_id': False,
            })
        return True
    
    def action_in_progress(self):
        """Mark the record as in progress."""
        for record in self:
            record.state = 'in_progress'
        return True
