import { useState, useEffect } from 'react'
import axios from 'axios'
import { 
  Shield, 
  ShieldAlert, 
  ShieldCheck, 
  Search, 
  Loader2, 
  Layers, 
  FileText, 
  BarChart3, 
  BookOpen, 
  Copy, 
  Check, 
  ExternalLink,
  Cpu,
  AlertTriangle,
  Zap,
  Sparkles
} from 'lucide-react'

const SAMPLE_URLS = [
  {
    name: 'Amazon Product',
    url: 'https://www.amazon.in/LEGO%C2%AE-Icons-Jaguar-Type-Accessories/dp/B01MZ9GNNN?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D',
    category: 'Urgency & Drip Pricing'
  },
  {
    name: 'Booking / Travel',
    url: 'https://www.booking.com/hotel/us/times-square.html',
    category: 'False Scarcity Countdown'
  },
  {
    name: 'Clean Domain (Safe)',
    url: 'https://example.com',
    category: 'Baseline Non-Deceptive'
  }
]

const MODEL_CONFIGS = {
  logistic_regression: {
    name: 'Logistic Regression',
    type: 'Linear Baseline',
    desc: 'Rapid linear classification using TF-IDF token frequency weights.'
  },
  svm: {
    name: 'Support Vector Machine',
    type: 'Margin Classifier',
    desc: 'High-dimensional linear hyperplane optimized for deceptive boundary margin.'
  },
  lstm: {
    name: 'LSTM Network',
    type: 'Recurrent Sequence',
    desc: 'Deep recurrent architecture modeling sequential word dependencies.'
  },
  gru: {
    name: 'GRU Network',
    type: 'Gated Recurrent',
    desc: 'Efficient gated sequence model evaluating contextual phrasing.'
  }
}

const TAXONOMY = [
  {
    name: 'Drip Pricing & Hidden Fees',
    badge: 'Price Deception',
    desc: 'Disclosing incremental fees, delivery charges, or service costs incrementally as the user navigates the checkout funnel.',
    examples: 'Ex: "₹50 delivery charge applied at final step", "Mandatory processing fee".'
  },
  {
    name: 'False Urgency & Scarcity',
    badge: 'Pressure Tactic',
    desc: 'Creating synthetic deadlines, countdown clocks, or low-stock alerts to trigger anxiety and impulsive purchase behavior.',
    examples: 'Ex: "Only 2 items remaining in stock", "Order in 04:12 to claim discount".'
  },
  {
    name: 'Confirmshaming',
    badge: 'Emotional Manipulation',
    desc: 'Framing the opt-out or decline choice in a self-deprecating or emotionally manipulative manner.',
    examples: 'Ex: "No thanks, I prefer paying full price", "I don\'t care about saving money".'
  },
  {
    name: 'Roach Motel / Forced Action',
    badge: 'Obstruction',
    desc: 'Making subscription signup effortless in 1 click, while making cancellation require complex navigation or phone calls.',
    examples: 'Ex: "One-click trial start", "Call support during business hours to cancel".'
  }
]

function App() {
  const [url, setUrl] = useState('https://www.amazon.in/LEGO%C2%AE-Icons-Jaguar-Type-Accessories/dp/B01MZ9GNNN?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D')
  const [selectedModel, setSelectedModel] = useState('svm')
  const [compareAll, setCompareAll] = useState(true)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [resultsData, setResultsData] = useState(null)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    // Forcibly set document title and refresh favicon
    document.title = "DarkShield AI | Deceptive Pattern Detection & Intelligence"
    
    // Dynamically replace favicon link in document head to break browser cache
    const existingIcons = document.querySelectorAll("link[rel*='icon']")
    existingIcons.forEach(el => el.remove())

    const svgLink = document.createElement('link')
    svgLink.rel = 'icon'
    svgLink.type = 'image/svg+xml'
    svgLink.href = `/favicon.svg?t=${Date.now()}`
    document.head.appendChild(svgLink)

    const pngLink = document.createElement('link')
    pngLink.rel = 'icon'
    pngLink.type = 'image/png'
    pngLink.sizes = '32x32'
    pngLink.href = `/favicon-32x32.png?t=${Date.now()}`
    document.head.appendChild(pngLink)
  }, [])

  const handleAnalyze = async (e) => {
    if (e) e.preventDefault()
    if (!url.trim()) return

    setLoading(true)
    setError('')
    setResultsData(null)

    try {
      if (compareAll) {
        // Multi-model benchmark endpoint
        const response = await axios.post('http://127.0.0.1:8000/analyze/all', {
          url: url.trim(),
          model: selectedModel
        })

        if (response.data.status === 'success') {
          setResultsData({
            isMulti: true,
            text: response.data.text,
            models: response.data.models,
            primaryResult: response.data.models[selectedModel] || Object.values(response.data.models)[0]
          })
        } else {
          setError(response.data.message || 'Analysis failed.')
        }
      } else {
        // Single model endpoint
        const response = await axios.post('http://127.0.0.1:8000/analyze/url', {
          url: url.trim(),
          model: selectedModel
        })

        if (response.data.status === 'success') {
          setResultsData({
            isMulti: false,
            text: response.data.data.text,
            primaryResult: response.data.data,
            models: { [selectedModel]: response.data.data }
          })
        } else {
          setError(response.data.message || 'Analysis failed.')
        }
      }
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || (err.message === 'Network Error' ? 'Failed to connect to backend server. Make sure FastAPI is running on port 8000.' : err.message)
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  const handleCopyText = () => {
    if (!resultsData?.text) return
    navigator.clipboard.writeText(resultsData.text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  // Calculate high-level metrics
  const activeResult = resultsData?.models?.[selectedModel] || resultsData?.primaryResult
  const isDark = activeResult?.is_dark_pattern
  const confidence = activeResult?.confidence || 0
  const flaggedElements = activeResult?.flagged_elements || []

  const modelKeys = resultsData?.models ? Object.keys(resultsData.models) : []
  const darkCount = modelKeys.filter(k => resultsData.models[k].is_dark_pattern).length

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <nav className="navbar">
        <div className="nav-brand">
          <div className="brand-icon">
            <img src="/favicon.svg" width="22" height="22" alt="DarkShield" style={{ display: 'block' }} />
          </div>
          <span className="brand-title">DarkShield AI</span>
        </div>
      </nav>

      {/* Hero Header */}
      <div className="hero-header">
        <div className="hero-tag">
          <Shield size={13} />
          <span>Deceptive Pattern Intelligence Platform</span>
        </div>
        <h1 className="hero-title">
          Detect & Expose <span>Dark Patterns</span> on Any Web Page
        </h1>
        <p className="hero-desc">
          Audit e-commerce pages for hidden costs, drip pricing, and synthetic urgency using multi-model machine learning and SHAP explanations.
        </p>
      </div>

      {/* Control Deck (Search & Config) */}
      <div className="glass-panel deck-card">
        <form onSubmit={handleAnalyze} className="search-form">
          <div className="input-row">
            <div className="url-input-wrapper">
              <ExternalLink size={18} className="input-icon" />
              <input
                type="url"
                className="url-input"
                placeholder="Enter live web page URL (e.g., https://www.amazon.in/...)..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="action-btn" disabled={loading || !url.trim()}>
              {loading ? <Loader2 size={18} className="loader" /> : <Zap size={18} />}
              {loading ? 'Inspecting DOM...' : 'Run Audit'}
            </button>
          </div>

          <div className="controls-row">
            <div className="model-selector-group">
              <span className="selector-label">Model Focus:</span>
              {Object.keys(MODEL_CONFIGS).map((key) => (
                <button
                  type="button"
                  key={key}
                  className={`model-btn ${selectedModel === key ? 'active' : ''}`}
                  onClick={() => setSelectedModel(key)}
                >
                  <Cpu size={14} />
                  {MODEL_CONFIGS[key].name}
                </button>
              ))}
            </div>

            <button
              type="button"
              className={`mode-toggle-btn ${compareAll ? 'active' : ''}`}
              onClick={() => setCompareAll(!compareAll)}
            >
              <Layers size={15} />
              {compareAll ? 'Benchmark All 4 Models: ON' : 'Single Model Mode'}
            </button>
          </div>
        </form>

        {/* Quick Sample Presets */}
        <div className="preset-row">
          <span className="preset-title">Test Scenarios:</span>
          {SAMPLE_URLS.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              className="preset-chip"
              onClick={() => {
                setUrl(sample.url)
              }}
            >
              <strong>{sample.name}</strong> • {sample.category}
            </button>
          ))}
        </div>

        {error && (
          <div className="error-banner">
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Results Workspace */}
      {resultsData && (
        <div className="results-workspace">
          {/* Executive KPI Grid */}
          <div className="kpi-grid">
            <div className="glass-panel kpi-card">
              <div className={`kpi-icon-box ${isDark ? 'danger' : 'safe'}`}>
                {isDark ? <ShieldAlert size={26} /> : <ShieldCheck size={26} />}
              </div>
              <div className="kpi-details">
                <span className="kpi-label">Deception Assessment</span>
                <span className="kpi-value" style={{ color: isDark ? 'var(--danger-primary)' : 'var(--success-primary)' }}>
                  {isDark ? 'POTENTIAL DARK PATTERNS' : 'VERIFIED CLEAN'}
                </span>
                <span className="kpi-subtext">
                  Focus Model: {MODEL_CONFIGS[selectedModel]?.name} ({(confidence * 100).toFixed(1)}% Confidence)
                </span>
              </div>
            </div>

            {resultsData.isMulti && (
              <div className="glass-panel kpi-card">
                <div className="kpi-icon-box info">
                  <Layers size={26} />
                </div>
                <div className="kpi-details">
                  <span className="kpi-label">Model Consensus</span>
                  <span className="kpi-value">
                    {darkCount} / {modelKeys.length} Models Flagged
                  </span>
                  <span className="kpi-subtext">
                    {darkCount === modelKeys.length ? '100% Unanimous Agreement' : `${((darkCount / modelKeys.length) * 100).toFixed(0)}% Cross-Model Alignment`}
                  </span>
                </div>
              </div>
            )}

            <div className="glass-panel kpi-card">
              <div className="kpi-icon-box info">
                <FileText size={26} />
              </div>
              <div className="kpi-details">
                <span className="kpi-label">Scanned DOM Surface</span>
                <span className="kpi-value">
                  {resultsData.text ? resultsData.text.split(/\s+/).filter(Boolean).length : 0} Tokens
                </span>
                <span className="kpi-subtext">Playwright Synchronous Extraction</span>
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="workspace-tabs">
            <button
              className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              <Layers size={16} />
              Model Comparison Matrix
            </button>
            <button
              className={`tab-btn ${activeTab === 'elements' ? 'active' : ''}`}
              onClick={() => setActiveTab('elements')}
            >
              <AlertTriangle size={16} />
              Detected Cues {flaggedElements.length > 0 && <span style={{ background: 'var(--danger-bg)', color: '#fca5a5', padding: '0.1rem 0.45rem', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 700 }}>{flaggedElements.length}</span>}
            </button>
            <button
              className={`tab-btn ${activeTab === 'shap' ? 'active' : ''}`}
              onClick={() => setActiveTab('shap')}
            >
              <BarChart3 size={16} />
              SHAP Feature Explainability
            </button>
            <button
              className={`tab-btn ${activeTab === 'inspector' ? 'active' : ''}`}
              onClick={() => setActiveTab('inspector')}
            >
              <FileText size={16} />
              Extracted Page Text
            </button>
            <button
              className={`tab-btn ${activeTab === 'taxonomy' ? 'active' : ''}`}
              onClick={() => setActiveTab('taxonomy')}
            >
              <BookOpen size={16} />
              Deceptive Taxonomy Reference
            </button>
          </div>

          {/* Tab 0: Element-Level Detected Cues */}
          {activeTab === 'elements' && (
            <div className="glass-panel shap-panel">
              <div className="shap-header">
                <h3 className="shap-title">Element-Level Deceptive Pattern Inspector</h3>
                <p className="shap-subtitle">
                  Granular audit isolating discrete buttons, banners, and timers to prevent whole-page false alarms.
                </p>
              </div>

              {flaggedElements.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                  {flaggedElements.map((el, idx) => (
                    <div
                      key={idx}
                      className="glass-panel"
                      style={{
                        padding: '1rem 1.25rem',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        gap: '1rem',
                        background: 'var(--bg-secondary)',
                        borderLeft: '4px solid var(--danger-primary)'
                      }}
                    >
                      <div>
                        <span
                          style={{
                            fontSize: '0.685rem',
                            fontWeight: 700,
                            color: '#fca5a5',
                            textTransform: 'uppercase',
                            letterSpacing: '0.04em'
                          }}
                        >
                          {el.category}
                        </span>
                        <p style={{ marginTop: '0.35rem', fontSize: '0.925rem', color: '#f8fafc', fontWeight: 500, lineHeight: 1.4 }}>
                          "{el.text}"
                        </p>
                      </div>
                      <div style={{ textAlign: 'right', flexShrink: 0 }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Confidence</div>
                        <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fca5a5', fontFamily: 'var(--font-mono)' }}>
                          {(el.confidence * 100).toFixed(1)}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ padding: '2.5rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  <ShieldCheck size={40} color="var(--success-primary)" style={{ margin: '0 auto 0.75rem auto' }} />
                  <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                    Zero Deceptive Elements Flagged
                  </div>
                  <p style={{ fontSize: '0.85rem', marginTop: '0.35rem', color: 'var(--text-muted)' }}>
                    All scanned buttons, badges, banners, and content blocks on this page comply with standard non-deceptive UX standards.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Tab 1: Multi-Model Comparison Matrix */}
          {activeTab === 'overview' && (
            <div className="comparison-grid">
              {Object.keys(resultsData.models).map((key) => {
                const item = resultsData.models[key]
                const itemDark = item.is_dark_pattern
                const itemConf = item.confidence
                const config = MODEL_CONFIGS[key] || { name: key, type: 'Machine Learning', desc: '' }

                return (
                  <div key={key} className={`glass-panel model-card ${selectedModel === key ? 'selected-border' : ''}`}>
                    <div>
                      <div className="model-card-header">
                        <div>
                          <div className="model-name">{config.name}</div>
                          <div className="model-type-badge">{config.type}</div>
                        </div>
                        <span className={`verdict-tag ${itemDark ? 'danger' : 'safe'}`}>
                          {itemDark ? 'Dark Pattern' : 'Clean'}
                        </span>
                      </div>

                      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: '1.4' }}>
                        {config.desc}
                      </p>

                      <div className="meter-track">
                        <div
                          className={`meter-fill ${itemDark ? 'danger' : 'safe'}`}
                          style={{ width: `${Math.min(100, Math.max(8, itemConf * 100))}%` }}
                        ></div>
                      </div>

                      <div className="score-row">
                        <span>Confidence Level:</span>
                        <strong style={{ color: itemDark ? '#fca5a5' : '#6ee7b7' }}>
                          {(itemConf * 100).toFixed(1)}%
                        </strong>
                      </div>
                    </div>

                    <div style={{ marginTop: '1.25rem', paddingTop: '0.85rem', borderTop: '1px solid var(--border-subtle)' }}>
                      <span style={{ fontSize: '0.725rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                        Key Indicators:
                      </span>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.4rem' }}>
                        {item.explanation && item.explanation.length > 0 ? (
                          item.explanation.slice(0, 3).map((exp, i) => (
                            <span
                              key={i}
                              style={{
                                fontSize: '0.75rem',
                                background: 'rgba(255,255,255,0.05)',
                                padding: '0.15rem 0.45rem',
                                borderRadius: '4px',
                                fontFamily: 'var(--font-mono)'
                              }}
                            >
                              {exp.word}
                            </span>
                          ))
                        ) : (
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                            No dominant manipulative tokens
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}

          {/* Tab 2: SHAP Feature Explainability */}
          {activeTab === 'shap' && (
            <div className="glass-panel shap-panel">
              <div className="shap-header">
                <h3 className="shap-title">Additive Feature Attribution (SHAP Analysis)</h3>
                <p className="shap-subtitle">
                  Visualizing which specific vocabulary tokens exerted the highest positive leverage pushing the classifier toward a Dark Pattern verdict for <strong>{MODEL_CONFIGS[selectedModel]?.name}</strong>.
                </p>
              </div>

              {activeResult?.explanation && activeResult.explanation.length > 0 ? (
                <div className="feature-bars-list">
                  {activeResult.explanation.map((item, idx) => {
                    const maxContrib = Math.max(...activeResult.explanation.map(e => e.contribution)) || 1
                    const barWidth = Math.min(100, Math.max(15, (item.contribution / maxContrib) * 100))

                    return (
                      <div key={idx} className="feature-bar-item">
                        <span className="feature-word">{item.word}</span>
                        <div className="bar-container">
                          <div className="bar-fill" style={{ width: `${barWidth}%` }}></div>
                        </div>
                        <span className="feature-impact">
                          +{item.contribution.toFixed(4)}
                        </span>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                  No significant positive dark pattern indicators detected by this model. The evaluated text appears standard.
                </div>
              )}
            </div>
          )}

          {/* Tab 3: DOM Content Inspector */}
          {activeTab === 'inspector' && (
            <div className="glass-panel inspector-panel">
              <div className="inspector-header">
                <div>
                  <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Extracted Web Page Corpus</h3>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    Raw textual hierarchy extracted directly from active DOM nodes via Playwright.
                  </p>
                </div>
                <button type="button" className="copy-btn" onClick={handleCopyText}>
                  {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
                  {copied ? 'Copied' : 'Copy All Text'}
                </button>
              </div>

              <div className="inspector-box">
                {resultsData.text || 'No text extracted.'}
              </div>
            </div>
          )}

          {/* Tab 4: Taxonomy Reference */}
          {activeTab === 'taxonomy' && (
            <div className="taxonomy-grid">
              {TAXONOMY.map((item, idx) => (
                <div key={idx} className="glass-panel taxonomy-card">
                  <span className="taxonomy-badge">{item.badge}</span>
                  <div className="taxonomy-name">{item.name}</div>
                  <p className="taxonomy-desc">{item.desc}</p>
                  <div className="taxonomy-examples">{item.examples}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      <footer>
        DarkShield AI • Multi-Model Black Pattern Detection & Explainability Platform
      </footer>
    </div>
  )
}

export default App
