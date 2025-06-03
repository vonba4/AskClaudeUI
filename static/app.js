async function loadConfig() {
  const res = await fetch('/config');
  const data = await res.json();
  document.getElementById('instructionInput').value = data.instruction || "";
  document.getElementById('temperatureInput').value = data.temperature ?? 1.0;
}

async function loadModels() {
  const res = await fetch('/models');
  const data = await res.json();
  const select = document.getElementById('modelSelect');
  select.innerHTML = '';
  data.models.forEach(model => {
    const opt = document.createElement('option');
    opt.value = model;
    opt.textContent = model;
    if (model === data.selected) opt.selected = true;
    select.appendChild(opt);
  });
}

window.onload = async function() {
  await loadModels();
  await loadConfig();
};

document.getElementById('modelSelect').onchange = async function() {
  const model = this.value;
  await fetch('/set_model', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({model})
  });
};

document.getElementById('saveInstructionBtn').onclick = async function() {
  const instruction = document.getElementById('instructionInput').value;
  await fetch('/set_instruction', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({instruction})
  });
};

document.getElementById('saveTemperatureBtn').onclick = async function() {
  const temperature = parseFloat(document.getElementById('temperatureInput').value);
  if (isNaN(temperature) || temperature < 0 || temperature > 1.0) {
    alert("Temperature must be between 0 and 1.0");
    return;
  }
  await fetch('/set_temperature', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({temperature})
  });
};

document.getElementById('promptForm').onsubmit = async function(e) {
  e.preventDefault();
  const resultElem = document.getElementById('result');
  resultElem.value = "Processing...";
  const prompt = this.prompt.value;
  const res = await fetch('/prompt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt})
  });
  const data = await res.json();
  resultElem.value = data.content || "No response";
};