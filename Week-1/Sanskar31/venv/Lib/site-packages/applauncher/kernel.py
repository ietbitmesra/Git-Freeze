import logging
import inject
import signal
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
import blinker
from mapped_config.loader import YmlLoader, InvalidDataException
import colorlog
import sys


class Configuration(object):
    """This class is only used for an friendly injection of configuration"""
    pass


class Environments(object):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    TEST = "test"


class EventHierarchy(type):
    def __new__(mcs, name, bases, dct):
        signal_list = [dct["event_name"]]
        for base in bases:
            if hasattr(base, "_signals"):
                signal_list += getattr(base, "_signals")
        dct["_signals"] = signal_list
        return type.__new__(mcs, name, bases, dct)


class Event(metaclass=EventHierarchy):
    event_name = "event"


class KernelReadyEvent(Event):
    event_name = "kernel.kernel_ready"


class ConfigurationReadyEvent(Event):
    event_name = "kernel.configuration_ready"

    def __init__(self, configuration):
        self.configuration = configuration


class InjectorReadyEvent(Event):
    event_name = "kernel.injector_ready"


class KernelShutdownEvent(Event):
    event_name = "kernel.kernel_shutdown"


class EventManager(object):
    def add_listener(self, event, listener):

        if isinstance(event, str):
            s = blinker.signal(event)
        else:
            s = blinker.signal(event.event_name)

        s.connect(listener)

    def dispatch(self, event):
        for i in getattr(event, "_signals"):
            blinker.signal(i).send(event)

class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message != "\n":
            self.logger.log(self.level, message)

    def flush(self):
        pass

class Kernel(object):

    def __init__(self,
                 environment,
                 bundles,
                 configuration_file="config/config.yml",
                 parameters_file="config/parameters.yml"):
        self.logger = None
        self.configuration_file = configuration_file
        self.parameters_file = parameters_file
        self.bundles = bundles
        self.environment = environment
        self.log_handlers = []
        self.is_shutdown = False
        max_workers = cpu_count() * 5
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.running_services = []
        self.event_manager = EventManager()

        # First of all, configure the logger
        self.configure_logger(environment=environment)

        try:
            self.configuration = self.load_configuration(environment)
            self.logger.info("Starting kernel")
            # Subscribe bundle events
            self.logger.info("Registering event listeners")
            for bundle in self.bundles:
                if hasattr(bundle, 'event_listeners'):
                    for event_type, listener in bundle.event_listeners:
                        self.event_manager.add_listener(event=event_type, listener=listener)
                        # event_list.append(event_type.__name__)
                    self.logger.debug((f"Registered events for {bundle.__class__.__name__}: {', '.join([event_type.__name__ for event_type, _ in bundle.event_listeners])}"))

            # Injection provided by the base system
            injection_bindings = {
                Kernel: self,
                Configuration: self.configuration,
                EventManager: self.event_manager
            }
            self.event_manager.dispatch(ConfigurationReadyEvent(self.configuration))
            # Injection from other bundles
            self.logger.info("Registering injection bindings")
            for bundle in self.bundles:
                if hasattr(bundle, 'injection_bindings'):
                    injection_bindings.update(bundle.injection_bindings)
                    self.logger.debug(f"Injection bindings for {bundle.__class__.__name__}: {', '.join([i.__name__ for i in bundle.injection_bindings.keys()])}")

            # Set this kernel and configuration available for injection
            def my_config(binder):
                for key, value in injection_bindings.items():
                    binder.bind(key, value)
            inject.configure(my_config)
            self.event_manager.dispatch(InjectorReadyEvent())

            self.logger.info("Registering log handlers")
            for bundle in self.bundles:
                if hasattr(bundle, 'log_handlers'):
                    for h in bundle.log_handlers:
                        logging.root.addHandler(h)
        except Exception as e:
            logging.exception(e)
            raise e

        self.register_signals()
        self.logger.info("Kernel Ready")
        self.event_manager.dispatch(KernelReadyEvent())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()

    def register_signals(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signal, frame):
        self.shutdown()

    def run_service(self, service_function, *args):
        self.running_services.append(self.thread_pool.submit(service_function, *args))

    def configure_logger(self, environment):
        log_level = logging.INFO
        # Console output
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.DEBUG)
        if environment == Environments.DEVELOPMENT:
            format = "%(bold)s%(asctime)s%(reset)s [%(log_color)s%(bold)s%(levelname)s%(reset)s] - %(thin_cyan)s%(name)s%(reset)s - %(log_color)s%(message)s%(reset)s (%(bold)s%(filename)s%(reset)s:%(lineno)d)"
            ch.setFormatter(colorlog.ColoredFormatter(
                format,
                reset=True,
            ))
        else:
            format = "s%(asctime)s [%(levelname)s] - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
            ch.setFormatter(logging.Formatter(format))

        # Reset handlers
        for h in logging.root.handlers:
            logging.root.removeHandler(h)
        logging.root.addHandler(ch)

        logging.root.setLevel(log_level)
        for i in self.log_handlers:
            logging.root.addHandler(i)

        # Redirect the output to the log
        print_logger = logging.getLogger("print")
        sys.stdout = LoggerWriter(logger=print_logger, level=logging.INFO)

        self.logger = logging.getLogger("kernel")

    def load_configuration(self, environment):
        mappings = {}
        for bundle in self.bundles:
            if hasattr(bundle, "config_mapping"):
                mappings.update(bundle.config_mapping)
        c = YmlLoader()
        config = c.load_config(self.configuration_file, self.parameters_file)
        try:
            config = c.build_config(config, mappings)
        except InvalidDataException as ex:
            print("Configuration error: ")
            for i in ex.errors:
                print(i)
            exit()

        return config

    def shutdown(self):
        if not self.is_shutdown:
            self.is_shutdown = True
            self.logger.info("Kernel shutting down")
            self.event_manager.dispatch(KernelShutdownEvent())
            self.logger.info("Waiting bundles services to end")
            self.thread_pool.shutdown()
            self.logger.info("Kernel shutdown")

    def wait(self):
        """Wait for all services to finish"""
        for i in self.running_services:
            i.result()
