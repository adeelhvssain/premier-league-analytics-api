import { useEffect, useState } from "react";

const API_SEASON = "2020/21";
const DEFAULT_LIMIT = 10;

function App() {
  const [baseUrl, setBaseUrl] = useState(
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  );
  const [apiKey, setApiKey] = useState("");

  const [teams, setTeams] = useState([]);
  const [players, setPlayers] = useState([]);
  const [topScorers, setTopScorers] = useState([]);
  const [topAssisters, setTopAssisters] = useState([]);
  const [topXg, setTopXg] = useState([]);
  const [teamSummaryTeamId, setTeamSummaryTeamId] = useState("");
  const [clubSummary, setClubSummary] = useState(null);

  const [teamsLoading, setTeamsLoading] = useState(false);
  const [playersLoading, setPlayersLoading] = useState(false);
  const [scorersLoading, setScorersLoading] = useState(false);
  const [assistersLoading, setAssistersLoading] = useState(false);
  const [xgLoading, setXgLoading] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(false);

  const [globalMessage, setGlobalMessage] = useState("");
  const [teamsError, setTeamsError] = useState("");
  const [playersError, setPlayersError] = useState("");
  const [scorersError, setScorersError] = useState("");
  const [assistersError, setAssistersError] = useState("");
  const [xgError, setXgError] = useState("");
  const [summaryError, setSummaryError] = useState("");

  const [teamCreateName, setTeamCreateName] = useState("");
  const [teamCreateShortName, setTeamCreateShortName] = useState("");
  const [teamCreateCity, setTeamCreateCity] = useState("");
  const [teamCreateStadium, setTeamCreateStadium] = useState("");
  const [teamCreateFoundedYear, setTeamCreateFoundedYear] = useState("");
  const [teamActionMessage, setTeamActionMessage] = useState("");
  const [teamActionError, setTeamActionError] = useState("");
  const [editingTeamId, setEditingTeamId] = useState(null);
  const [editingTeam, setEditingTeam] = useState({
    name: "",
    short_name: "",
    city: "",
    stadium: "",
    founded_year: "",
  });

  const [isLoadedOnce, setIsLoadedOnce] = useState(false);

  const sanitizeBaseUrl = (value) => value.trim().replace(/\/+$/, "");

  const teamShortNameById = teams.reduce((acc, team) => {
    acc[team.id] = team.short_name || team.name;
    return acc;
  }, {});

  const getTeamLabel = (teamId) => teamShortNameById[teamId] || "N/A";

  const request = async (path, setter, setLoading, setError) => {
    if (!baseUrl || !apiKey) {
      setError("Please enter both backend base URL and API key.");
      return null;
    }

    setLoading(true);
    setError("");
    try {
      const url = `${sanitizeBaseUrl(baseUrl)}${path}`;
      const response = await fetch(url, {
        headers: {
          "X-API-Key": apiKey,
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        const detail = await response.text().catch(() => "");
        const message = detail || `Request failed with status ${response.status}`;
        throw new Error(message);
      }

      const data = await response.json();
      setter(data);
      return data;
    } catch (error) {
      setError(error.message || "Something went wrong");
      return null;
    } finally {
      setLoading(false);
    }
  };

  const requestJson = async ({ path, method, payload }) => {
    if (!baseUrl || !apiKey) {
      throw new Error("Please enter both backend base URL and API key.");
    }

    const url = `${sanitizeBaseUrl(baseUrl)}${path}`;
    const response = await fetch(url, {
      method,
      headers: {
        "X-API-Key": apiKey,
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: payload ? JSON.stringify(payload) : undefined,
    });

    if (!response.ok) {
      const detail = await response.text().catch(() => "");
      const message = detail || `Request failed with status ${response.status}`;
      throw new Error(message);
    }

    if (response.status === 204) {
      return null;
    }

    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      return null;
    }

    return response.json();
  };

  const loadTeams = async () => {
    await request("/teams", setTeams, setTeamsLoading, setTeamsError);
  };

  const loadAll = async () => {
    setGlobalMessage("");
    setIsLoadedOnce(true);
    await Promise.all([
      loadTeams(),
      request("/players", setPlayers, setPlayersLoading, setPlayersError),
      request(
        `/analytics/top-scorers?season=${encodeURIComponent(API_SEASON)}&limit=${DEFAULT_LIMIT}`,
        setTopScorers,
        setScorersLoading,
        setScorersError,
      ),
      request(
        `/analytics/top-assisters?season=${encodeURIComponent(API_SEASON)}&limit=${DEFAULT_LIMIT}`,
        setTopAssisters,
        setAssistersLoading,
        setAssistersError,
      ),
      request(
        `/analytics/top-xg?season=${encodeURIComponent(API_SEASON)}&limit=${DEFAULT_LIMIT}`,
        setTopXg,
        setXgLoading,
        setXgError,
      ),
    ]);
  };

  const loadClubSummary = async () => {
    if (!teamSummaryTeamId) {
      setSummaryError("Select a team first.");
      return;
    }

    const data = await request(
      `/analytics/club-summary/${teamSummaryTeamId}?season=${encodeURIComponent(API_SEASON)}`,
      setClubSummary,
      setSummaryLoading,
      setSummaryError,
    );

    if (!data) {
      setClubSummary(null);
    }
  };

  const clearTeamForm = () => {
    setTeamCreateName("");
    setTeamCreateShortName("");
    setTeamCreateCity("");
    setTeamCreateStadium("");
    setTeamCreateFoundedYear("");
  };

  const startEditTeam = (team) => {
    setEditingTeamId(team.id);
    setEditingTeam({
      name: team.name || "",
      short_name: team.short_name || "",
      city: team.city || "",
      stadium: team.stadium || "",
      founded_year: team.founded_year ? String(team.founded_year) : "",
    });
  };

  const cancelEditTeam = () => {
    setEditingTeamId(null);
    setEditingTeam({
      name: "",
      short_name: "",
      city: "",
      stadium: "",
      founded_year: "",
    });
  };

  const buildTeamPayload = (value, includeFoundedYear = true) => {
    const payload = {};

    if (value.name.trim()) {
      payload.name = value.name.trim();
    }

    if (value.short_name.trim()) {
      payload.short_name = value.short_name.trim();
    }

    if (value.city.trim()) {
      payload.city = value.city.trim();
    }

    if (value.stadium.trim()) {
      payload.stadium = value.stadium.trim();
    }

    if (includeFoundedYear && value.founded_year !== "") {
      const parsed = Number.parseInt(value.founded_year, 10);
      if (!Number.isNaN(parsed)) {
        payload.founded_year = parsed;
      }
    }

    return payload;
  };

  const handleCreateTeam = async (event) => {
    event.preventDefault();
    setTeamActionMessage("");
    setTeamActionError("");

    const payload = buildTeamPayload(
      {
        name: teamCreateName,
        short_name: teamCreateShortName,
        city: teamCreateCity,
        stadium: teamCreateStadium,
        founded_year: teamCreateFoundedYear,
      },
      true,
    );

    try {
      await requestJson({
        path: "/teams",
        method: "POST",
        payload,
      });
      await loadTeams();
      clearTeamForm();
      setTeamActionMessage("Team created successfully.");
    } catch (error) {
      setTeamActionError(error.message || "Failed to create team.");
    }
  };

  const handleUpdateTeam = async (teamId) => {
    setTeamActionMessage("");
    setTeamActionError("");

    const payload = buildTeamPayload(editingTeam, true);

    try {
      await requestJson({
        path: `/teams/${teamId}`,
        method: "PUT",
        payload,
      });
      await loadTeams();
      cancelEditTeam();
      setTeamActionMessage("Team updated successfully.");
    } catch (error) {
      setTeamActionError(error.message || "Failed to update team.");
    }
  };

  const handleDeleteTeam = async (teamId, teamName) => {
    if (!window.confirm(`Delete ${teamName}?`)) {
      return;
    }

    setTeamActionMessage("");
    setTeamActionError("");

    try {
      await requestJson({
        path: `/teams/${teamId}`,
        method: "DELETE",
      });
      await loadTeams();
      setTeamActionMessage("Team deleted successfully.");
    } catch (error) {
      setTeamActionError(error.message || "Failed to delete team.");
    }
  };

  useEffect(() => {
    if (teams.length > 0 && !teamSummaryTeamId) {
      setTeamSummaryTeamId(String(teams[0].id));
    }
  }, [teams, teamSummaryTeamId]);

  useEffect(() => {
    if (apiKey && baseUrl) {
      loadAll();
    }
  }, []);

  return (
    <div className="pl-app">
      <div className="top-shell">
        <div className="top-nav">
          <div className="brand">Premier League Analytics</div>
        </div>
      </div>

      <header className="hero">
        <div className="hero-inner">
          <p className="hero-kicker">Stats Centre</p>
          <h1>Premier League Player Stats</h1>
        </div>
      </header>

      <main className="page">
        <section className="card config-card">
          <h2>API Settings</h2>
          <div className="field-grid">
            <label>
              Backend Base URL
              <input
                value={baseUrl}
                onChange={(event) => setBaseUrl(event.target.value)}
                placeholder="http://127.0.0.1:8000"
              />
            </label>
            <label>
              API Key
              <input
                value={apiKey}
                onChange={(event) => setApiKey(event.target.value)}
                placeholder="Enter X-API-Key"
              />
            </label>
          </div>
          <button type="button" onClick={loadAll}>
            Load Dashboard
          </button>
          {globalMessage && <p className="error">{globalMessage}</p>}
        </section>

        <section className="card">
          <h2>Create Team</h2>
          <form onSubmit={handleCreateTeam} className="team-form">
            <div className="field-grid two-col">
              <label>
                Name
                <input
                  value={teamCreateName}
                  onChange={(event) => setTeamCreateName(event.target.value)}
                  required
                />
              </label>
              <label>
                Short Name
                <input
                  value={teamCreateShortName}
                  onChange={(event) => setTeamCreateShortName(event.target.value)}
                  required
                />
              </label>
              <label>
                City
                <input
                  value={teamCreateCity}
                  onChange={(event) => setTeamCreateCity(event.target.value)}
                />
              </label>
              <label>
                Stadium
                <input
                  value={teamCreateStadium}
                  onChange={(event) => setTeamCreateStadium(event.target.value)}
                />
              </label>
              <label>
                Founded Year
                <input
                  value={teamCreateFoundedYear}
                  onChange={(event) => setTeamCreateFoundedYear(event.target.value)}
                  type="number"
                  min="1800"
                  max="2100"
                />
              </label>
            </div>
            <button type="submit">Create Team</button>
          </form>
          {teamActionMessage && <p className="status">{teamActionMessage}</p>}
          {teamActionError && <p className="error">{teamActionError}</p>}
        </section>

        <section className="card">
          <h2>Teams</h2>
          {teamsLoading && <p className="status">Loading teams...</p>}
          {teamsError && <p className="error">{teamsError}</p>}
          {!teamsLoading && !teamsError && teams.length === 0 && isLoadedOnce && (
            <p className="status">No teams found.</p>
          )}
          <ul className="list chip-list">
            {teams.map((team) => (
              <li key={team.id} className="team-row">
                <span className="item-main">{team.name}</span>
                <span className="team-pill">{team.short_name || team.name}</span>
                {editingTeamId === team.id ? (
                  <div className="row-actions edit-grid">
                    <input
                      value={editingTeam.name}
                      onChange={(event) =>
                        setEditingTeam((prev) => ({
                          ...prev,
                          name: event.target.value,
                        }))
                      }
                    />
                    <input
                      value={editingTeam.short_name}
                      onChange={(event) =>
                        setEditingTeam((prev) => ({
                          ...prev,
                          short_name: event.target.value,
                        }))
                      }
                    />
                    <input
                      value={editingTeam.city}
                      onChange={(event) =>
                        setEditingTeam((prev) => ({
                          ...prev,
                          city: event.target.value,
                        }))
                      }
                    />
                    <input
                      value={editingTeam.stadium}
                      onChange={(event) =>
                        setEditingTeam((prev) => ({
                          ...prev,
                          stadium: event.target.value,
                        }))
                      }
                    />
                    <input
                      value={editingTeam.founded_year}
                      type="number"
                      onChange={(event) =>
                        setEditingTeam((prev) => ({
                          ...prev,
                          founded_year: event.target.value,
                        }))
                      }
                    />
                    <div className="row-buttons">
                      <button type="button" onClick={() => handleUpdateTeam(team.id)}>
                        Save
                      </button>
                      <button type="button" className="secondary" onClick={cancelEditTeam}>
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    {team.is_user_created && (
                      <div className="row-actions">
                        <button type="button" onClick={() => startEditTeam(team)}>
                          Update
                        </button>
                        <button
                          type="button"
                          className="danger"
                          onClick={() => handleDeleteTeam(team.id, team.name)}
                        >
                          Delete
                        </button>
                      </div>
                    )}
                  </>
                )}
              </li>
            ))}
          </ul>
        </section>

        <section className="stats-grid">
          <section className="card stat-card">
            <h2>Top Scorers (2020/21)</h2>
            {scorersLoading && <p className="status">Loading top scorers...</p>}
            {scorersError && <p className="error">{scorersError}</p>}
            {!scorersLoading && !scorersError && topScorers.length === 0 && isLoadedOnce && (
              <p className="status">No scorer records found.</p>
            )}
            <ol className="list">
              {topScorers.map((row) => (
                <li key={row.player_id || row.player_name}>
                  <span className="item-main">{row.player_name}</span>
                  <span className="team-pill">
                    {row.club_name || row.team_name || row.team || getTeamLabel(row.team_id) || "Team N/A"}
                  </span>
                  <span className="metric">{row.goals} goals</span>
                </li>
              ))}
            </ol>
          </section>

          <section className="card stat-card">
            <h2>Top Assisters (2020/21)</h2>
            {assistersLoading && <p className="status">Loading top assisters...</p>}
            {assistersError && <p className="error">{assistersError}</p>}
            {!assistersLoading && !assistersError && topAssisters.length === 0 && isLoadedOnce && (
              <p className="status">No assister records found.</p>
            )}
            <ol className="list">
              {topAssisters.map((row) => (
                <li key={row.player_id || row.player_name}>
                  <span className="item-main">{row.player_name}</span>
                  <span className="team-pill">
                    {row.club_name || row.team_name || row.team || getTeamLabel(row.team_id) || "Team N/A"}
                  </span>
                  <span className="metric">{row.assists} assists</span>
                </li>
              ))}
            </ol>
          </section>

          <section className="card stat-card">
            <h2>Top xG (2020/21)</h2>
            {xgLoading && <p className="status">Loading top xG...</p>}
            {xgError && <p className="error">{xgError}</p>}
            {!xgLoading && !xgError && topXg.length === 0 && isLoadedOnce && (
              <p className="status">No xG records found.</p>
            )}
            <ol className="list">
              {topXg.map((row) => (
                <li key={row.player_id || row.player_name}>
                  <span className="item-main">{row.player_name}</span>
                  <span className="team-pill">
                    {row.club_name || row.team_name || row.team || getTeamLabel(row.team_id) || "Team N/A"}
                  </span>
                  <span className="metric">{row.xg} xG</span>
                </li>
              ))}
            </ol>
          </section>
        </section>

        <section className="card">
          <h2>Players</h2>
          {playersLoading && <p className="status">Loading players...</p>}
          {playersError && <p className="error">{playersError}</p>}
          {!playersLoading && !playersError && players.length === 0 && isLoadedOnce && (
            <p className="status">No players found.</p>
          )}
          <div className="scroll-list">
            <ul className="list">
              {players.map((player) => (
                <li key={player.id}>
                  <span className="item-main">{player.name}</span>
                  <span className="item-sub">{player.position || "Position N/A"}</span>
                  <span className="team-pill">{getTeamLabel(player.team_id)}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="card">
          <h2>Club Summary</h2>
          {teams.length === 0 ? (
            <p className="status">Load teams first to choose a club.</p>
          ) : (
            <label>
              Select team
              <select
                value={teamSummaryTeamId}
                onChange={(event) => setTeamSummaryTeamId(event.target.value)}
              >
                {teams.map((team) => (
                  <option key={team.id} value={String(team.id)}>
                    {team.name}
                  </option>
                ))}
              </select>
            </label>
          )}
          <button type="button" onClick={loadClubSummary} disabled={!teamSummaryTeamId}>
            Load Club Summary
          </button>
          {summaryLoading && <p className="status">Loading club summary...</p>}
          {summaryError && <p className="error">{summaryError}</p>}
          {clubSummary && !summaryLoading && (
            <div className="summary-grid">
              <p>
                <strong>Team:</strong> {clubSummary.team_name}
              </p>
              <p>
                <strong>Players:</strong> {clubSummary.player_count}
              </p>
              <p>
                <strong>Total Goals:</strong> {clubSummary.total_goals}
              </p>
              <p>
                <strong>Total Assists:</strong> {clubSummary.total_assists}
              </p>
              <p>
                <strong>Total xG:</strong> {clubSummary.total_xg}
              </p>
              <p>
                <strong>Total xA:</strong> {clubSummary.total_xa}
              </p>
              <p>
                <strong>Total Yellow Cards:</strong> {clubSummary.total_yellow_cards}
              </p>
              <p>
                <strong>Total Red Cards:</strong> {clubSummary.total_red_cards}
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
