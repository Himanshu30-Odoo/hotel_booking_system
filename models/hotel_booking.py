from odoo import models, fields, api,_
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError , UserError 
import re

#  ==============================================================This is a HotelRoom Class======================================================================================================

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'


    # This is a Some Fields 

    tracking = fields.Char(string="Tracking", readonly=True, default='New')
    name = fields.Char('Room Number', required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ], required=True)
    price = fields.Float('Price per Night')
    status = fields.Selection([
    ('available', 'Available'),
    ('booked', 'Booked'),
    ('cleaning', 'Cleaning Room'),
    ], string='Status', default='available')


    prioritys = fields.Selection([
        ('1', 'Very Low'),
        ('2', 'Urgent'),
        ], string="Priority", default='1', tracking=True)

    
    # This is a Sequence Number Generate 

    @api.model
    def create(self,vals):
        vals.update({
                    'tracking':self.env['ir.sequence'].next_by_code('hotel.room') or _('New')
                })
        res = super(HotelRoom,self).create(vals)
        return res
    

    # This is a button For Workflow in Status Field 

    def button_booked(self):
        for rec in self:
            rec.status = 'booked'

    def button_cleaning(self):
        for rec in self:
            rec.status = 'cleaning'

    def button_available(self):
        for rec in self:
            rec.status = 'available'

#  ==============================================================This is a HotelGuest Class======================================================================================================

class HotelGuest(models.Model):
    _name = 'hotel.guest'
    _description = 'Hotel Guest'

    tracking = fields.Char(string="Tracking", readonly=True, default='New')
    name = fields.Char('Guest Name', required=True)
    email = fields.Char('Email-ID')
    phone = fields.Char('Phone-No.', required=True, size=11)
    booking_date = fields.Date(string="Booking Date")
    adhar_no = fields.Char(string="Adhar-card No.", required=True, size=14)
    pan_no = fields.Char(string="Pan-card No.", required=True, size=10)
    prioritys = fields.Selection([
        ('1', 'Very Low'),
        ('2', 'Urgent'),
    ], string="Priority", default='1', tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)
    age = fields.Float(string="Age")
    nationality = fields.Many2one('res.country', string="Nationality", required=True)
    country_code = fields.Char(string="Country Code", size=5, compute='_compute_country_code', store=True)


    @api.model
    def create(self,vals):
        vals.update({
                    'tracking':self.env['ir.sequence'].next_by_code('hotel.guest') or _('New')
                })
        res = super(HotelGuest,self).create(vals)
        return res
    
    @api.onchange('adhar_no')
    def _onchange_adhar_no(self):
        if self.adhar_no:
            self.adhar_no = self._format_adhar(self.adhar_no)

    def _format_adhar(self, number):
        number = ''.join(filter(str.isdigit, number))  # Keep only numbers
        if len(number) == 12:
            return '{} {} {}'.format(number[:4], number[4:8], number[8:12])
        return number

    @api.depends('nationality')
    def _compute_country_code(self):
        for record in self:
            if record.nationality and record.nationality.phone_code:
                record.country_code = f'+{record.nationality.phone_code}'
            else:
                record.country_code = ''

    @api.onchange('nationality')
    def _onchange_nationality(self):
        for record in self:
            if record.nationality and record.nationality.phone_code:
                code = f'+{record.nationality.phone_code}'
                record.country_code = code

                if record.phone:
                    number = record.phone.lstrip('0')  # remove any starting zero
                    record.phone = f'{code} {number}'

    

#  ==============================================================This is a RoomBooking Class======================================================================================================

class RoomBooking(models.Model):
    _name = 'room.booking'
    _description = 'Room Booking'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    # This is a Some Fields 

    name = fields.Char(string="Ticket Reference", required=True, copy=False, readonly=True, default='New')
    tracking = fields.Char(string="Tracking", readonly=True, default='New')
    guest_id = fields.Many2one('hotel.guest', string='Guest', required=True)
    room_id = fields.Many2one('hotel.room', string='Room', required=True)
    description = fields.Text(String="Description")
    gender = fields.Selection(string='Gender', required=True,selection=[('male','Male'),('female','Female')])
    attachment_ids = fields.One2many('ir.attachment','booking_id',string= 'Document', required=True)
    facilities_ids = fields.Many2many('hotel.facility.ticket',string="Facility")
    document = fields.Binary(string='Documents',limit="5")
    check_in = fields.Date('Check-In', required=True )
    check_out = fields.Date('Check-Out', required=True)
    tax_ids = fields.Many2many('account.tax','tax_id',string="Taxes")
    total_amount = fields.Monetary(string="Total Amount", currency_field='currency_id',compute='_compute_total_amount', store=True)
    amount_with_tax = fields.Float(string="Total with Tax", compute='_compute_amount_with_tax', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], default='draft')
    
    priority = fields.Selection([
        ('1', 'Very Low'),
        ('2', 'Urgent'),
        ], string="Priority", default='1', tracking=True)
    
    prioritys = fields.Selection([
            ('1', 'Very Low'),
            ('2', 'Low'),
            ('3', 'Medium'),
            ('4', 'Very Medium'),
            ('5', 'High'),
            ('6', 'Very High')
            ], string="Priority", default='3', tracking=True) 
    
    invoice_ids = fields.One2many('account.move', 'room_booking_id', string="Invoices")  
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    user_id = fields.Many2one('res.users', string="Assigned User")
    activity_ids = fields.One2many('mail.activity', 'res_id', string="Activities")
    color = fields.Integer(string="Color Index", default=3)
    booking_date = fields.Date(string="Booking Date")
    start_date = fields.Date('Start Date') 
    end_date = fields.Date('End Date') 


    # This is A _comupte Method Use For Check_in & Check_out In Distance Days And Count Price  
    
    @api.depends('check_in', 'check_out', 'room_id')
    def _compute_total_amount(self):
        for record in self:
            if record.check_in and record.check_out and record.room_id:
                days = (record.check_out - record.check_in).days or 1
                record.total_amount = days * record.room_id.price
            else:
                record.total_amount = 0.0

    # This is a _coumpute Method Use For Count Amount With Tax

    @api.depends('total_amount', 'tax_ids')
    def _compute_amount_with_tax(self):
        for record in self:
            total = record.total_amount
            tax_amount = 0.0

            for tax in record.tax_ids:
                if tax.amount_type == 'percent':
                    tax_amount += total * (tax.amount / 100)
                elif tax.amount_type == 'fixed':
                    tax_amount += tax.amount

            record.amount_with_tax = total + tax_amount


    # This is a Sequence Number Generate 

    @api.model
    def create(self,vals):
        vals.update({
                    'tracking':self.env['ir.sequence'].next_by_code('room.booking') or _('New')
                })
        res = super(RoomBooking,self).create(vals)
        return res
    
    # This is a button For Workflow in Status Field 

    def button_draft(self):
       self.status='draft'
      
    def button_confirmed(self):
        self.status='confirmed'    
        
    def button_checked_in(self):
        self.status='checked_in'  

    def button_checked_out(self):
        self.status='checked_out' 

    def button_cancelled(self):
        self.status='cancelled'  


    # This is a Smart Button For Attachments 

    def view_booking(self):
        attachment_ids = self.attachment_ids

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Bookings',
            'res_model': 'ir.attachment',
            'view_mode': 'kanban',
            'context':"{'default_res_model': 'room.booking', 'default_res_id': active_id}",
        }

        if len(attachment_ids) == 1:
            action['views'] = [(self.env.ref('hotel_booking_system.ir.actions.act_window').id, 'kanban')]
            action['res_id'] = attachment_ids.ids
        elif len(attachment_ids) > 1:
            action['domain'] = [('id', 'in', attachment_ids.ids)]
        else:
            return {'type': 'ir.actions.act_window_close'}

        return action
    
    # This is a Smart Button In Count Data For Booking in Attachment Data 

    booking_total_count = fields.Integer(string="Booking Count", compute="_compute_booking_count")

    def _compute_booking_count(self):
        for rec in self:
            rec.booking_total_count = len(rec.attachment_ids)

    
    # This is a Smart Button For Rooms

    def view_rooms(self):

        room = self.room_id
        if not room:
            return {'type': 'ir.actions.act_window_close'}

        action = self.env.ref('hotel_booking_system.action_hotel_rooms').sudo().read()[0]

        action.update({
            'view_mode': 'form',
            'res_id': room.id,
            'context': dict(self._context),
        })

        return action

    
    # This is a Validation Error

    @api.onchange('check_in', 'check_out')
    def onchange_of_check_out(self):
       if self.check_in and self.check_out:
           if self.check_out <= self.check_in:
               raise ValidationError("Check Out must be greater than the Check In.")


    # This is a User Error

    @api.constrains('description')
    def onchange_description(self):
            if self.description:
                raise UserError("Please Enter A Description.")


    @api.onchange('guest_id')
    def _onchange_guest_id(self):
        if self.guest_id:
            self.booking_date = self.guest_id.booking_date

   


#  ==============================================================This is a HotelFacility Class======================================================================================================

class HotelFacilityTicket(models.Model):
    _name = 'hotel.facility.ticket'
    _description = 'Hotel Facility Ticket'


    # This is a Some Fields 

    tracking = fields.Char(string="Tracking", readonly=True, default='New')
    name = fields.Char(string="Ticket Reference", required=True, copy=False, readonly=True, default='New')
    # names = fields.Char(string='Facility Name', required=True)
    facility_name = fields.Char(string="Facility Name")
    user_id = fields.Many2one('res.users', string="Assigned User")
    activity_ids = fields.One2many('mail.activity', 'res_id', string="Activities")

    facility_type = fields.Selection([
            ('maintenance', 'Maintenance'),
            ('service', 'Guest Service'),
            ('booking', 'Facility Booking'),
        ], string="Facility Type", required=True)

    assigned_employee_id = fields.Many2one('hr.employee', string="Assigned Employee")
    date_requested = fields.Datetime(string="Date Requested", default=fields.Datetime.now)
    date_completed = fields.Datetime(string="Date Completed")
    description = fields.Text(string="Description")
    price = fields.Monetary(string="Price", currency_field='company_currency')
    file = fields.Image(string='Image', max_width=128, max_height=128)
    day = fields.Integer(string="Day", default=1)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')
    
    color = fields.Integer(string="Color Index", default=3)
    priority = fields.Selection([
            ('1', 'Very Low'),
            ('2', 'Low'),
            ('3', 'Medium'),
            ('4', 'Very Medium'),
            ('5', 'High'),
            ('6', 'Very High')
            ], string="Priority", default='3', tracking=True) 
      
    prioritys = fields.Selection([
            ('1', 'Very Low'),
            ('2', 'Urgent'),
            ], string="Priority", default='1', tracking=True)
   
    company_currency = fields.Many2one('res.currency', string="Company Currency", default=lambda self: self.env.company.currency_id)

    # This is a button For Workflow in Status Field 

    # def button_draft(self):
    #     self.write({'status': 'draft'})
    
    # def button_in_progress(self):
    #     self.write({'status': 'in_progress'})
    
    # def button_done(self):
    #     self.write({'status': 'done'})
    
    # def button_cancelled(self):
    #     self.write({'status': 'cancelled'})

    # This is a Sequence Number Generate 

    @api.model
    def create(self, vals):
        if 'name' not in vals:
            vals['name'] = self.env['ir.sequence'].next_by_code('hotel.facility.ticket') or 'New Ticket'
        return super(HotelFacilityTicket, self).create(vals)


#  ==============================================================This is a Attachments Class======================================================================================================

class Attachments(models.Model):
    _inherit = 'ir.attachment'

    # This is a Some Fields 

    booking_id = fields.Many2one('room.booking',string="Booking")



#  ==============================================================This is a AccountTax Class======================================================================================================


class AccountTax(models.Model):
    _inherit = 'account.tax'

    # This is a Some Fields 

    color = fields.Integer("Color Index")

#  ==============================================================This is a AccountMove Class======================================================================================================

class AccountMove(models.Model):
    _inherit = 'account.move'

    room_booking_id = fields.Many2one('room.booking', string="Room Booking")
