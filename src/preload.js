const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  getEntries: () => ipcRenderer.invoke('get-entries')
})