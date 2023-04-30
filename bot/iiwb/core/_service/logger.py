import logging

class ReverseLogger(logging.Logger):

	__slots__ = [
        'name',
        'instance',
        'logfile',
		'logformat',
		'formatter'
		'handler'
        'env'
    ]

	def __init__(self, name: str, level=logging.DEBUG, path="./", logformat="", initLog: bool = False, consoleStream:bool = False) -> None:
		"""Create a logger

		Parameters
		----------
		name : str
			Logger name
		level : [type], optional
			Sets the threshold for this logger. Logging messages which are less severe than level will be ignored, by default logging.DEBUG
		path : str, optional
			Logger filepath, by default "./"
		logformat : str, optional
			Specify the layout of log records in the final output, by default ""
		initLog : bool, optional
			Send a record at initialization, by default False
		"""
		super().__init__(name, level=level)
		self.logfile = "{}{}.log".format(path,name)
		self.logformat = logformat or ("[%(asctime)s] %(levelname)-8s :: %(message)s")
		self.formatter = logging.Formatter(self.logformat)
		self.handler = logging.FileHandler(self.logfile, encoding="utf-8")
		

		self.handler.setFormatter(self.formatter)
		self.addHandler(self.handler)
		self.setLevel(logging.DEBUG)
		# Create console handler for logger
		if(consoleStream): self.addHandler(logging.StreamHandler())
		# Message of initialization 
		if(initLog): self.info("Creation of the logging instance - {}/{}".format(self.name, self.logfile))
