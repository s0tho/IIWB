from urllib.parse import quote as _uriquote
import sys
import json
from iiwb.core import utils

import aiohttp
#from reverse import __version__


__version__ = '0.1.0'


async def json_or_text(response):
	text = await response.text(encoding='utf-8')
	try:
		if response.headers['content-type'] == 'application/json':
			return json.loads(text)
	except KeyError:
		# Thanks Cloudflare
		pass

	return text

class Route:
	ENV = utils.load_backend()['api']
	BASE = ENV['url']
	PARAMETERS = ''

	def __init__(self, method, path, fields='', **parameters):
		self.path = path
		self.method = method
		try:
			url = (self.BASE + self.path + self.PARAMETERS + fields)
			if parameters:
				self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
			else:
				self.url = url
		except:
			pass
		
		print(self.url)
		print(self.BASE)

class IIWBapi:
	  
	def __init__(self) -> None:
		self.name = "IIWBackend"
		self.token = None
		self.bot_token = None
		self._session = aiohttp.ClientSession()

		user_agent = 'IIWB (https://github.com/s0tho/IIWB {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
		self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

	def recreate(self):
		if(self._session.closed):
			self._session = aiohttp.ClientSession()


	async def request(self, route, *, files=None, **kwargs):
		method = route.method
		url = route.url

		headers = {
			'User-Agent': self.user_agent,
			'Content-Type': 'application/json'
		}

		""" if('user' in kwargs):
			headers['Authorization'] = 'Bearer ' + kwargs['user'] """


		kwargs['headers'] = headers

		async with self._session.request(method, url, **kwargs) as r:

			data = await json_or_text(r)

			if(300 > r.status >= 200):
				return data
			
			if(r.status == 400):
				self.errors(data)


	def errors(self, data):
		code = data["errors"][0].get("code", 0)
		text = data["errors"][0].get("text", "...")
		raise ValueError("{}: {}".format(code, text))
	

	async def index(self):
		r = Route('GET', '/')
		s = await self.request(r)
		return s
	
	
	async def getuserbyid(self, id):
		r = Route('GET', f'/v1/userbyidmp/{id}')
		s = await self.request(r)
		return s
	

	async def addusermp(self, json):
		r = Route('POST', f'/v1/usermp')
		s = await self.request(r, json=json)
		return s

	
	async def updateuser(self, id, json):
		r = Route('PUT', f'/v1/userbyid/{id}')
		s = await self.request(r, json=json)
		return s