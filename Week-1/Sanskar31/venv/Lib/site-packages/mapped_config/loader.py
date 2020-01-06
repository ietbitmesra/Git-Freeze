import yaml
import json
import re
from abc import ABCMeta, abstractmethod
import six
import os
from cerberus import Validator
from collections import namedtuple

class InvalidDataException(Exception):
    def __init__(self, errors):
        self.errors = errors


def dict_to_namedtuple(dictionary):
    for key, value in dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = dict_to_namedtuple(value)
            elif isinstance(value, list):
                el = []
                for i in value:
                    if isinstance(i, dict):
                        el.append(dict_to_namedtuple(i))
                    else:
                        el.append(i)
                dictionary[key] = el
    return namedtuple('Configuration', dictionary.keys())(**dictionary)


def is_string(value):
    try:
        float(value)
        return False
    except ValueError:
        if value.lower() in ["true", "false"]:
            return False
        else:
            return True


type_map = {
    int: "integer",
    str: "string",
    float: "float",
    bool: "boolean"
}
def mapped_to_cerberus(d):

    for key, value in d.items():

        if value is None:
            d[key] = {"required": True}
        elif isinstance(value, dict):
            if "type" not in value:
                schema_dict = {"type": "dict", "default": {}, "schema": mapped_to_cerberus(value)}
                d[key] = schema_dict

        elif isinstance(value, list):
            if len(value) > 0:
                schema_list = mapped_to_cerberus({"_":value[0]})["_"]
            else:
                schema_list = {}

            if isinstance(value, list):
                if isinstance(value[0], dict):
                    default_value = []
                else:
                    default_value = value
            elif not isinstance(value, dict):
                default_value = value
            else:
                default_value = []
            d[key] = {"type": "list", "default": default_value, "schema": schema_list}
        else:

                new_value = {
                    "type": type_map[type(value)],
                    "default": value,
                    "required": False
                }
                d[key] = new_value



    return d




def build_config(mapped_schema, config_data, as_named_tuple=True):
    if not isinstance(mapped_schema, dict):
        mapped_schema = mapped_schema.build()

    cer = mapped_to_cerberus(mapped_schema)
    v = Validator(cer)
    if v.validate(config_data):
        if as_named_tuple:
            config = dict_to_namedtuple(v.document)
        else:
            config = v.document
        return config
    else:
        raise InvalidDataException(format_errors(v.errors))



def format_errors(errors, prefix=[]):
    error_list = []
    for key, value in errors.items():
        for err in value:
            node_prefix = prefix + [str(key)]
            if isinstance(err, dict):
                error_list += format_errors(err, node_prefix)
            else:
                error_list.append("Field [{field}] {desc}".format(field=":".join(node_prefix), desc=err))
    return error_list






@six.add_metaclass(ABCMeta)
class ConfigurationLoader(object):
    @abstractmethod
    def load_parameters(self, source):
        """Convert the source into a dictionary"""
        pass

    @abstractmethod
    def load_config(self, config_source, parameters_source):
        pass

    def build_config(self, data, mapping, as_namedtuple=True):
        return build_config(mapped_schema=mapping, config_data=data, as_named_tuple=as_namedtuple)



class YmlLoader(ConfigurationLoader):
    def load_parameters(self, source):
        """For YML, the source it the file path"""
        with open(source) as parameters_source:
            loaded = yaml.safe_load(parameters_source.read())
            for k, v in loaded.items():
                if isinstance(v, str):
                    loaded[k] = "'"+v+"'"
            return loaded

    def load_config(self, config_source, parameters_source):
        """For YML, the source it the file path"""
        with open(config_source) as config_source:
            config_raw = config_source.read()

            parameters = {}
            """Parameteres from file"""
            if os.path.isfile(parameters_source):
                params = self.load_parameters(parameters_source)
                if params is not None:
                    parameters.update(params)

            """Overwrite parameteres with the environment variables"""
            env_params = {}
            env_params.update(os.environ)
            for k, v in env_params.items():
                if is_string(v):
                    env_params[k] = "'" + v + "'"

            parameters.update(env_params)

            """Replace the parameters"""
            final_configuration = config_raw.format(**parameters)
            final_configuration = yaml.safe_load(final_configuration)
            return final_configuration if final_configuration is not None else {}


class JsonLoader(ConfigurationLoader):
    def __init__(self):
        self.parameters = None

    def load_parameters(self, source):
        """For JSON, the source it the file path"""
        with open(source) as parameters_source:
            return json.loads(parameters_source.read())

    def load_config(self, config_source, parameters_source):
        """For JSON, the source it the file path"""
        with open(config_source) as config_source:
            config_raw = config_source.read()
            """Replace the parameters"""
            pattern = "(%[a-zA-Z_0-9]*%)"

            self.parameters = {}
            """Parameteres from file"""
            if os.path.isfile(parameters_source):
                self.parameters.update(self.load_parameters(parameters_source))

            """Overwrite parameteres with the environment variables"""
            self.parameters.update(os.environ)

            replaced_config = re.sub(pattern=pattern, repl=self._replace_function, string=config_raw)
            return json.loads(replaced_config)

    def _replace_function(self, match):
        # Remove % from the begining and from the end
        parameter_key = match.group(0)[1:-1]
        value = self.parameters[parameter_key]
        # Add the " for string values
        return str(value) if str(value).isdigit() else '"{value}"'.format(value=value)


