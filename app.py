import os
from datetime import date, timedelta
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

API_KEY = os.getenv("APIFOOTBALL_KEY", "").strip()
API_BASE = "https://v3.football.api-sports.io"

app = FastAPI(title="FOOT ANALYTICS PRO", version="2.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("static/index.html")

async def api_get(path: str, params: dict):
    if not API_KEY:
        raise HTTPException(status_code=503, detail="API non configurée. Ajoutez APIFOOTBALL_KEY dans les variables d'environnement du serveur.")
    headers = {"x-apisports-key": API_KEY}
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.get(f"{API_BASE}/{path}", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            raise HTTPException(status_code=502, detail={"message": "Erreur du fournisseur football", "errors": data["errors"]})
        return data.get("response", [])
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Fournisseur football : HTTP {e.response.status_code}")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Impossible de joindre le fournisseur football pour le moment.")

@app.get("/api/status")
async def status():
    return {"ok": True, "api_configured": bool(API_KEY), "provider": "API-Football", "version": "2.0.0"}

@app.get("/api/fixtures")
async def fixtures(day: date = Query(default_factory=date.today), league: Optional[int] = None, search: Optional[str] = None):
    params = {"date": day.isoformat(), "timezone": "Africa/Porto-Novo"}
    if league:
        params["league"] = league
        params["season"] = day.year if day.month >= 7 else day.year - 1
    items = await api_get("fixtures", params)
    output = []
    needle = (search or "").strip().lower()
    for x in items:
        f = x.get("fixture", {})
        t = x.get("teams", {})
        home = t.get("home", {}).get("name", "Domicile")
        away = t.get("away", {}).get("name", "Extérieur")
        if needle and needle not in home.lower() and needle not in away.lower():
            continue
        output.append({
            "id": f.get("id"), "date": f.get("date"), "timestamp": f.get("timestamp"),
            "status": f.get("status", {}).get("long"), "short": f.get("status", {}).get("short"),
            "league": x.get("league", {}).get("name"), "country": x.get("league", {}).get("country"),
            "home": home, "away": away,
            "home_goals": (x.get("goals") or {}).get("home"), "away_goals": (x.get("goals") or {}).get("away")
        })
    return {"date": day.isoformat(), "count": len(output), "fixtures": output}

@app.get("/api/search")
async def search_fixtures(q: str = Query(min_length=2, max_length=80), day: date = Query(default_factory=date.today)):
    return await fixtures(day=day, search=q)

@app.get("/api/team-last")
async def team_last(team_id: int, last: int = Query(default=10, ge=1, le=20)):
    items = await api_get("fixtures", {"team": team_id, "last": last, "timezone": "Africa/Porto-Novo"})
    out = []
    for x in items:
        f, t, goals = x.get("fixture", {}), x.get("teams", {}), x.get("goals", {})
        out.append({
            "date": f.get("date"), "competition": (x.get("league") or {}).get("name"),
            "home": (t.get("home") or {}).get("name"), "away": (t.get("away") or {}).get("name"),
            "home_goals": goals.get("home"), "away_goals": goals.get("away"),
            "status": (f.get("status") or {}).get("long")
        })
    return {"team_id": team_id, "count": len(out), "matches": out}

@app.get("/api/teams")
async def teams(search: str = Query(min_length=2, max_length=80), league: Optional[int] = None, season: Optional[int] = None):
    params = {"search": search}
    if league: params["league"] = league
    if season: params["season"] = season
    items = await api_get("teams", params)
    return [{"id": x.get("team", {}).get("id"), "name": x.get("team", {}).get("name"), "country": (x.get("team", {}).get("country"))} for x in items]

@app.get("/api/team-statistics")
async def team_statistics(team_id: int, league: int, season: int):
    items = await api_get("teams/statistics", {"team": team_id, "league": league, "season": season})
    return items[0] if items else {}
