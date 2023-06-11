import json
import os
import datetime
from functools import partial
from discord import Embed, Guild
from iiwb.core._models import Role

utils_open = partial(open, encoding="UTF-8")

def _load_config(name) -> json:
	"""Open file from default config folder and return a corresponding JSON object.

	Parameters
	----------
	name : str
		Config file name

	Returns
	-------
	JSON
		JSON object of the specified config file
	"""
	cwfd = os.path.dirname(os.path.realpath(__file__))  # the directory of utils.py
	jsonf = os.path.realpath(os.path.join(cwfd, '_env', name))
	with utils_open(jsonf) as fp:
		return json.load(fp)

def load_custom_config(name, file, path = '_env') -> json:
	"""Open file and return a corresponding JSON object.

	Parameters
	----------
	name : str
		Config file name
	file : str
	path : str, optional
		Filepath, by default '_env'

	Returns
	-------
	JSON
		JSON object of the specified config file
	"""
	cwfd = os.path.dirname(os.path.realpath(file))  # the directory of utils.py
	jsonf = os.path.realpath(os.path.join(cwfd, path, name))
	with utils_open(jsonf) as fp:
		return json.load(fp)

def _create_folder(folder) -> None:
	import pathlib
	cwfd = os.path.dirname(os.path.realpath(__file__))  # the directory of utils.py
	jsonf = os.path.realpath(os.path.join(cwfd, '_env', folder))
	pathlib.Path(jsonf).mkdir(parents=True, exist_ok=True)

def _load_logger(name, JSON=False, toArray=True) -> None:
	"""Open file and return a corresponding file object or JSON.

	JSON=False is an optional boolean that specifies if the log file is a JSON.
	"""
	cwfd = os.path.dirname(os.path.realpath(__file__))  # the directory of utils.py
	jsonf = os.path.realpath(os.path.join(cwfd, '_env', name))
	with utils_open(jsonf) as fp:
		if(JSON):
			return json.load(fp)
		if(toArray):
			lines = fp.read().splitlines()
			return lines
		return fp.read()

def load_backend() -> json:
	"""Open backend configuration file and return the corresponding JSON object.

	Returns
	-------
	JSON
		Return a JSON object of env.json
	"""
	return _load_config("env.json")

def parse_args(args, delimiter='--') -> tuple:
	"""Parse a list of arguments

	Parameters
	----------
	args : list
		List of str
	delimiter : str, optional
		Delimiter, by default '--'

	Returns
	-------
	tuple
		(**kwargs, *args)
	"""
	_kwargs = {}
	_args = []
	for index, value in enumerate(args):
		if delimiter in value:
			try:
				_kwargs[value[len(delimiter):]] = args[index+1]
			except:
				pass
		elif args[index-1][len(delimiter):] not in _kwargs.keys():
			_args.append(value)
		else:
			continue
	return (_kwargs, _args)

def isListContains(lesser: list, bigger: list) -> bool:
	"""Check if bigger contains all elements in lesser

	Parameters
	----------
	lesser : list
		Lesser list
	bigger : list
		Bigger list

	Returns
	-------
	bool
		If bigger list contains all elements of lesser list
	"""

	return all(elem in lesser for elem in bigger)

def isNameInList(name: str, array: list, attr: str = "name") -> bool:
	"""Look for strings in a list of object on specific attribute

	Parameters
	----------
	name : str
		String to find
	array : list
		List of object
	attr : str, optional
		Attribute to check in object, by default "name"
	""" 
	for role in array:
		if(name == getattr(role, attr)):
			return True
	return False

def listCogs(filterIn: dict= {'on'}) -> dict:
	"""Open config file and list all cogs to be load

	Parameters
	----------
	filterIn : dict, optional
		, by default {'on'}

	Returns
	-------
	dict
		List of cogs to load
	"""
	with open('cogs.json', 'r') as cogsList:
		data = json.load(cogsList)
	return dict(filter(lambda elem: elem[1] in filterIn, data.items()))

def formatEmbed(title: str, author: str, **kwargs) -> Embed:
	"""Return a formated embed from dict's keys and values

	Parameters
	----------
	title : str
		Embed title
	author : str
		Embed author

	Returns
	-------
	Embed
	"""
	embed=Embed(title=title, color=0xe80005)
	embed.set_author(name=author)
	for name, value in kwargs.items():
		embed.add_field(name=name, value=value, inline=False)
	embed.set_footer(text="Asked by {}".format(author))
	return embed

def getRole(role: int, guild: Guild) -> Role:
	"""Find a role in specific Guild from ID

	Parameters
	----------
	role : int
		Role Identifier
	guild : Guild
		Guild Object

	Returns
	-------
	Role
		Role object
	"""
	return Role(role, guild)

def now() -> datetime:
	"""Construct a datetime from time.time and datetime.timezone.utc

	Returns
	-------
	datetime
	"""
	return datetime.datetime.now(datetime.timezone.utc)

def time_until(when, startDate:datetime = None) -> float:
	"""A helper that give delta from specified time

	Parameters
	-----------
		when: :class:`datetime.datetime`
	"""
	if when.tzinfo is None:
		when = when.replace(tzinfo=datetime.timezone.utc)
	now = startDate or datetime.datetime.now(datetime.timezone.utc)
	delta = (when - now).total_seconds()

	return delta

async def specifiedRole(name: str, guild: list, author: list, attr: str = "name", ctx = None):
	"""A helper that check if the author has the specified role

	Parameters
	----------
	name : str
		Role name
	guild : list
		Discord Server
	author : list
		Author 
	attr : str, optional
		by default "name"
	ctx : [type], optional
		Context, by default None

	Returns
	-------
	Bool
	"""
	g_role = False
	a_role = False
	if(g_role := isNameInList(name, guild.roles)) == False:
		if(ctx is not None):
			await ctx.send("You need to create the role `{}` to use this on you server.".format(name))
	if(a_role := isNameInList(name, author.roles)) == False:
		if(ctx is not None):
			await ctx.send("You need the role `{}`.".format(name))
	return all([g_role, a_role])

def generate_next_call(startDate:datetime=None, days:int=0, seconds:int=0, microseconds:int=0, milliseconds:int=0, minutes:int=0, hours:int=0, weeks:int=0, adding:bool=False) -> datetime:
	"""Generate datetime from now

	Parameters
	----------
	days : int, optional
		by default 0
	seconds : int, optional
		by default 0
	microseconds : int, optional
		by default 0
	milliseconds : int, optional
		by default 0
	minutes : int, optional
		by default 0
	hours : int, optional
		by default 0
	weeks : int, optional
		by default 0
	adding : bool, optional
		by default False

	Returns
	-------
	datetime
	"""
	_now = startDate or now()
	if(not adding):
		return (_now + datetime.timedelta(days=days, weeks=weeks)).replace(second=seconds, microsecond=microseconds, minute=minutes, hour=hours)
	else:
		return _now + datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)


def getObjectsAttr(objects, attr) -> list:
	"""Get specified attribute from a list of objects

	Parameters
	----------
	objects : list of object

	Returns
	-------
	list
		list of attribute from objects
	"""
	_array = []
	for obj in objects:
		_array.append(getattr(obj, attr))
	return _array

def getAllMembers(guild: Guild, roleID: int) -> list:
	"""Get all members in guild, equivalent reverse.Role.getAllMembers()

	Parameters
	----------
	guild : Guild
		Discord server
	roleID : int
		Role id

	Returns
	-------
	list
	"""
	r = getRole(int(roleID), guild)
	return r.getAllMembers()

def valideDate(date_text):
	try:
		datetime.datetime.strptime(date_text, '%d-%m-%Y')
	except ValueError:
		return False
	
	return True

def strike(text):
	"""Strikethrough string

	Parameters
	----------
	text : Str

	Returns
	-------
	str
		Striketrough string
	"""
	return ''.join([u'\u0336{}'.format(c) for c in text])



def existInList(lists, value):
	_store = 0
	for row in lists:
		if(value in lists[row]):
			_store += 1
	return _store