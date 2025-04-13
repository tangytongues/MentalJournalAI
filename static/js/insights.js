/**
 * Insights page functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the insights page functionality
    initInsightsPage();
});

function initInsightsPage() {
    // Create mood trend chart
    const moodTrendEl = document.getElementById('mood-trend-chart');
    if (moodTrendEl) {
        const moodData = JSON.parse(moodTrendEl.dataset.mood);
        createMoodTrendChart(moodTrendEl, moodData);
    }
    
    // Create emotion distribution chart
    const emotionDistEl = document.getElementById('emotion-distribution-chart');
    if (emotionDistEl) {
        createEmotionDistributionChart(emotionDistEl);
    }
    
    // Create mental health signals chart
    const signalsChartEl = document.getElementById('mental-health-signals-chart');
    if (signalsChartEl) {
        const signalsData = JSON.parse(signalsChartEl.dataset.signals);
        createSignalsChart(signalsChartEl, signalsData);
    }
}

function createMoodTrendChart(element, moodData) {
    // Check if we have data to display
    if (!moodData.dates || moodData.dates.length === 0) {
        element.innerHTML = '<div class="alert alert-info">No mood data available yet. Create journal entries to see your mood trends.</div>';
        return;
    }
    
    // Calculate 7-day moving average
    const movingAvg = calculateMovingAverage(moodData.sentiment_scores, 7);
    
    // Create the chart
    const ctx = element.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: moodData.dates,
            datasets: [
                {
                    label: 'Daily Mood',
                    data: moodData.sentiment_scores,
                    borderColor: 'rgba(13, 110, 253, 0.5)',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: false,
                    pointRadius: 3,
                    borderWidth: 1.5
                },
                {
                    label: '7-day Average',
                    data: movingAvg,
                    borderColor: '#0D6EFD',
                    backgroundColor: 'transparent',
                    fill: false,
                    borderWidth: 2.5,
                    pointRadius: 0,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0,
                    max: 10,
                    title: {
                        display: true,
                        text: 'Mood Score'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

function createEmotionDistributionChart(element) {
    // Get emotion data from the element's data attribute
    const emotionLabels = JSON.parse(element.dataset.labels);
    const emotionValues = JSON.parse(element.dataset.values);
    
    // Check if we have data to display
    if (!emotionLabels || emotionLabels.length === 0) {
        element.innerHTML = '<div class="alert alert-info">No emotion data available yet. Create journal entries to see your emotion distribution.</div>';
        return;
    }
    
    // Define emotion colors
    const emotionColors = {
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
    
    // Create color array based on emotion labels
    const colors = emotionLabels.map(label => emotionColors[label] || '#ADB5BD');
    
    // Create the chart
    const ctx = element.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: emotionLabels,
            datasets: [{
                data: emotionValues,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const dataset = context.dataset;
                            const total = dataset.data.reduce((acc, data) => acc + data, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${percentage}%`;
                        }
                    }
                }
            }
        }
    });
}

function createSignalsChart(element, signalsData) {
    // Check if we have data to display
    if (!signalsData || Object.keys(signalsData).length === 0) {
        element.innerHTML = '<div class="alert alert-info">No mental health signals detected yet.</div>';
        return;
    }
    
    // Extract labels and values
    const labels = Object.keys(signalsData);
    const values = Object.values(signalsData);
    
    // Define signal colors
    const signalColors = {
        'anxiety': '#FFC107',
        'depression': '#6C757D',
        'stress': '#DC3545',
        'anger': '#E83E8C',
        'insomnia': '#6610F2'
    };
    
    // Create color array based on signal labels
    const colors = labels.map(label => signalColors[label] || '#ADB5BD');
    
    // Create the chart
    const ctx = element.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
            datasets: [{
                label: 'Frequency',
                data: values,
                backgroundColor: colors,
                borderWidth: 0,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Frequency in Journal Entries'
                    }
                }
            }
        }
    });
}

function calculateMovingAverage(data, window) {
    const result = [];
    
    // Fill with null for the first (window-1) points
    for (let i = 0; i < window - 1; i++) {
        result.push(null);
    }
    
    // Calculate moving averages
    for (let i = window - 1; i < data.length; i++) {
        let sum = 0;
        for (let j = 0; j < window; j++) {
            sum += data[i - j];
        }
        result.push(sum / window);
    }
    
    return result;
}
