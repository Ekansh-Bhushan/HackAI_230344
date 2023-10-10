from uagents import Agent, Context
agent = Agent(name="agent", seed="agent recovery phase")

@agent.on_interval(period=5)
async def currency_update(ctx:Context): # context is collection of data of the agents example name and seed

    ctx.logger.info(f'The current rate today is {ctx.name}')
    # ctx.logger.info(f'The current rate today is {self.output}')


agent.run()