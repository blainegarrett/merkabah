"""
Fishbat
"""

from django import forms
from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.utils.safestring import mark_safe

class MerkabahBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.setup(*args, **kwargs)

    def setup(self, *args, **kwargs):
        '''
        Allows derived forms to have a post init callback
        '''
        pass
            
    def as_table(self):
        return self.as_bootstrap()
        
    def as_bootstrap(self):
        errors_on_separate_row = False
        
        normal_row = u'%(label)s<div%(html_class_attr)s>%(field)s%(errors)s</div>'
        #normal_row = u'<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>'
        
        error_row = u'<span class="input-error" data-title="%s"><i class="icon-warning-sign"></i></span>'
        row_ender = u'</div>'
        help_text_html = u'<br />%s'
        errors_on_separate_row = False        
        
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = forms.forms.BoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                css_classes += ' input'
                
                if bf_errors:
                    css_classes += ' error'

                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''
                
                error_str = ''
                if bf_errors:
                    for error in bf_errors:
                        error_str += "%s " % error
                    
                    error_str = '<span class="input-error" data-title="%s"><i class="icon-warning-sign"></i></span>' % error_str
                
                output.append(normal_row % {
                    'errors': force_unicode(error_str),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        rendered = mark_safe(u'\n'.join(output))
        wrapper = '<div class="row-fluid"><div class="span6"><div class="padded">%s</div></div></div>'
        return mark_safe(wrapper % rendered)