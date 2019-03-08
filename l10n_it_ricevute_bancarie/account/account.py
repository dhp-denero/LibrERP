# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
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
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm


class account_payment_term(orm.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = 'account.payment.term'

    _columns = {
        'riba': fields.boolean('Riba'),
        'spese_incasso_id':  fields.many2one('product.product', 'Spese Incasso', domain=[('type', '=', 'service')]),
    }
    _defaults = {
        'riba': False,
    }

    def get_product_incasso(self, cr, uid, context):
        payment_term_obj = self.pool['account.payment.term']

        payment_with_spese_incasso_ids = payment_term_obj.search(cr, uid, [('spese_incasso_id', '!=', False)],
                                                                 context=context)
        excluse_product_ids = [payment.spese_incasso_id.id for payment in
                               payment_term_obj.browse(cr, uid, payment_with_spese_incasso_ids, context)]

        return excluse_product_ids

    def onchange_type(self, cr, uid, ids, type, context=None):
        result = super(account_payment_term, self).onchange_type(cr, uid, ids, type, context)
        if type:
            if type == 'RB':
                result['value']['riba'] = True
            else:
                result['value']['riba'] = False
        return result


class res_bank_add_field(orm.Model):
    _inherit = 'res.bank'
    _columns = {
        'banca_estera': fields.boolean('Banca Estera'),
    }


class res_partner_bank_add(orm.Model):
    _inherit = 'res.partner.bank'
    _columns = {
        'codice_sia': fields.char('Codice SIA', size=5, help="Identification Code of the Company in the System Interbank")
    }


# se distinta_line_ids == None allora non è stata emessa
class account_move_line(orm.Model):
    _inherit = "account.move.line"

    _columns = {
        'distinta_line_ids': fields.one2many('riba.distinta.move.line', 'move_line_id', "Dettaglio riba"),
        'riba': fields.related('stored_invoice_id', 'payment_term', 'riba',
            type='boolean', string='RiBa', store=False),
        'unsolved_invoice_ids': fields.many2many('account.invoice', 'invoice_unsolved_line_rel', 'line_id', 'invoice_id', 'Unsolved Invoices'),
        'iban': fields.related('partner_id', 'bank_ids', 'iban', type='char', string='IBAN', store=False),
        'abi': fields.related('partner_id', 'bank_riba_id', 'abi', type='char', string='ABI', store=False),
        'cab': fields.related('partner_id', 'bank_riba_id', 'cab', type='char', string='CAB', store=False),
    }
    _defaults = {
        'distinta_line_ids': None,
    }

    def _hook_get_invoice_line(self, cr, uid, line, context):
        invoice_pool = self.pool['account.invoice']
        res = invoice_pool.search(cr, 1, [('unsolved_move_line_ids', '=', line.id)], context=context)
        if res:
            return res[0]
        else:
            return super(account_move_line, self)._hook_get_invoice_line(cr, uid, line, context)

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context={}, toolbar=False, submenu=False):
        view_payments_tree_id = self.pool['ir.model.data'].get_object_reference(
            cr, uid, 'l10n_it_ricevute_bancarie', 'view_riba_da_emettere_tree')
        if view_id == view_payments_tree_id[1]:
            # Use RiBa list - grazie a eLBati @ account_due_list
            result = super(orm.Model, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        else:
            # Use special views for account.move.line object (for ex. tree view contains user defined fields)
            result = super(account_move_line, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        return result

    def unlink(self, cr, uid, ids, context=None, check=True):
        if not context:
            context = {}
        riba_distinta_line_obj = self.pool['riba.distinta.line']
        riba_distinta_move_line_obj = self.pool['riba.distinta.move.line']
        riba_distinta_move_line_ids = riba_distinta_move_line_obj.search(cr, uid, [('move_line_id', 'in', ids)], context=context)
        if riba_distinta_move_line_ids:
            riba_line_ids = riba_distinta_line_obj.search(cr, uid, [('move_line_ids', 'in', riba_distinta_move_line_ids)], context=context)
            if riba_line_ids:
                for riba_line in riba_distinta_line_obj.browse(cr, uid, riba_line_ids, context=context):
                    if riba_line.state in ['draft', 'cancel']:
                        riba_distinta_line_obj.unlink(cr, uid, riba_line_ids, context=context)
                        # TODO: unlink in 'accepted' state too?
        return super(account_move_line, self).unlink(cr, uid, ids, context=context, check=check)


class account_invoice(orm.Model):
    _inherit = "account.invoice"
    _columns = {
        'unsolved_move_line_ids': fields.many2many('account.move.line', 'invoice_unsolved_line_rel', 'invoice_id', 'line_id', 'Unsolved journal items'),
    }

    def invoice_validate_check(self, cr, uid, ids, context=None):
        context = context or self.pool['res.users'].context_get(cr, uid)
        res = super(account_invoice, self).invoice_validate_check(cr, uid, ids, context)
        show_except = not context.get('no_except', False)
        if not res:
            return False
        else:
            for invoice in self.browse(cr, uid, ids, context):
                if invoice.payment_term:
                    if invoice.payment_term.spese_incasso_id:
                        account_invoice_line_obj = self.pool['account.invoice.line']
                        account_invoice_line_ids = account_invoice_line_obj.search(cr, uid, [('product_id', '=', invoice.payment_term.spese_incasso_id.id), ('invoice_id', '=', invoice.id)], context=context)
                        if not account_invoice_line_ids:
                            # i have to add spese incasso
                            account_invoice_line_vals = {
                                'product_id': invoice.payment_term.spese_incasso_id.id,
                                'invoice_id': invoice.id
                            }

                            account_invoice_line_vals.update(account_invoice_line_obj.product_id_change(cr, uid, ids, invoice.payment_term.spese_incasso_id.id, False, type=invoice.type,
                                                           partner_id=invoice.partner_id.id, fposition_id=invoice.fiscal_position and invoice.fiscal_position.id,
                                                           context=context,
                                                           company_id=invoice.company_id.id).get('value'))

                            if account_invoice_line_vals.get('invoice_line_tax_id', False):
                                account_invoice_line_vals['invoice_line_tax_id'] = [(6, False, account_invoice_line_vals.get('invoice_line_tax_id'))]
                            account_invoice_line_vals['quantity'] = len(invoice.payment_term.line_ids)
                            account_invoice_line_obj.create(cr, uid, account_invoice_line_vals, context)
                            invoice.button_compute()

                    if invoice.payment_term.riba and invoice.type == 'out_invoice':
                        if not invoice.partner_id.bank_riba_id:
                            if show_except:
                                raise orm.except_orm(u'Fattura Cliente',
                                   u'Impossibile da validare in quanto non è impostata la banca appoggio Riba nel partner {partner}'.format(partner=invoice.partner_id.name))
                            else:
                                return False
                        if not invoice.partner_id.bank_riba_id.abi or not invoice.partner_id.bank_riba_id.cab:
                            if show_except:
                                raise orm.except_orm(u'Fattura Cliente',
                                   u'Impossibile da validare in quanto non è impostata ABI o CAB nella fattura di {partner}'.format(partner=invoice.partner_id.name))
                            else:
                                return False

        return True
