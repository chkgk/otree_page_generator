from dataclasses import dataclass, field


@dataclass
class Page:
    title: str
    paragraphs: list = field(default_factory=lambda: [])
    form_fields: list = field(default_factory=lambda: [])
    vars_for_template: list = field(default_factory=lambda: [])
    form_model: str = 'player'

    def render_model_fields(self):
        content = ''
        for field in self.form_fields:
            if field.input_type != 'generic':
                if field.input_type == 'longstring':
                    field_name = 'LongString'
                else:
                    field_name = field.input_type.capitalize()
                content += f"    {field.variable_name} = models.{field_name}Field()\n"

        return content

    def render_class(self):
        content = f"""
class {self.title}(Page):"""

        if self.form_fields:
            fields_str = ''
            for field in self.form_fields:
                fields_str += f"'{field.variable_name}', "
            fields_str = fields_str[:-2]
            content += f"""
    form_model = '{self.form_model}'
    form_fields = [{fields_str}]
"""
        if self.vars_for_template:
            vars_str = ''
            for v in self.vars_for_template:
                vars_str += f"'{v}': '',  # add your custom variable value here \n"
            vars_str = vars_str[:-2]
            content += f"""
    def vars_for_template(self):
        return {{
            {vars_str}
        }}
"""
        if not self.vars_for_template and not self.form_fields:
            content += """
    pass
"""
        return content

    def render_template(self):
        content = f"""
{{{{ block title }}}}
    { self.title }
{{{{ endblock }}}}

{{{{ block content }}}}
"""
        for paragraph in self.paragraphs:
            content += f"    {paragraph}\n"

        content += "{{ endblock }}"

        return content
