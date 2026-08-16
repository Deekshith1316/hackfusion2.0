async function loadPatients() {
  const response = await fetch('/api/patients');
  const result = await response.json();

  const patientGrid = document.getElementById('patientGrid');
  const stableCount = document.getElementById('stableCount');
  const watchCount = document.getElementById('watchCount');
  const criticalCount = document.getElementById('criticalCount');
  const liveAlerts = document.getElementById('liveAlerts');
  const avgRisk = document.getElementById('avgRisk');
  const generatedAt = document.getElementById('generatedAt');

  stableCount.textContent = result.summary.stable;
  watchCount.textContent = result.summary.watch;
  criticalCount.textContent = result.summary.critical;
  liveAlerts.textContent = result.summary.critical + result.summary.watch;

  const avg = Math.round(
    result.patients.reduce((sum, patient) => sum + patient.riskScore, 0) / result.patients.length
  );
  avgRisk.textContent = `${avg}%`;
  generatedAt.textContent = `Updated ${new Date(result.generatedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

  patientGrid.innerHTML = result.patients
    .map((patient) => {
      const badgeClass = patient.riskLevel === 'Critical' ? 'badge-critical' : patient.riskLevel === 'Watch' ? 'badge-watch' : 'badge-stable';
      const cardClass = patient.riskLevel === 'Critical' ? 'critical' : patient.riskLevel === 'Watch' ? 'watch' : 'stable';

      return `
        <article class="patient-card ${cardClass}">
          <div class="patient-header">
            <div>
              <h4 class="patient-name">${patient.name}</h4>
              <p class="patient-meta">${patient.condition} • ${patient.location}</p>
            </div>
            <span class="patient-badge ${badgeClass}">${patient.riskLevel}</span>
          </div>

          <div class="risk-box">
            <div>
              <span>AI risk score</span>
              <strong>${patient.riskScore}%</strong>
            </div>
            <div>
              <span>Alert</span>
              <strong>${patient.alert}</strong>
            </div>
          </div>

          <div class="metric-list">
            <div class="metric-row"><span>Heart rate</span><strong>${patient.heartRate} bpm</strong></div>
            <div class="metric-row"><span>SpO2</span><strong>${patient.spo2}%</strong></div>
            <div class="metric-row"><span>Temperature</span><strong>${patient.temperature}°C</strong></div>
            <div class="metric-row"><span>Blood pressure</span><strong>${patient.bloodPressure} mmHg</strong></div>
            <div class="metric-row"><span>Respiration</span><strong>${patient.respiration}/min</strong></div>
          </div>

          <div class="alert-panel">
            <strong>AI recommendation</strong>
            <p>${patient.recommendation}</p>
          </div>
        </article>
      `;
    })
    .join('');
}

window.addEventListener('DOMContentLoaded', () => {
  loadPatients();
  setInterval(loadPatients, 8000);
});
