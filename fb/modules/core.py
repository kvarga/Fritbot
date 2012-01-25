import fb.intent as intent
import fb.modules.base as base
import datetime

class CoreCommandsModule(base.FritbotModule):
	name="Core Commands"
	description="Core Fritbot Commands, minimum functionality."
	author="Michael Pratt (michael.pratt@bazaarvoice.com)"

	def register(self):
		intent.service.registerCommand("reload modules", self.reloadModules, self, "Reload Modules", "(admin) Reload installed modules", True)
		intent.service.registerCommand("allow", self.allow, self, "Allow", "(admin) Assigns an authorization to the current room", True)
		intent.service.registerCommand("disallow", self.disallow, self, "Disallow", "(admin) Unassigns an authorization to the current room", True)
		intent.service.registerCommand("auths", self.auths, self, "Authorizations", "Lists current authorizations for the current room", True)
		intent.service.registerCommand(["shut ?up", "(be )?quiet"], self.quiet, self, "Shut Up", "Shuts up the bot for non-core functions for 5 minutes", True)
		intent.service.registerCommand("come back", self.unquiet, self, "Come Back", "Allows the bot to talk again if shut up.", True)
	
	@base.admin
	def reloadModules(self, bot, room, user, args):

		try:
			intent.service.loadModules()
		except:
			user.send("Modules did not reload successfully, check the error log.")
			raise

		user.send("Modules loaded successfully!")
		return True

	@base.admin
	@base.room_only
	@base.response
	def allow(self, bot, room, user, args):
		if len(args) < 1:
			return u"Must specify a permission..."
		else:
			auths = set(room["auths"]) | set(args)
			room["auths"] = list(auths)
			room.save()

			return u"Ok, allowing the following authorizations: {0}".format(repr(args))

	@base.admin
	@base.room_only
	@base.response
	def disallow(self, bot, room, user, args):
		if len(args) < 1:
			return u"Must specify a permission..."
		else:
			auths = set(room["auths"]) - set(args)
			room["auths"] = list(auths)
			room.save()

			return u"Ok, disallowing the following authorizations: {0}".format(repr(args))

	@base.room_only
	@base.response
	def auths(self, bot, room, user, args):
		return u"I currently have the following authorizations for the {0} room: {1}".format(room.uid, ', '.join(room["auths"]))

	@base.room_only
	@base.response
	def quiet(self, bot, room, user, args):
		'''Squelches the bot for the given room.'''

		room["squelched"] = datetime.datetime.now() + datetime.timedelta(minutes=5);
		room.save()
		return "Shut up for 5 minutes."

	@base.room_only
	@base.response
	def unquiet(self, bot, room, user, args):

		room["squelched"] = datetime.datetime.now() - datetime.timedelta(minutes=5);
		room.save()
		return "And we're back."

module = CoreCommandsModule()