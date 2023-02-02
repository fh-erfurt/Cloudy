# Module Imports
from datetime import datetime
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
        user="weather",
        password="myweatherpassword",
        host="weatherdb",
        port=3306,
        database="weather"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
cur.execute('''
create table if not exists weather
(
    id             int auto_increment
        primary key,
    weatherstation int      not null,
    timestamp      datetime not null,
    temperature    float   null
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
setting_jaeger(app, "WeatherAPI")


@app.get("/greeting")
async def read_root():
    return {"Service": "WeatherAPI"}


@app.get("/list")
async def readStations():
    cur.execute("SELECT * FROM weather")
    return cur.fetchall()


class WeatherData(BaseModel):
    weatherstation: int
    timestamp: datetime
    temperature: float


@app.post("/create")
async def addWeatherData(data: WeatherData):
    cur.execute("INSERT INTO weather (weatherstation, timestamp, temperature) VALUES (?,?,?)",
                (data.weatherstation, data.timestamp, data.temperature))
    conn.commit()
    return {"Transaction", "Success"}


if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=80, log_config=log_config)
