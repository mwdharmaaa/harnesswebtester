const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class ProcessBridge {
  constructor(mainWindow) {
    this.mainWindow = mainWindow;
    this.activeProcess = null;
  }

  runScenario(scenarioPath, envOverrides = {}) {
    const projectRoot = path.resolve(__dirname, '../../');
    const fullScenarioPath = path.isAbsolute(scenarioPath)
      ? scenarioPath
      : path.join(projectRoot, scenarioPath);

    return this._spawnHarness(['-m', 'src.cli', 'run', fullScenarioPath], envOverrides);
  }

  runPrompt(url, goal, name = 'adhoc_test', envOverrides = {}) {
    return this._spawnHarness([
      '-m', 'src.cli', 'prompt',
      '--url', url,
      '--goal', goal,
      '--name', name
    ], envOverrides);
  }

  stopExecution() {
    if (this.activeProcess) {
      this.activeProcess.kill('SIGTERM');
      this.activeProcess = null;
      this._emitStatus('STOPPED', 'Execution manually halted by user');
      return true;
    }
    return false;
  }

  _spawnHarness(args, envOverrides) {
    if (this.activeProcess) {
      this.stopExecution();
    }

    const projectRoot = path.resolve(__dirname, '../../');
    const venvPythonWin = path.join(projectRoot, '.venv/Scripts/python.exe');
    const venvPythonUnix = path.join(projectRoot, '.venv/bin/python');
    
    let pythonExecutable = 'python';
    if (process.platform === 'win32' && fs.existsSync(venvPythonWin)) {
      pythonExecutable = venvPythonWin;
    } else if (fs.existsSync(venvPythonUnix)) {
      pythonExecutable = venvPythonUnix;
    }

    const mergedEnv = {
      ...process.env,
      PYTHONUNBUFFERED: '1',
      PYTHONPATH: projectRoot,
      ...envOverrides
    };

    this._emitStatus('RUNNING', 'Starting autonomous testing process...');

    this.activeProcess = spawn(pythonExecutable, args, {
      cwd: projectRoot,
      env: mergedEnv
    });

    this.activeProcess.stdout.on('data', (data) => {
      const text = data.toString();
      this._emitLog('stdout', text);
    });

    this.activeProcess.stderr.on('data', (data) => {
      const text = data.toString();
      this._emitLog('stderr', text);
    });

    this.activeProcess.on('close', (code) => {
      this.activeProcess = null;
      const status = code === 0 ? 'PASSED' : 'FAILED';
      this._emitStatus(status, `Process exited with code ${code}`);
    });

    return { status: 'started' };
  }

  _emitLog(stream, content) {
    if (this.mainWindow && !this.mainWindow.isDestroyed()) {
      this.mainWindow.webContents.send('harness:log', { stream, content, timestamp: new Date().toISOString() });
    }
  }

  _emitStatus(status, message) {
    if (this.mainWindow && !this.mainWindow.isDestroyed()) {
      this.mainWindow.webContents.send('harness:status', { status, message, timestamp: new Date().toISOString() });
    }
  }
}

module.exports = { ProcessBridge };
