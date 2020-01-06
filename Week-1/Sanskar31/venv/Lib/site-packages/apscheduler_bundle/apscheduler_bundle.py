import inject
from applauncher.kernel import Kernel
from applauncher.kernel import Configuration

from applauncher.kernel import KernelReadyEvent, KernelShutdownEvent

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock


class Scheduler(object):
    pass


class APSchedulerBundle(object):

    def __init__(self):
        self.config_mapping = {
            "apscheduler": {
                "jobstores": "",
                "executors": "",
                "coalesce": False,
                "max_instances": 3,
                "timezone": "UTC"
            }
        }

        self.scheduler = BackgroundScheduler()

        self.injection_bindings = {
            Scheduler: self.scheduler
        }

        self.event_listeners = [
            (KernelReadyEvent, self.kernel_ready),
            (KernelShutdownEvent, self.kernel_shutdown)
        ]
        self.bundle_lock = Lock()
        self.bundle_lock.acquire()

    def kernel_shutdown(self, event):
        self.bundle_lock.release()

    @inject.params(config=Configuration)
    @inject.params(kernel=Kernel)
    def kernel_ready(self, event, config, kernel):
        self.scheduler.configure(self.build_config(config.apscheduler))
        logging.info("APScheduler ready")
        kernel.run_service(self.run_service)

    def run_service(self):
        self.scheduler.start()
        self.bundle_lock.acquire()
        self.scheduler.shutdown()

    def build_config(self, config):
        apsconfig = {}
        for prop in ["jobstores", "executors"]:
            if isinstance(getattr(config, prop), dict) > 0:
                for prop_name, prop_config in getattr(config, prop).items():
                    apsconfig[".".join(['apscheduler', prop, prop_name])] = prop_config
        apsconfig["apscheduler.job_defaults.coalesce"] = config.coalesce
        apsconfig["apscheduler.job_defaults.max_instances"] = config.max_instances
        apsconfig["apscheduler.timezone"] = config.timezone
        return apsconfig
