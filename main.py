from uagents import Agent, Context
agent = Agent(name="agent", seed="agent recovery phase")
@agent.on_interval(period=60)
async def currency_update(ctx:Context):
    ctx.logger.info(f'The current rate today is {self.output}')

agent.run()