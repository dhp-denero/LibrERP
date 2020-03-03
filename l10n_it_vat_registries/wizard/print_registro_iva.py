# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _


class wizard_registro_iva(osv.osv_memory):

    def _get_period(self, cr, uid, context=None):
        return []
        ctx = dict(context or {}, account_period_prefer_normal=True)
        period_ids = self.pool['account.period'].find(cr, uid, context=ctx)
        return period_ids

    _name = "wizard.registro.iva"
    _columns = {
        'period_ids': fields.many2many(
            'account.period', 'registro_iva_periods_rel', 'period_id',
            'registro_id', 'Periods',
            help='Select periods you want retrieve documents from',
            required=True),
        'type': fields.selection([
            ('customer', 'Customer Invoices'),
            ('supplier', 'Supplier Invoices'),
            ('corrispettivi', 'Corrispettivi'),
        ], 'Layout', required=True),
        'journal_ids': fields.many2many(
            'account.journal', 'registro_iva_journals_rel', 'journal_id',
            'registro_id', 'Journals',
            help='Select journals you want retrieve documents from',
            required=True),
        'tax_sign': fields.float(
            'Tax amount sign',
            help="Use -1 you have negative tax amounts and you want to print "
                 "them prositive"),
        'message': fields.char('Message', size=64, readonly=True),
        'fiscal_page_base': fields.integer('Last printed page', required=True),
        'name': fields.char('Name', size=16),
        'order_by_date': fields.boolean('Ordina per data')
    }
    _defaults = {
        'type': 'customer',
        'period_ids': _get_period,
        'tax_sign': 1.0,
        'fiscal_page_base': 0,
    }

    def print_registro(self, cr, uid, ids, context=None):
        context = context or self.pool['res.users'].context_get(cr, uid)
        wizard = self.read(cr, uid, ids, context=context)[0]
        move_obj = self.pool['account.move']
        obj_model_data = self.pool['ir.model.data']
        if wizard['order_by_date']:
            order = 'date'
        else:
            order = 'name'

        move_ids = move_obj.search(cr, uid, [
            ('journal_id', 'in', wizard['journal_ids']),
            ('period_id', 'in', wizard['period_ids']),
            ('state', '=', 'posted'),
        ], order=order, context=context)
        if not move_ids:
            self.write(cr, uid, ids, {'message': _('No documents found in the current selection')}, context)
            model_data_ids = obj_model_data.search(cr, uid, [('model', '=', 'ir.ui.view'), ('name', '=', 'wizard_registro_iva')], context=context)
            resource_id = obj_model_data.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
            return {
                'name': _('No documents'),
                'res_id': ids[0],
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.registro.iva',
                'views': [(resource_id, 'form')],
                'context': context,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }

        datas = {
            'ids': move_ids,
            'model': 'account.move',
            'fiscal_page_base': wizard['fiscal_page_base'],
            'period_ids': wizard['period_ids'],
            'journal_ids': wizard['journal_ids'],
            'layout': wizard['type'],
            'tax_sign': wizard['tax_sign'],
        }

        res = {
            'type': 'ir.actions.report.xml',
            'datas': datas,
        }
        if wizard['type'] == 'customer':
            res['report_name'] = 'registro_iva_vendite'
        elif wizard['type'] == 'supplier':
            res['report_name'] = 'registro_iva_acquisti'
        elif wizard['type'] == 'corrispettivi':
            res['report_name'] = 'registro_iva_corrispettivi'
        #elif wizard['type'] == 'generale':
        #    res['report_name'] = 'registro_generale'
        return res

    def _get_journal(self, cr, uid, j_type, context=None):
        if context is None:
            context = {}
        journal_obj = self.pool['account.journal']
        res = []
        if j_type == 'supplier':
            res = journal_obj.search(cr, uid, [('type', 'in', ['purchase', 'purchase_refund'])], context=context)
        elif j_type == 'customer' or j_type == 'corrispettivi':
            res = journal_obj.search(cr, uid, [('type', 'in', ['sale', 'sale_refund'])], context=context)
        else:
            res = journal_obj.search(cr, uid, [('type', 'in', ['sale', 'sale_refund', 'purchase', 'purchase_refund'])], context=context)
        return res

    def on_type_changed(self, cr, uid, ids, j_type, context=None):
        res = {}
        if j_type:
            if j_type == 'supplier':
                res['value'] = {'tax_sign': -1}
            else:
                res['value'] = {'tax_sign': 1}
            res['value'].update({'journal_ids': self._get_journal(cr, uid, j_type, context=context)})
        return res


