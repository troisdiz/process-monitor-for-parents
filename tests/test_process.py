from os.path import dirname, join

from pmfp.pmfpconfig import PmfpConfig
from pmfp.pmfpprocess import ProcessMonitor, ProcessDescriptor


def test_process_by_query_id():
    config = PmfpConfig.read_config(join(dirname(__file__), 'test_config.yaml')).get_user_config('User1')
    pm: ProcessMonitor = ProcessMonitor(config=config,
                                        process_lister=None,
                                        user_name="User1",
                                        book_keeper=None,
                                        reactions_manager=None)
    processes: list[ProcessDescriptor] = [
        ProcessDescriptor(pid=34, exe_name="truc.exe", user_name="User1")
    ]
    process_by_query_id = pm._get_user_process_by_query_id(processes)

    assert len(process_by_query_id.keys()) == 1
