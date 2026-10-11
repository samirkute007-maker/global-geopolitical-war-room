/**
 * GLOBAL GEOPOLITICAL WAR ROOM — Frontend Application
 * Supports Mock Intelligence Mode (offline) and Live AI OSINT Mode.
 * Settings drawer enables runtime diagnostics, mode display, and billing info.
 */

document.addEventListener('DOMContentLoaded', () => {

  // ─── DOM References ────────────────────────────────────────────────────────
  const runWarRoomBtn         = document.getElementById('runWarRoomBtn');
  const btnSubtext            = document.getElementById('btnSubtext');
  const exportActionsWrap     = document.getElementById('exportActionsWrap');
  const exportPdfBtn          = document.getElementById('exportPdfBtn');
  const exportJsonBtn         = document.getElementById('exportJsonBtn');
  const printReportId         = document.getElementById('printReportId');
  const printReportDate       = document.getElementById('printReportDate');
  const printGeneratedAt      = document.getElementById('printGeneratedAt');
  const printModeTag          = document.getElementById('printModeTag');
  const standbyState          = document.getElementById('standbyState');
  const standbyDescription    = document.getElementById('standbyDescription');
  const scanningSection       = document.getElementById('scanningSection');
  const scanningTitle         = document.getElementById('scanningTitle');
  const scanModeLabel         = document.getElementById('scanModeLabel');
  const reportContainer       = document.getElementById('reportContainer');
  const reportMetaBox         = document.getElementById('reportMetaBox');
  const reportIdDisplay       = document.getElementById('reportIdDisplay');
  const reportDateDisplay     = document.getElementById('reportDateDisplay');
  const generatedAtDisplay    = document.getElementById('generatedAtDisplay');
  const errorBanner           = document.getElementById('errorBanner');
  const errorTitle            = document.getElementById('errorTitle');
  const errorMessage          = document.getElementById('errorMessage');
  const dismissErrorBtn       = document.getElementById('dismissErrorBtn');
  const retryBtn              = document.getElementById('retryBtn');
  const systemStatus          = document.getElementById('systemStatus');
  const connectionBadge       = document.getElementById('connectionBadge');
  const modeIndicatorBadge    = document.getElementById('modeIndicatorBadge');
  const liveClock             = document.getElementById('liveClock');
  const scanningLogBox        = document.getElementById('scanningLogBox');
  const theaterListContainer  = document.getElementById('theaterListContainer');
  const hotspotCountBadge     = document.getElementById('hotspotCountBadge');
  const resetMapBtn           = document.getElementById('resetMapBtn');
  const mapFilterBtns         = document.querySelectorAll('.map-filter-btn');
  const copyScriptBtn         = document.getElementById('copyScriptBtn');
  const footerSecurityTag     = document.getElementById('footerSecurityTag');
  const featurePills          = document.getElementById('featurePills');
  const pillMode              = document.getElementById('pillMode');

  // Settings Drawer
  const settingsToggleBtn     = document.getElementById('settingsToggleBtn');
  const settingsDrawer        = document.getElementById('settingsDrawer');
  const settingsCloseBtn      = document.getElementById('settingsCloseBtn');
  const settingsOverlay       = document.getElementById('settingsOverlay');
  const modeStatusDot         = document.getElementById('modeStatusDot');
  const modeStatusName        = document.getElementById('modeStatusName');
  const modeStatusDesc        = document.getElementById('modeStatusDesc');
  const apiKeyInput           = document.getElementById('apiKeyInput');
  const apiKeyToggleBtn       = document.getElementById('apiKeyToggleBtn');
  const switchMockBtn         = document.getElementById('switchMockBtn');
  const switchLiveBtn         = document.getElementById('switchLiveBtn');
  const modeSwitchNote        = document.getElementById('modeSwitchNote');
  const checkHealthBtn        = document.getElementById('checkHealthBtn');
  const checkModeBtn          = document.getElementById('checkModeBtn');
  const checkCreditsBtn       = document.getElementById('checkCreditsBtn');
  const diagOutput            = document.getElementById('diagOutput');

  // ─── State ─────────────────────────────────────────────────────────────────
  let currentReportData   = null;
  let tacticalMap         = null;
  let markersLayer        = null;
  let allHotspots         = [];
  let currentMapFilter    = 'all';
  const markerMapRef      = new Map();
  let currentRawVideoScript = '';
  let currentMode         = 'mock'; // updated after /api/mode call
  let scanStepInterval    = null;

  // ─── Scanning Step Sequences ───────────────────────────────────────────────
  const scanStepsMock = [
    '> Initializing Geopolitical Intelligence scan [MOCK MODE]...',
    '> Loading local demonstration dataset (offline, zero API credits)...',
    '> Evaluating Strait of Hormuz, Black Sea, Taiwan Strait, South Asia corridors...',
    '> Running cross-asset transmission model (Crude Oil, Gold, FX/DXY, USD/INR, Indian Equities)...',
    '> Formulating Base, Escalation, and De-escalation probabilistic scenarios...',
    '> Generating 90-second executive broadcast teleprompter script...',
    '> Finalizing War Room dossier — local intelligence engine complete.'
  ];
  const scanStepsLive = [
    '> Initializing Live AI OSINT Intelligence scan...',
    '> Connecting to OpenAI Responses API with web-search preview...',
    '> Querying real-time conflict theaters, chokepoints & trade corridors...',
    '> Synthesizing geopolitical developments from global OSINT feeds...',
    '> Modeling cross-asset transmission (Crude, Gold, FX/DXY, USD/INR, Nifty)...',
    '> Formulating probabilistic scenarios from live threat assessment...',
    '> Compiling executive dossier — AI synthesis in progress...'
  ];

  // ─── Live UTC Clock ────────────────────────────────────────────────────────
  function updateLiveClock() {
    const now = new Date();
    const hh = String(now.getUTCHours()).padStart(2, '0');
    const mm = String(now.getUTCMinutes()).padStart(2, '0');
    const ss = String(now.getUTCSeconds()).padStart(2, '0');
    if (liveClock) liveClock.textContent = `${hh}:${mm}:${ss} UTC`;
  }
  setInterval(updateLiveClock, 1000);
  updateLiveClock();

  // ─── Mode & Health Check on Load ──────────────────────────────────────────
  async function checkModeAndHealth() {
    try {
      const [modeRes, healthRes] = await Promise.all([
        fetch('/api/mode'),
        fetch('/health')
      ]);

      if (modeRes.ok) {
        const modeData = await modeRes.json();
        applyModeToUI(modeData.mode || 'mock', modeData.is_mock !== false);
      }

      if (healthRes.ok) {
        const healthData = await healthRes.json();
        if (healthData.status === 'ok') {
          if (connectionBadge) {
            connectionBadge.textContent = 'API: ONLINE';
            connectionBadge.style.color = '#10b981';
          }
        }
      } else {
        if (connectionBadge) {
          connectionBadge.textContent = 'API: OFFLINE';
          connectionBadge.style.color = '#ef4444';
        }
      }
    } catch (err) {
      console.warn('Health check error:', err);
      if (connectionBadge) {
        connectionBadge.textContent = 'API: OFFLINE';
        connectionBadge.style.color = '#ef4444';
      }
    }
  }

  function applyModeToUI(mode, isMock) {
    currentMode = mode;

    if (isMock || mode === 'mock') {
      // ── Mock Mode ──────────────────────────────────────────────────────────
      modeIndicatorBadge.textContent = 'MOCK MODE — LOCAL INTELLIGENCE';
      modeIndicatorBadge.className = 'hud-badge mode-badge mode-mock';
      if (btnSubtext) btnSubtext.textContent = '[ LOCAL MOCK SCAN ]';
      if (standbyDescription) {
        standbyDescription.innerHTML = 'Click <strong>[ RUN WAR ROOM ]</strong> to synthesize illustrative demonstration intelligence across active conflicts, energy security, USD/INR sensitivity, and 10 global assets.';
      }
      if (footerSecurityTag) {
        footerSecurityTag.textContent = '🛡️ MOCK MODE — LOCAL ISOLATION (NO CREDITS REQUIRED)';
      }
      if (pillMode) pillMode.textContent = '🛡️ Mock Intelligence Mode';

      // Settings drawer
      if (modeStatusDot) modeStatusDot.className = 'mode-status-indicator indicator-mock';
      if (modeStatusName) modeStatusName.textContent = 'MOCK MODE';
      if (modeStatusDesc) modeStatusDesc.textContent = 'Running on local demonstration intelligence data. Zero API credits required. Fully offline.';
      if (switchMockBtn) switchMockBtn.classList.add('active');
      if (switchLiveBtn) switchLiveBtn.classList.remove('active');
    } else {
      // ── Live Mode ──────────────────────────────────────────────────────────
      modeIndicatorBadge.textContent = 'LIVE AI MODE — OPENAI OSINT';
      modeIndicatorBadge.className = 'hud-badge mode-badge mode-live';
      if (btnSubtext) btnSubtext.textContent = '[ INITIATE AI OSINT SCAN ]';
      if (standbyDescription) {
        standbyDescription.innerHTML = 'Click <strong>[ RUN WAR ROOM ]</strong> to query the live AI engine for real-time conflict developments, macroeconomic linkages, and cross-asset impacts via OpenAI web-search.';
      }
      if (footerSecurityTag) {
        footerSecurityTag.textContent = '🔒 LIVE AI MODE — SERVER-SIDE OPENAI INTEGRATION';
      }
      if (pillMode) pillMode.textContent = '🔴 Live AI OSINT Mode';

      // Settings drawer
      if (modeStatusDot) modeStatusDot.className = 'mode-status-indicator indicator-live';
      if (modeStatusName) modeStatusName.textContent = 'LIVE AI MODE';
      if (modeStatusDesc) modeStatusDesc.textContent = 'Connected to OpenAI Responses API with web-search. Each scan uses ~$0.03–$0.10 of API credits.';
      if (switchLiveBtn) switchLiveBtn.classList.add('active');
      if (switchMockBtn) switchMockBtn.classList.remove('active');
    }
  }

  checkModeAndHealth();

  // ─── Settings Drawer ──────────────────────────────────────────────────────
  function openSettings() {
    settingsDrawer.style.display = 'block';
    settingsOverlay.style.display = 'block';
    setTimeout(() => {
      settingsDrawer.classList.add('open');
      settingsOverlay.classList.add('open');
    }, 10);
  }

  function closeSettings() {
    settingsDrawer.classList.remove('open');
    settingsOverlay.classList.remove('open');
    setTimeout(() => {
      settingsDrawer.style.display = 'none';
      settingsOverlay.style.display = 'none';
    }, 300);
  }

  if (settingsToggleBtn) settingsToggleBtn.addEventListener('click', openSettings);
  if (settingsCloseBtn) settingsCloseBtn.addEventListener('click', closeSettings);
  if (settingsOverlay) settingsOverlay.addEventListener('click', closeSettings);

  // API Key Visibility Toggle
  if (apiKeyToggleBtn && apiKeyInput) {
    apiKeyToggleBtn.addEventListener('click', () => {
      apiKeyInput.type = apiKeyInput.type === 'password' ? 'text' : 'password';
    });
  }

  // Mode Switch buttons — show instructions only (actual switch requires server restart)
  if (switchMockBtn) {
    switchMockBtn.addEventListener('click', () => {
      setDiagOutput('info', '🛡️ To use Mock Mode: set WAR_ROOM_MODE=mock in your .env file, then restart the server. No API key needed.');
    });
  }

  if (switchLiveBtn) {
    switchLiveBtn.addEventListener('click', () => {
      setDiagOutput('info', '🔴 To enable Live AI Mode: set WAR_ROOM_MODE=live and a valid OPENAI_API_KEY in your .env file, then restart the server.\n\nAdd billing credits at: https://platform.openai.com/settings/organization/billing');
    });
  }

  // Diagnostics
  if (checkHealthBtn) {
    checkHealthBtn.addEventListener('click', async () => {
      setDiagOutput('loading', '🩺 Checking backend health...');
      try {
        const res = await fetch('/health');
        const data = await res.json();
        setDiagOutput('success', `✅ Health: ${JSON.stringify(data, null, 2)}`);
      } catch (e) {
        setDiagOutput('error', `❌ Health check failed: ${e.message}`);
      }
    });
  }

  if (checkModeBtn) {
    checkModeBtn.addEventListener('click', async () => {
      setDiagOutput('loading', '📡 Fetching mode info...');
      try {
        const res = await fetch('/api/mode');
        const data = await res.json();
        setDiagOutput('success', `📡 Mode: ${JSON.stringify(data, null, 2)}`);
        applyModeToUI(data.mode, data.is_mock);
      } catch (e) {
        setDiagOutput('error', `❌ Mode check failed: ${e.message}`);
      }
    });
  }

  if (checkCreditsBtn) {
    checkCreditsBtn.addEventListener('click', async () => {
      setDiagOutput('loading', '💳 Testing OpenAI API credits via backend...');
      try {
        const res = await fetch('/api/credits/check');
        const data = await res.json();
        if (data.status === 'ok' || data.credits_available) {
          setDiagOutput('success', `✅ API Credits: AVAILABLE\n${data.message || ''}`);
        } else {
          setDiagOutput('error', `❌ ${data.message || 'No credits available. Add credits at https://platform.openai.com/settings/organization/billing'}`);
        }
      } catch (e) {
        setDiagOutput('error', `❌ Credits check failed: ${e.message}\n\nThis endpoint may not be available in your current version.`);
      }
    });
  }

  function setDiagOutput(type, msg) {
    if (!diagOutput) return;
    diagOutput.textContent = msg;
    diagOutput.className = `diag-output diag-output-${type}`;
  }

  // ─── Leaflet Tactical GIS Map ──────────────────────────────────────────────
  function initTacticalMap() {
    const mapEl = document.getElementById('tacticalMap');
    if (!mapEl || typeof L === 'undefined') return;

    if (tacticalMap) {
      tacticalMap.invalidateSize();
      return;
    }

    tacticalMap = L.map('tacticalMap', {
      center: [22.0, 48.0],
      zoom: 2.8,
      minZoom: 2,
      maxZoom: 10,
      zoomControl: true,
      attributionControl: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(tacticalMap);

    markersLayer = L.layerGroup().addTo(tacticalMap);
    loadBaselineTheaters();
  }

  async function loadBaselineTheaters() {
    try {
      const res = await fetch('/api/theaters/baseline');
      if (res.ok) {
        const data = await res.json();
        if (data.theaters && Array.isArray(data.theaters)) {
          allHotspots = data.theaters;
          renderMapMarkersAndList();
        }
      }
    } catch (err) {
      console.warn('Could not load baseline theaters:', err);
    }
  }

  function getThreatCategoryClass(threatLevel) {
    const lvl = String(threatLevel || '').toUpperCase();
    if (lvl.includes('CRITICAL')) return 'critical';
    if (lvl.includes('HIGH')) return 'high';
    if (lvl.includes('ELEVATED')) return 'elevated';
    return 'monitored';
  }

  function renderMapMarkersAndList() {
    if (!markersLayer || !tacticalMap) return;

    markersLayer.clearLayers();
    markerMapRef.clear();
    theaterListContainer.innerHTML = '';

    const filteredHotspots = allHotspots.filter(item => {
      const threat = (item.threat_level || '').toLowerCase();
      const type = (item.type || '').toLowerCase();
      if (currentMapFilter === 'all') return true;
      if (currentMapFilter === 'critical') return threat.includes('critical');
      if (currentMapFilter === 'chokepoint') return type.includes('chokepoint') || type.includes('strait') || type.includes('naval');
      if (currentMapFilter === 'conflict') return type.includes('conflict') || type.includes('border') || threat.includes('high') || threat.includes('critical');
      return true;
    });

    hotspotCountBadge.textContent = `${filteredHotspots.length} THEATERS`;

    if (filteredHotspots.length === 0) {
      theaterListContainer.innerHTML = '<p class="text-muted" style="padding: 12px; font-size: 0.82rem;">No hotspots match current filter.</p>';
      return;
    }

    filteredHotspots.forEach(spot => {
      const threatClass = getThreatCategoryClass(spot.threat_level);

      const customIcon = L.divIcon({
        className: 'custom-tactical-pin',
        html: `
          <div class="tactical-marker-wrap marker-${threatClass}">
            <div class="marker-pulse"></div>
            <div class="marker-core"></div>
          </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const marker = L.marker([spot.lat, spot.lon], { icon: customIcon });

      const popupHtml = `
        <div class="popup-tactical">
          <h4 class="popup-title">${escapeHtml(spot.name)}</h4>
          <div class="popup-meta">
            <span class="theater-threat-tag badge-severity severity-${threatClass}">${escapeHtml(spot.threat_level || 'ELEVATED')}</span>
            <span class="popup-coords">${spot.lat.toFixed(2)}°N, ${spot.lon.toFixed(2)}°E</span>
          </div>
          <p class="popup-summary">${escapeHtml(spot.summary || '')}</p>
          <div class="popup-metrics">
            <span class="metric-pill">THEATER: ${escapeHtml(spot.theater || 'Global')}</span>
            <span class="metric-pill">TYPE: ${escapeHtml(spot.type || 'Hotspot')}</span>
            ${spot.metrics?.risk_index ? `<span class="metric-pill">RISK: ${escapeHtml(spot.metrics.risk_index)}</span>` : ''}
            ${spot.metrics?.oil_flow ? `<span class="metric-pill">FLOW: ${escapeHtml(spot.metrics.oil_flow)}</span>` : ''}
          </div>
        </div>
      `;
      marker.bindPopup(popupHtml, { maxWidth: 340 });
      markersLayer.addLayer(marker);
      markerMapRef.set(spot.name, marker);

      const card = document.createElement('div');
      card.className = 'theater-item-card';
      card.innerHTML = `
        <div class="theater-item-top">
          <span class="theater-name">${escapeHtml(spot.name)}</span>
          <span class="theater-threat-tag badge-severity severity-${threatClass}">${escapeHtml(spot.threat_level || 'ELEVATED')}</span>
        </div>
        <p class="theater-summary-snippet">${escapeHtml(spot.summary || '')}</p>
        <div class="theater-card-footer">
          <span class="theater-type-badge">${escapeHtml(spot.type || 'Flashpoint')}</span>
          <span class="coords-tag">${spot.lat.toFixed(1)}°, ${spot.lon.toFixed(1)}°</span>
        </div>
      `;

      card.addEventListener('click', () => {
        document.querySelectorAll('.theater-item-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        tacticalMap.flyTo([spot.lat, spot.lon], 5.5, { duration: 1.2 });
        setTimeout(() => marker.openPopup(), 1200);
      });

      theaterListContainer.appendChild(card);
    });
  }

  // Map Filter Buttons
  mapFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      mapFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentMapFilter = btn.getAttribute('data-filter');
      renderMapMarkersAndList();
    });
  });

  if (resetMapBtn) {
    resetMapBtn.addEventListener('click', () => {
      if (tacticalMap) {
        tacticalMap.flyTo([22.0, 48.0], 2.8, { duration: 1.0 });
        tacticalMap.closePopup();
      }
      document.querySelectorAll('.theater-item-card').forEach(c => c.classList.remove('selected'));
    });
  }

  // Error / Retry
  dismissErrorBtn.addEventListener('click', () => { errorBanner.style.display = 'none'; });
  if (retryBtn) {
    retryBtn.addEventListener('click', () => {
      errorBanner.style.display = 'none';
      triggerWarRoomScan();
    });
  }

  // ─── Scanning Animation ────────────────────────────────────────────────────
  function startScanningAnimation() {
    standbyState.style.display = 'none';
    reportContainer.style.display = 'none';
    errorBanner.style.display = 'none';
    scanningSection.style.display = 'flex';
    systemStatus.textContent = 'STATUS: DEFCON 1 // ACTIVE SCANNING';
    systemStatus.style.color = '#f59e0b';
    runWarRoomBtn.disabled = true;

    const steps = currentMode === 'live' ? scanStepsLive : scanStepsMock;
    if (scanningTitle) scanningTitle.textContent = currentMode === 'live' ? 'LIVE AI OSINT SCANNING...' : 'WAR ROOM SCANNING...';
    if (scanModeLabel) scanModeLabel.textContent = currentMode === 'live' ? '[ LIVE AI — OpenAI Web Search Active ]' : '[ MOCK MODE — Local Intelligence Engine ]';

    let currentStep = 0;
    scanningLogBox.innerHTML = `<p class="scan-log-line active">${steps[0]}</p>`;

    if (scanStepInterval) clearInterval(scanStepInterval);
    scanStepInterval = setInterval(() => {
      currentStep = (currentStep + 1) % steps.length;
      const logLine = document.createElement('p');
      logLine.className = 'scan-log-line active';
      logLine.textContent = steps[currentStep];
      if (scanningLogBox.children.length >= 4) {
        scanningLogBox.removeChild(scanningLogBox.firstChild);
      }
      scanningLogBox.appendChild(logLine);
    }, 2400);
  }

  function stopScanningAnimation() {
    if (scanStepInterval) clearInterval(scanStepInterval);
    scanningSection.style.display = 'none';
    runWarRoomBtn.disabled = false;
  }

  function showError(title, msg) {
    stopScanningAnimation();
    errorTitle.textContent = title || 'INTELLIGENCE SCAN ERROR';
    errorMessage.textContent = msg || 'An unexpected error occurred while communicating with the War Room backend.';
    errorBanner.style.display = 'flex';
    systemStatus.textContent = 'STATUS: DEFCON 3 // SYSTEM ALERT';
    systemStatus.style.color = '#ef4444';
  }

  // ─── Rendering Helpers ─────────────────────────────────────────────────────
  function getLifecycleChipClass(stage) {
    const s = String(stage || '').toUpperCase().replace(/[\s-]/g, '_');
    if (s.includes('NEW_SHOCK') || s.includes('EMERGING')) return 'chip-new-shock';
    if (s.includes('ESCALAT')) return 'chip-escalation';
    if (s.includes('FULL_IMPACT') || s.includes('PEAK')) return 'chip-full-impact';
    if (s.includes('STABILIS') || s.includes('STABILIZ') || s.includes('DE_ESCALAT')) return 'chip-stabilisation';
    if (s.includes('RECOVERY') || s.includes('RESOLUTION')) return 'chip-recovery';
    if (s.includes('STRUCTURAL')) return 'chip-structural';
    return 'chip-escalation';
  }

  function getSeverityClass(severity) {
    const s = String(severity || '').toUpperCase();
    if (s.includes('CRITICAL')) return 'severity-critical';
    if (s.includes('HIGH')) return 'severity-high';
    return 'severity-medium';
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatParagraphs(text) {
    if (!text) return '<p class="text-muted">No intelligence summary provided.</p>';
    return String(text)
      .split('\n\n')
      .filter(p => p.trim().length > 0)
      .map(p => `<p>${escapeHtml(p)}</p>`)
      .join('');
  }

  // ─── Render Full Report ────────────────────────────────────────────────────
  function renderWarRoomReport(data) {
    currentReportData = data;
    stopScanningAnimation();
    systemStatus.textContent = 'STATUS: DEFCON 2 // INTELLIGENCE DOSSIER LIVE';
    systemStatus.style.color = '#10b981';

    const isLive = (data.mode === 'live');

    // Report Metadata
    if (data.report_id) {
      reportIdDisplay.textContent = data.report_id;
      if (printReportId) printReportId.textContent = data.report_id;
    }
    if (data.report_date) {
      reportDateDisplay.textContent = data.report_date;
      if (printReportDate) printReportDate.textContent = data.report_date;
    }
    if (data.generated_at) {
      const genDate = new Date(data.generated_at);
      const formatted = isNaN(genDate.getTime()) ? data.generated_at : genDate.toUTCString();
      generatedAtDisplay.textContent = formatted;
      if (printGeneratedAt) printGeneratedAt.textContent = formatted;
    }
    if (printModeTag) {
      printModeTag.textContent = isLive ? 'LIVE AI OSINT DOSSIER' : 'MOCK DEMONSTRATION DATASET';
    }
    reportMetaBox.style.display = 'flex';
    if (exportActionsWrap) exportActionsWrap.style.display = 'flex';

    // Regime Banner
    const marketRegimeTitle = document.getElementById('marketRegimeTitle');
    if (marketRegimeTitle && data.market_regime) {
      marketRegimeTitle.textContent = data.market_regime;
    }
    const reportModePill = document.getElementById('reportModePill');
    if (reportModePill) {
      if (isLive) {
        reportModePill.textContent = '🔴 LIVE AI DOSSIER';
        reportModePill.className = 'mock-notice-pill pill-live';
      } else {
        reportModePill.textContent = '🛡️ MOCK DEMONSTRATION DATA';
        reportModePill.className = 'mock-notice-pill pill-mock';
      }
    }

    // 1. Executive Summary
    const execSummaryEl = document.getElementById('executiveSummaryContent');
    if (typeof data.executive_summary === 'string') {
      execSummaryEl.innerHTML = data.executive_summary
        .split('\n\n')
        .filter(p => p.trim().length > 0)
        .map(p => `<p>${escapeHtml(p)}</p>`)
        .join('');
    } else {
      execSummaryEl.textContent = JSON.stringify(data.executive_summary);
    }

    // 2. Dynamic Hotspots → Tactical GIS Map
    if (Array.isArray(data.hotspots) && data.hotspots.length > 0) {
      allHotspots = data.hotspots;
      renderMapMarkersAndList();
    }

    // 3. Geopolitical Events Cards
    const geoEventsListEl = document.getElementById('geopoliticalEventsList');
    geoEventsListEl.innerHTML = '';
    const eventsToRender = (Array.isArray(data.geopolitical_events) && data.geopolitical_events.length > 0)
      ? data.geopolitical_events
      : (Array.isArray(data.top_events) ? data.top_events : []);

    if (eventsToRender.length > 0) {
      eventsToRender.forEach(evt => {
        const title        = evt.event_name || evt.title || 'Geopolitical Event';
        const region       = evt.region || 'Global Theater';
        const severity     = evt.severity || 'HIGH';
        const lifecycle    = evt.lifecycle_stage || 'ESCALATION';
        const severityClass = getSeverityClass(severity);
        const lifecycleClass = getLifecycleChipClass(lifecycle);
        const whatHappened = evt.what_happened || evt.summary || '';
        const transmission = evt.transmission_mechanism || evt.impact || '';
        const confidence   = evt.confidence_level || 'HIGH';

        let triggersHtml = '';
        if (Array.isArray(evt.key_triggers_to_monitor) && evt.key_triggers_to_monitor.length > 0) {
          triggersHtml = `
            <div class="geo-section-block">
              <span class="geo-section-title">KEY TRIGGERS TO MONITOR:</span>
              <ul class="geo-triggers-list">
                ${evt.key_triggers_to_monitor.map(t => `<li>${escapeHtml(t)}</li>`).join('')}
              </ul>
            </div>
          `;
        }

        let assetTagsHtml = '';
        if (Array.isArray(evt.bullish_assets) && evt.bullish_assets.length > 0) {
          assetTagsHtml += `<div class="asset-bias-group"><span class="bias-label bullish-label">BULLISH ASSETS:</span><div class="asset-pills-wrap">${evt.bullish_assets.map(a => `<span class="asset-tag tag-bullish">${escapeHtml(a)}</span>`).join('')}</div></div>`;
        }
        if (Array.isArray(evt.bearish_assets) && evt.bearish_assets.length > 0) {
          assetTagsHtml += `<div class="asset-bias-group"><span class="bias-label bearish-label">BEARISH ASSETS:</span><div class="asset-pills-wrap">${evt.bearish_assets.map(a => `<span class="asset-tag tag-bearish">${escapeHtml(a)}</span>`).join('')}</div></div>`;
        }

        let windowsHtml = '';
        if (evt.earliest_impact_window || evt.full_impact_window || evt.peak_risk_window || evt.stabilisation_window || evt.recovery_window) {
          windowsHtml = `
            <div class="impact-windows-box">
              <span class="geo-section-title">TRANSMISSION HORIZON WINDOWS:</span>
              <div class="windows-grid">
                ${evt.earliest_impact_window ? `<div class="window-item"><span class="w-label">EARLIEST:</span> <span class="w-val">${escapeHtml(evt.earliest_impact_window)}</span></div>` : ''}
                ${evt.full_impact_window ? `<div class="window-item"><span class="w-label">FULL IMPACT:</span> <span class="w-val">${escapeHtml(evt.full_impact_window)}</span></div>` : ''}
                ${evt.peak_risk_window ? `<div class="window-item"><span class="w-label">PEAK RISK:</span> <span class="w-val">${escapeHtml(evt.peak_risk_window)}</span></div>` : ''}
                ${evt.stabilisation_window ? `<div class="window-item"><span class="w-label">STABILISATION:</span> <span class="w-val">${escapeHtml(evt.stabilisation_window)}</span></div>` : ''}
                ${evt.recovery_window ? `<div class="window-item"><span class="w-label">RECOVERY:</span> <span class="w-val">${escapeHtml(evt.recovery_window)}</span></div>` : ''}
              </div>
            </div>
          `;
        }

        // Label 'WHAT HAPPENED' differently for live vs mock
        const whatHappenedLabel = isLive ? 'INTELLIGENCE ASSESSMENT:' : 'ILLUSTRATIVE SCENARIO // WHAT HAPPENED:';

        const card = document.createElement('div');
        card.className = 'geo-event-card-item';
        card.innerHTML = `
          <div class="geo-card-header">
            <div class="geo-header-left">
              <span class="geo-region-tag">${escapeHtml(region)}</span>
              <h3 class="geo-card-title">${escapeHtml(title)}</h3>
            </div>
            <div class="geo-badges-wrap">
              <span class="badge-lifecycle ${lifecycleClass}">${escapeHtml(lifecycle)}</span>
              <span class="badge-severity ${severityClass}">${escapeHtml(severity)}</span>
            </div>
          </div>
          <div class="geo-card-body">
            <div class="geo-section-block">
              <span class="geo-section-title">${whatHappenedLabel}</span>
              <p class="geo-section-text">${escapeHtml(whatHappened)}</p>
            </div>
            <div class="geo-section-block">
              <span class="geo-section-title">MACRO &amp; ASSET TRANSMISSION MECHANISM:</span>
              <p class="geo-section-text transmission-text">${escapeHtml(transmission)}</p>
            </div>
            ${windowsHtml}
            ${triggersHtml}
            <div class="geo-assets-row">${assetTagsHtml}</div>
            <div class="geo-card-footer">
              <span class="confidence-badge">CONFIDENCE: <strong>${escapeHtml(confidence)}</strong></span>
            </div>
          </div>
        `;
        geoEventsListEl.appendChild(card);
      });
    } else {
      geoEventsListEl.innerHTML = '<p class="text-muted">No specific geopolitical events reported.</p>';
    }

    // 4. Event Lifecycle Matrix
    const eventLifecycleListEl = document.getElementById('eventLifecycleList');
    eventLifecycleListEl.innerHTML = '';
    if (Array.isArray(data.event_lifecycle) && data.event_lifecycle.length > 0) {
      data.event_lifecycle.forEach(item => {
        const stageName  = item.stage || 'ESCALATION';
        const chipClass  = getLifecycleChipClass(stageName);
        const momentum   = item.momentum || 'Stable';
        const div = document.createElement('div');
        div.className = 'lifecycle-card-item';
        div.innerHTML = `
          <div class="lifecycle-card-top">
            <h4 class="lifecycle-title">${escapeHtml(item.event || 'Crisis')}</h4>
            <div class="lifecycle-status-tags">
              <span class="badge-lifecycle ${chipClass}">${escapeHtml(stageName)}</span>
              <span class="momentum-tag">${escapeHtml(momentum)}</span>
            </div>
          </div>
          <p class="lifecycle-commentary">${escapeHtml(item.details || '')}</p>
        `;
        eventLifecycleListEl.appendChild(div);
      });
    } else {
      eventLifecycleListEl.innerHTML = '<p class="text-muted">No lifecycle items recorded.</p>';
    }

    // 5. Asset Impact Matrix
    const assetImpactBodyEl = document.getElementById('assetImpactBody');
    assetImpactBodyEl.innerHTML = '';
    if (Array.isArray(data.asset_impact) && data.asset_impact.length > 0) {
      data.asset_impact.forEach(item => {
        const assetName   = item.asset_name || item.asset_class || 'Asset';
        const direction   = item.direction || item.bias || 'VOLATILE';
        const dirClass    = `bias-${direction.toLowerCase()}`;
        const shortTerm   = item.short_term_outlook || '--';
        const sevenDay    = item.seven_day_scenario || '--';
        const driver      = item.main_driver || item.driver || '--';
        const risk        = item.risk_level || item.magnitude || 'MEDIUM';
        const riskClass   = `risk-${risk.toLowerCase()}`;
        const confidence  = item.confidence || 'HIGH';
        const explanation = item.explanation || driver;

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="asset-col"><strong class="asset-name-text">${escapeHtml(assetName)}</strong></td>
          <td><span class="bias-badge ${dirClass}">${escapeHtml(direction)}</span></td>
          <td class="outlook-col">${escapeHtml(shortTerm)}</td>
          <td class="scenario-col">${escapeHtml(sevenDay)}</td>
          <td class="driver-col">${escapeHtml(driver)}</td>
          <td><span class="risk-badge ${riskClass}">${escapeHtml(risk)}</span></td>
          <td><span class="conf-badge">${escapeHtml(confidence)}</span></td>
          <td class="explanation-col">${escapeHtml(explanation)}</td>
        `;
        assetImpactBodyEl.appendChild(tr);
      });
    } else {
      assetImpactBodyEl.innerHTML = '<tr><td colspan="8">No asset impact matrix available.</td></tr>';
    }

    // 6. Scenario Engine
    const scenariosGridEl = document.getElementById('scenariosGrid');
    scenariosGridEl.innerHTML = '';
    if (Array.isArray(data.scenarios) && data.scenarios.length > 0) {
      data.scenarios.forEach(sc => {
        const title    = sc.scenario_name || sc.scenario || 'Scenario';
        const prob     = sc.probability || '50%';
        const trigger  = sc.trigger || '--';
        const geoDev   = sc.geopolitical_development || '';
        const oilImp   = sc.oil_impact || '';
        const usdImp   = sc.usd_impact || '';
        const goldImp  = sc.gold_impact || '';
        const inImp    = sc.indian_market_impact || '';
        const invalid  = sc.what_would_invalidate || '';
        const mktCons  = sc.market_consequence || '';

        const card = document.createElement('div');
        card.className = 'scenario-card-item';
        card.innerHTML = `
          <div class="scenario-top">
            <h4 class="scenario-title">${escapeHtml(title)}</h4>
            <span class="scenario-prob-badge">${escapeHtml(prob)}</span>
          </div>
          <div class="scenario-body">
            <div class="scenario-item-block">
              <span class="sc-label">TRIGGER CATALYST:</span>
              <p class="sc-text">${escapeHtml(trigger)}</p>
            </div>
            ${geoDev ? `<div class="scenario-item-block"><span class="sc-label">GEOPOLITICAL DEVELOPMENT:</span><p class="sc-text">${escapeHtml(geoDev)}</p></div>` : ''}
            <div class="scenario-subgrid">
              ${oilImp ? `<div class="sc-subitem"><span class="sub-label">OIL IMPACT:</span> <span>${escapeHtml(oilImp)}</span></div>` : ''}
              ${usdImp ? `<div class="sc-subitem"><span class="sub-label">USD / DXY:</span> <span>${escapeHtml(usdImp)}</span></div>` : ''}
              ${goldImp ? `<div class="sc-subitem"><span class="sub-label">GOLD &amp; METALS:</span> <span>${escapeHtml(goldImp)}</span></div>` : ''}
              ${inImp ? `<div class="sc-subitem"><span class="sub-label">INDIAN MARKETS:</span> <span>${escapeHtml(inImp)}</span></div>` : ''}
            </div>
            ${mktCons ? `<div class="scenario-item-block"><span class="sc-label">MARKET CONSEQUENCE:</span><p class="sc-text">${escapeHtml(mktCons)}</p></div>` : ''}
            ${invalid ? `<div class="scenario-item-block invalidation-block"><span class="sc-label invalidation-label">INVALIDATION CRITERIA:</span><p class="sc-text invalidation-text">${escapeHtml(invalid)}</p></div>` : ''}
          </div>
        `;
        scenariosGridEl.appendChild(card);
      });
    } else {
      scenariosGridEl.innerHTML = '<p class="text-muted">No scenarios outlined.</p>';
    }

    // 7. Strategic Watchlist
    const watchlistGridEl = document.getElementById('watchlistGrid');
    watchlistGridEl.innerHTML = '';
    if (Array.isArray(data.watchlist) && data.watchlist.length > 0) {
      data.watchlist.forEach(item => {
        const div = document.createElement('div');
        div.className = 'watchlist-item-card';
        div.innerHTML = `<div class="watch-icon">📡</div><div class="watch-text">${escapeHtml(item)}</div>`;
        watchlistGridEl.appendChild(div);
      });
    } else {
      watchlistGridEl.innerHTML = '<p class="text-muted">No specific watchlist items.</p>';
    }

    // 8. Video Script
    const videoScriptBoxEl = document.getElementById('videoScriptBox');
    currentRawVideoScript = data.video_script || '';
    if (currentRawVideoScript) {
      videoScriptBoxEl.innerHTML = currentRawVideoScript
        .split('\n\n')
        .filter(p => p.trim().length > 0)
        .map(p => {
          const lines  = p.split('\n');
          const header = lines[0];
          const body   = lines.slice(1).join('<br>');
          return `<div class="script-scene-block"><div class="script-scene-header">${escapeHtml(header)}</div><p class="script-scene-body">${body}</p></div>`;
        })
        .join('');
    } else {
      videoScriptBoxEl.innerHTML = '<p class="text-muted">No teleprompter script generated.</p>';
    }

    // 9. Outlooks & What Changed
    document.getElementById('outlook24Content').innerHTML = formatParagraphs(data.outlook_24_72h);
    document.getElementById('outlook7dContent').innerHTML = formatParagraphs(data.outlook_7d);
    document.getElementById('whatChangedContent').innerHTML = formatParagraphs(data.what_changed);

    // 10. Key Dates
    const keyDatesListEl = document.getElementById('keyDatesList');
    keyDatesListEl.innerHTML = '';
    if (Array.isArray(data.key_dates) && data.key_dates.length > 0) {
      data.key_dates.forEach(kd => {
        const item = document.createElement('div');
        item.className = 'key-date-item';
        item.innerHTML = `
          <div class="date-badge">${escapeHtml(kd.date || 'TBD')}</div>
          <div class="date-details">
            <div class="date-event-text">${escapeHtml(kd.event || '')}</div>
            <span class="badge-severity ${getSeverityClass(kd.importance)}">${escapeHtml(kd.importance || 'HIGH')}</span>
          </div>
        `;
        keyDatesListEl.appendChild(item);
      });
    } else {
      keyDatesListEl.innerHTML = '<p class="text-muted">No imminent calendar dates scheduled.</p>';
    }

    // 11. Sources
    const sourcesListEl = document.getElementById('sourcesList');
    sourcesListEl.innerHTML = '';
    if (Array.isArray(data.sources) && data.sources.length > 0) {
      data.sources.forEach(src => {
        const el = document.createElement(src.url ? 'a' : 'span');
        el.className = 'source-badge';
        if (src.url) {
          el.href = src.url.startsWith('http') ? src.url : `https://${src.url}`;
          el.target = '_blank';
          el.rel = 'noopener noreferrer';
        }
        el.innerHTML = `📄 ${escapeHtml(src.name || 'Intelligence Feed')}`;
        sourcesListEl.appendChild(el);
      });
    } else {
      sourcesListEl.innerHTML = '<span class="source-badge">OSINT Intelligence Aggregators</span>';
    }

    // 12. Disclaimer
    const disclaimerEl = document.getElementById('disclaimerContent');
    const defaultDisclaimer = isLive
      ? 'LIVE AI REPORT: Intelligence synthesized via OpenAI web-search preview. Validate critical data before operational decisions.'
      : 'MOCK DEMONSTRATION DATA: All prices, events, projections, and scenarios are illustrative data for testing and evaluation only. NOT investment advice.';
    const disclaimerText = data.disclaimer || defaultDisclaimer;
    disclaimerEl.innerHTML = `<p class="disclaimer-alert-text">⚠ <strong>COMPLIANCE NOTICE:</strong> ${escapeHtml(disclaimerText)}</p>`;

    // Show report
    reportContainer.style.display = 'grid';
    reportContainer.scrollIntoView({ behavior: 'smooth' });

    setTimeout(() => { if (tacticalMap) tacticalMap.invalidateSize(); }, 200);
  }

  // ─── Export PDF ────────────────────────────────────────────────────────────
  if (exportPdfBtn) {
    exportPdfBtn.addEventListener('click', () => {
      if (!currentReportData) {
        showError('EXPORT NOTICE', 'Please run the War Room scan first before exporting.');
        return;
      }
      const orig = document.title;
      document.title = `GLOBAL_WAR_ROOM_${currentReportData.report_id || 'DOSSIER'}_${currentReportData.report_date || 'LATEST'}`;
      window.print();
      setTimeout(() => { document.title = orig; }, 1000);
    });
  }

  // ─── Export JSON ───────────────────────────────────────────────────────────
  if (exportJsonBtn) {
    exportJsonBtn.addEventListener('click', () => {
      if (!currentReportData) {
        showError('EXPORT NOTICE', 'No dossier data available to export.');
        return;
      }
      try {
        const blob = new Blob([JSON.stringify(currentReportData, null, 2)], { type: 'application/json' });
        const url  = URL.createObjectURL(blob);
        const a    = document.createElement('a');
        a.href     = url;
        a.download = `warroom-dossier-${currentReportData.report_id || 'data'}-${currentReportData.report_date || 'latest'}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (err) {
        showError('EXPORT FAILURE', 'Could not generate JSON file for download.');
      }
    });
  }

  // ─── Copy Script ───────────────────────────────────────────────────────────
  if (copyScriptBtn) {
    copyScriptBtn.addEventListener('click', () => {
      if (!currentRawVideoScript) return;
      navigator.clipboard.writeText(currentRawVideoScript)
        .then(() => {
          const orig = copyScriptBtn.textContent;
          copyScriptBtn.textContent = '✅ COPIED!';
          setTimeout(() => { copyScriptBtn.textContent = orig; }, 2000);
        })
        .catch(() => {
          showError('COPY FAILED', 'Could not copy to clipboard. Please select the text manually.');
        });
    });
  }

  // ─── Main Scan Trigger ─────────────────────────────────────────────────────
  async function triggerWarRoomScan() {
    startScanningAnimation();

    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) {
        let errMessage = `Server responded with status ${response.status}`;
        try {
          const errData = await response.json();
          if (errData?.message) errMessage = errData.message;
          else if (errData?.detail) errMessage = errData.detail;
        } catch (_) {}

        // Special handling for no-credits error in live mode
        if (response.status === 400 && errMessage.toLowerCase().includes('api key')) {
          errMessage += '\n\nTip: Click ⚙ SETTINGS → TEST API CREDITS to check your account, or switch to MOCK MODE for free operation.';
        }
        showError('WAR ROOM ENGINE ERROR', errMessage);
        return;
      }

      const reportData = await response.json();
      // Update UI mode after each scan (mode may differ from initial load)
      if (reportData.mode) applyModeToUI(reportData.mode, reportData.mode === 'mock');
      renderWarRoomReport(reportData);
      loadHistoryCount();

    } catch (err) {
      console.error('Fetch error:', err);
      showError(
        'NETWORK COMMUNICATION ERROR',
        'Could not reach the War Room backend server. Please ensure FastAPI is running on http://localhost:8000.'
      );
    }
  }

  runWarRoomBtn.addEventListener('click', triggerWarRoomScan);

  // Initialize Map
  initTacticalMap();

  // ==========================================================================
  // PHASE 4: HISTORICAL DOSSIER ARCHIVE & RUN COMPARISON ENGINE
  // ==========================================================================
  const historyToggleBtn      = document.getElementById('historyToggleBtn');
  const quickHistoryBtn       = document.getElementById('quickHistoryBtn');
  const historyDrawer         = document.getElementById('historyDrawer');
  const historyCloseBtn       = document.getElementById('historyCloseBtn');
  const historyOverlay        = document.getElementById('historyOverlay');
  const hudHistoryCount       = document.getElementById('hudHistoryCount');
  const historyTotalCount     = document.getElementById('historyTotalCount');
  const historyListContainer  = document.getElementById('historyListContainer');
  const slotA                 = document.getElementById('slotA');
  const slotAText             = document.getElementById('slotAText');
  const slotB                 = document.getElementById('slotB');
  const slotBText             = document.getElementById('slotBText');
  const launchCompareBtn      = document.getElementById('launchCompareBtn');
  const seedHistoryBtn        = document.getElementById('seedHistoryBtn');
  const historyCompareNote    = document.getElementById('historyCompareNote');
  const compareModal          = document.getElementById('compareModal');
  const compareModalCloseBtn  = document.getElementById('compareModalCloseBtn');
  const compareBackdrop       = document.getElementById('compareBackdrop');
  const compareModalBody      = document.getElementById('compareModalBody');

  let selectedRunA = null;
  let selectedRunB = null;
  let cachedRuns = [];

  async function loadHistoryCount() {
    try {
      const res = await fetch('/api/history');
      if (res.ok) {
        const data = await res.json();
        const count = data.count || (data.runs ? data.runs.length : 0);
        if (hudHistoryCount) hudHistoryCount.textContent = count;
        if (historyTotalCount) historyTotalCount.textContent = count;
        cachedRuns = data.runs || [];
      }
    } catch (err) {
      console.warn('Failed to load history count:', err);
    }
  }

  function openHistoryDrawer() {
    if (!historyDrawer || !historyOverlay) return;
    historyDrawer.style.display = 'block';
    historyOverlay.style.display = 'block';
    setTimeout(() => {
      historyDrawer.classList.add('open');
      historyOverlay.classList.add('open');
    }, 10);
    fetchAndRenderHistory();
  }

  function closeHistoryDrawer() {
    if (!historyDrawer || !historyOverlay) return;
    historyDrawer.classList.remove('open');
    historyOverlay.classList.remove('open');
    setTimeout(() => {
      historyDrawer.style.display = 'none';
      historyOverlay.style.display = 'none';
    }, 300);
  }

  async function fetchAndRenderHistory() {
    if (!historyListContainer) return;
    historyListContainer.innerHTML = '<div class="compare-empty-state">Loading intelligence archive from database...</div>';

    try {
      const res = await fetch('/api/history');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      cachedRuns = data.runs || [];

      if (hudHistoryCount) hudHistoryCount.textContent = cachedRuns.length;
      if (historyTotalCount) historyTotalCount.textContent = cachedRuns.length;

      renderHistoryCards(cachedRuns);
    } catch (err) {
      historyListContainer.innerHTML = `<div class="compare-empty-state" style="color: #fca5a5;">Failed to load archive: ${escapeHtml(err.message)}</div>`;
    }
  }

  function renderHistoryCards(runs) {
    if (!historyListContainer) return;
    if (!runs || runs.length === 0) {
      historyListContainer.innerHTML = `
        <div class="compare-empty-state">
          No archived dossier runs found.<br><br>
          Run a War Room scan or click <strong>[SEED SAMPLES]</strong> to populate multi-day fixtures.
        </div>
      `;
      return;
    }

    historyListContainer.innerHTML = '';
    runs.forEach(run => {
      const card = document.createElement('div');
      card.className = 'history-card';
      card.id = `historyCard-${run.id}`;

      if (selectedRunA && selectedRunA.id === run.id) card.classList.add('card-selected-a');
      if (selectedRunB && selectedRunB.id === run.id) card.classList.add('card-selected-b');

      const title = run.title || `Intelligence Dossier #${run.id}`;
      const snippet = run.executive_summary_snippet || 'Strategic intelligence synthesis across conflict theaters and assets.';
      const dateStr = run.report_date || (run.created_at ? run.created_at.slice(0, 10) : 'Unknown');

      card.innerHTML = `
        <div class="history-card-top">
          <span class="history-card-id">DOSSIER #${run.id}</span>
          <span class="history-card-date">📅 ${escapeHtml(dateStr)}</span>
        </div>
        <div class="history-card-title">${escapeHtml(title)}</div>
        <div class="history-card-summary">${escapeHtml(snippet)}</div>
        <div class="history-card-meta-row">
          <div class="history-chips">
            <span class="h-chip h-chip-crit">🔴 ${run.critical_events_count || 0} CRITICAL</span>
            <span class="h-chip h-chip-hot">🗺️ ${run.hotspots_count || 0} HOTSPOTS</span>
          </div>
          <div class="history-card-actions">
            <button class="h-btn-action h-btn-view" data-run-id="${run.id}" title="Load this full dossier into the dashboard">👁 VIEW</button>
            <button class="h-btn-action h-btn-slot ${selectedRunA && selectedRunA.id === run.id ? 'active-a' : ''}" data-slot="A" data-run-id="${run.id}" title="Set as Baseline (A)">+ A</button>
            <button class="h-btn-action h-btn-slot ${selectedRunB && selectedRunB.id === run.id ? 'active-b' : ''}" data-slot="B" data-run-id="${run.id}" title="Set as Target (B)">+ B</button>
          </div>
        </div>
      `;
      historyListContainer.appendChild(card);
    });

    historyListContainer.querySelectorAll('.h-btn-view').forEach(btn => {
      btn.addEventListener('click', () => {
        const runId = btn.getAttribute('data-run-id');
        loadHistoricalRunIntoDashboard(runId);
      });
    });

    historyListContainer.querySelectorAll('.h-btn-slot').forEach(btn => {
      btn.addEventListener('click', () => {
        const slot = btn.getAttribute('data-slot');
        const runId = parseInt(btn.getAttribute('data-run-id'), 10);
        const run = cachedRuns.find(r => r.id === runId);
        if (run) setComparisonSlot(slot, run);
      });
    });
  }

  function setComparisonSlot(slot, run) {
    if (slot === 'A') {
      selectedRunA = run;
      if (slotAText) slotAText.textContent = `#${run.id} (${run.report_date})`;
      if (slotA) slotA.classList.add('active');
    } else {
      selectedRunB = run;
      if (slotBText) slotBText.textContent = `#${run.id} (${run.report_date})`;
      if (slotB) slotB.classList.add('active');
    }

    if (selectedRunA && selectedRunB) {
      if (selectedRunA.id === selectedRunB.id) {
        if (launchCompareBtn) launchCompareBtn.disabled = true;
        if (historyCompareNote) historyCompareNote.textContent = '⚠ Baseline (A) and Target (B) must be different runs.';
      } else {
        if (launchCompareBtn) launchCompareBtn.disabled = false;
        if (historyCompareNote) historyCompareNote.textContent = `Ready: Comparing #${selectedRunA.id} (${selectedRunA.report_date}) against #${selectedRunB.id} (${selectedRunB.report_date})`;
      }
    } else {
      if (launchCompareBtn) launchCompareBtn.disabled = true;
    }

    if (cachedRuns.length > 0) renderHistoryCards(cachedRuns);
  }

  async function loadHistoricalRunIntoDashboard(runId) {
    try {
      closeHistoryDrawer();
      showError('LOADING DOSSIER', `Retrieving archived Dossier #${runId} from database...`);
      const res = await fetch(`/api/history/${runId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (!data.dossier) throw new Error('No dossier payload in response');

      dismissError();
      renderWarRoomReport(data.dossier);
    } catch (err) {
      showError('ARCHIVE LOAD ERROR', `Could not load historical dossier #${runId}: ${err.message}`);
    }
  }

  async function handleSeedSamples() {
    if (!seedHistoryBtn) return;
    const origText = seedHistoryBtn.textContent;
    seedHistoryBtn.textContent = '⏳ SEEDING...';
    seedHistoryBtn.disabled = true;

    try {
      const res = await fetch('/api/history/seed-samples', { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await fetchAndRenderHistory();
      if (historyCompareNote) historyCompareNote.textContent = '✅ Sample historical dossiers seeded successfully!';
    } catch (err) {
      if (historyCompareNote) historyCompareNote.textContent = `❌ Seeding failed: ${err.message}`;
    } finally {
      seedHistoryBtn.textContent = origText;
      seedHistoryBtn.disabled = false;
    }
  }

  async function launchRunComparison() {
    if (!selectedRunA || !selectedRunB) return;
    if (selectedRunA.id === selectedRunB.id) return;

    if (!compareModal || !compareBackdrop || !compareModalBody) return;

    compareModal.style.display = 'flex';
    compareBackdrop.style.display = 'block';
    compareModalBody.innerHTML = '<div class="compare-empty-state">Computing delta between dossiers...</div>';

    try {
      const res = await fetch(`/api/history/compare/${selectedRunA.id}/${selectedRunB.id}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const cmp = data.comparison;
      renderComparisonModal(cmp, selectedRunA, selectedRunB);
    } catch (err) {
      compareModalBody.innerHTML = `<div class="compare-empty-state" style="color: #fca5a5;">Failed to compute comparison: ${escapeHtml(err.message)}</div>`;
    }
  }

  function renderComparisonModal(cmp, runA, runB) {
    if (!compareModalBody) return;

    const runMetaA = cmp.run_a || runA;
    const runMetaB = cmp.run_b || runB;

    let html = `
      <div class="compare-meta-grid">
        <div class="compare-meta-card baseline">
          <div class="compare-meta-tag">BASELINE DOSSIER (A)</div>
          <div class="compare-meta-val">RUN #${runMetaA.id || runA.id} — ${escapeHtml(runMetaA.report_date || runA.report_date || '')}</div>
          <div class="compare-meta-sub">${escapeHtml(runMetaA.title || runA.title || '')}</div>
        </div>
        <div class="compare-meta-card target">
          <div class="compare-meta-tag">TARGET DOSSIER (B)</div>
          <div class="compare-meta-val">RUN #${runMetaB.id || runB.id} — ${escapeHtml(runMetaB.report_date || runB.report_date || '')}</div>
          <div class="compare-meta-sub">${escapeHtml(runMetaB.title || runB.title || '')}</div>
        </div>
      </div>
    `;

    if (cmp.what_changed_today_b) {
      html += `
        <div class="compare-section">
          <div class="compare-section-header">⚡ KEY INTEL SHIFTS & 24H DELTA (TARGET RUN)</div>
          <div class="compare-what-changed-box">${formatParagraphs(cmp.what_changed_today_b)}</div>
        </div>
      `;
    }

    html += `
      <div class="compare-section">
        <div class="compare-section-header">📈 CROSS-ASSET TRANSMISSION & BIAS DELTA</div>
    `;
    if (Array.isArray(cmp.asset_changes) && cmp.asset_changes.length > 0) {
      html += `
        <table class="compare-table">
          <thead>
            <tr>
              <th>ASSET CLASS</th>
              <th>CHANGE TYPE</th>
              <th>BASELINE BIAS</th>
              <th>TARGET BIAS</th>
              <th>TARGET MAGNITUDE</th>
              <th>CATALYST / DRIVER SHIFT</th>
            </tr>
          </thead>
          <tbody>
      `;
      cmp.asset_changes.forEach(ac => {
        const biasBeforeBadge = getBiasBadge(ac.bias_before);
        const biasAfterBadge = getBiasBadge(ac.bias_after);
        html += `
          <tr>
            <td><strong>${escapeHtml(ac.asset_class || '')}</strong></td>
            <td><span class="badge-severity ${ac.type === 'NEW' ? 'sev-high' : 'sev-elevated'}">${escapeHtml(ac.type || 'MODIFIED')}</span></td>
            <td>${biasBeforeBadge}</td>
            <td>${biasAfterBadge}</td>
            <td><span class="badge-magnitude mag-${(ac.magnitude_after || 'MED').toLowerCase()}">${escapeHtml(ac.magnitude_after || 'MEDIUM')}</span></td>
            <td><small>${escapeHtml(ac.driver_after || 'Catalyst realignment')}</small></td>
          </tr>
        `;
      });
      html += `</tbody></table>`;
    } else {
      html += `<div class="compare-empty-state">No direct asset bias deviations detected between these two runs.</div>`;
    }
    html += `</div>`;

    html += `
      <div class="compare-section">
        <div class="compare-section-header">🔄 CRISIS LIFECYCLE & TRAJECTORY SHIFTS</div>
    `;
    if (Array.isArray(cmp.lifecycle_shifts) && cmp.lifecycle_shifts.length > 0) {
      html += `
        <table class="compare-table">
          <thead>
            <tr>
              <th>EVENT / CRISIS</th>
              <th>CHANGE TYPE</th>
              <th>BASELINE STAGE</th>
              <th>TARGET STAGE</th>
              <th>TARGET TRAJECTORY</th>
            </tr>
          </thead>
          <tbody>
      `;
      cmp.lifecycle_shifts.forEach(ls => {
        html += `
          <tr>
            <td><strong>${escapeHtml(ls.event || '')}</strong></td>
            <td><span class="badge-severity ${ls.type === 'NEW' ? 'sev-critical' : 'sev-elevated'}">${escapeHtml(ls.type || 'SHIFTED')}</span></td>
            <td><code>${escapeHtml(ls.stage_before || '—')}</code></td>
            <td><strong style="color: var(--color-amber);">${escapeHtml(ls.stage_after || '—')}</strong></td>
            <td><span class="badge-shift-${(ls.momentum_after || '').toLowerCase().includes('accel') ? 'escalation' : 'neutral'}">${escapeHtml(ls.momentum_after || ls.details_after || 'Stable')}</span></td>
          </tr>
        `;
      });
      html += `</tbody></table>`;
    } else {
      html += `<div class="compare-empty-state">Crisis lifecycle stages remained consistent across both evaluation windows.</div>`;
    }
    html += `</div>`;

    if (Array.isArray(cmp.hotspot_shifts) && cmp.hotspot_shifts.length > 0) {
      html += `
        <div class="compare-section">
          <div class="compare-section-header">🗺️ STRATEGIC THEATER & CHOKEPOINT SHIFTS</div>
          <table class="compare-table">
            <thead>
              <tr>
                <th>THEATER / LOCATION</th>
                <th>DELTA</th>
                <th>BASELINE THREAT</th>
                <th>TARGET THREAT</th>
              </tr>
            </thead>
            <tbody>
      `;
      cmp.hotspot_shifts.forEach(hs => {
        html += `
          <tr>
            <td><strong>${escapeHtml(hs.name || '')}</strong></td>
            <td><span class="badge-severity sev-elevated">${escapeHtml(hs.type || 'MODIFIED')}</span></td>
            <td>${escapeHtml(hs.threat_before || '—')}</td>
            <td><strong style="color: #fca5a5;">${escapeHtml(hs.threat_after || '—')}</strong></td>
          </tr>
        `;
      });
      html += `</tbody></table></div>`;
    }

    compareModalBody.innerHTML = html;
  }

  function getBiasBadge(bias) {
    const b = (bias || '').toUpperCase();
    if (b.includes('BULL')) return `<span class="badge-shift-bullish">🟢 ${escapeHtml(b)}</span>`;
    if (b.includes('BEAR')) return `<span class="badge-shift-bearish">🔴 ${escapeHtml(b)}</span>`;
    return `<span class="badge-shift-neutral">⚪ ${escapeHtml(b || 'NEUTRAL')}</span>`;
  }

  function closeCompareModal() {
    if (compareModal) compareModal.style.display = 'none';
    if (compareBackdrop) compareBackdrop.style.display = 'none';
  }

  if (historyToggleBtn) historyToggleBtn.addEventListener('click', openHistoryDrawer);
  if (quickHistoryBtn) quickHistoryBtn.addEventListener('click', openHistoryDrawer);
  if (historyCloseBtn) historyCloseBtn.addEventListener('click', closeHistoryDrawer);
  if (historyOverlay) historyOverlay.addEventListener('click', closeHistoryDrawer);
  if (seedHistoryBtn) seedHistoryBtn.addEventListener('click', handleSeedSamples);
  if (launchCompareBtn) launchCompareBtn.addEventListener('click', launchRunComparison);
  if (compareModalCloseBtn) compareModalCloseBtn.addEventListener('click', closeCompareModal);
  if (compareBackdrop) compareBackdrop.addEventListener('click', closeCompareModal);

  loadHistoryCount();
});
