from fastapi import FastAPI, WebSocket, Form
from fastapi.responses import Response, HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
import pathlib
from uuid import uuid4


template = Jinja2Templates(pathlib.Path(__file__).parent/'templates')

app = FastAPI()

app.mount('/static',StaticFiles(directory='static'),name='static')




app.sockets = dict()




async def check_socket(websocket: WebSocket, app, chat_id):
    while websocket.client_state.name == "CONNECTED":
        await asyncio.sleep(1)
    
    for i,j in enumerate(app.sockets[chat_id]):
        
        if j == websocket:
            app.sockets[chat_id].remove(j)
            


async def bridge(websocket: WebSocket, app, chat_id):
    while True:
        text = await websocket.receive_text()
        for i in app.sockets[chat_id]:
            if i != websocket:
                other_cli = i
        
        await other_cli.send_text(text)



@app.websocket('/ws/{chat_id}')
async def websocket_entry(websocket: WebSocket, chat_id):
    await websocket.accept()  
    
    print(app.sockets)
    
    app.sockets[chat_id].append(websocket)
    print(app.sockets)
        
    await websocket.send_text('waiting')
    await asyncio.gather(
        bridge(websocket, app, chat_id),
        check_socket(websocket, app, chat_id)
        )
    

@app.route('/')
async def open_websocket(request:Request):
    chat_id = uuid4()
    chat_url = f'{request.base_url}' + f'connect/{chat_id}'
    return HTMLResponse(f"""
                        <a href="{chat_url}">{chat_url}</a>
                        """)
    

@app.get('/connect/{chat_id}')
async def connect_websocket(request: Request, chat_id):
    
    if not app.sockets.get(chat_id, None):
        app.sockets[chat_id] = []
    
    return template.TemplateResponse(name='index-s.html', context={
        'request':request
        
    })








# app.sockets = set() 


# async def check_socket(tasks, websocket: WebSocket):
#     while websocket.client_state.name == "CONNECTED":
#         await asyncio.sleep(5)
    
#     for task in tasks:
#         task:asyncio.Task
#         task.cancel()
    
    
    
        
        

# async def reciver(websocket: WebSocket):
#     while True:
#         print(await websocket.receive_text())
    
        
# async def sender(websocket: WebSocket):
#     while True:
#         txt = await aioconsole.ainput(f'{websocket.client}')
#         await websocket.send_text(txt)




# async def worker(websocket: WebSocket):
#     # inp = asyncio.create_task(aioconsole.ainput(f'{websocket.client}'))
#     t1 = asyncio.create_task(reciver(websocket))
#     t2 = asyncio.create_task(sender(websocket))
#     t3 = asyncio.create_task(check_socket([t1,t2],websocket))
#     await asyncio.gather(t1,t2,t3)


    
    

    
    
    
# @app.route('/')
# async def view_sockets(request:Request):
    
#     discoonect = set()
#     for sock in request.app.sockets:
#         if sock.client_state.name != "CONNECTED":
#             discoonect.add(sock)
#     sockets = request.app.sockets.difference(discoonect)
            
    
#     return template.TemplateResponse('index.html',
#                                      context={
#                                          'request':request,
#                                          'sockets':sockets})

# @app.route('/send')
# async def bridge(request:Request):
#     socket = request.query_params.get('socket')
#     text = request.query_params.get('text')
    
#     for sock in app.sockets:
#         if str(sock.client) == socket:
#             await sock.send_text(text)
    
    
#     return RedirectResponse('/')