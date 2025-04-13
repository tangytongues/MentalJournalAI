/**
 * Journal entry related functions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the journal page functionality
    initJournalPage();
    
    // Initialize the entry view page functionality if on that page
    if (document.getElementById('entry-view')) {
        initEntryView();
    }
});

function initJournalPage() {
    const journalForm = document.getElementById('journal-form');
    const titleInput = document.getElementById('entry-title');
    const contentTextarea = document.getElementById('entry-content');
    const charCounter = document.getElementById('char-counter');
    const submitButton = document.getElementById('submit-entry');
    
    // If we're not on the journal page, return
    if (!journalForm) return;
    
    // Character counter for journal entries
    if (contentTextarea && charCounter) {
        contentTextarea.addEventListener('input', function() {
            const charCount = contentTextarea.value.length;
            charCounter.textContent = `${charCount} characters`;
            
            // Visual feedback based on entry length
            if (charCount < 20) {
                charCounter.className = 'text-danger';
            } else if (charCount < 100) {
                charCounter.className = 'text-warning';
            } else {
                charCounter.className = 'text-success';
            }
        });
    }
    
    // Form validation
    if (journalForm) {
        journalForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate title
            if (!titleInput.value.trim()) {
                showValidationError(titleInput, 'Please enter a title for your journal entry');
                isValid = false;
            } else {
                hideValidationError(titleInput);
            }
            
            // Validate content
            if (!contentTextarea.value.trim()) {
                showValidationError(contentTextarea, 'Please write something in your journal entry');
                isValid = false;
            } else if (contentTextarea.value.trim().length < 20) {
                showValidationError(contentTextarea, 'Your entry is too short. Please write at least 20 characters');
                isValid = false;
            } else {
                hideValidationError(contentTextarea);
            }
            
            if (!isValid) {
                event.preventDefault();
            } else {
                // Show loading state
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
            }
        });
    }
}

function initEntryView() {
    // Initialize emotion chart if the element exists
    const emotionChartEl = document.getElementById('emotion-chart');
    if (emotionChartEl) {
        const emotionData = JSON.parse(emotionChartEl.dataset.emotions);
        createEmotionChart(emotionChartEl, emotionData);
    }
}

function createEmotionChart(element, emotionData) {
    // Extract labels and values from the emotion data
    const labels = Object.keys(emotionData);
    const values = Object.values(emotionData);
    
    // Define colors for each emotion category
    const colorMap = {
        'joy': '#FFC107',
        'sadness': '#6C757D',
        'anger': '#DC3545',
        'fear': '#6610F2',
        'surprise': '#17A2B8',
        'disgust': '#198754',
        'trust': '#0D6EFD',
        'anticipation': '#FD7E14',
        'neutral': '#ADB5BD'
    };
    
    // Create array of colors based on labels
    const colors = labels.map(label => colorMap[label] || '#ADB5BD');
    
    // Create the chart
    new Chart(element, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                }
            }
        }
    });
}

function showValidationError(inputElement, message) {
    // Find or create the feedback element
    let feedback = inputElement.nextElementSibling;
    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        inputElement.parentNode.insertBefore(feedback, inputElement.nextSibling);
    }
    
    // Set the message and show the error
    feedback.textContent = message;
    inputElement.classList.add('is-invalid');
}

function hideValidationError(inputElement) {
    inputElement.classList.remove('is-invalid');
}
