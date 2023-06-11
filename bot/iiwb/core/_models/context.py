from discord.ext.commands import Context
from iiwb.core._models import Message

class Context(Context):

    DEBUG = False

    def __init__(self, ctx: Context, clsName: str = "Unknown"):
        super().__init__(
            message=ctx.message,
            bot=ctx.bot,
            args=ctx.args,
            kwargs=ctx.kwargs,
            prefix=ctx.prefix,
            command=ctx.command,
            view=ctx.view,
            invoked_with=ctx.invoked_with,
            invoked_subcommand=ctx.invoked_subcommand,
            subcommand_passed=ctx.subcommand_passed,
            command_failed=ctx.command_failed
        )
        self.initClsName = clsName # Store the class name that initialized the Context
        self.run()
    
    def run(self):
        self.on_message()

    def toggleDebug(self):
        Context.Debug != Context.Debug

    def isDebug(self):
        return Context.DEBUG
    
    def on_message(self):
        if(Context.DEBUG): print('New context found, triggered by {}, message : {}'.format(self.initClsName, self.message))

