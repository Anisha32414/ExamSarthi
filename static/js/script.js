// JavaScript for ExamSarthi

function updateSemesterOptions() {
    const yearSelect = document.getElementById('year');
    const semSelect = document.getElementById('sem');
    if (!yearSelect || !semSelect) {
        return;
    }

    const semesterMap = {
        '1': ['1', '2'],
        '2': ['3', '4'],
        '3': ['5', '6'],
        '4': ['7', '8']
    };

    const selectedYear = yearSelect.value;
    const selectedSem = semSelect.dataset.selected || '';
    semSelect.innerHTML = '<option value="">Select Semester</option>';

    if (semesterMap[selectedYear]) {
        semesterMap[selectedYear].forEach((semester) => {
            const option = document.createElement('option');
            option.value = semester;
            option.textContent = semester;
            if (semester === selectedSem) {
                option.selected = true;
            }
            semSelect.appendChild(option);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateSemesterOptions();
    const yearSelect = document.getElementById('year');
    if (yearSelect) {
        yearSelect.addEventListener('change', updateSemesterOptions);
    }
});

console.log('ExamSarthi script loaded');