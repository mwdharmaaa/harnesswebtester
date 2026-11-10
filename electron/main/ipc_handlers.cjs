const { ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

function setupIpcHandlers(mainWindow, processBridge) {
  const projectRoot = path.resolve(__dirname, '../../');
  const scenariosDir = path.join(projectRoot, 'scenarios');
  const reportsDir = path.join(projectRoot, 'reports');

  // Window Controls
  ipcMain.handle('window:minimize', () => mainWindow.minimize());
  ipcMain.handle('window:maximize', () => {
    if (mainWindow.isMaximized()) mainWindow.unmaximize();
    else mainWindow.maximize();
  });
  ipcMain.handle('window:close', () => mainWindow.close());

  // Scenarios Management
  ipcMain.handle('scenarios:list', async () => {
    if (!fs.existsSync(scenariosDir)) return [];
    const files = fs.readdirSync(scenariosDir).filter(f => f.endsWith('.json'));
    return files.map(file => {
      const fullPath = path.join(scenariosDir, file);
      try {
        const content = JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
        return { file, path: fullPath, ...content };
      } catch (_) {
        return { file, path: fullPath, name: file, description: 'Parse error' };
      }
    });
  });

  ipcMain.handle('scenarios:save', async (_, { filename, data }) => {
    if (!fs.existsSync(scenariosDir)) fs.mkdirSync(scenariosDir, { recursive: true });
    const targetFile = filename.endsWith('.json') ? filename : `${filename}.json`;
    const fullPath = path.join(scenariosDir, targetFile);
    fs.writeFileSync(fullPath, JSON.stringify(data, null, 2), 'utf-8');
    return { success: true, path: fullPath };
  });

  // Reports Management
  ipcMain.handle('reports:list', async () => {
    if (!fs.existsSync(reportsDir)) return [];
    const files = fs.readdirSync(reportsDir).filter(f => f.endsWith('.json'));
    return files.map(file => {
      const fullPath = path.join(reportsDir, file);
      try {
        const content = JSON.parse(fs.readFileSync(fullPath, 'utf-8'));
        return { file, ...content };
      } catch (_) {
        return { file, scenario: file, status: 'UNKNOWN' };
      }
    });
  });

  // Execution Handlers
  ipcMain.handle('harness:run-scenario', async (_, { scenarioPath, env }) => {
    return processBridge.runScenario(scenarioPath, env);
  });

  ipcMain.handle('harness:run-prompt', async (_, { url, goal, name, env }) => {
    return processBridge.runPrompt(url, goal, name, env);
  });

  ipcMain.handle('harness:stop', async () => {
    return processBridge.stopExecution();
  });
}

module.exports = { setupIpcHandlers };
