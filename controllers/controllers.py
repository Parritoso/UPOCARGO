# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)


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
            proveedor = request.env['upocargo.proveedor'].sudo().search([('email', '=', email)])
            if proveedor:
                if proveedor._check_password(password):
                    request.session['proveedor_id'] = proveedor.id_proveedor
                    return request.redirect('/upocargo/portal_home_proveedor')  # Página del proveedor
                else:
                    return http.request.render('upocargo.login_template', {
                        'error': 'Credenciales incorrectas, intente de nuevo.'
                    })
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
    @http.route('/upocargo', type='http', auth='none')
    def upocargo(self, **kwargs):
        return http.request.render('upocargo.upocargo_index')

    @http.route('/upocargo/portal_home', type='http', auth='public',methods=['GET','POST'])
    def portal_home(self,**kwargs):
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return request.redirect('/upocargo/login')
        cliente = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',cliente_id)],limit=1)
        if not cliente:
            return request.redirect('/upocargo/login')
        return http.request.render('upocargo.portal_home_template')
    
    @http.route('/upocargo/modificar_datos', type='http', auth='public',csfr=True)
    def modificar_datos(self, **kwargs):
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return request.redirect('/upocargo/login')
        user = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',cliente_id)],limit=1)
        return http.request.render('upocargo.modificar_datos_template', {'user': user})
    
    # Ruta para guardar los cambios del usuario
    @http.route('/upocargo/guardar_datos', type='http', auth='user', methods=['POST'], csfr=True)
    def guardar_datos(self, **kwargs):
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return request.redirect('/upocargo/login')
        user = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',cliente_id)],limit=1)
        email = kwargs.get('email')
        name = kwargs.get('name')
        dir = kwargs.get('dir')
        telf = kwargs.get('tlf')
        password = kwargs.get('password')

        # Verificar que la contraseña introducida sea correcta
        if not user._check_password(password):
            return request.render('upocargo.modificar_datos_template', {
                'error': 'Contraseña incorrecta. Por favor, intente de nuevo.',
                'user': user
            })

        # Guardar los cambios en los datos del usuario
        user.write({
            'email': email,
            'name': name,
            'direccion': dir,
            'telefono': telf
        })
        
        # Redirigir al usuario a la página de inicio con un mensaje de éxito
        return http.request.redirect('/upocargo/portal_home')
    
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
    
    @http.route('/upocargo/mudanzas/<string:id_mudanza>', type='http', auth='public')
    def show_mudanza(self, id_mudanza, **kwargs):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        mudanza = request.env['upocargo.mudanza'].sudo().search([('id_mudanza','=',id_mudanza)],limit=1)
        if not mudanza:
            return http.request.not_found("Mudanza no encontrada D:")
        if not user_id == mudanza.cliente.id_cliente:
            return request.redirect('/upocargo/mudanzas')
        servicios_cliente = request.env['upocargo.servicios_adicionales'].sudo().search([('cliente.id_cliente', '=', user_id), ('estado', '=', 'true'),'|', ('aplicable_a','=','mudanza'),('aplicable_a', '=', 'ambos')])
        if http.request.httprequest.method == 'POST':
            _logger.info("Method POST")
            action = kwargs.get('action')
            _logger.info("action: "+action)
            if action == 'cancelar':
                _logger.info("cancelar")
                return self.cancelar_mudanza(mudanza)
            elif action == 'atrasar':
                return self.atrasar_mudanza(mudanza, kwargs.get('dias_atraso'))
            elif action == 'agregar_servicio':
                # Obtener el servicio adicional seleccionado
                servicio_id = kwargs.get('servicio_id')
                if servicio_id:
                    servicio = request.env['upocargo.servicios_adicionales'].sudo().search([('id_servicios', '=', servicio_id)], limit=1)
                    if servicio:
                        # Asignar el servicio a la mudanza
                        mudanza.servicios_adicionales = [(4, servicio.id)]
        return http.request.render('upocargo.mudanza_detail',{
            'id_mudanza': mudanza,
            'servicios_disponibles': servicios_cliente
        })
    
    def cancelar_mudanza(self, mudanza):
        # Cambiar el estado a 'Cancelado'
        mudanza.write({'estado': 'cancelado'})
        
        # Comprobar si la fecha de la mudanza es dentro de una semana
        if mudanza.fecha and mudanza.fecha <= (fields.Date.today() + timedelta(weeks=1)):
            # Generar factura con la mitad del precio
            factura = mudanza.factura
            if factura:
                precio_original = factura.precio
                factura.write({'precio': precio_original / 2})
                factura.agregar_gasto("Mudanza Cancelada", precio_original-(precio_original/2))
        
        # Redirigir a la página de detalles de la mudanza
        return request.redirect('/upocargo/mudanzas/%s' % mudanza.id_mudanza)

    def atrasar_mudanza(self, mudanza, dias_atraso):
        # Atrasar la fecha de la mudanza
        if not dias_atraso=='':
            nueva_fecha = fields.Date.from_string(mudanza.fecha) + timedelta(days=int(dias_atraso))
            mudanza.write({'fecha': nueva_fecha})
            
            # Actualizar la factura añadiendo el coste extra por día de atraso
            factura = mudanza.factura
            if factura:
                # Suponemos un coste extra por día
                coste_extra_por_dia = 10  # Por ejemplo, 10 unidades de la moneda por día
                aumento = (int(dias_atraso) * coste_extra_por_dia)
                nuevo_precio = factura.precio + aumento
                factura.write({'precio': nuevo_precio})
                factura.agregar_gasto(("Mudanza atrasana "+dias_atraso+" dias"),aumento)
        
        # Redirigir a la página de detalles de la mudanza
        return request.redirect('/upocargo/mudanzas/%s' % mudanza.id_mudanza)
    
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
    
    @http.route('/upocargo/facturas/<string:id_factura>', type='http', auth='public')
    def show_factura(self, id_factura):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        factura = request.env['upocargo.factura'].sudo().search([('id_factura','=',id_factura)],limit=1)
        if not factura:
            return http.request.not_found("Factura no encontrada D:")
        if not user_id == factura.mudanza_id.cliente.id_cliente:
            return request.redirect('/upocargo/facturas')
        return http.request.render('upocargo.factura_detail',{
            'factura': factura
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
    
    @http.route('/upocargo/almacenamientos/<string:id_almacenamiento>', type='http', auth='public')
    def show_almacenamiento(self, id_almacenamiento, **kwargs):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        almacenamiento = request.env['upocargo.almacenamiento'].sudo().search([('id_almacenamiento','=',id_almacenamiento)],limit=1)
        if not almacenamiento:
            return http.request.not_found("Almacenamiento no encontrada D:")
        if not user_id == almacenamiento.cliente.id_cliente:
            return request.redirect('/upocargo/almacenamiento')
        servicios_cliente = request.env['upocargo.servicios_adicionales'].sudo().search([('cliente.id_cliente', '=', user_id), ('estado', '=', 'true'),'|', ('aplicable_a','=','almacenamiento'),('aplicable_a', '=', 'ambos')])
        if http.request.httprequest.method == 'POST':
            action = kwargs.get('action')
            if action == 'atrasar':
                return self.atrasar_almacenamiento(almacenamiento, kwargs.get('dias_atraso'))
            elif action == 'agregar_servicio':
                # Obtener el servicio adicional seleccionado
                servicio_id = kwargs.get('servicio_id')
                if servicio_id:
                    servicio = request.env['upocargo.servicios_adicionales'].sudo().search([('id_servicios', '=', servicio_id)], limit=1)
                    if servicio:
                        # Asignar el servicio a la mudanza
                        almacenamiento.servicios_adicionales = [(4, servicio.id)]
        return http.request.render('upocargo.mudanza_detail',{
            'almacenamiento': almacenamiento,
            'servicios_disponibles': servicios_cliente
        })
    
    def atrasar_almacenamiento(self, almacenamiento, dias_atraso):
        # Atrasar la fecha de salida
        if not dias_atraso=='':
            nueva_fecha_salida = fields.Date.from_string(almacenamiento.fecha_salida) + timedelta(days=int(dias_atraso))
            almacenamiento.write({'fecha_salida': nueva_fecha_salida})
            
            # Actualizar la factura, añadiendo un costo adicional por cada día extra
            factura = almacenamiento.factura_id
            if factura:
                # Supongamos que el costo adicional es de 5 unidades monetarias por cada día adicional
                coste_extra_por_dia = 5  # Ejemplo: 5 unidades monetarias por día
                aumento = (int(dias_atraso) * coste_extra_por_dia)
                nuevo_precio = factura.precio + aumento
                factura.write({'precio': nuevo_precio})
                factura.agregar_gasto("Almacenamiento "+almacenamiento.id_almacenamiento+" atrasado "+dias_atraso+" dias",aumento)
        
        # Redirigir a la página de detalles del almacenamiento
        return request.redirect('/upocargo/almacenamientos/%s' % almacenamiento.id_almacenamiento)
    
    @http.route('/upocargo/marketplace', type='http', auth="public")
    def marketplace(self, **kwargs):
        # Obtener todos los servicios adicionales activos
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        services = request.env['upocargo.servicios_adicionales'].search([('estado', '=', 'true')])

        # Obtener los datos del usuario
        user = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',user_id)])

        # Devolver la página con los servicios y la información del usuario
        return request.render('upocargo.marketplace_page', {
            'services': services,
            'user': user,
        })
    
    @http.route('/upocargo/search_servicios', type='http', auth="public")
    def search_servicios(self, search='', **kwargs):
        # Definir los dominios de búsqueda
        domain = []
        
        if search:
            # Filtrar por nombre del servicio adicional
            domain += ['|', ('tipo', 'ilike', search), ('proveedores.name', 'ilike', search)]

        # Obtener los servicios que coinciden con el criterio de búsqueda
        services = request.env['upocargo.servicios_adicionales'].search(domain)

        # Obtener los datos del usuario
        user = request.env.user

        # Devolver la página con los servicios filtrados
        return request.render('upocargo.marketplace_page', {
            'services': services,
            'user': user,
        })
    
    @http.route('/upocargo/servicio_adicional/<string:service>', 
                type='http', auth="public")
    def servicio_adicional(self, service, **kwargs):
        # Comprobar si el usuario está suscrito a este servicio
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        servicio = request.env['upocargo.servicios_adicionales'].sudo().search([('id_servicios','=', service)],limit=1)
        if not servicio:
            return http.request.not_found("Servicio no encontrado D:")
        user = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',user_id)])
        is_subscribed = bool(request.env['upocargo.servicios_adicionales'].sudo().search([('cliente.id_cliente','=',user_id)]))

        # Mostrar la vista del servicio con los detalles
        return request.render('upocargo.servicio_adicional_page', {
            'service': servicio,
            'user': user,
            'is_subscribed': is_subscribed,
        })
    
    @http.route('/upocargo/suscribirse_servicio/<string:service>', 
                type='http', auth="public")
    def suscribirse_servicio(self, service, **kwargs):
        user_id = request.session.get('cliente_id')
        user = request.env['upocargo.cliente'].sudo().search([('id_cliente','=',user_id)])
        # Comprobar si el usuario ya está suscrito al servicio
        servicio_adicional = request.env['upocargo.servicios_adicionales'].search([
            ('id_servicios', '=', service),
            ('cliente', '=', user.id)
        ], limit=1)

        if servicio_adicional:
            # Si está suscrito, desuscribir
            servicio_adicional.write({'cliente': None})
        else:
            # Si no está suscrito, suscribir
            servicio = request.env['upocargo.servicios_adicionales'].search([
                ('id_servicios', '=', service)
            ], limit=1)
            if servicio:
                servicio.write({'cliente': user.id})

        # Redirigir al usuario de nuevo a la página del servicio
        return request.redirect('/upocargo/servicio_adicional/{}'.format(service))
    
    @http.route('/upocargo/servicios_contratados', type='http', auth="public")
    def servicios_contratados(self, **kwargs):
        # Obtener el id del cliente desde la sesión
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')

        # Obtener los servicios suscritos por el usuario
        servicios_contratados = request.env['upocargo.servicios_adicionales'].search([
            ('cliente.id_cliente', '=', user_id)
        ])

        # Obtener la información del usuario
        user = request.env['upocargo.cliente'].sudo().search([('id_cliente', '=', user_id)])

        # Renderizar la página con los servicios suscritos y la información del usuario
        return request.render('upocargo.servicios_contratados_page', {
            'services': servicios_contratados,
            'user': user,
        })
    
    @http.route('/upocargo/guardar_servicio_adicional', type='http', auth='public', methods=['POST'], csrf=True)
    def crear_servicio_adicional(self, **post):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        proveedor_id = request.session.get('proveedor_id')
        if not proveedor_id:
            return request.redirect('/upocargo/login')
        tipo = post.get('tipo')
        estado = post.get('estado')
        aplicable_a = post.get('aplicable_a')
        precio_base = float(post.get('precio_base'))
        
        
        # Crear el servicio adicional
        servicio_adicional = request.env['upocargo.servicios_adicionales'].create({
            'tipo': tipo,
            'estado': estado,
            'aplicable_a': aplicable_a,
            'precio_base': precio_base,
            'proveedores': [(6, 0, [proveedor_id])]
        })
        
        return request.redirect('/upocargo/servicio_adicional/%s' % servicio_adicional.id_servicios)
    
    @http.route('/upocargo/portal_home_proveedor', type='http', auth='public')
    def portal_home_proveedor(self, **post):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        proveedor_id = request.session.get('proveedor_id')
        if not proveedor_id:
            return request.redirect('/upocargo/login')
        return http.request.render('upocargo.portal_home_proveedor')
    
    @http.route('/upocargo/crear_servicio_adicional', type='http', auth='public')
    def portal_home_proveedor(self, **post):
        user_id = request.session.get('cliente_id')
        if not user_id:
            return request.redirect('/upocargo/login')
        proveedor_id = request.session.get('proveedor_id')
        if not proveedor_id:
            return request.redirect('/upocargo/login')
        return http.request.render('upocargo.crear_servicio_adicional_template')