from fastapi_utils.tasks import repeat_every

from run import app


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 12)
def run_etl():
    from core.hsreplay_etl import HSReplayETL
    return HSReplayETL()
