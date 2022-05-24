class Experiment:
    def __init__(self, adapter):
        self.adapter = adapter
        self.adapter.parse()

        self.pages = self.adapter.pages
        self.player_fields = self.adapter.player_fields
        self.group_fields = self.adapter.group_fields

    @staticmethod
    def _render_class(class_name, fields):
        content = f"class {class_name}(Base{class_name}):\n"
        for field in fields:
            content += f"{field}\n"
        return content

    def render_player_class(self):
        return self._render_class('Player', self.player_fields)

    def render_group_class(self):
        return self._render_class('Group', self.group_fields)

