# Cloudy

Dieses Repository ist das Ergebnis des Master Modules "Mobile Computing 2" an der FH-Erfurt

Es beinhaltet eine Docker - Infrastruktur, welche verwendet wird, um eine Microservice Architektur mit 7 Services zu
realisieren.

- weatherdb (MariaDB)
- stationdb (MariaDB)
- grafana
- jagdwurst (Jaeger Tracer)
- stationapi (Python REST API)
- weatherapi (Python REST API)
- traefik (Load Balancer)

## 1. Voraussetzungen

- Eine Domain (Im Fall des Projektes war es draxento.de)
- Linux Debian 11 oder höher
- Python 3.9

## 2. Installation

Für dieses Projekt gibt es zwei Möglichkeiten, um es zu starten.
Zum einen, die "Out of the box" Ansatz, welcher hier als "Alternativer Ansatz" beschrieben wird.
Zum Zweiten, der präferierte Ansatz "Klonen und Anpassen". Dies bietet eine deutlich höhere Anpassungsmöglichkeit,
gegenüber den ersten Ansatz.

#### Git und Pip

```
sudo apt update && sudo apt install git python3-pip
```

#### Docker

Für die Installation von Docker und Docker Compose eignet sich die Docker eigene
Installationsseite (https://docs.docker.com/engine/install/debian/
und https://docs.docker.com/compose/install/linux/#install-using-the-repository)

### 2.1 Klonen und Anpassen

#### Klonen des Git-Repository

```
git clone https://github.com/fh-erfurt/Cloudy.git
```

#### Wechseln in das geklonte Verzeichnis
```
cd Cloudy
```

#### Editieren der docker-compose.yml

Alle Vorkommnisse von "draxento.de" sind durch die eigene Domain zu ersetzen.

#### Ausführen 
```
docker compose up
```

#### Nach der Installation können Sie die einzelnen Dienste unter den folgenden URLs erreichen:

```
Traefik: http://[Eigene Domain]:8080
Grafana: http://grafana.[Eigene Domain]
Jaeger Tracer: http://tracer.[Eigene Domain]
Station API: http://[Eigene Domain]/station/greeting
Wetter API: http://[Eigene Domain]/weather/greeting
```

### 2.2 Alternativer Ansatz

#### Pullen des fertigen Images für die GitHub Registry

```
docker login ghcr.io && docker pull ghcr.io/fh-erfurt/cloudy:stationapi && docker pull ghcr.io/fh-erfurt/cloudy:weatherapi
```

#### Nach der Installation können Sie die einzelnen Dienste unter den folgenden URLs erreichen:

```
Traefik: http://draxento.de:8080
Grafana: http://grafana.draxento.de
Jaeger Tracer: http://tracer.draxento.de
Station API: http://draxento.de/station/greeting
Wetter API: http://draxento.de/weather/greeting
```