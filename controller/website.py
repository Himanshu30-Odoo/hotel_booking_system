from odoo import http
from odoo.http import request

class HotelBookingWebsite(http.Controller):

    @http.route('/hotel/rooms', auth='public', website=True)
    def show_rooms(self, **kw):
        # Fetch available rooms
        rooms = request.env['hotel.room'].search([('available', '=', True)])
        return request.render('hotel_booking_system.room_list_template', {
            'rooms': rooms
        })
    
    @http.route('/hotel/book/<int:room_id>', auth='public', website=True)
    def book_room(self, room_id, **kw):
        # Fetch the selected room
        room = request.env['hotel.room'].browse(room_id)
        return request.render('hotel_booking_system.booking_form', {
            'room': room
        })
    
    @http.route('/hotel/confirm_booking', auth='public', website=True, methods=['POST'])
    def confirm_booking(self, **kw):
        room_id = int(kw.get('room_id'))
        guest_name = kw.get('guest_name')
        checkin_date = kw.get('checkin_date')
        checkout_date = kw.get('checkout_date')

        # Create guest record, if it doesn't exist
        guest = request.env['hotel.guest'].search([('name', '=', guest_name)], limit=1)
        if not guest:
            guest = request.env['hotel.guest'].create({
                'name': guest_name
            })

        # Fetch the selected room
        room = request.env['hotel.room'].browse(room_id)

        # Create the booking record
        room_booking = request.env['room.booking'].create({
            'guest_id': guest.id,  # Link to guest
            'room_id': room.id,  # Link to room
            'check_in': checkin_date,  # Set check-in date
            'check_out': checkout_date,  # Set check-out date
            'status': 'confirmed',  # Initial status
        })

        # Render confirmation page with booking details
        return request.render('hotel_booking_system.booking_confirmation', {
            'guest_name': guest_name,
            'room_name': room.name,
            'checkin_date': checkin_date,
            'checkout_date': checkout_date,
        })



class RoomWebsiteController(http.Controller):

    @http.route(['/rooms'], type='http', auth='public', website=True)
    def list_rooms(self, **kwargs):
        rooms = request.env['hotel.room'].sudo().search([])
        return request.render('hotel_booking_system.rooms_template', {
            'rooms': rooms
        })
    

class HotelRoomResetController(http.Controller):

    @http.route('/reset/rooms', type='json', auth='user')
    def reset_rooms(self):
        rooms = request.env['hotel.room'].sudo().search([])
        for room in rooms:
            room.write({'status': 'available'})
        return {'status': 'success', 'message': 'All rooms reset to available.'}
