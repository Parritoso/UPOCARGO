from odoo.tests.common import HttpCase
from odoo import fields
import json

class TestUpocargoControllers(HttpCase):
    def test_login_correcto(self):
        # Simula una solicitud GET para cargar la página de login
        response = self.url_open('/upocargo/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<form action="/upocargo/login" method="post">', response.text)

        # Simula una solicitud POST para hacer login (usando credenciales válidas)
        post_data = {
            'email': 'cliente@upocargo.com',
            'password': '123456'
        }
        response = self.url_open('/upocargo/login', method='POST', data=post_data)
        self.assertRedirects(response, '/upocargo/portal_home')  # Verifica que la redirección es correcta
    
    def test_login_incorrecto(self):
        # Intento de login con credenciales incorrectas
        post_data = {
            'email': 'cliente@upocargo.com',
            'password': 'wrongpassword'
        }
        response = self.url_open('/upocargo/login', method='POST', data=post_data)
        self.assertIn('Credenciales incorrectas, intente de nuevo.', response.text)
    
    def test_logout(self):
        # Inicia sesión primero para poder probar el logout
        self.env['upocargo.cliente'].create({
            'id_cliente': 1,
            'email': 'cliente@upocargo.com',
            'password': '123456',
        })
        self.env['ir.http'].sudo().session.authenticate('db', 1, '123456')
        
        response = self.url_open('/upocargo/logout')
        self.assertRedirects(response, '/upocargo/login')  # Verifica que redirige al login
    
    def test_change_password(self):
        # Cambia la contraseña de un cliente autenticado
        cliente = self.env['upocargo.cliente'].create({
            'id_cliente': 1,
            'email': 'cliente@upocargo.com',
            'password': '123456'
        })
        
        self.env['ir.http'].sudo().session.authenticate('db', 1, '123456')
        
        # Simula una solicitud GET a la página de cambio de contraseña
        response = self.url_open('/upocargo/change_password')
        self.assertEqual(response.status_code, 200)
        
        # Simula la solicitud POST para cambiar la contraseña
        post_data = {
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }
        response = self.url_open('/upocargo/change_password', method='POST', data=post_data)
        self.assertRedirects(response, '/upocargo/portal_home')  # Verifica que redirige correctamente
        
        # Verifica si la contraseña fue realmente cambiada
        cliente = cliente.sudo().browse(cliente.id_cliente)
        self.assertEqual(cliente.password, 'newpassword')

    def test_show_mudanzas(self):
        # Crear un cliente de prueba con una mudanza
        cliente = self.env['upocargo.cliente'].create({
            'id_cliente': 1,
            'email': 'cliente@upocargo.com',
            'password': '123456'
        })
        self.env['ir.http'].sudo().session.authenticate('db', 1, '123456')
        
        mudanza = self.env['upocargo.mudanza'].create({
            'id_mudanza': 1,
            'cliente_id': cliente.id_cliente,
            'estado': 'pendiente'
        })
        
        response = self.url_open('/upocargo/mudanzas')
        self.assertEqual(response.status_code, 200)
        self.assertIn(mudanza.id_mudanza, response.text)

    def test_show_factura(self):
        # Crear una factura asociada a un cliente
        cliente = self.env['upocargo.cliente'].create({
            'id_cliente': 1,
            'email': 'cliente@upocargo.com',
            'password': '123456'
        })
        factura = self.env['upocargo.factura'].create({
            'id_factura': 1,
            'cliente_id': cliente.id_cliente,
            'precio': 100.0
        })
        
        response = self.url_open('/upocargo/facturas/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(factura.precio), response.text)
    
    def test_page_not_found(self):
        # Prueba para una página que no existe
        response = self.url_open('/upocargo/no_existe')
        self.assertEqual(response.status_code, 404)