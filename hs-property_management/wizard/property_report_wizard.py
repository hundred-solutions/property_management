from odoo import fields, models


class VisitorReport(models.TransientModel):
    _name = 'property.report.wizard'

    department = fields.Many2one("hr.department",string="Department")
    employee = fields.Many2one("hr.employee",string="Employee")

    def property_report(self):
        print(self.department,self.employee)
        if self.employee and self.department:
            property_data = self.env["hr.employee"].search([('department_id','=',self.department.id),('id','=',self.employee.id)])
            print(property_data.given_materials_line_ids)
            properties = []
            for data in property_data.given_materials_line_ids:
                product= {
                    "name":data.name.name,
                    "assign_date":data.assign_date,
                    "qty":data.qty,
                    "given_condition":data.given_condition,
                    "return_date":data.return_date,
                    "returned":data.returned,
                    "return_condition":data.return_condition,
                }
                properties.append(product)
            data = {
                'flag':0,
                'name': property_data.name,
                "department":self.department.name,
                'mobile': property_data.work_phone,
                'properties': properties,
            }
            return self.env.ref('hs-property_management.property_report_action').report_action(self, data=data)
        elif self.department:
            property_data = self.env["hr.employee"].search(
                [('department_id', '=', self.department.id)])
            issued_count=0
            return_count=0
            damage_count=0
            properties =[]
            for property in property_data:
                for data in property.given_materials_line_ids:
                    issued_count+=data.qty
                    if data.return_condition == "damaged":
                        damage_count+=data.qty
                    if data.returned:
                        return_count+=data.qty
                    product = {
                        "name": data.name.name,
                        "given_to":property.name,
                        "assign_date": data.assign_date.strftime('%m/%d/%Y %I:%M:%S %p'),
                        "qty": data.qty,
                        "given_condition": data.given_condition,
                        "return_date": data.return_date,
                        "returned": data.returned,
                        "return_condition": data.return_condition,
                    }
                    properties.append(product)


            data = {
                'flag': 1,
                'name': self.department.name,
                'issued_count':issued_count,
                'damage_count':damage_count,
                'return_count':return_count,
                'properties': properties,
            }
            return self.env.ref('hs-property_management.property_report_action').report_action(self, data=data)
