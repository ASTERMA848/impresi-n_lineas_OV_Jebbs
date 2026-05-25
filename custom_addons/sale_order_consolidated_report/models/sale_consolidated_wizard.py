# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleConsolidatedReportWizard(models.TransientModel):
    _name = 'sale.consolidated.report.wizard'
    _description = 'Asistente de Reporte Consolidado de Ventas'

    order_ids = fields.Many2many(
        'sale.order',
        string='Órdenes de Venta',
        required=True,
        help='Seleccione las órdenes de venta a consolidar'
    )
    
    qty_source = fields.Selection([
        ('ordered', 'Cantidad Pedida'),
        ('delivered', 'Cantidad Entregada')
    ], string='Cantidad a Sumar', default='ordered', required=True)
    
    show_prices = fields.Boolean(
        string='Mostrar Precios y Subtotales',
        default=False,
        help='Si se activa, el PDF mostrará los precios unitarios promedio y subtotales por producto.'
    )

    @api.model
    def default_get(self, fields_list):
        res = super(SaleConsolidatedReportWizard, self).default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')
        if active_model == 'sale.order' and active_ids:
            res['order_ids'] = [(6, 0, active_ids)]
        return res

    def get_order_names(self):
        """Devuelve los nombres de las órdenes seleccionadas separados por comas."""
        self.ensure_one()
        return ", ".join(self.order_ids.mapped('name'))

    def get_consolidated_lines(self):
        """Agrupa y consolida las líneas de productos por categoría."""
        self.ensure_one()
        categories_dict = {}

        for order in self.order_ids:
            for line in order.order_line:
                # Omitimos líneas sin producto (como notas o secciones)
                if not line.product_id:
                    continue
                
                # Categoría de producto
                category = line.product_id.categ_id
                category_name = category.complete_name or category.name or 'Sin Categoría'
                
                # Cantidad según configuración del wizard
                qty = line.product_uom_qty if self.qty_source == 'ordered' else line.qty_delivered
                
                # Datos del producto
                product = line.product_id
                uom_name = line.product_uom_id.name or product.uom_id.name or 'UoM'
                price_unit = line.price_unit
                subtotal = line.price_subtotal if self.qty_source == 'ordered' else (line.qty_delivered * line.price_unit)
                
                if category_name not in categories_dict:
                    categories_dict[category_name] = {}
                    
                product_id = product.id
                if product_id not in categories_dict[category_name]:
                    categories_dict[category_name][product_id] = {
                        'product_name': product.display_name or product.name,
                        'qty': 0.0,
                        'uom': uom_name,
                        'price_total': 0.0,
                        'subtotal': 0.0,
                        'line_count': 0,
                    }
                    
                categories_dict[category_name][product_id]['qty'] += qty
                categories_dict[category_name][product_id]['price_total'] += price_unit
                categories_dict[category_name][product_id]['subtotal'] += subtotal
                categories_dict[category_name][product_id]['line_count'] += 1

        # Construcción de la estructura ordenada para el QWeb
        sorted_categories = []
        for cat_name, products in sorted(categories_dict.items()):
            product_list = []
            for prod_id, data in sorted(products.items(), key=lambda item: item[1]['product_name']):
                # Precio promedio ponderado
                avg_price = data['subtotal'] / data['qty'] if data['qty'] > 0 else (data['price_total'] / data['line_count'] if data['line_count'] > 0 else 0.0)
                product_list.append({
                    'name': data['product_name'],
                    'qty': data['qty'],
                    'uom': data['uom'],
                    'price_unit': avg_price,
                    'subtotal': data['subtotal'],
                })
            sorted_categories.append({
                'name': cat_name,
                'products': product_list,
            })
            
        return sorted_categories

    def action_print_report(self):
        """Lanza la acción del reporte QWeb cargando el wizard como origen de datos."""
        self.ensure_one()
        return self.env.ref('sale_order_consolidated_report.action_report_sale_consolidated').report_action(self)
