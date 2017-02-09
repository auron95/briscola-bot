class View:
	def redirect(self,user,session=None):
		user.view = self.__class__.__name__
		session.add(user)
		
	def get_input(self,user,text):
		if text in self.ITA_OPTIONS:
			self.ITA_OPTIONS[text](user)

	def __init__(self, user, bot)
		self.user = user
		self.bot = bot
		
class MainMenu(View):
	ITA = 'Menu` principale. Cosa vuoi fare?'
	ITA_OPTIONS = {
		"Crea nuova partita:": new_game
	}
	
	
	def new_game(self,user):
		print "Test"
		
		
