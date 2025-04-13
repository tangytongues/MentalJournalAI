/**
 * Mood chart visualization
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the mood chart if the element exists
    const moodChartEl = document.getElementById('mood-chart');
    if (moodChartEl) {
        const moodData = JSON.parse(moodChartEl.dataset.mood);
        createMoodChart(moodChartEl, moodData);
    }
    
    // Initialize time range selector
    const timeRangeSelector = document.getElementById('time-range');
    if (timeRangeSelector) {
        timeRangeSelector.addEventListener('change', function() {
            fetchMoodData(timeRangeSelector.value);
        });
    }
});

function createMoodChart(element, moodData) {
    // Check if we have data to display
    if (!moodData.dates || moodData.dates.length === 0) {
        element.innerHTML = '<div class="alert alert-info">No mood data available yet. Create journal entries to see your mood trends.</div>';
        return;
    }
    
    // Define colors for emotion markers
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
    
    // Create the emotion point styles
    const pointStyles = moodData.emotions.map(emotion => {
        return {
            pointRadius: 6,
            pointBackgroundColor: emotionColors[emotion] || '#ADB5BD',
            pointBorderColor: '#fff',
            pointBorderWidth: 1,
            pointStyle: 'circle'
        };
    });
    
    // Create the chart
    const ctx = element.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: moodData.dates,
            datasets: [{
                label: 'Mood Score',
                data: moodData.sentiment_scores,
                borderColor: '#0D6EFD',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: function(context) {
                    const index = context.dataIndex;
                    const emotion = moodData.emotions[index];
                    return emotionColors[emotion] || '#ADB5BD';
                }
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0,
                    max: 10,
                    title: {
                        display: true,
                        text: 'Mood Score (0-10)'
                    },
                    ticks: {
                        callback: function(value) {
                            if (value === 0) return 'Very Negative';
                            if (value === 5) return 'Neutral';
                            if (value === 10) return 'Very Positive';
                            return value;
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const score = context.raw;
                            const emotion = moodData.emotions[index];
                            return [
                                `Mood Score: ${score}`,
                                `Primary Emotion: ${emotion}`
                            ];
                        }
                    }
                },
                legend: {
                    display: false
                }
            }
        }
    });
    
    // Create the emotion legend
    createEmotionLegend(element, moodData.emotions, emotionColors);
}

function createEmotionLegend(chartElement, emotions, colorMap) {
    // Get unique emotions
    const uniqueEmotions = [...new Set(emotions)];
    
    // Create legend container
    const legendContainer = document.createElement('div');
    legendContainer.className = 'mood-chart-legend d-flex flex-wrap justify-content-center mt-3';
    
    // Add legend items
    uniqueEmotions.forEach(emotion => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item d-flex align-items-center me-3 mb-2';
        
        const colorBox = document.createElement('div');
        colorBox.className = 'legend-color me-1';
        colorBox.style.width = '12px';
        colorBox.style.height = '12px';
        colorBox.style.backgroundColor = colorMap[emotion] || '#ADB5BD';
        colorBox.style.borderRadius = '3px';
        
        const emotionText = document.createElement('span');
        emotionText.className = 'legend-text small';
        emotionText.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        
        legendItem.appendChild(colorBox);
        legendItem.appendChild(emotionText);
        legendContainer.appendChild(legendItem);
    });
    
    // Add the legend below the chart
    chartElement.parentNode.insertBefore(legendContainer, chartElement.nextSibling);
}

function fetchMoodData(days) {
    // Show loading state
    const moodChartEl = document.getElementById('mood-chart');
    if (moodChartEl) {
        moodChartEl.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    }
    
    // Fetch mood data for the selected time range
    fetch(`/api/mood_data?days=${days}`)
        .then(response => response.json())
        .then(data => {
            // Update the chart with new data
            if (moodChartEl) {
                moodChartEl.innerHTML = '';  // Clear loading indicator
                createMoodChart(moodChartEl, data);
            }
        })
        .catch(error => {
            console.error('Error fetching mood data:', error);
            if (moodChartEl) {
                moodChartEl.innerHTML = '<div class="alert alert-danger">Error loading mood data. Please try again later.</div>';
            }
        });
}
