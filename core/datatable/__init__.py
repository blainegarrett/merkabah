from django.template.loader import render_to_string


class DatatableColumn(object):
    columns = []
    
    def render_row(self):
        output = '<tr>';
        
        for column in columns:
            output += column.render_cell()
        
        output += '</tr>'
        return output
        
    def render_content(self, obj):
        return getattr(obj, self.id)
        
    def render_cell(self, obj):
        return '<td>%s</td>' % self.render_content(obj)

class Datatable(object):
    template = 'merkabah/admin/datatable/datatable.html'
    
    def __str__(self):
        return self.render()
        
    def __init__(self, entities, request, context):
        self.entities = entities
        self.request = request
        self.context = context
        self.unsorted_columns = []
        self.columns = []
        self.rows = []
        
        
        import logging
        for attr in dir(self):
            logging.error([attr, getattr(self, attr)])
        
        
        for attr in dir(self):
            column = getattr(self, attr)
            if isinstance(column, DatatableColumn):
                column.name = attr.replace('_', ' ')
                column.id = attr
                self.unsorted_columns.append(column)
            elif attr == 'column_order':
                self.column_order = column
            
        for column_id in self.column_order:
            for column in self.unsorted_columns:
                if column.id == column_id:
                    self.columns.append(column)
            
        
        for entity in entities:
            row = self.build_row(entity)
            self.rows.append(row)
        
        
    def build_row(self, obj):
        return {
            'object': obj, 
            #'css': self.get_row_css(obj),
            'cells': self.get_row_cells(obj),
            #'guid' : self.get_row_identifier(obj)
        }
        
    def render_row(self, obj):
        row = self.build_row(obj)
        return render_to_string('merkabah/admin/datatable/row.html', {'row': row})
    
    def get_row_cells(self, obj):
        return [column.render_cell(obj) for column in self.columns]
        
    def render(self):
        self.context['entities'] = self.entities
        
        self.context['rows'] = self.rows        
        self.context['columns'] = self.columns
        rendered_string = render_to_string(self.template, self.context)
        
        return rendered_string