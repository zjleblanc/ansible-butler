import yaml

class ButlerDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(ButlerDumper, self).increase_indent(flow, False)