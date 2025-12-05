        const datasets = [
            {
                name: "Neighborhood × Gender - Raanana",
                comment: "Diversimax prefers completely equal intersection sizes, unbiased by the distribution in the pool",
                gini: { leximin: 0.1, diversimax: 0 },
                distribution: {
                    rows: ["South", "North East", "North West"],
                    cols: ["Female", "Male"],
                    rows_name: "neighborhood",
                    cols_name: "gender",
                    leximin: [[14, 8], [9, 9], [9, 11]],
                    diversimax: [[10, 10], [10, 10], [10, 10]]
                },
                neighborhood_quotas: {
                    rows: ["North East", "North West", "South"],
                    quotas: [[18, 22], [15, 22], [19, 22]]
                },
                gender_quotas: {
                    rows: ["Male", "Female"],
                    quotas: [[28, 32], [28, 32]]
                }
            },
            {
                name: "Neighborhood × Religiousness - Raanana",
                gini: { leximin: 0.41, diversimax: 0.27 },
                distribution: {
                    rows: ["South", "North East", "North West"],
                    cols: ["Religious", "Secular", "Traditional"],
                    rows_name: "neighborhood",
                    cols_name: "religiousness",
                    leximin: [[5, 16, 1], [6, 10, 2], [2, 13, 5]],
                    diversimax: [[5, 10, 5], [5, 12, 3], [3, 12, 5]]
                },
                religiousness_quotas: {
                    rows: ["Secular", "Traditional", "Religious"],
                    quotas: [[34, 41], [8, 13], [8, 13]]
                },
                neighborhood_quotas: {
                    rows: ["North East", "North West", "South"],
                    quotas: [[18, 22], [15, 22], [19, 22]]
                }
            },
            {
                name: "Education × Gender - Raanana",
                gini: { leximin: 0.39, diversimax: 0.26 },
                distribution: {
                    rows: ["High School Diploma", "BA", "MA+", "Non-Academic Diploma"],
                    cols: ["Female", "Male"],
                    rows_name: "education",
                    cols_name: "gender",
                    leximin: [[0, 3], [15, 10], [14, 10], [3, 5]],
                    diversimax: [[4, 5], [14, 10], [9, 10], [3, 5]]
                },
                gender_quotas: {
                    rows: ["Male", "Female"],
                    quotas: [[28, 32], [28, 32]]
                },
                education_quotas: {
                    rows: ["Non-Academic Diploma", "MA+", "BA", "High School Diploma"],
                    quotas: [[6, 8], [12, 24], [21, 27], [3, 9]]
                }
            },
            {
                name: "Age × Gender - Kfar Saba",
                comment: "Diversimax prefers higher representation of underrepresented groups, other algorithms may stick to the lower end of the quota range",
                gini: { leximin: 0.35, diversimax: 0.11 },
                distribution: {
                    rows: ["22-29", "30-39", "40-49", "50-59", "60-69", "70+"],
                    cols: ["Female", "Male"],
                    rows_name: "age",
                    cols_name: "gender",
                    leximin: [[1, 2], [7, 0], [8, 7], [2, 5], [5, 7], [11, 5]],
                    diversimax: [[4, 3], [4, 4], [6, 5], [5, 6], [6, 6], [5, 6]]
                },
                age_quotas: {
                    rows: ["22-29", "30-39", "40-49", "50-59", "60-69", "70+"],
                    quotas: [[3, 7], [7, 9], [10, 15], [7, 13], [8, 12], [11, 16]]
                },
                gender_quotas: {
                    rows: ["Male", "Female"],
                    quotas: [[28, 32], [28, 32]]
                }
            },
            {
                name: "Religiousness × Gender - Kfar Saba",
                gini: { leximin: 0.43, diversimax: 0.33 },
                distribution: {
                    rows: ["Religious", "Secular", "Traditional"],
                    cols: ["Female", "Male"],
                    rows_name: "religiousness",
                    cols_name: "gender",
                    leximin: [[2, 1], [26, 18], [6, 7]],
                    diversimax: [[4, 4], [18, 19], [8, 7]]
                },
                gender_quotas: {
                    rows: ["Male", "Female"],
                    quotas: [[26, 34], [26, 34]]
                },
                religiousness_quotas: {
                    rows: ["Secular", "Traditional", "Religious"],
                    quotas: [[36, 44], [10, 16], [3, 8]]
                }
            },
                        {
                name: "Neighborhood × Education - Kfar Saba (narrow quota ranges)",
                comment: "Even when the quota ranges are narrow (each category totals to the same value in both algorithms), Diversimax achieves a more balanced distribution",
                gini: { leximin: 0.43, diversimax: 0.31},
                distribution: {
                    rows: ["East", "West", "Center-South", "Center-North", "New 60", "New 80"],
                    cols: ["9-12", "13-15", "16+"],
                    rows_name: "neighborhood",
                    cols_name: "education",
                    leximin: [[2, 2,7], [2,2,2], [4,11,0], [5,4,9], [3,0,2], [2,1,2]],
                    diversimax: [[2, 4,5], [2,2,2], [5,6,4], [5,4,9], [2,2,1], [2,2,1]]
                },
                education_quotas: {
                    rows: ["9-12", "13-15", "16+"],
                    quotas: [[18, 18], [20, 20], [22, 22]]
                },
                neighborhood_quotas: {
                    rows: ["East", "West", "Center-South", "Center-North", "New 60", "New 80"],
                    quotas: [[9, 9], [6, 6], [15,15],[18,18],[5,5],[5,5]]
                }
            },
            {
                name: "Education - Kfar Saba",
                comment: "Even when looking at a single dimension, Diversimax tends to a more balanced distribution",
                gini: { diversimax: 0.04, leximin: 0.1 },
                distribution: {
                    rows: ["12-9", "15-13", "16+"],
                    cols: ["Count"],
                    rows_name: "education",
                    cols_name: "count",
                    diversimax: [[18], [22], [20]],
                    leximin: [[15], [21], [24]]
                },
                education_quotas: {
                    rows: ["12-9", "15-13", "16+"],
                    quotas: [[15, 25], [20, 24], [16, 24]]
                }
            }
        ];

function getCellColor(value) {
    if (value === 0) return '#dc3545';
    if (value <= 2) return '#ffd7a3';
    if (value <= 5) return '#fff9c4';
    if (value <= 9) return '#c8e6c9';
    return '#81c784';
}

function getQuotaForRow(dataset, rowName) {
    const rowsName = dataset.distribution.rows_name;
    const quotasKey = rowsName + '_quotas';

    if (dataset[quotasKey]) {
        const idx = dataset[quotasKey].rows.indexOf(rowName);
        if (idx !== -1) {
            return dataset[quotasKey].quotas[idx];
        }
    }
    return null;
}

function getQuotaForCol(dataset, colName) {
    const colsName = dataset.distribution.cols_name;
    const quotasKey = colsName + '_quotas';

    if (dataset[quotasKey]) {
        const idx = dataset[quotasKey].rows.indexOf(colName);
        if (idx !== -1) {
            return dataset[quotasKey].quotas[idx];
        }
    }
    return null;
}

function calculateStats(data) {
    const flat = data.flat();
    const empty = flat.filter(x => x === 0).length;
    const sparse = flat.filter(x => x >= 1 && x <= 2).length;

    return { empty, sparse };
}

function renderTable(containerId, data, dataset, algorithm) {
    const container = document.getElementById(containerId);
    const dist = dataset.distribution;
    const matrix = dist[algorithm];

    // Capitalize first letter for display
    const rowsLabel = dist.rows_name.charAt(0).toUpperCase() + dist.rows_name.slice(1);
    const colsLabel = dist.cols_name.charAt(0).toUpperCase() + dist.cols_name.slice(1);

    let html = '<table><thead><tr>';
    html += `<th class="corner">${rowsLabel} ↓<br>${colsLabel} →</th>`;

    dist.cols.forEach(col => {
        html += `<th class="header-cell">${col}</th>`;
    });
    html += `<th class="header-cell">Total<br><span class="quota-info">Quota ranges</span></th>`;
    html += '</tr></thead><tbody>';

    dist.rows.forEach((row, i) => {
        html += '<tr>';
        html += `<td class="row-header">${row}</td>`;

        dist.cols.forEach((col, j) => {
            const value = matrix[i][j];
            const color = getCellColor(value);
            html += `<td class="data-cell" style="background: ${color}; color: ${value === 0 ? 'white' : 'inherit'};">${value}</td>`;
        });

        const rowSum = matrix[i].reduce((a, b) => a + b, 0);
        const quota = getQuotaForRow(dataset, row);
        const quotaText = quota ? `<span class="quota-info">${quota[0]}-${quota[1]}</span>` : '';
        html += `<td class="margin-cell">${rowSum}<br>${quotaText}</td>`;
        html += '</tr>';
    });

    html += '<tr>';
    html += `<td class="row-header">Total<br><span class="quota-info" style="color: rgba(255,255,255,0.7);">Quota ranges</span></td>`;

    dist.cols.forEach((col, j) => {
        const colSum = matrix.reduce((sum, row) => sum + row[j], 0);
        const quota = getQuotaForCol(dataset, col);
        const quotaText = quota ? `<span class="quota-info">${quota[0]}-${quota[1]}</span>` : '';
        html += `<td class="margin-cell">${colSum}<br>${quotaText}</td>`;
    });

    const total = matrix.flat().reduce((a, b) => a + b, 0);
    html += `<td class="margin-cell"><strong>${total}</strong></td>`;
    html += '</tr>';

    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderStats(containerId, dataset, algorithm) {
    const container = document.getElementById(containerId);
    const stats = calculateStats(dataset.distribution[algorithm]);
    const gini = dataset.gini[algorithm];

    container.innerHTML = `
        <div class="stat-item gini">
            <div class="stat-label">Gini Coefficient<br>(lower = more evenly distributed)</div>
            <div class="stat-value">${gini.toFixed(2)}</div>
        </div>
        <div class="stat-item empty">
            <div class="stat-label">No Representation</div>
            <div class="stat-value">${stats.empty}</div>
        </div>
        <div class="stat-item sparse">
            <div class="stat-label">Low Representation (1-2)</div>
            <div class="stat-value">${stats.sparse}</div>
        </div>
    `;
}

function updateVisualization() {
    const selectedIndex = document.getElementById('datasetSelect').value;
    const dataset = datasets[selectedIndex];

    // Handle comment section
    const commentSection = document.getElementById('commentSection');
    if (dataset.comment) {
        commentSection.textContent = dataset.comment;
        commentSection.classList.add('active');
    } else {
        commentSection.classList.remove('active');
    }

    renderTable('diversimaxTable', dataset, dataset, 'diversimax');
    renderTable('leximinTable', dataset, dataset, 'leximin');

    renderStats('diversimaxStats', dataset, 'diversimax');
    renderStats('leximinStats', dataset, 'leximin');
}

function init() {
    const select = document.getElementById('datasetSelect');
    datasets.forEach((ds, i) => {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = ds.name;
        // Set Age × Gender - Kfar Saba as default (index 3)
        if (i === 3) {
            option.selected = true;
        }
        select.appendChild(option);
    });

    select.addEventListener('change', updateVisualization);
    updateVisualization();
}

init();
