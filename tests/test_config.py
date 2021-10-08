from os.path import dirname, join
from enum import Enum
from pmfp.pmfpconfig import PmfpConfig, PmfpUserConfig, PmfpActionType

import pytest


class TestConfigFiles(Enum):
    STANDARD = "config-files/test_config.yaml"
    NO_PROCESS = "config-files/no-process-config.yaml"


def test_parse_config():

    configs: PmfpConfig = PmfpConfig.read_config(join(dirname(__file__), 'config-files/test_config.yaml'))
    assert configs.get_user_config('User1') is not None

    user1_config = configs.get_user_config('User1')
    assert len(user1_config.process_monitors) == 1

    pm_config = user1_config.process_monitors[0]
    assert pm_config is not None
    assert len(pm_config.actions) == 2


@pytest.mark.parametrize("test_file_enum", [member for name, member in TestConfigFiles.__members__.items()])
def test_eval(test_file_enum):
    configs: PmfpConfig = PmfpConfig.read_config(join(dirname(__file__), test_file_enum.value))
