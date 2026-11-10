// UI state and event wiring
let scenariosCache = [];

document.addEventListener('DOMContentLoaded', async () => {
  wireWindowControls();
  wireTabs();
  wireExecutionHandlers();
  loadSettings();
  await refreshScenarios();
  await refreshReports();
});

function wireWindowControls() {
  document.getElementById('btn-minimize').onclick = () => window.harnessApi?.minimizeWindow();
  document.getElementById('btn-maximize').onclick = () => window.harnessApi?.maximizeWindow();
  document.getElementById('btn-close').onclick = () => window.harnessApi?.closeWindow();
}

function wireTabs() {
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(`view-${btn.dataset.tab}`);
      if (target) target.classList.add('active');
    };
  });
}

function wireExecutionHandlers() {
  const btnRun = document.getElementById('btn-run');
  const btnStop = document.getElementById('btn-stop');
  const btnClear = document.getElementById('btn-clear-log');
  const termStream = document.getElementById('terminal-stream');

  btnClear.onclick = () => { termStream.innerHTML = ''; };

  btnRun.onclick = async () => {
    const url = document.getElementById('input-url').value.trim();
    const goal = document.getElementById('input-goal').value.trim();
    if (!url || !goal) return;

    btnRun.disabled = true;
    btnStop.disabled = false;
    updateStatusPill('RUNNING');

    const env = getActiveEnvOverrides();
    await window.harnessApi?.runPrompt(url, goal, 'desktop_run', env);
  };

  btnStop.onclick = async () => {
    await window.harnessApi?.stopExecution();
    btnStop.disabled = true;
    btnRun.disabled = false;
  };

  // Wire stream events
  window.harnessApi?.onLog(({ stream, content }) => {
    const line = document.createElement('div');
    line.className = `log-line ${stream === 'stderr' ? 'log-stderr' : ''}`;
    line.textContent = content.trim();
    termStream.appendChild(line);
    termStream.scrollTop = termStream.scrollHeight;
  });

  window.harnessApi?.onStatus(({ status, message }) => {
    updateStatusPill(status);
    if (status !== 'RUNNING') {
      btnRun.disabled = false;
      btnStop.disabled = true;
    }
  });

  document.getElementById('select-scenario-quick').onchange = (e) => {
    const selected = scenariosCache.find(s => s.file === e.target.value);
    if (selected) {
      document.getElementById('input-url').value = selected.start_url || '';
      document.getElementById('input-goal').value = selected.goal || '';
    }
  };
}

async function refreshScenarios() {
  const quickSelect = document.getElementById('select-scenario-quick');
  const list = await window.harnessApi?.listScenarios() || [];
  scenariosCache = list;
  quickSelect.innerHTML = '<option value="">Load Preset Scenario...</option>';
  list.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.file;
    opt.textContent = `${s.name} (${s.file})`;
    quickSelect.appendChild(opt);
  });
}

async function refreshReports() {
  const container = document.getElementById('reports-list');
  const reports = await window.harnessApi?.listReports() || [];
  container.innerHTML = reports.length === 0
    ? '<p class="empty-state">No execution reports recorded yet.</p>'
    : reports.map(r => `
      <div class="report-card">
        <strong>${r.scenario || r.file}</strong>:
        <span class="status-badge status-${(r.status || 'unknown').toLowerCase()}">${r.status}</span>
        <small>${r.duration_seconds ? r.duration_seconds + 's' : ''}</small>
      </div>
    `).join('');
}

function updateStatusPill(status) {
  const pill = document.getElementById('status-pill');
  pill.textContent = status;
  pill.className = `status-badge status-${status.toLowerCase()}`;
}

function loadSettings() {
  const url = localStorage.getItem('ai_base_url') || 'https://api.deepseek.com/v1';
  const key = localStorage.getItem('ai_api_key') || '';
  const model = localStorage.getItem('ai_model_name') || 'deepseek-chat';
  const headless = localStorage.getItem('headless') !== 'false';

  document.getElementById('setting-base-url').value = url;
  document.getElementById('setting-api-key').value = key;
  document.getElementById('setting-model').value = model;
  document.getElementById('setting-headless').checked = headless;
  document.getElementById('active-model-pill').textContent = model;

  document.getElementById('btn-save-settings').onclick = () => {
    localStorage.setItem('ai_base_url', document.getElementById('setting-base-url').value);
    localStorage.setItem('ai_api_key', document.getElementById('setting-api-key').value);
    localStorage.setItem('ai_model_name', document.getElementById('setting-model').value);
    localStorage.setItem('headless', document.getElementById('setting-headless').checked);
    document.getElementById('active-model-pill').textContent = document.getElementById('setting-model').value;
    alert('Settings successfully updated');
  };
}

function getActiveEnvOverrides() {
  return {
    AI_BASE_URL: document.getElementById('setting-base-url').value,
    AI_API_KEY: document.getElementById('setting-api-key').value,
    AI_MODEL_NAME: document.getElementById('setting-model').value,
    HEADLESS: document.getElementById('setting-headless').checked ? 'true' : 'false'
  };
}
