import sys


class RedirectLog:
    def __init__(self):
        self.buff = ''
        self.__console__ = sys.stdout

    def write(self, output_stream):
        self.buff += output_stream

    def to_console(self):
        sys.stdout = self.__console__
        print(self.buff)
        return self.buff

    def to_file(self, file_path):
        f = open(file_path, 'w')
        sys.stdout = f
        print(self.buff)
        f.close()

    def flush(self):
        self.buff = ''

    def reset(self):
        sys.stdout = self.__console__
