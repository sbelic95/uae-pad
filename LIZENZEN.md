# Lizenzen und Quellen

UAE Pad ist ein inoffizielles Fanprojekt für die Flugsimulation. Es ist nicht mit Emirates verbunden und wird nicht von ihr unterstützt.
Name und Logo von Emirates gehören Emirates. Das Logo wird nicht verwendet: das Pad zeigt nur einen eigenen Schriftzug.
Die App-Symbole und Grafiken sind eigene Entwürfe. Code und Aufbau stammen aus dem eigenen Projekt [ASL Pad](https://github.com/sbelic95/asl-pad).

## Mitgelieferte Software und Schriften (`vendor/`)

| Was | Lizenz |
|---|---|
| [Leaflet](https://leafletjs.com) 1.9.4 | BSD-2-Clause, © Volodymyr Agafonkin, CloudMade |
| Roboto, Roboto Condensed | Apache License 2.0 (Google) |
| B612 Mono | SIL Open Font License 1.1 (Airbus, Intactile Design, ENAC) |

## Daten

| Was | Quelle und Lizenz |
|---|---|
| `airports.json` (Koordinaten, Städte, Zeitzonen) | [mwgg/Airports](https://github.com/mwgg/Airports), MIT |
| Stände, Gates, Terminals | © OpenStreetMap-Mitwirkende, [ODbL](https://www.openstreetmap.org/copyright) |
| Pisten | [OurAirports](https://ourairports.com/data/), Public Domain |
| CTAF der US-Flughäfen (`ctaf-us.json`, `tools/build-ctaf.py`) | [OurAirports](https://ourairports.com/data/) airport-frequencies, Public Domain |
| Kartenkacheln | © OpenStreetMap-Mitwirkende, [ODbL](https://www.openstreetmap.org/copyright); Kacheln von tile.openstreetmap.org nach der [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/) |
| `vendor/world.json` (Länder, Küsten, Grenzen der Flugkarte) | [Natural Earth](https://www.naturalearthdata.com) 1:50m, Public Domain; umgewandelt aus [world-atlas](https://github.com/topojson/world-atlas) 2.0.2 (ISC) |
| Flugplan (OFP) | SimBrief (Navigraph) – Daten des eigenen Kontos |
| Netzwerkdaten, METAR, ATIS | VATSIM |
| Luftraumgrenzen und Center-Präfixe (Frequenz-Führer) | [VATSpy Data Project](https://github.com/vatsimnetwork/vatspy-data-project), SimAware TRACON Project (über `vdgs-slot-board`, Zweig `atc`) – jeweilige Projektlizenz |
| ACARS / CPDLC | [Hoppie ACARS](https://www.hoppie.nl/acars/) – mit dem eigenen Logon-Code |
| IVAO-Radar | IVAO Tracker API (`api.ivao.aero/v2/tracker/whazzup`), öffentliche Daten |
| TAF der Wetter-App | [aviationweather.gov](https://aviationweather.gov/data/api/) (NOAA), gemeinfrei |
| NOTAMs im Crew Desk | Aus dem SimBrief-OFP des Piloten |
| Slot-Zeiten | vIFF CDM |
| Stand-Zuweisungen UK | VATSIM UK (über `vdgs-slot-board`) |

Flugplan, Flughäfen und Flotte stammen aus dem vAMSYS-Export von Emirates Virtual (November 2026).
