from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import yaml
from yaml import load


class PmfpConfig:
    def __init__(self, user_configs: list[PmfpUserConfig]):
        self.user_configs_by_user_name: dict[str, PmfpUserConfig] = {user_config.user_name: user_config for user_config in user_configs}

    def get_user_config(self, user_name: str) -> PmfpUserConfig:
        if user_name in self.user_configs_by_user_name:
            return self.user_configs_by_user_name[user_name]
        else:
            return None

    @staticmethod
    def read_config(file_path: str):
        with open(file_path) as yaml_file:
            yaml_conf = load(yaml_file, Loader=yaml.BaseLoader)
            user_configs: list[PmfpUserConfig] = [_read_user_config(yaml_conf['configs'][yaml_user_config]) for
                                                  yaml_user_config in yaml_conf['configs'].keys()]
        return PmfpConfig(user_configs)


def _read_user_config(user_config: dict) -> PmfpUserConfig:
    if 'processes' in user_config:
        processes_yaml = user_config['processes']
    else:
        processes_yaml = []
    process_configs: list[PmfpProcessMonitor] = [_read_process_monitor(pm_config) for pm_config in processes_yaml]
    return PmfpUserConfig(user_name=user_config['name'], process_monitors=process_configs)


def _read_process_monitor(processmonitor_config: dict) -> PmfpProcessMonitor:
    action_list: list[PmfpAction] = []
    if 'actions' in processmonitor_config:
        action_list: list[PmfpAction] = [_read_monitor_action(action_key, processmonitor_config['actions'][action_key]) for action_key in processmonitor_config['actions']]
    return PmfpProcessMonitor(processmonitor_config['name'], prog_name=processmonitor_config['glob'], actions=action_list)


def _read_monitor_action(action_type_str: str, action_config: dict) -> PmfpAction:
    action_type: PmfpActionType = PmfpActionType[action_type_str.upper()]
    max_time: int = int(action_config['time'])
    max_time_per_unit: PmfpTimeUnit = PmfpTimeUnit[action_config['unit'].upper()]
    return PmfpAction(type=action_type, max_time=max_time, max_time_per_unit=max_time_per_unit)


@dataclass
class PmfpUserConfig:
    user_name: str
    process_monitors: list[PmfpProcessMonitor]


class PmfpTimeUnit(Enum):
    SECONDS = 1
    MINUTE = 2
    HOUR = 3


class PmfpActionType(Enum):
    WARN_NOTIF = 1
    WARN_VOCAL = 1 << 2
    KILL = 1 << 3


@dataclass
class PmfpAction:
    type: PmfpActionType
    max_time: int
    max_time_per_unit: PmfpTimeUnit


@dataclass
class PmfpProcessMonitor:
    processm_id: str
    prog_name: str
    actions: list[PmfpAction]
