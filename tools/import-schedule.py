#!/usr/bin/env python3
"""Emirates Virtual schedule → UAE Pad.

Reads the vAMSYS import files of the VA (CSV) and writes the pad's network files:
  va/routes.json  airports, routes (both ways, with the types flown) and every scheduled flight
  va/fleet.json   every aircraft with registration and type

    python3 tools/import-schedule.py <folder with the CSVs>

Expected files in the folder (the month in the name may change):
  UAE_Passenger_Schedule_*.csv, UAE_Cargo_Schedule_*.csv (optional), UAE_airports_*.csv, UAE_fleet_*.csv, UAE_Aircraft_*.csv
Times in the schedule are UTC, as in vAMSYS. Run it again whenever the VA publishes a new schedule.
"""
import csv, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def one(folder, pattern):
    hits = sorted(glob.glob(os.path.join(folder, pattern)))
    if not hits:
        sys.exit("missing " + pattern + " in " + folder)
    return hits[-1]

def rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main(folder):
    sched, apts, fleet, acs = (one(folder, p) for p in ("UAE_Passenger_Schedule_*.csv", "UAE_airports_*.csv", "UAE_fleet_*.csv", "UAE_Aircraft_*.csv"))
    db = json.load(open(os.path.join(ROOT, "airports.json"), encoding="utf-8"))  # [lat, lon, city, tz] by ICAO
    old = {}
    try:
        old = json.load(open(os.path.join(ROOT, "va", "routes.json"), encoding="utf-8")).get("airports", {})
    except Exception:
        pass
    type_of = {r["Name"].strip(): r["Type Code"].strip() for r in rows(fleet)}

    airports = {}
    for r in rows(apts):
        icao = r["ICAO/IATA"].strip().upper()
        d = db.get(icao)
        if not d:
            print("not in airports.json, skipped:", icao)
            continue
        city = old.get(icao, {}).get("name") or (d[2] or "").replace("-", " ") or r["Name"].strip()
        airports[icao] = {"name": city, "full": r["Name"].strip(), "lat": round(d[0], 2), "lon": round(d[1], 2)}

    flights, pairs = [], {}
    cargo = sorted(glob.glob(os.path.join(folder, "UAE_Cargo_Schedule_*.csv")))
    all_rows = [(r, False) for r in rows(sched)] + [(r, True) for r in (rows(cargo[-1]) if cargo else [])]
    for r, is_cargo in all_rows:
        if r.get("Is Hidden", "").upper() == "TRUE" or r.get("_delete", "").upper() == "TRUE":
            continue
        dep, arr = r["Departure Airport (ICAO/IATA)"].strip().upper(), r["Arrival Airport (ICAO/IATA)"].strip().upper()
        if dep not in airports or arr not in airports:
            print("airport missing, flight skipped:", r["Flight Number"], dep, arr)
            continue
        fleet_name = r["Fleet IDs"].split("@")[0].strip()
        typ = type_of.get(fleet_name, "")
        days = sorted({DAYS.index(x.strip().lower()) + 1 for x in r["Service Days"].split(",") if x.strip().lower() in DAYS})
        rem = r.get("Remarks", "").strip()
        term = gate = ""
        for part in rem.split("|"):
            p = part.strip()
            if p.lower().startswith("departure terminal"):
                term = p[len("departure terminal"):].strip()
            elif p.lower().startswith("departure gate"):
                gate = p[len("departure gate"):].strip()
        flights.append({"no": r["Flight Number"].strip(), "cs": r["Callsign"].strip(), "dep": dep, "arr": arr,
                        "std": r["Departure Time (HH:MM)"].strip(), "sta": r["Arrival Time (HH:MM)"].strip(),
                        "blk": r["Flight Length (HH:MM)"].strip(), "nm": int(r["Flight Distance (NM)"] or 0) or None,
                        "days": days, "type": typ, "fleet": fleet_name, "term": term, "gate": gate, **({"cargo": True} if is_cargo else {})})
        key = tuple(sorted((dep, arr)))
        pairs.setdefault(key, set()).add(typ)

    order = ["A388", "B77W", "B77L", "A359"]
    routes = [{"from": a, "to": b, "types": sorted(t for t in ts if t) or ["B77W"]} for (a, b), ts in sorted(pairs.items())]
    for r in routes:
        r["types"].sort(key=lambda t: order.index(t) if t in order else 99)
    flights.sort(key=lambda f: (f["dep"] != "OMDB", f["dep"], f["std"], f["no"]))
    used = {f["dep"] for f in flights} | {f["arr"] for f in flights}
    out = {
        "_help": "Emirates Virtual schedule (vAMSYS import, passenger and cargo). Do not edit by hand – run: python3 tools/import-schedule.py <folder with the CSVs>. Times are UTC.",
        "proposal": False, "source": os.path.basename(sched), "base": "OMDB",
        "airports": {k: v for k, v in sorted(airports.items()) if k in used},
        "routes": routes, "flights": flights,
    }
    json.dump(out, open(os.path.join(ROOT, "va", "routes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    aircraft = []
    for r in rows(acs):
        if r.get("_delete", "").upper() == "TRUE":
            continue
        name = r["Name"].strip()
        aircraft.append({"reg": r["Registration"].strip().upper(), "type": type_of.get(name, ""), "name": name, "selcal": r.get("SELCAL", "").strip()})
    aircraft.sort(key=lambda a: (order.index(a["type"]) if a["type"] in order else 99, a["reg"]))
    json.dump({"_help": "Emirates Virtual fleet (vAMSYS import). Run tools/import-schedule.py for a new version.",
               "source": os.path.basename(acs), "aircraft": aircraft},
              open(os.path.join(ROOT, "va", "fleet.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(flights), "flights,", len(routes), "routes,", len(out["airports"]), "airports,", len(aircraft), "aircraft")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
