from discord import Role, Guild, Member
from discord.utils import get

class Role:

	def __new__(cls, role: int, guild: Guild):
		role = get(guild.roles, id=role)
		if(not role):
			return None
		return super(Role, cls).__new__(cls)

	def __init__(self, role: int, guild: Guild):
		self.role = get(guild.roles, id=role)
		self.guild = guild
		self.id = self.role.id
		self.name = self.role.name

	def getAllMembers(self) -> list:
		_m = []
		for v in self.guild.members:
			if(self.role in v.roles):
				_m.append(v)
		return _m