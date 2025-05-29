from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class PortalBooking(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        booking_count = request.env['room.booking'].search_count([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        values['booking_count'] = booking_count
        return values

    @http.route(['/my/bookings'], type='http', auth="user", website=True)
    def portal_my_bookings(self, **kwargs):
        bookings = request.env['room.booking'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        return request.render("hotel_booking_system.portal_my_bookings_template", {
            'bookings': bookings
        })
