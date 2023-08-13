import ansiblebutler.playbook._update as update
import pytest
import yaml
import os
import filecmp

class TestClass:
    examples_dir = os.path.dirname(os.path.abspath(__file__)) + '/examples'
    configs_dir = os.path.dirname(os.path.abspath(__file__)) + '/configs'
    
    @pytest.fixture()
    def config(self):
        with open(self.configs_dir + '/update_config.yml') as cfg:
            return yaml.safe_load(cfg)

    @pytest.mark.parametrize('playbook', ['windows','azure','aws'])
    def test_playbook_update(self, playbook):
        actual_path = self.examples_dir + f'/test-{playbook}.butler.yml'
        expected_path = self.examples_dir + f'/test-{playbook}.butler.expected.yml'
        update.update_playbook(self.examples_dir + f'/test-{playbook}.yml', config={}, in_place=False)
        assert filecmp.cmp(actual_path, expected_path, shallow=False)

    @pytest.mark.parametrize('playbook', ['custom-config'])
    def test_playbook_update_config(self, config, playbook):
        actual_path = self.examples_dir + f'/test-{playbook}.butler.yml'
        expected_path = self.examples_dir + f'/test-{playbook}.butler.expected.yml'
        update.update_playbook(self.examples_dir + f'/test-{playbook}.yml', config=config, in_place=False)
        assert filecmp.cmp(actual_path, expected_path, shallow=False)
