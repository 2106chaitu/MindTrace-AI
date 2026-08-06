import { useState } from "react";

import { assessText } from "./api";
import HistoryPage from "./HistoryPage";

const features = [
  ["prediction", "AI prediction", "Machine-learning analysis identifies meaningful patterns in written text."],
  ["shield", "Risk assessment", "A clear, educational risk-level result supports awareness and next steps."],
  ["lock", "Privacy first", "Text is submitted only to generate the requested assessment."],
  ["bolt", "Fast analysis", "Receive a structured result in seconds through a focused workflow."],
  ["text", "Natural language processing", "Text preparation and TF-IDF features help the model understand language signals."],
  ["heart", "Wellness suggestions", "Practical, calm suggestions are presented alongside every result."]
];

const pipeline = [
  ["edit", "User enters text", "Written content is submitted for an educational screening."],
  ["clean", "Text cleaning", "Links, punctuation, and extra formatting are normalized."],
  ["text", "Text preprocessing", "The input is prepared for consistent model evaluation."],
  ["grid", "TF-IDF vectorization", "Relevant terms are represented as numerical features."],
  ["chart", "Linear SVC prediction", "The trained classifier evaluates language patterns in context."],
  ["gauge", "Confidence calculation", "The model score is translated into an easy-to-read confidence value."],
  ["shield", "Risk classification", "The result is grouped into an understandable risk level."],
  ["heart", "Personalized suggestions", "Supportive wellbeing guidance is displayed with the assessment."]
];

const technologyCards = [
  ["Frontend", "HTML5", "Semantic structure keeps the experience accessible and easy to navigate."],
  ["Frontend", "CSS3", "Responsive layouts, visual hierarchy, and subtle interaction states."],
  ["Frontend", "JavaScript", "Connects thoughtful interface behavior to the assessment workflow."],
  ["Frontend", "React", "Component-driven views keep the assessment and history experience focused."],
  ["Backend", "FastAPI", "A high-performance API layer delivers model results to the interface."],
  ["Backend", "Python", "Provides the dependable runtime for the assessment service."],
  ["Backend", "Uvicorn", "Runs the API application locally with a lightweight ASGI server."],
  ["Machine learning", "Scikit-learn", "Supplies proven machine-learning tools for text classification."],
  ["Machine learning", "Linear SVC", "The trained classifier evaluates language patterns in the input."],
  ["Machine learning", "TF-IDF", "Transforms meaningful terms into weighted numerical features."],
  ["Machine learning", "Label Encoder", "Converts the model output into a clear, readable prediction."],
  ["Machine learning", "NumPy & Pandas", "Support efficient numerical processing and data preparation."],
  ["Development", "VS Code", "Supports a productive, maintainable development workflow."],
  ["Development", "Google Colab", "Enables experimentation and notebook-based model exploration."],
  ["Development", "Swagger UI", "Makes the API transparent and straightforward to validate."],
  ["Development", "Git", "Keeps source changes traceable throughout the project lifecycle."]
];

const wellnessTips = [
  "Stay hydrated and choose nutritious food.", "Take a short walk or exercise regularly.", "Spend time with family or talk to friends.", "Maintain a steady, restful sleep routine.", "Practice gratitude or listen to relaxing music.", "Continue hobbies and activities that bring you meaning."
];

const supportTips = [
  "Reach out to someone you trust and avoid facing difficult feelings alone.", "Pause for slow breaths, drink water, and focus on one small next step.", "Try to have a nourishing meal and create a calm, comfortable space.", "Consider connecting with a qualified mental-health professional.", "You are not alone—support is available, and reaching out can help."
];

function Icon({ name }) {
  const paths = {
    prediction: "M4 19V5m6 14V9m6 10V3m6 16v-7", shield: "M12 3 20 6v5c0 5-3.2 8.6-8 10-4.8-1.4-8-5-8-10V6l8-3Zm-3 9 2 2 4-4", lock: "M7 10V7a5 5 0 0 1 10 0v3m-12 0h14v10H5V10Z", bolt: "m13 2-8 12h6l-1 8 9-13h-6l0-7Z", text: "M5 5h14M5 10h10M5 15h14M5 20h9", heart: "M20.8 8.6c0 6-8.8 11.4-8.8 11.4S3.2 14.6 3.2 8.6A4.3 4.3 0 0 1 11 6l1 1.3L13 6a4.3 4.3 0 0 1 7.8 2.6Z", edit: "M4 20h4l11-11-4-4L4 16v4Zm9-14 4 4", clean: "M5 19 18 6m-8 13 7-7m-3-7 4 4", grid: "M4 4h6v6H4V4Zm10 0h6v6h-6V4ZM4 14h6v6H4v-6Zm10 0h6v6h-6v-6Z", chart: "M4 19V5m0 14h16M8 16v-4m4 4V8m4 8v-6", gauge: "M4 17a8 8 0 1 1 16 0M12 12l4-3"
  };
  return <svg className="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={paths[name]} /></svg>;
}

function HealthLogo() {
  return <svg className="health-logo" viewBox="0 0 42 42" aria-hidden="true"><path d="M21 3 35 8v10c0 9-5.4 16.8-14 21-8.6-4.2-14-12-14-21V8l14-5Z" fill="currentColor" /><path d="M10 22h7l2.2-6 3.1 11 2.1-5H32" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" /><circle cx="21" cy="11" r="2.5" fill="#93C5FD" /></svg>;
}

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [activePage, setActivePage] = useState("home");

  function scrollToAssessment() {
    setActivePage("home");
    window.setTimeout(() => document.querySelector("#assessment")?.scrollIntoView({ behavior: "smooth" }), 0);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!text.trim()) { setError("Please enter text before running an assessment."); return; }
    setError(""); setResult(null); setIsLoading(true);
    try { setResult(await assessText(text)); } catch (requestError) { setError(requestError.message); } finally { setIsLoading(false); }
  }

  const elevated = result?.risk_level === "elevated";
  const tips = elevated ? supportTips : wellnessTips;
  const navigateHome = () => setActivePage("home");

  return <div className="app-shell">
    <header className="navbar">
      <a className="brand" href="#home" onClick={navigateHome} aria-label="MindTrace home"><HealthLogo /><span>Mind<span>Trace</span></span></a>
      <nav aria-label="Primary navigation"><a href="#home" onClick={navigateHome}>Home</a><a href="#features" onClick={navigateHome}>Features</a><a href="#how-it-works" onClick={navigateHome}>How it works</a><a href="#technology" onClick={navigateHome}>Technology</a><a href="#history" onClick={() => setActivePage("history")}>History</a></nav>
      <button className="nav-cta" onClick={scrollToAssessment}>Analyze text</button>
    </header>

    {activePage === "history" ? <HistoryPage /> : <main>
      <section id="home" className="hero">
        <div className="hero-copy reveal"><p className="eyebrow">AI-assisted mental wellness screening</p><h1>AI Mental Wellness <span>Screening</span></h1><p>Analyze written text using Machine Learning and Natural Language Processing to identify potential indicators of emotional distress.</p><div className="hero-actions"><button className="primary-button" onClick={scrollToAssessment}>Analyze Text <span>→</span></button><a className="secondary-button" href="#how-it-works">Learn More</a></div><div className="hero-assurance"><span><Icon name="shield" /> Educational screening</span><span><Icon name="lock" /> Privacy-conscious</span></div></div>
        <div className="hero-visual reveal delay-1"><div className="signal-orbit" /><div className="hero-dot dot-one" /><div className="hero-dot dot-two" /><div className="medical-panel"><div className="panel-top"><HealthLogo /><span>MindTrace AI</span><i>Ready</i></div><div className="pulse-line"><span /><span /><span /><span /><span /></div><div className="panel-result"><p>Assessment engine</p><strong>Text analysis ready</strong><span>Secure • Fast • Supportive</span></div></div><div className="floating-stat"><Icon name="chart" /><div><span>Structured result</span><strong>In seconds</strong></div></div></div>
        <a className="scroll-cue" href="#about"><span>Scroll to explore</span><i /></a>
      </section>

      <section id="about" className="about-section"><div className="about-graphic"><div className="about-ring" /><HealthLogo /><span className="about-pulse"><Icon name="heart" /></span></div><div className="about-copy"><p className="eyebrow">About MindTrace AI</p><h2>Technology that supports awareness, with care.</h2><p>MindTrace AI is an educational mental-wellness screening project that combines a modern web experience with Natural Language Processing and a trained machine-learning classifier.</p><p>It helps turn written context into a clear, supportive signal—while remaining transparent about its purpose: awareness and conversation, never clinical diagnosis.</p><div className="about-points"><span><Icon name="shield" /> Educational use</span><span><Icon name="text" /> NLP-informed</span><span><Icon name="heart" /> Supportive by design</span></div></div></section>

      <section id="features" className="features-section"><div className="section-heading reveal"><p className="eyebrow">Designed for clarity</p><h2>A calm, capable screening experience</h2><p>Every part of the experience is designed to make the assessment process clear, considered, and approachable.</p></div><div className="feature-grid">{features.map(([icon, title, copy]) => <article className="feature-card reveal" key={title}><span className="icon-wrap"><Icon name={icon} /></span><h3>{title}</h3><p>{copy}</p></article>)}</div></section>

      <section id="assessment" className="assessment-section"><div className="assessment-layout"><div className="assessment-intro reveal"><p className="eyebrow">Start an assessment</p><h2>Turn written context into a clearer signal.</h2><p>Enter text below to receive an educational model result and practical, wellbeing-focused suggestions.</p><div className="assessment-note"><Icon name="shield" /><span>This is AI-assisted screening, not a medical diagnosis.</span></div></div><div className="assessment-card reveal"><form onSubmit={handleSubmit}><div className="field-heading"><label htmlFor="assessment-text">Text to assess</label><span>{text.length.toLocaleString()} / 10,000</span></div><textarea id="assessment-text" value={text} onChange={(event) => setText(event.target.value)} placeholder="Write or paste text for a thoughtful, educational assessment…" maxLength={10000} rows={9} disabled={isLoading} /><div className="assessment-actions"><button className="clear-button" type="button" onClick={() => { setText(""); setError(""); }} disabled={!text || isLoading}>Clear</button><button className="primary-button" type="submit" disabled={isLoading}>{isLoading ? <><i className="spinner" />Analyzing</> : <>Analyze text <span>→</span></>}</button></div></form>{error && <p className="error-message" role="alert">{error}</p>}</div></div>
        {result && <section className={`result-card ${elevated ? "elevated" : "low"}`} aria-live="polite"><div className="result-heading"><div><p className="eyebrow">Assessment result</p><h2>{elevated ? "Elevated risk language detected" : "Low risk language detected"}</h2></div><span className="risk-badge">{elevated ? "Elevated" : "Low"} risk</span></div><div className="result-grid"><div className="result-metric"><span>Prediction</span><strong>{result.label}</strong></div><div className="result-metric"><span>Risk level</span><strong>{result.risk_level}</strong></div><div className="confidence-metric"><div><span>Confidence</span><strong>{result.confidence}%</strong></div><div className="progress-track"><span style={{ width: `${result.confidence}%` }} /></div></div></div><div className="result-disclaimer"><Icon name="shield" /><p>{result.disclaimer}</p></div><div className="suggestions"><div><p className="eyebrow">{elevated ? "Supportive guidance" : "Wellness suggestions"}</p><h3>{elevated ? "You do not have to navigate this alone." : "Support everyday wellbeing."}</h3></div><ul>{tips.map((tip) => <li key={tip}>{tip}</li>)}</ul>{result.support_message && <p className="support-message">{result.support_message}</p>}</div></section>}
      </section>

      <section id="how-it-works" className="pipeline-section"><div className="section-heading reveal"><p className="eyebrow">Transparent process</p><h2>From text input to supportive next steps</h2><p>A focused machine-learning pipeline converts written text into an understandable educational assessment.</p></div><div className="pipeline">{pipeline.map(([icon, title, copy], index) => <article className="pipeline-step reveal" key={title}><span className="step-number">{String(index + 1).padStart(2, "0")}</span><span className="pipeline-icon"><Icon name={icon} /></span><div><h3>{title}</h3><p>{copy}</p></div>{index < pipeline.length - 1 && <i className="pipeline-connector" />}</article>)}</div></section>

      <section id="technology" className="technology-section"><div className="section-heading reveal"><p className="eyebrow">Trusted foundations</p><h2>Technologies used</h2><p>Every layer of MindTrace AI is selected to make the experience responsive, transparent, and dependable.</p></div><div className="technology-grid">{technologyCards.map(([category, title, copy]) => <article className="technology-card reveal" key={title}><div className="technology-card-top"><span>{category}</span><Icon name={category === "Machine learning" ? "chart" : category === "Backend" ? "bolt" : category === "Development" ? "edit" : "grid"} /></div><h3>{title}</h3><p>{copy}</p></article>)}</div></section>
    </main>}

    <footer><div><strong>© 2026 AI Mental Wellness Screening</strong><span>AI-assisted screening • Not a medical diagnosis</span></div><p>Every conversation matters.<br />Small steps can lead to meaningful change.</p></footer>
  </div>;
}
