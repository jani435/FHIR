# -*- coding: utf-8 -*-

from openerp import models, fields, api

class HcExtension(models.Model):
	_inherit = 'hc.address'

	postal_code_id = fields.Many2one(comodel_name="hc.vs.country.postal.code", string="Postal Code", help="Postal code for area.")
	district_id = fields.Many2one(related='postal_code_id.district_id', string="District/County", help="The name of the administrative area (e.g., county).")
	state_id = fields.Many2one(related='postal_code_id.state_id', string="State", help="Sub-unit of country (abreviations ok).")
	
	division_id = fields.Many2one(related='postal_code_id.division_id', string="Division", help="Group of states (e.g., Pacific, Mountain).")
	region_id = fields.Many2one(related='postal_code_id.region_id', string="Region", help="First level subdivision of a country (e.g. West, Midwest).")
	country_id = fields.Many2one(related='postal_code_id.country_id', string="Country", help="Country (can be ISO 3166 3 letter code).")

	@api.model
	def create(self, vals):
		lines = vals['line1']+', '+vals['line2']+', '+vals['line3']+', '
		city = self.env['hc.vs.country.city'].browse(vals['city_id']).name
		state = self.env['res.country.state'].browse(vals['state_id']).name
		pin = self.env['hc.vs.country.postal.code'].browse(vals['postal_code_id']).name
		district = self.env['hc.vs.country.district'].browse(vals['district_id']).name
		division = self.env['hc.vs.country.division'].browse(vals['division_id']).name
		region = self.env['hc.vs.country.region'].browse(vals['region_id']).name
		country = self.env['res.country'].browse(vals['country_id']).name
		address = lines+city+', '+pin+', '+district+', '+division+', '+region+', '+country
		vals['name'] = address
		return super(HcExtension, self).create(vals)


	@api.multi
	def write(self, vals):
		#I think this code can be improved but time is constraint so...
		if 'line1' in vals:
			line1 = vals['line1']
		else:
			line1 = self.line1

		if 'line2' in vals:
			line2 = vals['line2']
		else: 
			line2 = self.line2

		if 'line3' in vals:
			line3 = vals['line3']
		else:
			line3 = self.line3

		if 'city_id' in vals:	
			city = self.env['hc.vs.country.postal.city'].browse(vals['city_id']).name
		else:
			city = self.city_id.name

		if 'postal_code_id' in vals:	
			pin = self.env['hc.vs.country.postal.code'].browse(vals['postal_code_id']).name
		else:
			pin = self.city_id.name

		if 'state_id' in vals:	
			state = self.env['res.country.state'].browse(vals['state_id']).name
		else:
			state = self.state_id.name

		if 'district_id' in vals:
			district = self.env['hc.vs.country.district'].browse(vals['district_id']).name
		else:
			district = self.district_id.name

		if 'division_id' in vals:
			division = self.env['hc.vs.country.division'].browse(vals['division_id']).name
		else:
			division = self.division_id.name

		if 'region_id' in vals:
			region = self.env['hc.vs.country.region'].browse(vals['region_id']).name
		else:
			region = self.region_id.name

		if 'country_id' in vals:
			country = self.env['res.country'].browse(vals['country_id']).name
		else:
			country = self.country_id.name

		address = line1+', '+line2+', '+line3+', '+city+', '+pin+', '+district+', '+division+', '+region+', '+country
		vals['name'] = address
		return super(HcExtension, self).write(vals)
