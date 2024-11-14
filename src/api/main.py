import os
import contextlib

from fastapi.staticfiles import StaticFiles
from azure.ai.projects.aio import AIProjectClient
from azure.identity import AzureCliCredential

import fastapi

from dotenv import load_dotenv

from .shared import globals


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    project = AIProjectClient.from_connection_string(
        # credential=AzureDeveloperCliCredential(tenant_id="1bd0d125-6c64-49d1-af0d-88fa60e18074"),
        credential=AzureCliCredential(tenant_id="1bd0d125-6c64-49d1-af0d-88fa60e18074"),
        conn_str=os.environ["AZURE_AIPROJECT_CONNECTION_STRING"],
    )

    chat = await project.inference.get_chat_completions_client()
    globals["project"] = project
    globals["chat"] = chat

    yield

    await project.close()
    await chat.close()


def create_app():
    if not os.getenv("RUNNING_IN_PRODUCTION"):
        print("Loading .env file")
        load_dotenv(override=True)

    app = fastapi.FastAPI(lifespan=lifespan)
    app.mount("/static", StaticFiles(directory="api/static"), name="static")

    from . import routes  # noqa

    app.include_router(routes.router)

    return app
