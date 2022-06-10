from distributed import Client  # type: ignore
from backend.config import get_settings


def get_dask_client() -> Client:
    settings = get_settings()
    return Client(settings.dask_scheduler_host, asynchronous=True)
