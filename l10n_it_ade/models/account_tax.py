# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    © 2017-2019 Didotech srl (www.didotech.com)
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
from openerp.tools.translate import _

SOCIAL_SECURITY_TYPE = [
    ('TC01', 'Cassa Nazionale Previdenza e Assistenza Avvocati e Procuratori Legali'),
    ('TC02', 'Cassa Previdenza Dottori Commercialisti'),
    ('TC03', 'Cassa Previdenza e Assistenza Geometri'),
    ('TC04', 'Cassa Nazionale Previdenza e Assistenza Ingegneri e Architetti Liberi Professionisti'),
    ('TC05', 'Cassa Nazionale del Notariato'),
    ('TC06', 'Cassa Nazionale Previdenza e Assistenza Ragionieri e Periti Commerciali'),
    ('TC07', 'Ente Nazionale Assistenza Agenti e Rappresentanti di Commercio (ENASARCO)'),
    ('TC08', 'Ente Nazionale Previdenza e Assistenza Consulenti del Lavoro (ENPACL)'),
    ('TC09', 'Ente Nazionale Previdenza e Assistenza Medici (ENPAM)'),
    ('TC10', 'Ente Nazionale Previdenza e Assistenza Farmacisti (ENPAF)'),
    ('TC11', 'Ente Nazionale Previdenza e Assistenza Veterinari (ENPAV)'),
    ('TC12', "Ente Nazionale Previdenza e Assistenza Impiegati dell'Agricoltura (ENPAIA)"),
    ('TC13', "Fondo Previdenza Impiegati Imprese di Spedizione e Agenzie Marittime"),
    ('TC14', 'Istituto Nazionale Previdenza Giornalisti Italiani (INPGI)'),
    ('TC15', 'Opera Nazionale Assistenza Orfani Sanitari Italiani (ONAOSI)'),
    ('TC16', 'Cassa Autonoma Assistenza Integrativa Giornalisti Italiani (CASAGIT)'),
    ('TC17', 'Ente Previdenza Periti Industriali e Periti Industriali Laureati (EPPI)'),
    ('TC18', 'Ente Previdenza e Assistenza Pluricategoriale (EPAP)'),
    ('TC19', 'Ente Nazionale Previdenza e Assistenza Biologi (ENPAB)'),
    ('TC20', 'Ente Nazionale Previdenza e Assistenza Professione Infermieristica (ENPAPI)'),
    ('TC21', 'Ente Nazionale Previdenza e Assistenza Psicologi (ENPAP)'),
    ('TC22', 'INPS')
]

class AccountTax(orm.Model):
    _inherit = 'account.tax'

    _columns = {
        'non_taxable_nature': fields.selection([
            ('N1', 'escluse ex art. 15'),
            ('N2', 'non soggette'),
            ('N3', 'non imponibili'),
            ('N4', 'esenti'),
            ('N5', 'regime del margine/IVA non esposta'),
            ('N6', 'inversione contabile (acq. in reverse charge)'),
            ('N7', 'IVA assolta in altro stato UE'),
            ('FC', 'FC applicazione IVA'),
            ], string="Non taxable nature"),
        'payability': fields.selection([
            ('I', 'Immediate payability'),
            ('D', 'Deferred payability'),
            ('S', 'Split payment'),
            ], string="VAT payability"),
        'law_reference': fields.char(
            'Law reference', size=100),
        'withholding_tax': fields.boolean("Ritenuta d'acconto"),
        'causale_pagamento_id': fields.selection([
            ('A', "Prestazioni di lavoro autonomo rientranti nell'esercizio di arte o professione abituale"),
            ('B', "Utilizzazione economica, da parte dell'autore o dell'inventore, di opere dell'ingegno, di brevetti industriali e di processi, formule o informazioni relativi a esperienze acquisite in campo industriale, commerciale o scientifico"),
            ('C', "Utili derivanti da contratti di associazione in partecipazione e da contratti di cointeressenza, quando l'apporto è costituito esclusivamente dalla prestazione di lavoro"),
            ('D', "Utili spettanti ai soci promotori e ai soci fondatori delle società di capitali"),
            ('E', "Levata di protesti cambiari da parte dei segretari comunali"),
            ('G', "Indennità corrisposte per la cessazione di attività sportiva professionale"),
            ('H', "Indennità corrisposte per la cessazione dei rapporti di agenzia delle persone fisiche e delle società di persone, con esclusione delle somme maturate entro il 31.12.2003, già imputate per competenza e tassate come reddito d'impresa"),
            ('I', "Indennità corrisposte per la cessazione da funzioni notarili"),
            ('L', "Utilizzazione economica, da parte di soggetto diverso dall'autore o dall'inventore, di opere dell'ingegno, di brevetti industriali e di processi, formule e informazioni relative a esperienze acquisite in campo industriale, commerciale o scientifico"),
            ('M', "Prestazioni di lavoro autonomo non esercitate abitualmente, obblighi di fare, di non fare o permettere"),
            ('N', "Indennità di trasferta, rimborso forfetario di spese, premi e compensi erogati: nell'esercizio diretto di attività sportive dilettantistiche"),
            ('O', "Prestazioni di lavoro autonomo non esercitate abitualmente, obblighi di fare, di non fare o permettere, per le quali non sussiste l'obbligo di iscrizione alla gestione separata (Circ. Inps 104/2001)"),
            ('P', "Compensi corrisposti a soggetti non residenti privi di stabile organizzazione per l'uso o la concessione in uso di attrezzature industriali, commerciali o scientifiche che si trovano nel territorio dello"),
            ('Q', "Provvigioni corrisposte ad agente o rappresentante di commercio monomandatario"),
            ('R', "Provvigioni corrisposte ad agente o rappresentante di commercio plurimandatario"),
            ('S', "Provvigioni corrisposte a commissionario"),
            ('T', "Provvigioni corrisposte a mediatore"),
            ('U', "Provvigioni corrisposte a procacciatore di affari"),
            ('V', "Provvigioni corrisposte a incaricato per le vendite a domicilio e provvigioni corrisposte a incaricato per la vendita porta a porta e per la vendita ambulante di giornali quotidiani e periodici (L. 25.02.1987, n. 67)"),
            ('W', "Corrispettivi erogati nel 2013 per prestazioni relative a contratti d'appalto cui si sono resi applicabili le disposizioni contenute nell'art. 25-ter D.P.R. 600/1973"),
            ('X', "Canoni corrisposti nel 2004 da società o enti residenti, ovvero da stabili organizzazioni di società estere di cui all'art. 26-quater, c. 1, lett. a) e b) D.P.R. 600/1973, a società o stabili organizzazioni di società, situate in altro Stato membro dell'Unione Europea in presenza dei relativi requisiti richiesti, per i quali è stato effettuato nel 2006 il rimborso della ritenuta ai sensi dell'art. 4 D. Lgs. 143/2005"),
            ('Y', "Canoni corrisposti dal 1.01.2005 al 26.07.2005 da soggetti di cui al punto precedente"),
            ('Z', "Titolo diverso dai precedenti")
        ], string="Causale Ritenuta"),
        'social_security': fields.boolean("Cassa Previdenziale"),
        'social_security_type': fields.selection(SOCIAL_SECURITY_TYPE, string='Tipo Cassa Previdenziale'),
        'amount_e_invoice': fields.integer(
            'Amount in XML', required=False,
            help="For taxes of type percentage, enter % ratio between 0-100"),
    }
    _sql_constraints = [
        ('description_uniq', 'unique(description)', _('Description must be unique !')),
    ]
    # _defaults = {
    #     'payability': 'I',
    # }

    def copy(self, cr, uid, ids, defaults, context=None):
        defaults.update({
            'description': False
        })
        return super(AccountTax, self).copy(cr, uid, ids, defaults, context)

    def get_tax_by_invoice_tax(self, cr, uid, invoice_tax, context=None):
        if ' - ' in invoice_tax:
            tax_descr = invoice_tax.split(' - ')[0]
            tax_ids = self.search(cr, uid, [
                ('description', '=', tax_descr),
                ], context=context)
            if not tax_ids:
                raise orm.except_orm(
                    _('Error'), _('No tax %s found') %
                    tax_descr)
            if len(tax_ids) > 1:
                raise orm.except_orm(
                    _('Error'), _('Too many tax %s found') %
                    tax_descr)
        else:
            tax_name = invoice_tax
            tax_ids = self.search(cr, uid, [
                ('name', '=', tax_name),
                ], context=context)
            if not tax_ids:
                raise orm.except_orm(
                    _('Error'), _('No tax %s found') %
                    tax_name)
            if len(tax_ids) > 1:
                raise orm.except_orm(
                    _('Error'), _('Too many tax %s found') %
                    tax_name)
        return tax_ids[0]
