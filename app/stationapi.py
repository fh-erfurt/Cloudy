# Module Imports
import mariadb
import sys
import uvicorn

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import \
    JaegerExporter as ThriftJaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.types import ASGIApp
from pydantic import BaseModel

app = FastAPI()

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="weatherstation",
        password="mystationpassword",
        host="stationdb",
        port=3306,
        database="station"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
cur.execute('''
create table if not exists stations
(
    id     int auto_increment
        primary key,
    city   varchar(64) null,
    vendor varchar(64) null
);
''')


# https://github.com/blueswen/fastapi-jaeger
def setting_jaeger(app: ASGIApp, app_name: str, log_correlation: bool = True) -> None:
    # Setting jaeger
    # set the service name to show in traces
    resource = Resource.create(attributes={
        "service.name": app_name
    })

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    tracer.add_span_processor(BatchSpanProcessor(ThriftJaegerExporter(
        agent_host_name="jagdwurst",
        agent_port=6831,
    )))

    # override logger format which with trace id and span id
    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)


# Setting jaeger exporter
setting_jaeger(app, "StationAPI")


@app.get("/greeting")
async def read_root():
    return {"Service": "StationAPI"}


@app.get("/list")
async def readStations():
    cur.execute("SELECT * FROM stations")
    return cur.fetchall()


class StationData(BaseModel):
    city: str
    vendor: str


@app.post("/create")
async def addStationData(data: StationData):
    cur.execute("INSERT INTO stations (city, vendor) VALUES (?,?)", (data.city, data.vendor))
    conn.commit()
    return {"Transaction", "Success"}


if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=80, log_config=log_config)
