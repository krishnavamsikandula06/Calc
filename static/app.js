const exprInput = document.getElementById('expr')
const resultEl = document.getElementById('result')
const historyEl = document.getElementById('history')

function appendHistory(expr, out) {
  const el = document.createElement('div')
  el.textContent = `${expr} = ${out}`
  historyEl.prepend(el)
}

document.querySelectorAll('[data-insert]').forEach(b => {
  b.addEventListener('click', () => {
    const v = b.getAttribute('data-insert')
    const start = exprInput.selectionStart
    const end = exprInput.selectionEnd
    const before = exprInput.value.slice(0, start)
    const after = exprInput.value.slice(end)
    exprInput.value = before + v + after
    exprInput.focus()
    exprInput.selectionStart = exprInput.selectionEnd = start + v.length
  })
})

document.getElementById('clear').addEventListener('click', () => {
  exprInput.value = ''
  resultEl.textContent = ''
})

document.getElementById('back').addEventListener('click', () => {
  exprInput.value = exprInput.value.slice(0, -1)
})

document.getElementById('eval').addEventListener('click', doEval)
exprInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') { e.preventDefault(); doEval() }
})

function doEval() {
  const expr = exprInput.value.trim()
  if (!expr) return
  fetch('/api/calc', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ expr })
  }).then(r => r.json())
    .then(data => {
      if (data.error) {
        resultEl.textContent = 'Error: ' + data.error
        resultEl.style.color = 'crimson'
      } else {
        resultEl.textContent = data.result
        resultEl.style.color = '#111'
        appendHistory(expr, data.result)
      }
    }).catch(err => {
      resultEl.textContent = 'Network error'
      resultEl.style.color = 'crimson'
    })
}
