import log
import os

class IgnoreMapping:
    """Provides convenience methods for accessing and manipulating the JSON ignore object."""

    def __init__(self, root, config):
        """
        Args:
            root: the directory containing the config file; the root of the exile context
            config: the parsed representation of the file configuration
        """
        self.__root = root
        self.__config = config

    def __path_components(self, path):
        """
        Splits a path into a list of path components relative to the configuration file.

        For example, if the manifest file was at /tmp/exile.manifest:

            /tmp/path/to/a/file

        becomes:

            ['path', 'to', 'a', 'file']
        """

        path = os.path.realpath(path)
        if not path.startswith(self.__root):
            if not self.__silent:
                log.info("skipping path outside manifest scope: " + path)
            return None

        relative = os.path.relpath(path, self.__root)

        parts = []
        head, tail = os.path.split(relative)
        while tail:
            parts = [tail] + parts
            head, tail = os.path.split(head)

        if head:
            parts = [head] + parts

        return parts

    def __get(self, parts):
        """
        For a given path, returns True if the file or directory should be ignored.

        Args:
            parts: a list of components of the path (probably from __path_components)
        """
        try:
            value = self.__config
            for part in parts:
                value = value[part]
                if value == "": # means it is ignored if the value is an empty string rather than another dict
                    return True
            return False
        except (KeyError, TypeError):
            return False

    def get(self, path):
        """
        For a given path, returns True if the file or directory should be ignored.
        """
        value = self.__get(self.__path_components(path))
        return value

    def add(self, path):
        """
        Add the given path to the ignores.

        Args:
            path: the path to the file to add
        """

        parts = self.__path_components(path)
        if not parts:
            return

        dict = self.__config
        for i in range(len(parts)):
            if i is len(parts) - 1:
                if parts[i] not in dict:
                    dict[parts[i]] = ""

            if parts[i] not in dict:
                dict[parts[i]] = {}

            dict = dict[parts[i]]

    def isEmpty(self):
        for k in self.__config:
            return False
        return True