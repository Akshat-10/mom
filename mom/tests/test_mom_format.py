# -*- coding: utf-8 -*-
from odoo.tests import common, TransactionCase
from odoo import fields
from odoo.exceptions import UserError


class TestMOMFormat(TransactionCase):
    """Test MOM format functionality"""
    
    def setUp(self):
        super(TestMOMFormat, self).setUp()
        
        # Create test employees
        self.employee_1 = self.env['hr.employee'].create({
            'name': 'Test Employee 1',
        })
        self.employee_2 = self.env['hr.employee'].create({
            'name': 'Test Employee 2',
        })
        
        # Create test partner
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })
        
        # Create test open point
        self.open_point = self.env['mom.open.point'].create({
            'name': 'Test Action Item',
            'category': 'action',
            'priority': 'high',
            'description': 'Test Description',
        })
    
    def test_mom_format_creation(self):
        """Test MOM format creation with auto sequence"""
        
        # Create MOM format
        mom_format = self.env['mom.format.base'].create({
            'meeting_title': 'Test Meeting',
            'meeting_date': fields.Date.today(),
            'open_point_id': self.open_point.id,
            'target_date': fields.Date.today(),
            'attendee_ids': [(6, 0, [self.employee_1.id, self.employee_2.id])],
            'conducted_by_id': self.employee_1.id,
        })
        
        # Check that sequence was generated
        self.assertTrue(mom_format.name and mom_format.name != 'New')
        self.assertIn('MOM/', mom_format.name)
        
        # Check initial state
        self.assertEqual(mom_format.state, 'draft')
        
        # Check state history
        self.assertIn('Record created in Draft state', mom_format.state_history)
    
    def test_mom_state_transitions(self):
        """Test MOM state transitions"""
        
        mom_format = self.env['mom.format.base'].create({
            'meeting_title': 'Test Meeting 2',
            'meeting_date': fields.Date.today(),
            'open_point_id': self.open_point.id,
            'target_date': fields.Date.today(),
        })
        
        # Test transition to in_progress
        mom_format.action_in_progress()
        self.assertEqual(mom_format.state, 'in_progress')
        self.assertIn('State changed from Draft to In Progress', mom_format.state_history)
        
        # Test completion without actual date (should fail)
        with self.assertRaises(UserError):
            mom_format.action_complete()
        
        # Set actual completion date and complete
        mom_format.actual_completion_date = fields.Date.today()
        mom_format.action_complete()
        self.assertEqual(mom_format.state, 'completed')
        
        # Test approval
        mom_format.action_approve()
        self.assertEqual(mom_format.state, 'approved')
        self.assertTrue(mom_format.approve_date)
        self.assertEqual(mom_format.approved_by_id, self.env.user)
        
        # Test cannot cancel approved record
        with self.assertRaises(UserError):
            mom_format.action_cancel()
    
    def test_open_point_statistics(self):
        """Test open point MOM count computation"""
        
        # Create multiple MOMs for the same open point
        for i in range(3):
            self.env['mom.format.base'].create({
                'meeting_title': f'Test Meeting {i}',
                'meeting_date': fields.Date.today(),
                'open_point_id': self.open_point.id,
                'target_date': fields.Date.today(),
            })
        
        # Check MOM count
        self.assertEqual(self.open_point.mom_count, 3)
        
        # Test action to view MOMs
        action = self.open_point.action_view_moms()
        self.assertEqual(action['res_model'], 'mom.format.base')
        self.assertEqual(action['domain'], [('open_point_id', '=', self.open_point.id)])
