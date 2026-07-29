import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, ShieldAlert, Cpu, Stethoscope, Sparkles, Send, RefreshCw, 
  AlertTriangle, ChevronRight, User, Bot, HeartPulse, MessageSquare, Briefcase, Linkedin, Github, ExternalLink
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://helpq-backend.onrender.com';

// DEVELOPER SOCIAL & AUTHOR VERIFICATION LINKS
const DEVELOPER_LINKS = {
  whatsapp: 'https://wa.me/?text=Hi%20Muhammad%20Abdullah%2C%20I%20reviewed%20your%20H.E.L.P-Q%20AI%20Medical%20Platform',
  upwork: 'https://www.upwork.com/freelancers/~015bf9ec6e1f0e2ec6', // Replace with your exact Upwork Profile URL if needed
  linkedin: 'https://www.linkedin.com/in/muhammad-abdullah', // Replace with your exact LinkedIn Profile URL if needed
  github: 'https://github.com/Muhammad-Abdullah990/HELP-Q-Multi-Tier-Clinical-RAG-Triage-Platform'
};

const TEST_PROMPTS = [
  {
    id: 1,
    title: '🚨 Emergency Scenario',
    query: 'I have been experiencing a sudden, crushing chest pain that radiates down my left arm for the past fifteen minutes, accompanied by severe trouble breathing, dizziness, and cold sweats, and I feel like I might lose consciousness at any moment.'
  },
  {
    id: 2,
    title: '🩺 Skin Rash & Itching',
    query: 'For the past three days, I have noticed severe skin rash spreading across my arms and neck, accompanied by intense itching, redness, and slight shivering, which gets worse after taking a hot shower.'
  },
  {
    id: 3,
    title: 'ℹ️ System Support Query',
    query: 'Can you explain how this system works, who built the H.E.L.P-Q engine, what machine learning model is running under the hood to diagnose my condition, and how it determines which specialist doctor to route me to?'
  },
  {
    id: 4,
    title: '🫁 Multi-Symptom Respiratory',
    query: 'I have been suffering from a persistent high fever, continuous coughing with thick mucus, joint pain, chest tightness when taking deep breaths, and extreme fatigue that has left me bedridden for forty-eight hours.'
  },
  {
    id: 5,
    title: '❓ Ambiguous / Negation Test',
    query: 'I just feel somewhat uneasy and uncomfortable today without any specific sharp physical pain, fever, or skin issues, but I am not sure if I should be concerned or if I need to see a doctor.'
  }
];

export default function App() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Hello! I am the H.E.L.P-Q Clinical AI Engine powered by Gemini RAG and a 4-Layer Microservice Architecture. How can I assist with your health concerns today?',
      trace: null
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeTelemetry, setActiveTelemetry] = useState(null);
  const [emergencyAlert, setEmergencyAlert] = useState(null);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || inputQuery;
    if (!query.trim() || isLoading) return;

    const userMsg = { sender: 'user', text: query };
    setMessages(prev => [...prev, userMsg]);
    if (!textToSend) setInputQuery('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat?user_query=${encodeURIComponent(query)}`, {
        method: 'POST'
      });
      const data = await response.json();

      const botMsg = {
        sender: 'bot',
        text: data.reply || 'Analysis complete.',
        recommended_doctor: data.recommended_doctor,
        details: data.details,
        trace: data.architecture_trace
      };

      setMessages(prev => [...prev, botMsg]);
      setActiveTelemetry(data.architecture_trace);

      if (data.architecture_trace?.Layer_1_Gateway_Firewall?.status === 'TRIGGERED') {
        setEmergencyAlert(data);
      } else {
        setEmergencyAlert(null);
      }
    } catch (error) {
      console.error('API Error:', error);
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: '⚠️ Connection failure to H.E.L.P-Q Backend. If the server was sleeping (Render Free Tier), please retry in 30 seconds while it completes cold start.',
          trace: null
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* HEADER */}
      <header className="app-header">
        <div className="header-brand">
          <div className="brand-icon">
            <HeartPulse size={24} />
          </div>
          <div>
            <h1 className="brand-title">
              H.E.L.P-Q <span className="badge-rag">GEMINI RAG ENGINE</span>
            </h1>
            <p className="brand-subtitle">Healthcare Expert Location & Patient-Triage Architecture</p>
          </div>
        </div>

        {/* DEVELOPER VERIFICATION & SOCIAL CONTACT BAR */}
        <div className="developer-contact-bar">
          <a 
            href={DEVELOPER_LINKS.whatsapp} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="social-btn whatsapp"
            title="Contact Developer on WhatsApp"
          >
            <MessageSquare size={14} />
            <span>WhatsApp</span>
          </a>
          <a 
            href={DEVELOPER_LINKS.upwork} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="social-btn upwork"
            title="Hire Developer on Upwork"
          >
            <Briefcase size={14} />
            <span>Upwork</span>
          </a>
          <a 
            href={DEVELOPER_LINKS.linkedin} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="social-btn linkedin"
            title="Verify Developer on LinkedIn"
          >
            <Linkedin size={14} />
            <span>LinkedIn</span>
          </a>
          <a 
            href={DEVELOPER_LINKS.github} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="social-btn github"
            title="View Source on GitHub"
          >
            <Github size={14} />
            <span>GitHub</span>
          </a>
        </div>
      </header>

      {/* DASHBOARD GRID */}
      <main className="dashboard-grid">
        
        {/* LEFT PANEL: CHAT INTERFACE */}
        <section className="glass-panel chat-panel">
          
          {/* QUICK PROMPT CHIPS */}
          <div className="quick-prompts-bar">
            {TEST_PROMPTS.map(p => (
              <button
                key={p.id}
                onClick={() => handleSend(p.query)}
                disabled={isLoading}
                className="prompt-chip"
              >
                <span>{p.title}</span>
                <ChevronRight size={12} opacity={0.6} />
              </button>
            ))}
          </div>

          {/* MESSAGES FEED */}
          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-bubble-row ${msg.sender}`}>
                {msg.sender === 'bot' && (
                  <div className="avatar bot">
                    <Bot size={20} />
                  </div>
                )}

                <div className={`message-card ${msg.sender}`}>
                  <p style={{ whiteSpace: 'pre-line' }}>{msg.text}</p>

                  {/* DOCTOR BADGE */}
                  {msg.recommended_doctor && (
                    <div className="doc-badge">
                      <span style={{ color: 'var(--text-muted)', display: 'flex', items: 'center', gap: '6px' }}>
                        <Stethoscope size={14} color="var(--accent-cyan)" />
                        Recommended Doctor:
                      </span>
                      <span className="doc-pill">{msg.recommended_doctor}</span>
                    </div>
                  )}

                  {/* PRECAUTIONS LIST */}
                  {msg.details?.precautions && msg.details.precautions.length > 0 && (
                    <div className="precautions-box">
                      <div className="precautions-title">
                        <ShieldAlert size={14} />
                        Actionable Care Precautions:
                      </div>
                      <ul className="precautions-list">
                        {msg.details.precautions.map((prec, i) => (
                          <li key={i} style={{ textTransform: 'capitalize' }}>{prec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {msg.sender === 'user' && (
                  <div className="avatar user">
                    <User size={18} />
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="chat-bubble-row bot">
                <div className="avatar bot">
                  <RefreshCw size={18} className="animate-spin" />
                </div>
                <div className="message-card bot" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)', fontSize: '0.85rem' }}>
                  <Sparkles size={16} />
                  <span>Processing through Microservice Pipeline & Gemini RAG Synthesizer...</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* INPUT FORM */}
          <form className="input-form" onSubmit={(e) => { e.preventDefault(); handleSend(); }}>
            <input
              type="text"
              className="chat-input"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder="Describe your physical symptoms (e.g. skin rash, shivering, chest tightness)..."
              disabled={isLoading}
            />
            <button type="submit" className="send-btn" disabled={isLoading || !inputQuery.trim()}>
              <span>Send</span>
              <Send size={16} />
            </button>
          </form>
        </section>

        {/* RIGHT PANEL: LIVE 4-LAYER TELEMETRY INSPECTOR & AUTHOR VERIFICATION */}
        <section className="glass-panel telemetry-panel">
          <div className="telemetry-header">
            <h2 className="telemetry-title">
              <Cpu size={18} color="var(--accent-cyan)" />
              Live 4-Layer Architecture Inspector
            </h2>
            <span style={{ fontSize: '0.65rem', fontWeight: 700, padding: '2px 8px', borderRadius: '4px', background: 'rgba(0,242,254,0.1)', color: 'var(--accent-cyan)', border: '1px solid rgba(0,242,254,0.3)', fontFamily: 'var(--font-mono)' }}>
              TELEMETRY ACTIVE
            </span>
          </div>

          {!activeTelemetry ? (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
              <Activity size={48} color="var(--text-dim)" style={{ margin: '0 auto 12px auto' }} />
              <p style={{ fontWeight: 600, fontSize: '0.9rem' }}>No Active Telemetry Data</p>
              <p style={{ fontSize: '0.75rem', marginTop: '6px', color: 'var(--text-dim)' }}>
                Send a symptom prompt to inspect microservice layer outputs in real time.
              </p>
            </div>
          ) : (
            <div>
              {/* LAYER 1: GATEWAY FIREWALL */}
              <div className="layer-card">
                <div className="layer-head">
                  <span className="layer-name">
                    <ShieldAlert size={16} color="var(--accent-amber)" />
                    Layer 1: Gateway Firewall
                  </span>
                  <span className={`status-badge ${activeTelemetry.Layer_1_Gateway_Firewall?.status === 'TRIGGERED' ? 'triggered' : 'passed'}`}>
                    {activeTelemetry.Layer_1_Gateway_Firewall?.status}
                  </span>
                </div>
                <p style={{ color: 'var(--text-muted)' }}>
                  Status: {activeTelemetry.Layer_1_Gateway_Firewall?.reason || activeTelemetry.Layer_1_Gateway_Firewall?.status}
                </p>
              </div>

              {/* LAYER 2: TRIAGE SERVICE (spaCy NLP) */}
              <div className="layer-card">
                <div className="layer-head">
                  <span className="layer-name">
                    <Activity size={16} color="var(--accent-cyan)" />
                    Layer 2: NLP Triage (spaCy)
                  </span>
                  <span className="status-badge completed">
                    {activeTelemetry.Layer_2_Triage_Service?.status}
                  </span>
                </div>
                <div style={{ marginTop: '6px' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Extracted POS Tokens:</span>
                  <div style={{ marginTop: '4px' }}>
                    {activeTelemetry.Layer_2_Triage_Service?.output_symptoms?.map((sym, i) => (
                      <span key={i} className="token-tag">{sym}</span>
                    )) || <span style={{ color: 'var(--text-dim)' }}>None / Bypassed</span>}
                  </div>
                </div>
              </div>

              {/* LAYER 3: DIAGNOSIS SERVICE (RandomForest ML) */}
              <div className="layer-card">
                <div className="layer-head">
                  <span className="layer-name">
                    <Cpu size={16} color="var(--accent-purple)" />
                    Layer 3: Diagnosis (RandomForest)
                  </span>
                  <span className="status-badge completed">
                    {activeTelemetry.Layer_3_Diagnosis_Service?.status}
                  </span>
                </div>
                <p style={{ fontWeight: 600, color: 'var(--text-main)', marginTop: '4px' }}>
                  Predicted: <span style={{ color: 'var(--accent-purple)' }}>{activeTelemetry.Layer_3_Diagnosis_Service?.predicted_disease || 'N/A'}</span>
                </p>
                <p style={{ color: 'var(--text-dim)', fontSize: '0.7rem', marginTop: '2px' }}>
                  Model: {activeTelemetry.Layer_3_Diagnosis_Service?.ml_model || 'Bypassed'}
                </p>
              </div>

              {/* LAYER 4: RECOMMENDATION SERVICE */}
              <div className="layer-card">
                <div className="layer-head">
                  <span className="layer-name">
                    <Stethoscope size={16} color="var(--accent-emerald)" />
                    Layer 4: Recommendation Engine
                  </span>
                  <span className="status-badge completed">
                    {activeTelemetry.Layer_4_Recommendation_Service?.status}
                  </span>
                </div>
                <p style={{ color: 'var(--text-main)', marginTop: '4px' }}>
                  Specialist: <span style={{ color: 'var(--accent-emerald)', fontWeight: 600 }}>{activeTelemetry.Layer_4_Recommendation_Service?.specialist || 'N/A'}</span>
                </p>
              </div>

              {/* LAYER 5: GEMINI RAG SYNTHESIZER */}
              <div className="layer-card">
                <div className="layer-head">
                  <span className="layer-name">
                    <Sparkles size={16} color="var(--accent-blue)" />
                    Layer 5: Gemini RAG Synthesizer
                  </span>
                  <span className={`status-badge ${activeTelemetry.Layer_5_RAG_Synthesizer?.status?.includes('ERROR') ? 'fallback' : 'completed'}`}>
                    {activeTelemetry.Layer_5_RAG_Synthesizer?.status?.includes('ERROR') ? 'FALLBACK' : activeTelemetry.Layer_5_RAG_Synthesizer?.status}
                  </span>
                </div>
                <p style={{ color: 'var(--text-muted)', marginTop: '4px' }}>
                  Model: <span style={{ color: 'var(--accent-blue)' }}>{activeTelemetry.Layer_5_RAG_Synthesizer?.model}</span>
                </p>
              </div>

            </div>
          )}

          {/* DEVELOPER VERIFICATION & AUTHORSHIP FOOTER CARD */}
          <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--border-glass)' }}>
            <div style={{ background: 'rgba(15, 22, 38, 0.9)', border: '1px solid var(--border-glass)', borderRadius: '12px', padding: '14px' }}>
              <p style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-cyan)', marginBottom: '4px', display: 'flex', items: 'center', gap: '6px' }}>
                <User size={14} />
                Developed & Engineered By Muhammad Abdullah
              </p>
              <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '10px' }}>
                Full-Stack AI Microservices & MedTech RAG Architect. Verify authorship or contact for consulting below:
              </p>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                <a href={DEVELOPER_LINKS.whatsapp} target="_blank" rel="noopener noreferrer" className="social-btn whatsapp" style={{ fontSize: '0.7rem', padding: '4px 8px' }}>
                  <MessageSquare size={12} /> WhatsApp
                </a>
                <a href={DEVELOPER_LINKS.upwork} target="_blank" rel="noopener noreferrer" className="social-btn upwork" style={{ fontSize: '0.7rem', padding: '4px 8px' }}>
                  <Briefcase size={12} /> Upwork
                </a>
                <a href={DEVELOPER_LINKS.linkedin} target="_blank" rel="noopener noreferrer" className="social-btn linkedin" style={{ fontSize: '0.7rem', padding: '4px 8px' }}>
                  <Linkedin size={12} /> LinkedIn
                </a>
                <a href={DEVELOPER_LINKS.github} target="_blank" rel="noopener noreferrer" className="social-btn github" style={{ fontSize: '0.7rem', padding: '4px 8px' }}>
                  <Github size={12} /> Source Code
                </a>
              </div>
            </div>
          </div>
        </section>

      </main>

      {/* EMERGENCY OVERLAY MODAL */}
      {emergencyAlert && (
        <div className="emergency-modal-backdrop">
          <div className="emergency-modal-content">
            <div className="emergency-icon">
              <AlertTriangle size={36} />
            </div>
            <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-rose)', marginBottom: '10px' }}>
              CRITICAL MEDICAL EMERGENCY DETECTED
            </h2>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', marginBottom: '20px', lineHeight: 1.6 }}>
              {emergencyAlert.reply}
            </p>

            <div style={{ background: 'rgba(255, 75, 43, 0.1)', border: '1px solid rgba(255, 75, 43, 0.3)', borderRadius: '12px', padding: '14px', textAlign: 'left', fontSize: '0.8rem', color: '#fca5a5', marginBottom: '24px' }}>
              <p style={{ fontWeight: 700, marginBottom: '6px' }}>Emergency Protocol Activated:</p>
              <ul style={{ paddingLeft: '18px' }}>
                <li>Layer 1 Gateway Firewall triggered zero-latency ER escalation.</li>
                <li>Call emergency services immediately (1122 or 911).</li>
                <li>Sit down and do not attempt to drive yourself.</li>
              </ul>
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                onClick={() => setEmergencyAlert(null)}
                style={{ flex: 1, padding: '12px', borderRadius: '12px', background: 'rgba(255, 255, 255, 0.1)', border: '1px solid var(--border-glass)', color: 'var(--text-main)', fontWeight: 600, cursor: 'pointer' }}
              >
                Acknowledge & Close
              </button>
              <a href="tel:911" className="emergency-btn-call" style={{ flex: 1 }}>
                Call Emergency (911)
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
