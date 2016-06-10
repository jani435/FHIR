# -*- coding: utf-8 -*-

from openerp import models, fields, api

class HcExtension(models.Model):
	_inherit = 'hc.address'
	#This model will extends hc.address and override fields defined below. 
	#I am redefining below fields in this new models so it will override fields definition in the parent model
	#Made all the fields related, related fields are kind of computed fileds so they have the value of the subfield that we have defined as related.


	#This is the method for computed field and it id depends on fileds we listed in bracket, so it will call every time when there is 
	# any changes ni listed fields and change the value of our name fields accordingly
	@api.depends('line1','line2','line3','city_id','postal_code_id', 'district_id', 'state_id', 'division_id', 'region_id', 'country_id')
	def compute_address(self):
		address = ''
		lines = ''
		line1 = self.line1 and self.line1 or ''
		line2 = self.line2 and ', '+self.line2 or ''
		line3 = self.line3 and ', '+self.line3 or ''
		city = self.city_id and ', '+self.city_id.name or ''
		pin = self.postal_code_id and ', '+self.postal_code_id.name or ''
		district = self.district_id and ', '+self.district_id.name or ''
		state = self.state_id and ', '+self.state_id.code or ''
		division = self.division_id and ', '+self.division_id.name or ''
		region = self.region_id and ', '+self.region_id.name or ''
		country = self.country_id and ', '+self.country_id.name or ''
		lines = line1+line2+line3+city+pin+district+state+division+region+country+lines
		self.name = lines
	
	postal_code_id = fields.Many2one(comodel_name="hc.vs.country.postal.code", string="Postal/ZIP Code", help="Postal code for area.")
	name = fields.Char(compute='compute_address', store=True)
	district_id = fields.Many2one(related='postal_code_id.district_id', string="District/County", help="The name of the administrative area (e.g., county).")
	state_id = fields.Many2one(related='postal_code_id.state_id', string="State", help="Sub-unit of country (abreviations ok).")
	
	division_id = fields.Many2one(related='postal_code_id.division_id', string="Division", help="Group of states (e.g., Pacific, Mountain).")
	region_id = fields.Many2one(related='postal_code_id.region_id', string="Region", help="First level subdivision of a country (e.g. West, Midwest).")
	country_id = fields.Many2one(related='postal_code_id.country_id', string="Country", help="Country (can be ISO 3166 3 letter code).")

	#Overriding create method, this method get called by framework everytime when record gets created.
	'''@api.model
	def create(self, vals):
		#@param: vals - contains value of all the fields.
		#Concating fields line1, line2 and line3 in new variable lines.
		lines = vals['line1']+', '+vals['line2']+', ' or '' +vals['line3']+', ' or ''
		#All other fields are not simple character fields but many2one fields, so we need to fetch it's name from the datbase.
		#Therefore used browse method, browse method used to get recordset from database for given id of record.
		city = self.env['hc.vs.country.city'].browse(vals['city_id']).name or ''
		state = self.env['res.country.state'].browse(vals['state_id']).code or ''
		pin = self.env['hc.vs.country.postal.code'].browse(vals['postal_code_id']).name or ''
		district = self.env['hc.vs.country.district'].browse(vals['district_id']).name or ''
		division = self.env['hc.vs.country.division'].browse(vals['division_id']).name or ''
		region = self.env['hc.vs.country.region'].browse(vals['region_id']).name or ''
		country = self.env['res.country'].browse(vals['country_id']).name or ''
		#Concating all the value in single in variable address.
		address = lines+city+', '+pin+', '+district+', '+division+', '+region+', '+country
		#Assigning value of address to field name of the record.
		vals['name'] = address
		#Calling super method and returning the newly updated values.
		return super(HcExtension, self).create(vals)'''


	'''@api.multi
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
		return super(HcExtension, self).write(vals)'''

class HcExtensionHumanName(models.Model):
    _inherit = 'hc.human.name'

    @api.model
    def create(self, vals):

        first = self.env['hc.human.name.term'].browse(vals['first_id']).name or ''
        last = self.env['hc.human.name.term'].browse(vals['surname_id']).name or ''
        maiden = self.env['hc.human.name.term'].browse(vals['mother_maiden_name_id']).name or ''
        full = first+' '+last
        vals['name'] = full

        return super(HcExtensionHumanName, self).create(vals)

    @api.multi
    def write(self, vals):
       

        if 'first_id' in vals:   
            first = self.env['hc.human.name.term'].browse(vals['first_id']).name
        else:
            first = self.first_id.name

        if 'surname_id' in vals:    
            last = self.env['hc.human.name.term'].browse(vals['surname_id']).name
        else:
            last = self.surname_id.name

        full = first+' '+last
        vals['name'] = full

        return super(HcExtensionHumanName, self).create(vals)
