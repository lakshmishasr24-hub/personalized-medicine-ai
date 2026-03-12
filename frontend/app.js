const form = document.getElementById('health-form');
const resultSection = document.getElementById('result-section');
const steps = document.querySelectorAll('.form-step');
const nextBtns = document.querySelectorAll('.next-btn');
const prevBtns = document.querySelectorAll('.prev-btn');

// 1. Navigation Logic
nextBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const currentStep = btn.closest('.form-step');
        const nextStep = currentStep.nextElementSibling;
        if (nextStep && nextStep.classList.contains('form-step')) {
            currentStep.classList.remove('active');
            nextStep.classList.add('active');
        }
    });
});

prevBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const currentStep = btn.closest('.form-step');
        const prevStep = currentStep.previousElementSibling;
        if (prevStep && prevStep.classList.contains('form-step')) {
            currentStep.classList.remove('active');
            prevStep.classList.add('active');
        }
    });
});

// 2. Submission Logic
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        weight: parseFloat(document.getElementById('weight').value),
        height: parseFloat(document.getElementById('height').value),
        blood_group: document.getElementById('blood_group').value,

        existing_conditions: document.getElementById('conditions').value.split(',').map(s => s.trim()).filter(s => s),
        family_history: document.getElementById('family_history').value.split(',').map(s => s.trim()).filter(s => s),
        previous_surgeries: [],
        allergies: document.getElementById('allergies').value.split(',').map(s => s.trim()).filter(s => s),

        symptoms: document.getElementById('symptoms').value.split(',').map(s => s.trim()).filter(s => s),

        smoking_status: document.getElementById('smoking').value,
        alcohol_consumption: document.getElementById('alcohol').value,
        exercise_frequency: document.getElementById('exercise').value,
        sleep_hours: parseInt(document.getElementById('sleep').value),
        diet_type: "Balanced", // Defaulted for simplicity in UI

        blood_pressure_sys: parseInt(document.getElementById('bp_sys').value || 120),
        blood_pressure_dia: parseInt(document.getElementById('bp_dia').value || 80),
        blood_sugar: parseInt(document.getElementById('sugar').value || 100),
        cholesterol: parseInt(document.getElementById('cholesterol').value || 200),
        heart_rate: parseInt(document.getElementById('heart_rate').value || 72),
        oxygen_saturation: parseInt(document.getElementById('oxygen').value || 98)
    };

    const submitBtn = document.getElementById('submit-btn');
    submitBtn.textContent = "Processing Biometric Data...";
    submitBtn.disabled = true;

    try {
        const response = await fetch('https://med-rec-api.onrender.com', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Backend Analysis Failed');

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error(error);
        alert('Connectivity Error: Make sure the AI Engine is running.');
    } finally {
        submitBtn.textContent = "Run AI Analysis";
        submitBtn.disabled = false;
    }
});

function displayResults(result) {
    form.classList.add('hidden');
    resultSection.classList.remove('hidden');

    document.getElementById('disease-type').textContent = result.disease_prediction;
    document.getElementById('treatment-text').textContent = result.recommended_treatment;

    const score = Math.round(result.risk_score * 100);
    document.getElementById('risk-percent').textContent = `${score}%`;
    document.getElementById('risk-fill').style.width = `${score}%`;

    // Explanation list
    const explList = document.getElementById('explanation-list');
    explList.innerHTML = '';
    result.explanation_details.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        explList.appendChild(li);
    });

    const medList = document.getElementById('medication-list');
    medList.innerHTML = '';
    result.suggested_medicines.forEach(med => {
        const li = document.createElement('li');
        li.textContent = med;
        medList.appendChild(li);
    });

    // Badge styling
    const badge = document.getElementById('risk-badge');
    if (score > 60) {
        badge.style.background = "var(--danger)";
        badge.textContent = "Critical Risk";
    } else if (score > 30) {
        badge.style.background = "var(--warning)";
        badge.textContent = "Moderate Concern";
    } else {
        badge.style.background = "var(--success)";
        badge.textContent = "Healthy Profile";
    }

    resultSection.scrollIntoView({ behavior: 'smooth' });
}
