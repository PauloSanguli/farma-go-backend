import uvicorn
from dotenv import load_dotenv
from src.infra.configs import api



if __name__=="__main__":
    load_dotenv()
    uvicorn.run(api, port=3435, reload=True)
