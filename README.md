Dieses GitHub Repository enthält eine Konfiguration für eine Anwendung mit Docker Compose. Folgende Dienste sind Teil dieser Konfiguration:

    weatherdb (MariaDB)
    stationdb (MariaDB)
    grafana
    jagdwurst (Jaeger Tracer)
    stationapi
    weatherapi
    traefik

Installation

    Clone dieses Repository auf Ihren Computer:

bash

> git clone https://github.com/fh-erfurt/Cloudy.git

Wechseln Sie in das Verzeichnis des Repositories:

bash
>cd Cloudy

    Führen Sie Docker Compose aus:

docker-compose up -d

Verwendung

Nach der Installation können Sie die einzelnen Dienste unter den folgenden URLs erreichen:

    Grafana: http://grafana.draxento.de
    Jaeger Tracer: http://tracer.draxento.de
    Station API: http://draxento.de/station
    Wetter API: http://draxento.de/weather

Hinweise

    Die MariaDB-Datenbanken werden in Volumes gespeichert, um Datenverlust zu vermeiden.
    Die Dockerfiles für die APIs stationapi und weatherapi müssen im selben Verzeichnis wie die docker-compose.yml-Datei liegen.