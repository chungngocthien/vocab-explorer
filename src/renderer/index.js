let allEntries = []
let currentBlock = 0
const BLOCK_SIZE = 100

function parseCSV(raw) {
  const lines = raw.trim().split('\n')
  const headers = lines[0].split(',').map(h => h.trim())
  const result = []
  for (let i = 1; i < lines.length; i++) {
    const cols = []
    let cur = '', inQuote = false
    for (const ch of lines[i]) {
      if (ch === '"') { inQuote = !inQuote }
      else if (ch === ',' && !inQuote) { cols.push(cur.trim()); cur = '' }
      else cur += ch
    }
    cols.push(cur.trim())
    const obj = {}
    headers.forEach((h, idx) => obj[h] = cols[idx] ?? '')
    result.push(obj)
  }
  return result
}

function zipfColor(val) {
  const n = Math.floor(parseFloat(val))
  if (n >= 7) return '#e2c97e'
  if (n === 6) return '#7eb8a0'
  if (n === 5) return '#7a9cbf'
  if (n === 4) return '#8a7aaa'
  return '#666666'
}

function zipfBadge(val) {
  if (!val || val === '') return '<span class="badge empty">—</span>'
  const color = zipfColor(val)
  return `<span class="badge" style="color:${color};border-color:${color}40">${parseFloat(val).toFixed(2)}</span>`
}

function cefrBadge(val) {
  if (!val || val === '') return '<span class="badge empty">—</span>'
  const cls = 'cefr' + val.replace(/[^A-Z0-9]/g, '')
  return `<span class="badge ${cls}">${val}</span>`
}

async function init() {
  allEntries = await window.api.getEntries()
  renderList()

  document.getElementById('page-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      const v = parseInt(e.target.value)
      const max = Math.ceil(allEntries.length / BLOCK_SIZE)
      if (!isNaN(v) && v >= 1 && v <= max) {
        currentBlock = v - 1
        renderList()
      }
    }
  })
}

function renderList() {
  const start = currentBlock * BLOCK_SIZE
  const slice = allEntries.slice(start, start + BLOCK_SIZE)
  document.getElementById('list').innerHTML = slice.map((e, i) => `
    <div class="word-row">
      <div class="rank">${start + i + 1}</div>
      <div class="word">${e.word}</div>
      <div class="pos">${e.ox_pos || '—'}</div>
      ${cefrBadge(e.ox_cefr)}
      ${zipfBadge(e.wf_zipf)}
      ${zipfBadge(e.sub_zipf)}
    </div>
  `).join('')
  document.getElementById('stats').textContent =
    `${allEntries.length} entries · page ${currentBlock + 1} of ${Math.ceil(allEntries.length / BLOCK_SIZE)}`
}

init()