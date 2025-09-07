import React, { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
    const [content, setContent] = useState("");
    const [entries, setEntries] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function fetchEntries() {
        setLoading(true);
        setError("");
        try {
            const res = await fetch(`${API_URL}/api/entries/`);
            const data = await res.json();
            setEntries(data);
        } catch (e) {
            setError("Failed to load entries");
        } finally {
            setLoading(false);
        }
    }

    async function addEntry(e) {
        e.preventDefault();
        if (!content.trim()) return;
        try {
            const res = await fetch(`${API_URL}/api/entries/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content }),
            });
            if (!res.ok) throw new Error("Request failed");
            setContent("");
            await fetchEntries();
        } catch (e) {
            setError("Failed to add entry");
        }
    }

    useEffect(() => {
        fetchEntries();
    }, []);

    return (
        <div
            style={{
                maxWidth: 720,
                margin: "2rem auto",
                fontFamily: "system-ui, sans-serif",
            }}
        >
            <h1>Journal & Mood Tracker</h1>
            <form onSubmit={addEntry} style={{ marginBottom: "1rem" }}>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Write your thoughts..."
                    rows={5}
                    style={{ width: "100%", padding: "0.75rem" }}
                />
                <button
                    type="submit"
                    style={{ padding: "0.5rem 1rem", marginTop: "0.5rem" }}
                >
                    Add Entry
                </button>
            </form>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "crimson" }}>{error}</p>}

            <ul style={{ listStyle: "none", padding: 0 }}>
                {entries.map((e) => (
                    <li
                        key={e.id}
                        style={{
                            padding: "0.75rem 0",
                            borderBottom: "1px solid #eee",
                        }}
                    >
                        <div style={{ whiteSpace: "pre-wrap" }}>
                            {e.content}
                        </div>
                        <small>
                            Created at:{" "}
                            {new Date(e.created_at).toLocaleString()}
                        </small>
                        {e.sentiment && (
                            <div>
                                <small>
                                    Sentiment: {e.sentiment}{" "}
                                    ({e.sentiment_score?.toFixed?.(2)})
                                </small>
                            </div>
                        )}
                        {e.emotions && (
                            <div>
                                <small>Emotions:</small>
                                {Object.entries(e.emotions).map(([label, score]) => (
                                    <div key={label}>
                                        <small style={{ marginLeft: "10px" }}>
                                            {label}: {score.toFixed(2)}
                                        </small>
                                    </div>
                                ))}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
}
