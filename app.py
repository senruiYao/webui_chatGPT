from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import openai

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return FileResponse('index.html')


@app.post('/api')
async def api(request: Request):
    def msg(datalist):
        messages = []
        for index, data in enumerate(datalist):
            messages.append({})
            if index / 2:
                messages[index]["role"] = "assistant"
            else:
                messages[index]["role"] = "user"
            messages[index]["content"] = data
        return messages

    datalist = request.json()
    msg = msg(await datalist)
    openai.api_key = 'YOUR_API_KEY'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg
    )
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    uvicorn.run(app='app:app',
                port=80,
                reload=True)
