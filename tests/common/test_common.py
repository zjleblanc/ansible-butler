import ansiblebutler.common as common
import os

class TestClass:
    configs_dir = os.path.dirname(os.path.abspath(__file__)) + '/configs'

    def test_process_config_merge(self):
        config = common.process_config(self.configs_dir + '/ansible-butler.yml')
        assert config == common.load_yml(self.configs_dir + '/ansible-butler.expected.yml')