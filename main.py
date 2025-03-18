import uvicorn
from dotenv import load_dotenv
from src.infra.configs import api



if __name__=="__main__":

    uvicorn.run(api, port=3435)
