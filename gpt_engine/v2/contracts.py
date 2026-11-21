"""Typed contracts for the GPT v2 data/model boundary.

All internal times are UTC. Source timestamps are separately preserved as
provider-native strings, because some providers publish Eastern or local time.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import hashlib
import json
from typing import Any

VALID_AVAILABILITY = frozenset({
    "confirmed_available", "probable", "questionable", "doubtful", "out", "unknown"
})

def utc(value: str | datetime) -> datetime:
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Naive timestamp forbidden: include UTC offset")
    return value.astimezone(timezone.utc)

def iso(value: str | datetime) -> str:
    return utc(value).isoformat(timespec="seconds").replace("+00:00", "Z")

def display_tip(tip_utc: str, tz_name: str = "Asia/Manila") -> str:
    return utc(tip_utc).astimezone(ZoneInfo(tz_name)).strftime("%Y-%m-%d %I:%M %p %Z")

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()

def internal_id(entity: str, provider: str, provider_id: str) -> str:
    if entity not in ("team", "player", "game", "coach"):
        raise ValueError("Unknown entity kind")
    if not provider or not str(provider_id).strip():
        raise ValueError("Provider and ID required")
    return f"{entity}:{provider}:{str(provider_id).strip()}"

@dataclass(frozen=True)
class Provenance:
    source_id: str
    retrieved_at_utc: str
    source_timestamp: str | None = None
    quality_flags: tuple[str, ...] = ()
    def __post_init__(self):
        if not self.source_id:
            raise ValueError("source_id required")
        object.__setattr__(self, "retrieved_at_utc", iso(self.retrieved_at_utc))

@dataclass(frozen=True)
class GameContext:
    game_id: str
    season: int
    game_date_eastern: str
    tip_utc: str
    home_team_id: str
    away_team_id: str
    neutral_site: bool = False
    def __post_init__(self):
        if self.home_team_id == self.away_team_id:
            raise ValueError("Game must involve different teams")
        object.__setattr__(self, "tip_utc", iso(self.tip_utc))

@dataclass(frozen=True)
class Availability:
    player_id: str
    normalized_status: str
    provider_status: str
    report_utc: str
    source_id: str
    def __post_init__(self):
        if self.normalized_status not in VALID_AVAILABILITY:
            raise ValueError("Provider status not mapped to known enum")
        object.__setattr__(self, "report_utc", iso(self.report_utc))

@dataclass(frozen=True)
class FeatureSnapshot:
    game_id: str
    cutoff_utc: str
    definition_version: str
    features: dict[str, Any]
    missingness: dict[str, Any] = field(default_factory=dict)
    sources: tuple[str, ...] = ()
    quality_flags: tuple[str, ...] = ()
    def __post_init__(self):
        object.__setattr__(self, "cutoff_utc", iso(self.cutoff_utc))
    def stable_id(self) -> str:
        return "snapshot:" + digest({
            "game_id": self.game_id, "cutoff": self.cutoff_utc,
            "version": self.definition_version, "data": self.features
        })[:24]

@dataclass(frozen=True)
class Prediction:
    game_id: str
    snapshot_id: str
    model_version: str
    cutoff_utc: str
    created_at_utc: str
    scenario_label: str
    values: dict[str, Any]
    def __post_init__(self):
        object.__setattr__(self, "cutoff_utc", iso(self.cutoff_utc))
        object.__setattr__(self, "created_at_utc", iso(self.created_at_utc))
        if utc(self.created_at_utc) < utc(self.cutoff_utc):
            raise ValueError("Prediction cannot predate its information cutoff")
    def stable_id(self) -> str:
        return "prediction:" + digest({
            "game": self.game_id, "snapshot": self.snapshot_id,
            "version": self.model_version, "cutoff": self.cutoff_utc,
            "scenario": self.scenario_label
        })[:24]
