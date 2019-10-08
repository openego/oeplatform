from django.utils.safestring import mark_safe

LICENSE_KEY = 'license'
COLUMNS_KEY = 'fields'


class MetaDataWidget:
    """Html display of metadata JSON variable"""

    def __init__(self, json):
        self.json = json

    def __convert_to_html(self, data, level=0, parent=''):
        """Formats variables into html code

        :param data: either a dict, a list or a string
        :param level: the level of indentation inside the JSON variable
        :return:
        """

        if level == 0:
            html = '<table class="table">'
        elif level == 1:
            html = '<td>'
        else:
            html = ''

        if isinstance(data, dict):

            html += '' if level == 0 else '<ul>'
            for key, value in data.items():
                if level == 0:
                    html += f'<tr><th>{key.capitalize()}:</th> {self.__convert_to_html(value, level + 1, parent=key)}</tr>'
                elif level >= 1:
                    if LICENSE_KEY in key:
                        html += self.__format_license(value, level)
                    elif COLUMNS_KEY in key:
                        html += self.__format_columns(value, level)
                    else:
                        html += f'<li><b>{key.capitalize()}:</b> {self.__convert_to_html(value, level + 1, parent=key)}</li>'

            html += '' if level == 0 else '</ul>'

        elif isinstance(data, list):

            # For list item control
            no_valid_item = True

            # Check if the first item of the list is a string
            string_list = False
            if len(data) > 0:
                if isinstance(data[0], str):
                    string_list = True
                    no_valid_item = False

            if string_list:
                html += '<ul>'
                for item in data:
                    html += f'<li>{self.__convert_to_html(item, level + 1, parent=parent)}</li>'
                html += '</ul>'

            else:

                for item in data:
                    if isinstance(item, dict):
                        item = item.copy()
                        name = item.pop('title', None)
                        if name is None or name == '':
                            name = item.pop('name', None)
                        else:
                            item.pop('name', None)
                        url = item.pop('url', '')
                        if url != '':
                            name = f'<a href="{url}">{name}</a>'
                        if name is not None and name != '':
                            no_valid_item = False
                            html += f'<p class="metaproperty">{name}{self.__convert_to_html(item, level + 1, parent=parent)}</p>'
                    else:
                        html += f'<p>Not implemented yet</p>'

            if no_valid_item:
                html += f'<p class="metaproperty">There is no valid entry for this field</p>'

        elif isinstance(data, str):
            html += f'{data}'
        else:
            html += str(type(data))

        if level == 0:
            html += '</table>'
        elif level == 1:
            html += '</td>'

        return html

    def __format_license(self, value, level):
        return f'<li><b>License:</b> {self.__convert_to_html(value, level + 1)}</li>'

    def __format_columns(self, columns, level):
        html = '<p class="metaproperty">'
        for item in columns:
            item = item.copy()

            name = item.pop('name')
            unit = item.pop('unit', '')
            if unit != '':
                html += f'{name} ({unit})'
            else:
                html += f'{name}'

            descr = item.pop('description', '')
            if descr != '':
                html += f': {descr}'
        html += '</p>'
        return html

    def render(self):
        answer = mark_safe(self.__convert_to_html(data=self.json))
        return answer

    def __convert_to_form(self, data, level=0, parent=''):
        """Formats variables into html form for editing

        :param data: either a dict, a list or a string
        :param level: the level of indentation inside the JSON variable
        :return:
        """

        if level == 0:
            # separate each item with a horizontal line
            html = ''
            for key, value in data.items():
                html += f'{self.__convert_to_form(value, level + 1, parent=key)}'
                html += '<hr>'
            html.rstrip('<hr>')
        elif level > 0:
            # between the horizontal lines the item can be a string, a list of objects or a dict
            if isinstance(data, str):
                # simply an input field and a label within a div
                html = '<div class="form_group">'
                if level == 1:
                    label = parent.capitalize()
                else:
                    label = parent.split('_')[-1].capitalize()
                html += f'<label for="{parent}"> {label} </label>'
                html += f'<input class="form-control" id="{parent}" name="{parent}" type="text" value="{data}" />'
                html += '</div>'
            elif isinstance(data, dict):
                html = '<table style="width:100%">'
                html += f'<tr><td style="width:150px"><label>{parent.capitalize()}</label></td></tr>'
                html += '<tr><td></td><td>'
                for key, value in data.items():
                    html += self.__convert_to_form(
                        value,
                        level + 1,
                        parent='{}_{}'.format(parent, key)
                    )

                html += '</td></tr>'
                html += '</table>'
            elif isinstance(data, list):
                html = '<table style="width:100%">'
                html += f'<tr><td style="width:150px"><label for="{parent}_container">{parent.capitalize()}</label></td></tr>'
                html += '<tr><td>'
                html += f'<div id="{parent}_container">'
                for item in data:
                    html += self.__convert_to_form(
                        item,
                        level + 1,
                        parent='{}'.format(parent)
                    )

                html += '</div>'
                html += f'<a onclick="add_{parent}($(\'#{parent}_container\'))">Add</a>'

                html += '</td></tr>'
                html += '</table>'

        return html

    def render_editmode(self):

        answer = mark_safe(self.__convert_to_form(data=self.json))
        return answer