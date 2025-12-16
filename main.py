from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse # 引入 HTMLResponse
from app.core.auth import api_token_auth
from app.routers import train, models, visualization, llm, deploy, knowledge
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Industrial AI Platform")
@app.get("/", include_in_schema=False) # include_in_schema=False 表示不将此路径包含在文档中
async def root():
    # 可以返回一个简单的 HTML 欢迎页面
    return HTMLResponse(
        """
        <html>
            <head>
                <title>Welcome to the Industrial AI Platform Backend</title>
            </head>
            <body>
                <h1>Industrial AI Platform is Running!</h1>
                <p>Access the API documentation at: <a href="/docs">/docs</a></p>
                <p>If you see this, the server is live and healthy.</p>
            </body>
        </html>
        """
    )
app.include_router(train.router, dependencies=[Depends(api_token_auth)])
app.include_router(models.router, dependencies=[Depends(api_token_auth)])
app.include_router(visualization.router, dependencies=[Depends(api_token_auth)])
app.include_router(llm.router, dependencies=[Depends(api_token_auth)])
app.include_router(deploy.router, dependencies=[Depends(api_token_auth)])
app.include_router(knowledge.router, dependencies=[Depends(api_token_auth)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=int(__import__("os").getenv("PORT", 8000)),
    reload=True,
    )