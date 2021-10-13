from __future__ import annotations

import fnmatch
import logging
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from itertools import groupby
from typing import Protocol

import psutil

from pmfp.pmfpconfig import PmfpUserConfig

logger = logging.getLogger(f"pmfp.{__name__}")


@dataclass
class ProcessDescriptor:
    pid: int
    exe_name: str
    user_name: str


@dataclass
class ProcessQuery:
    id: str
    name_glob: str


class ProcessLister(Protocol):
    def get_current_processes(self, user_name: str) -> list[ProcessDescriptor]:
        pass

    def kill_process(self, pd: ProcessDescriptor) -> bool:
        pass


class PsUtilProcessLister(ProcessLister):
    def get_current_processes(self, user_name: str) -> list[ProcessDescriptor]:
        return [
            ProcessDescriptor(p.info['pid'], p.info['name'], p.info['username'])
            for p in psutil.process_iter(['pid', 'name', 'username'])
        ]

    def kill_process(self, pd: ProcessDescriptor) -> bool:
        pass


class ProcessMonitor:

    def __init__(self, config: PmfpUserConfig, process_lister: ProcessLister, user_name: str, book_keeper: ProcessBookKeeper, reactions_manager: ReactionsManager):
        self.process_lister: ProcessLister = process_lister
        self.user_name: str = user_name
        self.process_queries: list[ProcessQuery] = [
            ProcessQuery(process_config.processm_id, process_config.prog_name)
            for process_config in config.process_monitors
        ]

    def _get_user_process_by_query_id(self, running_processes: list[ProcessDescriptor]) -> dict[str, list[ProcessDescriptor]]:
        # filter user processes
        user_running_processes: list[ProcessDescriptor] = [
            pd for pd in running_processes if pd.user_name == self.user_name
        ]

        # map to add ProcessQuery id
        processes_with_query_id: list[tuple[str, ProcessDescriptor]] = [
            self._associate_query_id(self.process_queries, running_process) for running_process in
            user_running_processes
        ]

        # Group by ProcessQuery id
        processes_by_query_id: dict[str, list[ProcessDescriptor]] = {}
        # query_id: list_of_processes
        for query_id, list_of_processes in groupby(processes_with_query_id, lambda t: t[0]):
            if list_of_processes is not None:
                processes_by_query_id[query_id] = [p[1] for p in list_of_processes]

        return processes_by_query_id

    def do_check(self):
        # Get process list
        running_processes: list[ProcessDescriptor] = self.process_lister.get_current_processes(self.user_name)

        process_by_query_id: dict[str, list[ProcessDescriptor]] = self._get_user_process_by_query_id(running_processes=running_processes)

        logger.info(f"[{self.name}] Start Job at : " + str(datetime.now()))
        logger.info(f"[{self.name}] Do something")
        logger.info(f"[{self.name}] End Job at   : " + str(datetime.now()))

    @staticmethod
    def _associate_query_id(process_queries: list[ProcessQuery], running_process: ProcessDescriptor) -> tuple[str, ProcessDescriptor]:
        for process_query in process_queries:
            if fnmatch.fnmatch(running_process.exe_name, process_query.name_glob):
                return process_query.id, running_process


# list process
# filter monitored ones
# for each do accounting


class ProcessBookKeeper:
    def __init__(self, process_descriptors: list[ProcessQuery]):
        pass

    def notify_running_processes(self, time, pq: ProcessQuery, pds: list[ProcessDescriptor]) -> int:
        pass


class ReactionsManager:
    def __init__(self, process_queries: list[ProcessQuery]):
        self.process_queries: list[ProcessQuery] = process_queries

    def notify_process_event(self, process, state, total_time: int):
        pass


# ProcessAccounter
# file current time (list of minutes)
# file history : nb of minutes by day
#   * keep max n days
# current day in memory
# evaluate alerts => other object
# handleEvent(process, running or not, time in minutes)
#   processTotal
#   => in Db
#   => AlertingHandler

# AlertingHandler
# should alert ?
# alert
#   what
#       notify
#           where (logs, voice)
#       kill


def is_process_running(name_glob: str) -> bool:
    procs = {p.info['name']: p.info for p in psutil.process_iter(['name', 'username'])}
    for name in procs.keys():
        if fnmatch.fnmatch(name, name_glob):
            print(f"Found {name}")
            return True
    return False

