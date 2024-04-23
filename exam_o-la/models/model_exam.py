from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # The fields 'bono' and 'moneda_para_bonos' are defined and are editable only in the 'draft' state.
    resumen_bono_ids = fields.One2many('resumen.bono', 'sale_order_id', string='Resumen de Bonos')
    bono = fields.Boolean(string='Bono', readonly=True, states={'draft': [('readonly', False)]})
    moneda_para_bonos = fields.Many2one('res.currency', string='Moneda para bonos', readonly=True, states={'draft': [('readonly', False)]})
    # A function is defined that is triggered when 'order_line' or 'moneda_para_bonos' changes.
    @api.onchange('order_line', 'moneda_para_bonos')
    def _compute_bono(self):
        for record in self:
            if record.bono:
                # Delete existing records in 'resumen_bono_ids'.
                record.resumen_bono_ids = [(5, 0, 0)]
                # For each order line with 'bono' activated, a new record is created in 'resumen_bono_ids'.
                for line in record.order_line:
                    if line.bono:
                         # The amount is calculated as 20% of the subtotal of the line converted into the currency of the bond.
                        monto = line.price_subtotal * 0.20
                        if record.moneda_para_bonos != line.currency_id:
                            monto = line.currency_id._convert(monto, record.moneda_para_bonos, record.company_id, fields.Date.today())
                        # The new register is created
                        record.resumen_bono_ids = [(0, 0, {
                            'name': f"Bono de {line.product_id.name} para {record.name}",
                            'producto': line.product_id.id,
                            'monto': monto,
                        })]
                pass

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    bono = fields.Boolean(string='Bono')
    # Here is the logic for updating the bono field
    @api.onchange('product_id')
    def _onchange_bono(self):
        self.bono = True
        pass

class ResumenBono(models.Model):
    _name = 'resumen.bono'
    name = fields.Char(compute='_compute_name')
    producto = fields.Many2one('product.product', string='Producto')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    moneda_para_bonos = fields.Many2one('res.currency', related='sale_order_id.moneda_para_bonos', string='Moneda para bonos', readonly=True)
    monto = fields.Monetary(string='Monto', currency_field='moneda_para_bonos')

    @api.depends('producto')
    def _compute_name(self):
        for record in self:
            record.name = f"Bono de {record.producto.name} para {record.sale_order_id.name}"


