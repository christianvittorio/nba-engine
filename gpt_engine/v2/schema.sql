-- GPT NBA engine v2: normalized, timestamped, point-in-time auditable data model.
-- UTC timestamps are ISO-8601 with Z or explicit +00:00 offset. The caller
-- validates normalization before writes. Source-local timestamps are retained
-- verbatim in *_source_timestamp fields when present.
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS schema_migrations (
 version INTEGER PRIMARY KEY,
 applied_at_utc TEXT NOT NULL,
 description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sources (
 source_id TEXT PRIMARY KEY,
 label TEXT NOT NULL,
 upstream_uri TEXT,
 license_notes TEXT,
 created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS teams (
 team_id TEXT PRIMARY KEY,
 current_name TEXT,
 active INTEGER NOT NULL DEFAULT 1,
 created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS players (
 player_id TEXT PRIMARY KEY,
 canonical_name TEXT,
 rookie_season INTEGER,
 created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS provider_ids (
 entity_type TEXT NOT NULL CHECK(entity_type IN ('team','player','game','coach')),
 internal_id TEXT NOT NULL,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 provider_id TEXT NOT NULL,
 observed_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 PRIMARY KEY(entity_type, source_id, provider_id),
 UNIQUE(entity_type, internal_id, source_id)
);
CREATE INDEX IF NOT EXISTS idx_provider_lookup ON provider_ids(entity_type,internal_id);
CREATE TABLE IF NOT EXISTS coaches (
 coach_id TEXT PRIMARY KEY,
 coach_name TEXT NOT NULL,
 created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS coach_tenures (
 tenure_id INTEGER PRIMARY KEY,
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 coach_id TEXT NOT NULL REFERENCES coaches(coach_id),
 role TEXT NOT NULL,
 valid_from_utc TEXT,
 valid_to_utc TEXT,
 season INTEGER,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json))
);
CREATE INDEX IF NOT EXISTS idx_coach_tenures ON coach_tenures(team_id,valid_from_utc,valid_to_utc);

CREATE TABLE IF NOT EXISTS roster_assignments (
 assignment_id INTEGER PRIMARY KEY,
 player_id TEXT NOT NULL REFERENCES players(player_id),
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 season INTEGER NOT NULL,
 valid_from_utc TEXT,
 valid_to_utc TEXT,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 published_position TEXT,
 role_label TEXT,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 UNIQUE(player_id,team_id,season,valid_from_utc)
);
CREATE INDEX IF NOT EXISTS idx_roster_effective ON roster_assignments(player_id,valid_from_utc,valid_to_utc);

CREATE TABLE IF NOT EXISTS games (
 game_id TEXT PRIMARY KEY,
 season INTEGER NOT NULL,
 game_date_eastern TEXT NOT NULL,
 tip_utc TEXT,
 home_team_id TEXT NOT NULL REFERENCES teams(team_id),
 away_team_id TEXT NOT NULL REFERENCES teams(team_id),
 game_type TEXT NOT NULL DEFAULT 'regular_season',
 neutral_site INTEGER NOT NULL DEFAULT 0,
 status TEXT NOT NULL CHECK(status IN ('scheduled','in_progress','final','postponed','cancelled','unknown')),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 CHECK(home_team_id <> away_team_id)
);
CREATE INDEX IF NOT EXISTS idx_games_tip ON games(tip_utc);
CREATE INDEX IF NOT EXISTS idx_games_season ON games(season,game_date_eastern);

CREATE TABLE IF NOT EXISTS team_game_stats (
 game_id TEXT NOT NULL REFERENCES games(game_id),
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 season INTEGER NOT NULL,
 stats_json TEXT NOT NULL CHECK(json_valid(stats_json)),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 PRIMARY KEY(game_id,team_id,source_id)
);
CREATE TABLE IF NOT EXISTS player_game_stats (
 game_id TEXT NOT NULL REFERENCES games(game_id),
 player_id TEXT NOT NULL REFERENCES players(player_id),
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 season INTEGER NOT NULL,
 stats_json TEXT NOT NULL CHECK(json_valid(stats_json)),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 PRIMARY KEY(game_id,player_id,team_id,source_id)
);
CREATE INDEX IF NOT EXISTS idx_player_history ON player_game_stats(player_id,game_id);

CREATE TABLE IF NOT EXISTS play_by_play (
 game_id TEXT NOT NULL REFERENCES games(game_id),
 action_id TEXT NOT NULL,
 event_utc TEXT,
 period INTEGER,
 clock_seconds REAL,
 team_id TEXT REFERENCES teams(team_id),
 player_id TEXT REFERENCES players(player_id),
 event_type TEXT NOT NULL,
 event_json TEXT NOT NULL CHECK(json_valid(event_json)),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 PRIMARY KEY(game_id,action_id,source_id)
);
CREATE TABLE IF NOT EXISTS tracking_matchups (
 game_id TEXT NOT NULL REFERENCES games(game_id),
 observation_id TEXT NOT NULL,
 offensive_player_id TEXT REFERENCES players(player_id),
 defensive_player_id TEXT REFERENCES players(player_id),
 offensive_team_id TEXT REFERENCES teams(team_id),
 defensive_team_id TEXT REFERENCES teams(team_id),
 observed_position TEXT,
 partial_possessions REAL,
 minutes REAL,
 stats_json TEXT NOT NULL CHECK(json_valid(stats_json)),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 PRIMARY KEY(game_id,observation_id,source_id)
);
CREATE INDEX IF NOT EXISTS idx_tracking_def ON tracking_matchups(defensive_team_id,observed_position);

CREATE TABLE IF NOT EXISTS availability_reports (
 report_id TEXT PRIMARY KEY,
 game_id TEXT NOT NULL REFERENCES games(game_id),
 player_id TEXT NOT NULL REFERENCES players(player_id),
 provider_status TEXT NOT NULL,
 normalized_status TEXT NOT NULL CHECK(normalized_status IN
 ('confirmed_available','probable','questionable','doubtful','out','unknown')),
 is_confirmed INTEGER NOT NULL DEFAULT 0,
 report_utc TEXT NOT NULL,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json))
);
CREATE INDEX IF NOT EXISTS idx_availability_asof ON availability_reports(game_id,player_id,report_utc);
CREATE TABLE IF NOT EXISTS lineup_reports (
 lineup_id TEXT PRIMARY KEY,
 game_id TEXT NOT NULL REFERENCES games(game_id),
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 player_id TEXT NOT NULL REFERENCES players(player_id),
 lineup_type TEXT NOT NULL CHECK(lineup_type IN ('confirmed_starter','projected_starter','rotation','out')),
 confirmation_utc TEXT NOT NULL,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json))
);
CREATE INDEX IF NOT EXISTS idx_lineups_asof ON lineup_reports(game_id,team_id,confirmation_utc);
CREATE TABLE IF NOT EXISTS rotation_stints (
 game_id TEXT NOT NULL REFERENCES games(game_id),
 player_id TEXT NOT NULL REFERENCES players(player_id),
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 stint_index INTEGER NOT NULL,
 in_elapsed_seconds REAL NOT NULL,
 out_elapsed_seconds REAL NOT NULL,
 on_court_points_for INTEGER,
 on_court_points_against INTEGER,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 PRIMARY KEY(game_id,player_id,stint_index,source_id)
);

CREATE TABLE IF NOT EXISTS model_versions (
 model_version TEXT PRIMARY KEY,
 created_at_utc TEXT NOT NULL,
 code_commit_sha TEXT,
 architecture TEXT NOT NULL,
 config_json TEXT NOT NULL CHECK(json_valid(config_json)),
 training_cutoff_utc TEXT,
 training_manifest_hash TEXT,
 notes TEXT
);
CREATE TABLE IF NOT EXISTS experiment_runs (
 experiment_id TEXT PRIMARY KEY,
 model_version TEXT NOT NULL REFERENCES model_versions(model_version),
 started_at_utc TEXT NOT NULL,
 finished_at_utc TEXT,
 train_start_utc TEXT,
 train_end_utc TEXT,
 validation_start_utc TEXT,
 validation_end_utc TEXT,
 test_start_utc TEXT,
 test_end_utc TEXT,
 hyperparams_json TEXT NOT NULL CHECK(json_valid(hyperparams_json)),
 metrics_json TEXT CHECK(json_valid(metrics_json)),
 random_seed INTEGER,
 status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS feature_snapshots (
 snapshot_id TEXT PRIMARY KEY,
 game_id TEXT NOT NULL REFERENCES games(game_id),
 cutoff_utc TEXT NOT NULL,
 generated_at_utc TEXT NOT NULL,
 definition_version TEXT NOT NULL,
 features_json TEXT NOT NULL CHECK(json_valid(features_json)),
 source_max_timestamp_utc TEXT,
 source_manifest_hash TEXT,
 missingness_json TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(missingness_json)),
 source_ids_json TEXT NOT NULL CHECK(json_valid(source_ids_json)),
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 UNIQUE(game_id,cutoff_utc,definition_version)
);
CREATE INDEX IF NOT EXISTS idx_feature_asof ON feature_snapshots(game_id,cutoff_utc);

CREATE TABLE IF NOT EXISTS pregame_predictions (
 prediction_id TEXT PRIMARY KEY,
 game_id TEXT NOT NULL REFERENCES games(game_id),
 snapshot_id TEXT NOT NULL REFERENCES feature_snapshots(snapshot_id),
 model_version TEXT NOT NULL REFERENCES model_versions(model_version),
 experiment_id TEXT REFERENCES experiment_runs(experiment_id),
 cutoff_utc TEXT NOT NULL,
 created_at_utc TEXT NOT NULL,
 prediction_json TEXT NOT NULL CHECK(json_valid(prediction_json)),
 scenario_label TEXT NOT NULL DEFAULT 'base',
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json)),
 UNIQUE(game_id,model_version,cutoff_utc,scenario_label)
);
CREATE TABLE IF NOT EXISTS simulation_summaries (
 simulation_id TEXT PRIMARY KEY,
 prediction_id TEXT NOT NULL REFERENCES pregame_predictions(prediction_id),
 seed INTEGER NOT NULL,
 simulation_count INTEGER NOT NULL CHECK(simulation_count >= 50),
 batch_size INTEGER NOT NULL CHECK(batch_size > 0),
 parameters_json TEXT NOT NULL CHECK(json_valid(parameters_json)),
 summary_json TEXT NOT NULL CHECK(json_valid(summary_json)),
 sample_error_json TEXT NOT NULL CHECK(json_valid(sample_error_json)),
 created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS actual_results (
 game_id TEXT PRIMARY KEY REFERENCES games(game_id),
 season INTEGER NOT NULL,
 home_score INTEGER NOT NULL,
 away_score INTEGER NOT NULL,
 player_totals_json TEXT CHECK(json_valid(player_totals_json)),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 finalized_at_utc TEXT,
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json))
);
CREATE TABLE IF NOT EXISTS forecast_evaluations (
 evaluation_id TEXT PRIMARY KEY,
 prediction_id TEXT NOT NULL REFERENCES pregame_predictions(prediction_id),
 game_id TEXT NOT NULL REFERENCES games(game_id),
 evaluated_at_utc TEXT NOT NULL,
 actual_source_id TEXT NOT NULL REFERENCES sources(source_id),
 metrics_json TEXT NOT NULL CHECK(json_valid(metrics_json)),
 evaluator_version TEXT NOT NULL,
 UNIQUE(prediction_id,evaluator_version)
);
CREATE TABLE IF NOT EXISTS market_snapshots (
 market_id TEXT PRIMARY KEY,
 game_id TEXT NOT NULL REFERENCES games(game_id),
 player_id TEXT REFERENCES players(player_id),
 provider_market_id TEXT,
 market_type TEXT NOT NULL,
 selection TEXT,
 line REAL,
 american_odds INTEGER,
 decimal_odds REAL,
 observed_at_utc TEXT NOT NULL,
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 source_timestamp TEXT,
 retrieved_at_utc TEXT NOT NULL,
 quality_flags_json TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(quality_flags_json))
);
CREATE INDEX IF NOT EXISTS idx_markets_asof ON market_snapshots(game_id,observed_at_utc);
CREATE TABLE IF NOT EXISTS season_simulations (
 season_run_id TEXT PRIMARY KEY,
 season INTEGER NOT NULL,
 cutoff_utc TEXT NOT NULL,
 model_version TEXT NOT NULL REFERENCES model_versions(model_version),
 simulation_count INTEGER NOT NULL CHECK(simulation_count >= 50),
 seed INTEGER NOT NULL,
 inputs_hash TEXT NOT NULL,
 generated_at_utc TEXT NOT NULL,
 assumptions_json TEXT NOT NULL CHECK(json_valid(assumptions_json))
);
CREATE TABLE IF NOT EXISTS season_standings_distributions (
 season_run_id TEXT NOT NULL REFERENCES season_simulations(season_run_id),
 team_id TEXT NOT NULL REFERENCES teams(team_id),
 wins_mean REAL,
 wins_q10 REAL,
 wins_q50 REAL,
 wins_q90 REAL,
 playoffs_probability REAL,
 seed_probability REAL,
 finals_probability REAL,
 championship_probability REAL,
 distribution_json TEXT NOT NULL CHECK(json_valid(distribution_json)),
 PRIMARY KEY(season_run_id,team_id)
);

-- Predictions and their snapshots are immutable. Superseding predictions
-- must receive a new cutoff/version/scenario, never overwrite a past claim.
CREATE TRIGGER IF NOT EXISTS immutable_prediction_update
BEFORE UPDATE ON pregame_predictions BEGIN
 SELECT RAISE(ABORT,'pregame prediction is immutable');
END;
CREATE TRIGGER IF NOT EXISTS immutable_prediction_delete
BEFORE DELETE ON pregame_predictions BEGIN
 SELECT RAISE(ABORT,'pregame prediction is immutable');
END;
CREATE TRIGGER IF NOT EXISTS immutable_snapshot_update
BEFORE UPDATE ON feature_snapshots BEGIN
 SELECT RAISE(ABORT,'feature snapshot is immutable');
END;
CREATE TRIGGER IF NOT EXISTS immutable_snapshot_delete
BEFORE DELETE ON feature_snapshots BEGIN
 SELECT RAISE(ABORT,'feature snapshot is immutable');
END;
CREATE TRIGGER IF NOT EXISTS guard_prediction_cutoff
BEFORE INSERT ON pregame_predictions
BEGIN
 SELECT CASE
 WHEN NEW.cutoff_utc <> (SELECT cutoff_utc FROM feature_snapshots WHERE snapshot_id=NEW.snapshot_id)
 THEN RAISE(ABORT,'prediction cutoff must match feature snapshot')
 WHEN NEW.game_id <> (SELECT game_id FROM feature_snapshots WHERE snapshot_id=NEW.snapshot_id)
 THEN RAISE(ABORT,'prediction game must match feature snapshot')
 WHEN EXISTS(SELECT 1 FROM games WHERE game_id=NEW.game_id AND tip_utc IS NOT NULL
 AND NEW.cutoff_utc >= tip_utc) THEN RAISE(ABORT,'prediction cutoff must be before tipoff')
 END;
END;
