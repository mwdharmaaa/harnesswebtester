const { app, BrowserWindow } = require('electron');
const path = require('path');
const { ProcessBridge } = require('./process_bridge.cjs');
const { setupIpcHandlers } = require('./ipc_handlers.cjs');

let mainWindow = null;
let processBridge = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 900,
    minHeight: 600,
    title: 'AI Web Test Harness',
    backgroundColor: '#0c0c0e',
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, '../preload/preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  processBridge = new ProcessBridge(mainWindow);
  setupIpcHandlers(mainWindow, processBridge);

  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));

  mainWindow.webContents.on('will-navigate', (event, navigationUrl) => {
    try {
      const parsedUrl = new URL(navigationUrl);
      if (parsedUrl.protocol !== 'file:') {
        event.preventDefault();
      }
    } catch (_) {
      event.preventDefault();
    }
  });

  mainWindow.on('closed', () => {
    if (processBridge) {
      processBridge.stopExecution();
    }
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
