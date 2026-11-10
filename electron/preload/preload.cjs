const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('harnessApi', {
  // Window Controls
  minimizeWindow: () => ipcRenderer.invoke('window:minimize'),
  maximizeWindow: () => ipcRenderer.invoke('window:maximize'),
  closeWindow: () => ipcRenderer.invoke('window:close'),

  // Scenarios Management
  listScenarios: () => ipcRenderer.invoke('scenarios:list'),
  saveScenario: (filename, data) => ipcRenderer.invoke('scenarios:save', { filename, data }),

  // Reports
  listReports: () => ipcRenderer.invoke('reports:list'),

  // Execution
  runScenario: (scenarioPath, env) => ipcRenderer.invoke('harness:run-scenario', { scenarioPath, env }),
  runPrompt: (url, goal, name, env) => ipcRenderer.invoke('harness:run-prompt', { url, goal, name, env }),
  stopExecution: () => ipcRenderer.invoke('harness:stop'),

  // Real-time Event Streaming
  onLog: (callback) => {
    const handler = (_, data) => callback(data);
    ipcRenderer.on('harness:log', handler);
    return () => ipcRenderer.removeListener('harness:log', handler);
  },
  onStatus: (callback) => {
    const handler = (_, data) => callback(data);
    ipcRenderer.on('harness:status', handler);
    return () => ipcRenderer.removeListener('harness:status', handler);
  }
});
