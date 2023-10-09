import uagents
from enum import Enum

from uagents import Agent, Buraeu, Context, Model

class Tablestatus(str,Enum):
    RESERVED="reserved"
    FREE="free"
class QueryTableRequest(Model):
    table_number:int
class QueryTabResponse(Model):
    status: Tablestatus
class BookTableRequest(Model):
    table_number:int
class BookTableResponse(Model):
    success:bool

customer=Agent(name="Customer")
restaurant=Agent(name="Restaurant")

@customer.on_interval(period=3.0, messages=QueryTableRequest)
async def inyterval(cyx: Context):
    started=ctx.storage.get("started")

    if not started:
        await ctx.send(restaurant.address,QueryTableRequest(table_number=42))
    ctx.storage.set("started",True)
@customer.on_message(QueryTableRespinse,replies=BookTbleRequest)
async def handle_query_response(ctx: Context,sender: str,msg: QueryTableRequest):
    if msg.status==TableStatus.FREE:
        ctx.logger.info("Table is free, attempting to book it now")
        await ctx.send(restuarant.address,BookTableRequest(table_number=42))
    else:
        ctx.longer.info("Table is not free - nothing more to do")

    @customer.on_message(BooktableResponse,replies=set())
    async def handle_book_response(ctx: Context,sender:str,msg:BookTableResponse):
        if msg.success:
            ctx.logger.info("Table reservation was successful")
        else:
            ctx.logger.info("Table reservation was UNSUCCESSFUL ")
@restaurant.on_message(model=QueryTableRequest,replies=QueryTableResponse)
async def handle_query_request(ctx: Context, sender:str, msg: QueryTableRequest):
    if ctx.storage.has(str(msg.table_number)):
        status=TableStatus.RESERVED
    else:
        status=TableStatus.FREE 
    ctx.logger.info(f"Table {msg.table_number} query.Status{status}")
        await ctx.send(sender,QueryTableResponse(status=status))
@restuarant.on_message(model=BookTableRequest,replies=BookTableResponse)
async def handle_book_request(ctx: Context,sender:str,msg:BookTableRequest):
    if ctx.storage.has(str(msg.table_number)):
        success=False
    else:
        success=True
        ctx.storage.set(str(msg.table_number),sender)
    await ctx.send(sender,BookTableResponse(success=success))