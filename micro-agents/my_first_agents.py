import uagents
from uagents import Agent, Context

Alice = Agent(name="alice", seed="alice recovery phrase")

@Alice.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'Hello, my name is {Alice.name}')

if __name__ == "__main__":
    Alice.run()
