const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')

const userDataPath = path.join(__dirname, '..', 'app-data')
if (!fs.existsSync(userDataPath)) fs.mkdirSync(userDataPath, { recursive: true })

app.setPath('userData', path.join(__dirname, '..', 'app-data'))

function loadCSV() {
  const filePath = path.join(__dirname, '..', 'data', 'merged.csv')
  const raw = fs.readFileSync(filePath, 'utf-8')
  const lines = raw.trim().split('\n')
  const headers = lines[0].split(',')
  return lines.slice(1).map(line => {
    const vals = line.split(',')
    const obj = {}
    headers.forEach((h, i) => obj[h.trim()] = vals[i]?.trim() ?? '')
    return obj
  })
}

app.whenReady().then(() => {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'))
})

ipcMain.handle('get-entries', () => loadCSV())