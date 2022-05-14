import re

TYPE_COLORS = {
    'FF0000': 'page',
    '00B050': 'output',
    '0070C0': 'input',
    '808080': 'comment'
}


class Token:
    def render(self):
        return None


class NewPage(Token):
    def __init__(self, title, form_model='player'):
        self.type = 'page'
        self.title = title
        self.form_model = form_model


class Comment(Token):
    def __init__(self, text):
        self.type = 'comment'
        self.text = text

    def render(self):
        return f"{{# {self.text} #}}"


class Output(Token):
    def __init__(self, variable):
        self.type = 'output'
        self.variable_name = variable
        self.var_for_template = None

        parts = self.variable_name.split('.')
        if len(parts) == 1:
            self.var_for_template = self.variable_name

    def render(self):
        return f"{{{{ {self.variable_name} }}}}"


class Input(Token):
    def __init__(self, variable, input_type='generic'):
        self.type = 'input'
        self.input_type = input_type
        self.variable_name = variable

    def render(self):
        return f"{{{{ formfield '{self.variable_name}' }}}}"


class Button(Input):
    def __init__(self, text):
        self.type = 'input'
        self.input_type = 'button'
        self.text = text

    def render(self):
        if self.text == 'next':
            return "{{ next_button }}"
        else:
            return f"<button type='button' class='btn btn-primary'>{self.text}</button>"


class Text(Token):
    def __init__(self, run):
        self.type = 'text'
        self.run = run

    def render(self):
        prefix = postfix = ''
        if self.run.bold:
            prefix += '<b>'
            postfix += '</b>'
        if self.run.italic:
            prefix += '<i>'
            postfix += '</i>'
        return f"{prefix}{self.run.text}{postfix}"


def token_from_colored_control_sequence(run, match_string):
    if not match_string or len(match_string) < 3:
        return None

    kind = get_type_from_color(run)
    match_string = match_string[1:-1].strip()

    token = None
    if kind == 'page':
        if ':' in match_string:
            parts = match_string.split(':')
            form_model, title = parts[0].strip(), "".join(parts[1:]).strip()
            token = NewPage(title=title, form_model=form_model)
        else:
            token = NewPage(title=match_string)

    if kind == 'comment':
        token = Comment(text=match_string)

    if kind == 'input':
        if ':' in match_string:
            parts = match_string.split(':')
            input_type, identifier = parts[0].strip(), "".join(parts[1:]).strip()
            if input_type in ['boolean', 'currency', 'integer', 'float', 'string', 'longstring']:
                token = Input(variable=identifier, input_type=input_type)
            if input_type == 'button':
                token = Button(text=identifier)
        else:
            token = Input(variable=match_string)

    if kind == 'output':
        token = Output(variable=match_string)

    return token


def has_same_style(previous_run, current_run):
    return previous_run.bold == current_run.bold and \
           previous_run.italic == current_run.italic and \
           previous_run.font.color.rgb == current_run.font.color.rgb


def get_type_from_color(run):
    run_color = str(run.font.color.rgb)
    if run_color not in TYPE_COLORS:
        return None
    return TYPE_COLORS[run_color]


def get_token(run):
    if run.text is None:
        return None

    match = re.search(r"\[[A-Za-z\d\s.,_!?:]*\]", run.text, re.MULTILINE)
    if match:
        # return token_from_control_sequence(match.string)
        return token_from_colored_control_sequence(run, match.string)

    if match is None:
        return Text(run=run)


def merge_runs_with_same_style(runs):
    if not runs:
        return []

    merged_runs = [runs[0]]
    for i, run in enumerate(runs[1:]):
        if has_same_style(runs[i], run):
            merged_runs[-1].text += run.text
        else:
            merged_runs.append(run)
    return merged_runs