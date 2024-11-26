# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


# class Gym(http.Controller):
#     @http.route('/gym/gym', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gym/gym/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gym.listing', {
#             'root': '/gym/gym',
#             'objects': http.request.env['gym.gym'].search([]),
#         })

#     @http.route('/gym/gym/objects/<model("gym.gym"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gym.object', {
#             'object': obj
#         })
#class UpocargoApi(http.Controller):
#    @http.route('/api/upocargo/data', type='json', auth='user', methods=['GET'], csrf=False)
#    def get_data(self):
#        data = request.env[''].search([]).read(['',''])
#        return {'data': data}
    
#    @http.route('api/upocargo/create', type='json', auth='user', methods=['POST'], CSRF=False)
#    def create_data(self, **kwargs):
#        nuevo_registro = request.env[''].create(**kwargs)
#        return {'success':True,'id':nuevo_registro.id}

class UpocargoAuth(http.Controller):
    @http.route('/upocargo/login', type='http', auth='public', methods=['GET','POST'], csrf=True)
    def login(self,**kwargs):
        if http.request.httprequest.method == 'POST':
            email = kwargs.get('email')
            password = kwargs.get('password')
            user = request.env['upocargo.cliente'].sudo().search([('email','=', email)])
            if user: #and user._check_password(password):
                if password == str(user.id_cliente) and not user.password:
                    request.session['cliente_id'] = user.id_cliente
                    return request.redirect('/upocargo/change_password')
                elif user._check_password(password):
                    request.session['cliente_id'] = user.id_cliente
                    return request.redirect('/upocargo/portal_home')
                else:
                    return http.request.render('upocargo.login_template',{
                        'error' : 'Credenciales incorrectas, intente de nuevo.'
                    })
            else:
                return http.request.render('upocargo.login_template',{
                    'error' : 'Credenciales incorrectas, intente de nuevo.'
                })
        else:
            return http.request.render('upocargo.login_template')
    
    @http.route('/upocargo/logout', type='http', auth='public',website=True)
    def logout(self):
        request.session.logout()
        return request.redirect('/upocargo/login')
    
    @http.route('/upocargo/change_password', type='http', auth='public', methods=['GET','POST'], csrf=True)
    def change_password(self,**kwargs):
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return request.redirect('/upocargo/login')
        cliente = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',cliente_id)],limit=1)
        if not cliente:
            return request.redirect('/upocargo/login')
        if http.request.httprequest.method == 'POST':
            new_password = kwargs.get("password")
            confirm_password = kwargs.get("password")
            if not new_password or new_password != confirm_password:
                return http.request.render('upocargo.change_password_template', {
                    'error': 'Las contraseñas no coinciden'
                })
            cliente.sudo().write({'password': new_password})
            return request.redirect('/upocargo/portal_home')
        return http.request.render('upocargo.change_password_template')

class UpocargoPortal(http.Controller):
    @http.route('/upocargo/portal_home', type='http', auth='public',methods=['GET','POST'])
    def portal_home(self,**kwargs):
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return request.redirect('/upocargo/login')
        cliente = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',cliente_id)],limit=1)
        if not cliente:
            return request.redirect('/upocargo/login')
        return http.request.render('upocargo.portal_home_template')
    
    @http.route('/upocargo/mudanzas', type='http', auth='public')
    def show_mudanzas(self):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        cliente = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',user_id)])#.browse(user_id)#.search(['id_cliente','=',user_id])
        if not cliente.exists():
            return request.redirect('/upocargo/login')
        mudanzas = cliente.mudanzas
        return request.render('upocargo.mudanzas_template', {
            'mudanzas': mudanzas
        })
    
    @http.route('/upocargo/facturas', type='http', auth='public')
    def show_facturas(self):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        cliente = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',user_id)])#.browse(user_id)#.search(['id_cliente','=',user_id])
        if not cliente.exists():
            return request.redirect('/upocargo/login')
        facturas = cliente.mudanzas.factura
        #facturas = request.env['upocargo.factura'].search([('mudanza_id.cliente','=',cliente.id_cliente)])
        return request.render('upocargo.facturas_template', {
            'facturas': facturas
        })
    
    @http.route('/upocargo/almacenamientos', type='http', auth='public')
    def show_almacenamientos(self):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        cliente = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',user_id)])#.browse(user_id)#.search(['id_cliente','=',user_id])
        if not cliente.exists():
            return request.redirect('/upocargo/login')
        almacenamientos = cliente.almacenamiento
        return request.render('upocargo.almacenamientos_template', {
            'almacenamientos': almacenamientos
        })