# -*- coding: utf-8 -*-
{
    'name': 'Reporte Consolidado de Órdenes de Venta',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Genera un reporte PDF consolidado agrupando las líneas de múltiples órdenes de venta por categoría.',
    'description': """
Módulo que permite seleccionar múltiples Órdenes de Venta desde la vista de lista
y abrir un asistente para generar un reporte PDF consolidado. Agrupa los productos
por su categoría, suma cantidades (pedidas o entregadas) y calcula precios promedio/subtotales.
    """,
    'author': 'Antigravity',
    'website': 'https://www.odoo.com',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_action.xml',
        'report/report_action.xml',
        'report/consolidated_report.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
