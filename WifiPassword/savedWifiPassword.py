# python savedWifiPassword.py
import re,os

class savedWifiPassword :
	"""aim to get wifi password saved in device
	# 1. extract wifi name
	# cmd commands - netsh wlan show profile
	# 2. check each of then that does their password is saved in pc
	# cmd commands - netsh wlan show profile {wifi-name} key = clear
	# looking for | Security key : Present |
	# if true # 3. get password"""
	def __init__(self,wifi_name=''):
		if wifi_name != "":
			self.names = [wifi_name]
		else:
			self.names = self.extract_name()
	
	def command_executor(self,command):
		data = os.popen(command).read()
		return data

	def extract_name(self):
		name_command = "netsh wlan show profile"
		patern = r'All User Profile\s*:\s(.*)'
		# get data e.g. - "All User Profile     : Stay_away"
		response = self.command_executor(name_command)
		# extract name form data
		res = re.findall(patern,response)
		return res

	def extract_password(self):
		result_dict = {}
		for name in self.names:
			password_command = f'netsh wlan show profile "{name}" key = clear'
			# get data e.g. "Security key : Present \n Key Content : password"
			results = self.command_executor(password_command)
			# extract security key 
			key_present = re.findall(r"Security key.*: (.*)",results)
			if key_present :
				# extract content key(password)
				password = re.findall(r"Key Content.*: (.*)",results)[0]
				result_dict[name] = password
			else : result_dict[name] = ''

		return result_dict  

	@classmethod
	def wifi_names(cls):
		# return all the wifi names ever connected to
		return cls().names

	@classmethod
	def all(cls):
		# all password
		rishi = cls()
		return rishi.extract_password()

	@classmethod
	def target(cls,name):
		# single password 
		rishi = cls(name)
		return rishi.extract_password()
 
if __name__ == "__main__":
	print(savedWifiPassword.wifi_names())
	print(savedWifiPassword.target('Redmi h'))  # my device for testing
	print(savedWifiPassword.all())
