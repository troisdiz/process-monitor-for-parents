from yaml import load, dump
from os.path import dirname, join

from pmfp.pmfpconfig import PmfpConfig, PmfpUserConfig, PmfpActionType


def test_parse_config():

    configs: PmfpConfig = PmfpConfig.read_config(join(dirname(__file__), 'test_config.yaml'))
    assert configs.get_user_config('User1') is not None

    user1_config = configs.get_user_config('User1')
    assert len(user1_config.process_monitors) == 1

    pm_config = user1_config.process_monitors[0]
    assert pm_config is not None
    assert len(pm_config.actions) == 2
