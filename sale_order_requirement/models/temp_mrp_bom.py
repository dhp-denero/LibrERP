# -*- coding: utf-8 -*-
# © 2017 Antonio Mignolli - Didotech srl (www.didotech.com)

from openerp.osv import orm, fields
import decimal_precision as dp
from mrp import mrp_bom


class temp_mrp_bom(orm.Model):
    _name = 'temp.mrp.bom'

    def _stock_availability(self, cr, uid, ids, name, args, context=None):
        context = context or self.pool['res.users'].context_get(cr, uid)
        warehouse_order_point_obj = self.pool['stock.warehouse.orderpoint']
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {
                'stock_availability': 0,
                'spare': 0,
            }
            spare = 0
            try:
                warehouse = line.sale_order_id.shop_id.warehouse_id
                order_point_ids = warehouse_order_point_obj.search(cr, uid, [('product_id', '=', line.product_id.id), ('warehouse_id', '=', warehouse.id)], context=context, limit=1)
                if order_point_ids:
                    spare = warehouse_order_point_obj.browse(cr, uid, order_point_ids, context)[0].product_min_qty

                res[line.id] = {
                    'stock_availability': line.product_id and line.product_id.type != 'service' and line.product_id.qty_available or False,
                    'spare': spare,
                }
            except Exception as e:
                print e.message
        return res

    def get_color(self, cr, uid, ids, field_name, arg, context):
        res = {}
        colors = ['black', 'blue', 'cadetblue', 'grey']
        for line in self.browse(cr, uid, ids, context):
            try:
                row_color = colors[line.level]
            except KeyError:
                row_color = 'grey'

            if line.stock_availability < line.spare:
                row_color = 'red'
            res[line.id] = row_color
        return res

    _columns = {
        'name': fields.char('Name', size=160, readonly=True),
        'complete_name': fields.char('Complete name', readonly=True),
        'order_requirement_line_id': fields.many2one('order.requirement.line', 'Order requirement line', required=True),
        'bom_lines': fields.one2many('temp.mrp.bom', 'bom_id', 'BoM Lines'),
        'bom_id': fields.many2one('temp.mrp.bom', 'Parent BoM', select=True),

        'product_id': fields.many2one('product.product', 'Product', required=True),
        'product_uos_qty': fields.float('Product UOS Qty'),
        'product_uos': fields.many2one('product.uom', 'Product UOS',
                                       help="Product UOS (Unit of Sale) is the unit of measurement for the invoicing and promotion of stock."),
        'product_qty': fields.float('Product Qty', required=True, digits_compute=dp.get_precision('Product UoM')),
        'product_uom': fields.many2one('product.uom', 'Product UOM', required=True,
                                       help="UoM (Unit of Measure) is the unit of measurement for the inventory control"),
        'product_type': fields.char('Pr.Type', size=10, readonly=True),
        'sale_order_id': fields.related('order_requirement_line_id', 'order_requirement_id', 'sale_order_id',
                                        string='Sale Order', relation='sale.order', type='many2one', readonly=True),
        'tmp_id': fields.integer('tmp_id'),
        'tmp_parent_id': fields.integer('tmp_parent'),
        'parent_id': fields.many2one('temp.mrp.bom', 'Parent'),
        'level': fields.integer('Level'),
        # todo remove parent_id_num
        'parent_id_num': fields.related('parent_id', 'id', type='integer', string='Parent'),
        'is_manufactured': fields.boolean('Manufacture'),
        'supplier_ids': fields.many2many('res.partner', string='Suppliers'),
        'supplier_id': fields.many2one('res.partner', 'Supplier', domain="[('id', 'in', supplier_ids[0][2])]"),
        'stock_availability': fields.function(_stock_availability, method=True, multi='stock_availability',
                                              type='float', string='Stock Availability', readonly=True),
        'spare': fields.function(_stock_availability, method=True, multi='stock_availability', type='float',
                                 string='Spare', readonly=True),
        'is_leaf': fields.boolean('Leaf', readonly=True),
        'position': fields.char('Internal Reference', size=64, help="Reference to a position in an external plan.",
                                readonly=True),

        'routing_id': fields.many2one('mrp.routing', 'Routing',
                                      help="The list of operations (list of work centers) to produce the finished product. The routing is mainly used to compute work center costs during operations and to plan future loads on work centers based on production planning."),
        'company_id': fields.many2one('res.company', 'Company', required=True),

        'row_color': fields.function(get_color, string='Row color', type='char', readonly=True, method=True),
    }

    # _parent_name = 'bom_id'

    def _check_product(self, cr, uid, ids, context=None):
        # Serve per permettere l'inserimento di una BoM con lo stesso bom_id e product_id ma con position diversa.
        # La position è la descrizione.
        return True

    _constraints = [
        (_check_product, 'BoM line product should not be same as BoM product.', ['product_id']),
    ]

    @staticmethod
    def get_all_temp_bom_children_ids(father, temp_mrp_bom_ids):
        # Retrieve recursively all children
        # father is a dict of vals, temp_mrp_bom_ids must be in the form [ [x,x,{}], ... ]
        try:
            father_id = father['tmp_id']
        except (KeyError, TypeError):
            return []
        children = [t for t in temp_mrp_bom_ids if
                    t[2] and 'tmp_parent_id' in t[2] and t[2]['tmp_parent_id'] == father_id]
        res = children
        for child in children:
            vals = child[2]
            res.extend(temp_mrp_bom.get_all_temp_bom_children_ids(vals['tmp_id'], temp_mrp_bom_ids))
        return res

    @staticmethod
    def check_parents(temp, temp_mrp_bom_ids):
        # Return True if all the parents are present up to level 0
        # temp is a dict of vals, temp_mrp_bom_ids must be in the form [ [x,x,{}], ... ]
        try:
            level = temp['level']
        except (KeyError, TypeError):
            return False
        # If I am at level 0 => True (no need for lookup parents)
        if level == 0:
            return True
        # Direct fathers
        father_id = temp['tmp_parent_id']
        parents_ids = [t for t in temp_mrp_bom_ids if t[2] and 'tmp_id' in t[2] and t[2]['tmp_id'] == father_id]
        if level == 1:
            return bool(parents_ids)
        for parent in parents_ids:
            vals = parent[2]
            if temp_mrp_bom.check_parents(vals, temp_mrp_bom_ids):
                return True
        return False

    @staticmethod
    def get_temp_mrp_bom(cr, uid, bom_ids, context):
        # Returns a list of VALS
        temp_mrp_bom_vals = []

        if not bom_ids:
            return []

        for bom_father in bom_ids:
            children_levels = mrp_bom.get_all_mrp_bom_children(bom_father.child_buy_and_produce_ids, 0)

            def _get_rec(bom_rec):
                bom_children = bom_rec.child_buy_and_produce_ids
                if not bom_children:
                    return
                for bom in bom_children:
                    if True: # bom.product_id.type == 'product':
                        # coolname = u' {1} - {0} {2}'.format(bom.id, bom_rec.id, bom.name)
                        level = children_levels[bom.id]['level']
                        complete_name = bom.name
                        if level > 0:
                            complete_name = '-----' * level + '> ' + complete_name
                        newbom_vals = {
                            'name': bom.name,
                            # tmp_* Could be useful for reconstructing hierarchy
                            'tmp_id': bom.id,
                            'tmp_parent_id': bom_rec.id,
                            'complete_name': complete_name,
                            'name': bom.name,
                            # 'bom_id': bom.bom_id.id,
                            'product_id': bom.product_id.id,
                            'product_qty': bom.product_qty,
                            'product_uom': bom.product_uom.id,
                            'product_efficiency': bom.product_efficiency,
                            'product_type': bom.product_id.type,
                            'routing_id': bom.routing_id.id,
                            'company_id': bom.company_id.id,
                            'position': bom.position,
                            'is_leaf': not bool(bom.child_buy_and_produce_ids),
                            'level': level,
                            'row_color': row_color
                        }
                        temp_mrp_bom_vals.append(newbom_vals)
                    # Even if not product I must check all children
                    _get_rec(bom)

            _get_rec(bom_father)
        return temp_mrp_bom_vals

    def onchange_manufacture(self, cr, uid, ids, is_manufactured, context=None):
        res = {}
        if is_manufactured:
            res['supplier_id'] = False
        return {'value': res}

    def get_suppliers(self, cr, uid, ids, new_product_id, qty=0, supplier_id=False, context=None):
        context = context or self.pool['res.users'].context_get(cr, uid)
        supplierinfo_obj = self.pool['product.supplierinfo']
        result_dict = {}
        if new_product_id:
            product = self.pool['product.product'].browse(cr, uid, new_product_id, context)
            if not supplier_id:
                # --find the supplier
                supplier_info_ids = supplierinfo_obj.search(cr, uid,
                                                            [('product_id', '=', product.product_tmpl_id.id)],
                                                            order="sequence", context=context)
                supplier_infos = supplierinfo_obj.browse(cr, uid, supplier_info_ids, context=context)
                seller_ids = [info.name.id for info in supplier_infos]

                if seller_ids:
                    result_dict.update({
                        'supplier_id': seller_ids[0],
                        'supplier_ids': seller_ids,
                    })
                else:
                    result_dict.update({
                        'supplier_id': False,
                        'supplier_ids': [],
                    })

        else:
            result_dict.update({
                'supplier_id': False,
                'supplier_ids': [],
            })

        return result_dict

    def onchange_temp_product_id(self, cr, uid, ids, new_product_id, qty=0, supplier_id=False, context=None):
        ret = {}
        suppliers = self.get_suppliers(cr, uid, ids, new_product_id, qty, supplier_id, context)
        ret.update(suppliers)
        product_obj = self.pool['product.product']
        product = product_obj.browse(cr, uid, new_product_id, context)
        temp_mrp_bom_ids = temp_mrp_bom.get_temp_mrp_bom(cr, uid, product.bom_ids, context)
        # mrp_bom.
        return {'value': ret}

