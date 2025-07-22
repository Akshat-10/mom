# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MOMFormat(models.Model):
    _name = 'mom.format.base'
    _description = 'Minutes of Meeting Format'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Sequence and basic fields
    sequence = fields.Integer(string='Sequence', default=10, help='Used to order records in list view')
    name = fields.Char(string='Meeting Reference', required=True, copy=False, 
                      default=lambda self: _('New'))
    meeting_title = fields.Char(string='Meeting Title', required=True)
    
    # Meeting Information
    meeting_date = fields.Date(string='Meeting Date', required=True, default=fields.Date.today)
    meeting_type = fields.Selection([
        ('regular', 'Regular Meeting'),
        ('review', 'Review Meeting'),
        ('planning', 'Planning Meeting'),
        ('emergency', 'Emergency Meeting'),
        ('other', 'Other')
    ], string='Meeting Type', default='regular', required=True)
    
    # Project/Context Information
    project_name = fields.Char(string='Project Name')
    customer_id = fields.Many2one('res.partner', string='Customer')
    
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
    attendee_ids = fields.Many2many('hr.employee', 'mom_attendee_rel', 'mom_id', 'employee_id', string='Attendees')
    conducted_by_id = fields.Many2one('hr.employee', string='Conducted By/Champion')
    
    # Meeting Location
    meeting_location = fields.Char(string='Meeting Location')
    
    # Approval fields
    approve_date = fields.Datetime(string='Approve Date', readonly=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True)
    
    # Company
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    
    # State History Tracking
    state_history = fields.Text(string='State History', readonly=True, copy=False)
    
    # Additional meeting details
    meeting_duration = fields.Float(string='Duration (Hours)')
    next_meeting_date = fields.Date(string='Next Meeting Date')
    meeting_notes = fields.Html(string='Meeting Notes')
    
    @api.model
    def create(self, vals):
        """Create MOM format and generate sequence number."""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mom.format.base') or _('New')
        
        # Initialize state_history
        if 'state_history' not in vals:
            vals['state_history'] = ''
        
        res = super(MOMFormat, self).create(vals)
        # Update state history for the 'created' event
        res._update_state_history('created', res.state or 'draft')
        return res
    
    def write(self, vals):
        """Override write to handle state changes and update state history."""
        old_states = {rec.id: rec.state for rec in self}
        
        res = super(MOMFormat, self).write(vals)
        
        if 'state' in vals:
            for record in self:
                old_state = old_states.get(record.id)
                new_state = vals.get('state')
                if old_state != new_state:
                    record._update_state_history(old_state, new_state)
        
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
        """Approve the MOM format record."""
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
        """Mark the MOM format as completed."""
        for record in self:
            if not record.actual_completion_date:
                raise UserError(_('Please set the actual completion date before marking as completed.'))
            record.state = 'completed'
        return True
    
    def action_cancel(self):
        """Cancel the MOM format record."""
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
    
    def action_print_mom(self):
        """Print the MOM report."""
        # This can be implemented later with a report template
        return {
            'type': 'ir.actions.report',
            'report_name': 'mom.report_mom_format',
            'report_type': 'qweb-pdf',
            'data': {},
            'context': self.env.context,
            'res_ids': self.ids,
        }
    
    @api.onchange('meeting_date')
    def _onchange_meeting_date(self):
        """Update target date based on meeting date if not set."""
        if self.meeting_date and not self.target_date:
            # Set target date to 7 days after meeting date by default
            self.target_date = fields.Date.add(self.meeting_date, days=7)
