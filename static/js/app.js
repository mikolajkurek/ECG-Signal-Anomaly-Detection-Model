/* ECG Signal Anomaly Detection - Main JavaScript */

class ECGApp {
	constructor() {
		this.currentRowIndex = 0;
		this.currentFilteredIndex = 0;
		this.totalRows = 0;
		this.currentFilter = "all";
		this.filteredIndices = [];
		this.ecgChart = null;
	}

	// Initialize the chart
	initChart() {
		const ctx = document.getElementById("ecgChart").getContext("2d");
		this.ecgChart = new Chart(ctx, {
			type: "line",
			data: {
				labels: [],
				datasets: [
					{
						label: "ECG Signal",
						data: [],
						borderColor: "#667eea",
						backgroundColor: "rgba(102, 126, 234, 0.1)",
						borderWidth: 2,
						fill: true,
						tension: 0.1,
						pointRadius: 0,
					},
				],
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				scales: {
					x: {
						title: {
							display: true,
							text: "Time (samples)",
						},
					},
					y: {
						title: {
							display: true,
							text: "Amplitude",
						},
					},
				},
				plugins: {
					legend: {
						display: false,
					},
				},
			},
		});
	}

	// Load filtered indices
	async loadFilteredIndices(filterType) {
		try {
			const response = await fetch(`/api/filter/${filterType}`);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const data = await response.json();

			if (data.error) {
				throw new Error(data.error);
			}

			this.filteredIndices = data.indices;
			this.currentFilter = filterType;
			this.currentFilteredIndex = 0;

			// Update filter info
			document.getElementById("filteredCount").textContent = data.count;
			document.getElementById("totalCount").textContent = data.total_rows;

			// Load first item in filtered results
			if (this.filteredIndices.length > 0) {
				await this.loadFilteredData(this.currentFilteredIndex);
			} else {
				this.showError("No samples found for the selected filter");
			}
		} catch (error) {
			console.error("Error loading filtered indices:", error);
			this.showError("Failed to load filtered data: " + error.message);
		}
	}

	// Load data for specific filtered index
	async loadFilteredData(filteredIndex) {
		try {
			const response = await fetch(
				`/api/data/filtered/${this.currentFilter}/${filteredIndex}`
			);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const data = await response.json();

			if (data.error) {
				throw new Error(data.error);
			}

			this.updateChart(data.signal_data);
			this.updatePrediction(data);
			this.updateUI(data);

			this.totalRows = data.total_filtered;
			document.getElementById("totalRows").textContent = this.totalRows;
			document.getElementById("currentRow").textContent = filteredIndex + 1;

			// Update navigation buttons
			document.getElementById("prevBtn").disabled = filteredIndex === 0;
			document.getElementById("nextBtn").disabled =
				filteredIndex === this.totalRows - 1;
		} catch (error) {
			console.error("Error loading filtered data:", error);
			this.showError("Failed to load data: " + error.message);
		}
	}

	// Update the chart with new data
	updateChart(signalData) {
		const labels = Array.from({ length: signalData.length }, (_, i) => i);

		this.ecgChart.data.labels = labels;
		this.ecgChart.data.datasets[0].data = signalData;
		this.ecgChart.update();
	}

	// Update prediction display
	updatePrediction(data) {
		const predictionResult = document.getElementById("predictionResult");
		const actualLabel = document.getElementById("actualLabel");

		if (data.prediction) {
			const pred = data.prediction;
			const isCorrect = pred.prediction === (data.actual_label > 0 ? 1 : 0);

			predictionResult.innerHTML = `
                <div class="prediction-class ${pred.class_name.toLowerCase()}">
                    ${pred.class_name}
                </div>
                <div class="confidence">
                    Confidence: ${(pred.confidence * 100).toFixed(1)}%
                </div>
                <div style="font-size: 0.8rem; color: #718096;">
                    Raw Score: ${pred.raw_score.toFixed(4)}
                </div>
            `;

			actualLabel.style.display = "block";
			actualLabel.innerHTML = `
                <strong>Actual:</strong> ${data.actual_class} (${
				data.actual_label
			})
                <div style="margin-top: 8px; font-size: 0.8rem;">
                    <span style="color: ${
											isCorrect ? "#38a169" : "#e53e3e"
										}; font-weight: bold;">
                        ${isCorrect ? "✓ Correct" : "✗ Incorrect"}
                    </span>
                </div>
            `;
		} else {
			predictionResult.innerHTML =
				'<div class="error">Failed to make prediction</div>';
			actualLabel.style.display = "none";
		}
	}

	// Update UI elements
	updateUI(data) {
		const signalInfo = document.getElementById("signalInfo");
		signalInfo.innerHTML = `
            <div class="info-item">
                <span class="info-label">Min</span>
                <span class="info-value">${Math.min(
									...data.signal_data
								).toFixed(3)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Max</span>
                <span class="info-value">${Math.max(
									...data.signal_data
								).toFixed(3)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Mean</span>
                <span class="info-value">${(
									data.signal_data.reduce((a, b) => a + b, 0) /
									data.signal_data.length
								).toFixed(3)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Row</span>
                <span class="info-value">${data.row_index + 1}</span>
            </div>
        `;
	}

	// Show error message
	showError(message) {
		const predictionResult = document.getElementById("predictionResult");
		predictionResult.innerHTML = `<div class="error">${message}</div>`;
	}

	// Navigation functions
	previousSample() {
		if (this.currentFilteredIndex > 0) {
			this.currentFilteredIndex--;
			this.loadFilteredData(this.currentFilteredIndex);
		}
	}

	nextSample() {
		if (this.currentFilteredIndex < this.totalRows - 1) {
			this.currentFilteredIndex++;
			this.loadFilteredData(this.currentFilteredIndex);
		}
	}

	// Filter functions
	setFilter(filterType) {
		// Update active button
		document
			.querySelectorAll(".filter-button")
			.forEach((btn) => btn.classList.remove("active"));
		document
			.getElementById(
				`filter${filterType.charAt(0).toUpperCase() + filterType.slice(1)}`
			)
			.classList.add("active");

		// Load filtered data
		this.loadFilteredIndices(filterType);
	}

	// Setup event listeners
	setupEventListeners() {
		// Filter event listeners
		document
			.getElementById("filterAll")
			.addEventListener("click", () => this.setFilter("all"));
		document
			.getElementById("filterNormal")
			.addEventListener("click", () => this.setFilter("normal"));
		document
			.getElementById("filterAbnormal")
			.addEventListener("click", () => this.setFilter("abnormal"));

		// Navigation event listeners
		document
			.getElementById("prevBtn")
			.addEventListener("click", () => this.previousSample());
		document
			.getElementById("nextBtn")
			.addEventListener("click", () => this.nextSample());

		// Keyboard navigation
		document.addEventListener("keydown", (e) => {
			if (e.key === "ArrowLeft") {
				this.previousSample();
			} else if (e.key === "ArrowRight") {
				this.nextSample();
			} else if (e.key === "1") {
				this.setFilter("all");
			} else if (e.key === "2") {
				this.setFilter("normal");
			} else if (e.key === "3") {
				this.setFilter("abnormal");
			}
		});
	}

	// Initialize the application
	async init() {
		this.initChart();
		this.setupEventListeners();

		// Load initial data (all samples)
		await this.loadFilteredIndices("all");
	}
}

// Initialize app when page loads
let ecgApp;
window.addEventListener("load", () => {
	ecgApp = new ECGApp();
	ecgApp.init();
});
