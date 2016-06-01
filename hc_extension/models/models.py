# -*- coding: utf-8 -*-

from openerp import models, fields, api

class HcExtension(models.Model):
	_inherit = 'hc.address'
	#This model will extends hc.address and override fields defined below. 
	#I am redefining below fields in this new models so it will override fields definition in the parent model
	#Made all the fields related, related fields are kind of computed fileds so they have the value of the subfield that we have defined as related.
	district_id = fields.Many2one(related='postal_code_id.district_id', string="District/County", help="The name of the administrative area (e.g., county).")
	state_id = fields.Many2one(related='postal_code_id.state_id', string="State", help="Sub-unit of country (abreviations ok).")
	
	division_id = fields.Many2one(related='postal_code_id.division_id', string="Division", help="Group of states (e.g., Pacific, Mountain).")
	region_id = fields.Many2one(related='postal_code_id.region_id', string="Region", help="First level subdivision of a country (e.g. West, Midwest).")
	country_id = fields.Many2one(related='postal_code_id.country_id', string="Country", help="Country (can be ISO 3166 3 letter code).")

	#Overriding create method, this method get called by framework everytime when record gets created.
	@api.model
	def create(self, vals):
		#@param: vals - contains value of all the fields.
		#Concating fields line1, line2 and line3 in new variable lines.
		lines = vals['line1']+', '+vals['line2']+', '+vals['line3']+', '
		#All other fields are not simple character fields but many2one fields, so we need to fetch it's name from the datbase.
		#Therefore used browse method, browse method used to get recordset from database for given id of record.
		city = self.env['hc.vs.country.city'].browse(vals['city_id']).name
		state = self.env['res.country.state'].browse(vals['state_id']).code
		pin = self.env['hc.vs.country.postal.code'].browse(vals['postal_code_id']).name
		district = self.env['hc.vs.country.district'].browse(vals['district_id']).name
		division = self.env['hc.vs.country.division'].browse(vals['division_id']).name
		region = self.env['hc.vs.country.region'].browse(vals['region_id']).name
		country = self.env['res.country'].browse(vals['country_id']).name
		#Concating all the value in single in variable address.
		address = lines+city+', '+pin+', '+district+', '+division+', '+region+', '+country
		#Assigning value of address to field name of the record.
		vals['name'] = address
		#Calling super method and returning the newly updated values.
		return super(HcExtension, self).create(vals)


	@api.multi
	def write(self, vals):
		#This method gets called when updating the record.
		#@param: vals - vals contains only fields which are updated.
		#Here we are updating the value of name field of the record but vals paramaeter of write method only contains the field which has updated
		#we need to check every field 
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
		#Concating and same procedure as create method.
		address = line1+', '+line2+', '+line3+', '+city+', '+pin+', '+district+', '+division+', '+region+', '+country
		vals['name'] = address
		return super(HcExtension, self).write(vals)
