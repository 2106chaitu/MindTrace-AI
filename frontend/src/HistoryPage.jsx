import { useEffect, useMemo, useState } from "react";

import { fetchAnalysisHistory } from "./api";

function riskCategory(riskLevel) {
  const value = String(riskLevel ?? "").toLowerCase();
  if (["high", "elevated"].includes(value)) return "high";
  if (["medium", "moderate"].includes(value)) return "medium";
  return "low";
}

function formatDateTime(timestamp) {
  const date = new Date(timestamp);
  return {
    date: date.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" }),
    time: date.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" })
  };
}

export default function HistoryPage() {
  const [records, setRecords] = useState([]);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isCurrent = true;
    fetchAnalysisHistory()
      .then((history) => { if (isCurrent) setRecords(history); })
      .catch((requestError) => { if (isCurrent) setError(requestError.message); })
      .finally(() => { if (isCurrent) setIsLoading(false); });
    return () => { isCurrent = false; };
  }, []);

  const summary = useMemo(() => records.reduce((counts, record) => {
    counts[riskCategory(record.risk_level)] += 1;
    return counts;
  }, { high: 0, medium: 0, low: 0 }), [records]);

  return (
    <main id="history" className="history-page">
      <section className="history-hero">
        <p className="eyebrow">Analysis dashboard</p>
        <h1>Assessment history</h1>
        <p>Review saved screening results and their supporting assessment details.</p>
      </section>

      <section className="summary-grid" aria-label="History summary">
        <article><span>Total analyses</span><strong>{records.length}</strong></article>
        <article className="high"><span>High risk</span><strong>{summary.high}</strong></article>
        <article className="medium"><span>Medium risk</span><strong>{summary.medium}</strong></article>
        <article className="low"><span>Low risk</span><strong>{summary.low}</strong></article>
      </section>

      <section className="history-list-section">
        <div className="history-list-heading"><div><p className="eyebrow">Saved analyses</p><h2>Recent assessments</h2></div><span>{records.length} record{records.length === 1 ? "" : "s"}</span></div>
        {isLoading && <div className="history-state"><i className="spinner dark-spinner" />Loading saved analyses…</div>}
        {error && <div className="history-state history-error" role="alert">{error}</div>}
        {!isLoading && !error && records.length === 0 && <div className="history-state">No saved analyses yet. New completed assessments will appear here.</div>}
        <div className="history-grid">
          {records.map((record) => {
            const dateTime = formatDateTime(record.created_at);
            const category = riskCategory(record.risk_level);
            return <article className="history-card" key={record.id}>
              <div className="history-card-top"><span className={`history-risk ${category}`}>{category} risk</span><span className="confidence-chip">{record.confidence}%</span></div>
              <p className="history-date">{dateTime.date}</p><p className="history-time">{dateTime.time}</p>
              <button className="details-button" onClick={() => setSelectedRecord(record)}>View details <span>→</span></button>
            </article>;
          })}
        </div>
      </section>

      {selectedRecord && <HistoryModal record={selectedRecord} onClose={() => setSelectedRecord(null)} />}
    </main>
  );
}

function HistoryModal({ record, onClose }) {
  const dateTime = formatDateTime(record.created_at);
  return <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
    <section className="details-modal" role="dialog" aria-modal="true" aria-labelledby="details-title" onMouseDown={(event) => event.stopPropagation()}>
      <button className="modal-close" onClick={onClose} aria-label="Close details">×</button>
      <p className="eyebrow">Saved assessment</p><h2 id="details-title">Analysis details</h2>
      <div className="modal-metrics"><div><span>Risk level</span><strong>{record.risk_level}</strong></div><div><span>Confidence</span><strong>{record.confidence}%</strong></div><div><span>Date & time</span><strong>{dateTime.date} · {dateTime.time}</strong></div></div>
      <div className="detail-block"><span>Input text</span><p>{record.input_text}</p></div>
      <div className="detail-block"><span>Predicted label</span><p>{record.predicted_label}</p></div>
      <div className="detail-block"><span>Disclaimer</span><p>{record.disclaimer}</p></div>
      <div className="detail-block"><span>Support message</span><p>{record.support_message ?? "No additional support message was provided."}</p></div>
    </section>
  </div>;
}
