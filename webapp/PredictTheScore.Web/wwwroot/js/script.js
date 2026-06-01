const APP_CONFIG = {
  apiBaseUrl: '',
  predictEndpoint: '/Predict/Submit',
  requestTimeoutMs: 15000
};

const SCENARIOS = {
  web_minimal: {
    label: 'Dự đoán nhanh',
    description: 'Kịch bản nhập nhanh, chỉ dùng các thông tin cơ bản.'
  },
  early_warning: {
    label: 'Cảnh báo sớm',
    description: 'Kịch bản cảnh báo sớm, bổ sung môn học, mong muốn học tiếp và thời gian đi học.'
  },
  reference: {
    label: 'Tham chiếu có điểm G1/G2',
    description: 'Kịch bản tham chiếu, bổ sung điểm G1/G2 nên thường cho kết quả tốt hơn nhưng cần biết điểm quá trình.'
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('prediction-form');
  const resetBtn = document.getElementById('resetBtn');
  const submitBtn = document.getElementById('submitBtn');
  const historyBody = document.getElementById('historyBody');
  if (!form || !resetBtn || !submitBtn || !historyBody) {
    console.warn('Trang hiện tại không có form dự đoán, bỏ qua script.js.');
    return;
  }

  const advancedSection = document.getElementById('advancedSection');
  const upgradeModelButton = document.getElementById('upgradeModelButton');
  const scenarioSelect = document.getElementById('scenario');
  const scenarioTitle = document.getElementById('scenarioTitle');
  const scenarioDescription = document.getElementById('scenarioDescription');
  let advancedMode = false;

  const fields = {
    studentName: field('studentName', 'studentNameError', (value) => value.trim() ? '' : 'Vui lòng nhập họ và tên học sinh.'),
    className: field('className', 'classNameError', (value) => value.trim() ? '' : 'Vui lòng nhập lớp.'),
    studyTime: field('studyTime', 'studyTimeError', (value) => value ? '' : 'Vui lòng chọn mức thời gian tự học.'),
    absences: field('absences', 'absencesError', (value) => validateIntegerRange(value, 0, 93, 'Số buổi vắng học')),
    failures: field('failures', 'failuresError', (value) => validateIntegerRange(value, 0, 4, 'Số lần chưa đạt')),
    schoolsup: field('schoolsup', 'schoolsupError', (value) => value !== '' ? '' : 'Vui lòng chọn hỗ trợ từ nhà trường.'),
    famsup: field('famsup', 'famsupError', (value) => value !== '' ? '' : 'Vui lòng chọn hỗ trợ từ gia đình.'),
    internet: field('internet', 'internetError', (value) => value !== '' ? '' : 'Vui lòng chọn tình trạng Internet.'),
    subject: field('subject', 'subjectError', (value) => ['mat', 'por'].includes(value) ? '' : 'Vui lòng chọn môn học.'),
    higher: field('higher', 'higherError', (value) => value !== '' ? '' : 'Vui lòng chọn mong muốn học tiếp.'),
    traveltime: field('traveltime', 'traveltimeError', (value) => value ? '' : 'Vui lòng chọn thời gian đi học.'),
    g1: field('g1', 'g1Error', (value) => validateIntegerRange(value, 0, 20, 'G1')),
    g2: field('g2', 'g2Error', (value) => validateIntegerRange(value, 0, 20, 'G2'))
  };

  const result = {
    resultPanel: document.getElementById('resultPanel'),
    predictedScore: document.getElementById('predictedScore'),
    predictedScore10: document.getElementById('predictedScore10'),
    scoreStatus: document.getElementById('scoreStatus'),
    scoreDesc: document.getElementById('scoreDesc'),
    feedbackText: document.getElementById('feedbackText'),
    summaryStudent: document.getElementById('summaryStudent'),
    summaryClass: document.getElementById('summaryClass'),
    summaryScenario: document.getElementById('summaryScenario'),
    summaryStudyTime: document.getElementById('summaryStudyTime'),
    summaryAbsences: document.getElementById('summaryAbsences'),
    summarySchoolsup: document.getElementById('summarySchoolsup'),
    summaryFamsup: document.getElementById('summaryFamsup'),
    summaryInternet: document.getElementById('summaryInternet'),
    summarySubject: document.getElementById('summarySubject'),
    summaryHigher: document.getElementById('summaryHigher'),
    summaryTraveltime: document.getElementById('summaryTraveltime'),
    summaryGrades: document.getElementById('summaryGrades'),
    summaryFailures: document.getElementById('summaryFailures'),
    summaryRequestedAt: document.getElementById('summaryRequestedAt'),
    requestStatusBadge: document.getElementById('requestStatusBadge'),
    formStateBadge: document.getElementById('formStateBadge'),
    connectionBadge: document.getElementById('connectionBadge'),
    apiEndpointLabel: document.getElementById('apiEndpointLabel')
  };

  const studyTimeLabels = {
    1: 'Dưới 2 giờ/tuần',
    2: 'Từ 2 đến 5 giờ/tuần',
    3: 'Từ 5 đến 10 giờ/tuần',
    4: 'Trên 10 giờ/tuần'
  };

  const subjectLabels = {
    mat: 'Toán',
    por: 'Portuguese'
  };

  initializeConfig();
  initScenarioUi();
  loadHistoryFromDatabase();

  form.addEventListener('submit', handleSubmit);
  resetBtn.addEventListener('click', handleReset);
  upgradeModelButton?.addEventListener('click', toggleAdvancedMode);
  scenarioSelect?.addEventListener('change', updateScenarioFields);

  function field(inputId, errorId, validate) {
    return {
      input: document.getElementById(inputId),
      error: document.getElementById(errorId),
      validate
    };
  }

  function initializeConfig() {
    if (result.apiEndpointLabel) {
      result.apiEndpointLabel.textContent = 'Dự đoán khả năng';
    }
  }

  function initScenarioUi() {
    advancedMode = false;
    if (scenarioSelect) {
      scenarioSelect.value = 'web_minimal';
      scenarioSelect.disabled = true;
    }
    advancedSection?.classList.add('hidden');
    if (upgradeModelButton) {
      upgradeModelButton.textContent = 'Nâng cấp mô hình dự đoán';
    }
    updateScenarioFields();
  }

  function toggleAdvancedMode() {
    advancedMode = !advancedMode;
    if (!advancedMode) {
      initScenarioUi();
      return;
    }

    advancedSection?.classList.remove('hidden');
    if (scenarioSelect) {
      scenarioSelect.disabled = false;
      scenarioSelect.value = 'early_warning';
    }
    if (upgradeModelButton) {
      upgradeModelButton.textContent = 'Thu gọn mô hình dự đoán';
    }
    updateScenarioFields();
  }

  function getSelectedScenario() {
    if (!advancedMode) return 'web_minimal';
    return scenarioSelect?.value || 'web_minimal';
  }

  function updateScenarioFields() {
    const scenario = getSelectedScenario();

    document.querySelectorAll('.advanced-field').forEach((group) => {
      setFieldGroupVisible(group, false);
    });

    if (advancedMode && scenario === 'early_warning') {
      document.querySelectorAll('.field-early-warning').forEach((group) => {
        setFieldGroupVisible(group, true);
      });
    }

    if (advancedMode && scenario === 'reference') {
      document.querySelectorAll('.field-reference').forEach((group) => {
        setFieldGroupVisible(group, true);
      });
    }

    if (scenarioTitle) scenarioTitle.textContent = SCENARIOS[scenario].label;
    if (scenarioDescription) scenarioDescription.textContent = SCENARIOS[scenario].description;
    Object.keys(fields).forEach((key) => showError(key, ''));
  }

  function setFieldGroupVisible(group, visible) {
    group.classList.toggle('hidden', !visible);
    group.querySelectorAll('input, select, textarea').forEach((control) => {
      control.disabled = !visible;
    });
  }

  function activeFieldKeys() {
    const common = ['studentName', 'className', 'studyTime', 'absences', 'failures', 'schoolsup', 'famsup', 'internet'];
    const scenario = getSelectedScenario();
    if (scenario === 'early_warning') return [...common, 'subject', 'higher', 'traveltime'];
    if (scenario === 'reference') return [...common, 'subject', 'higher', 'traveltime', 'g1', 'g2'];
    return common;
  }

  function validateIntegerRange(value, min, max, label) {
    // Giữ range phía frontend khớp với Pydantic validation ở FastAPI.
    if (value === '') return `Vui lòng nhập ${label.toLowerCase()}.`;
    const numeric = Number(value);
    if (!Number.isInteger(numeric)) return `${label} phải là số nguyên.`;
    if (numeric < min || numeric > max) return `${label} phải trong khoảng ${min} đến ${max}.`;
    return '';
  }

  function showError(fieldKey, message) {
    const currentField = fields[fieldKey];
    if (!currentField?.input || !currentField?.error) return;
    currentField.error.textContent = message;
    currentField.input.classList.toggle('input-error', Boolean(message));
    currentField.input.setAttribute('aria-invalid', Boolean(message));
  }

  function validateForm() {
    let valid = true;
    activeFieldKeys().forEach((key) => {
      const message = fields[key].validate(fields[key].input.value);
      showError(key, message);
      if (message) valid = false;
    });
    return valid;
  }

  function buildPredictionPayload() {
    // Chỉ gửi field mà scenario đang chọn cần dùng.
    const scenario = getSelectedScenario();
    const payload = {
      scenario,
      student_name: fields.studentName.input.value.trim(),
      class_name: fields.className.input.value.trim(),
      studytime: Number(fields.studyTime.input.value),
      absences: Number(fields.absences.input.value),
      failures: Number(fields.failures.input.value),
      schoolsup: Number(fields.schoolsup.input.value),
      famsup: Number(fields.famsup.input.value),
      internet: Number(fields.internet.input.value),
      note: document.getElementById('note')?.value.trim() ?? ''
    };

    if (scenario === 'early_warning' || scenario === 'reference') {
      payload.subject = fields.subject.input.value;
      payload.higher = Number(fields.higher.input.value);
      payload.traveltime = Number(fields.traveltime.input.value);
    }

    if (scenario === 'reference') {
      payload.G1 = Number(fields.g1.input.value);
      payload.G2 = Number(fields.g2.input.value);
    }

    return payload;
  }

  function buildApiUrl(endpoint) {
    if (!APP_CONFIG.apiBaseUrl) return endpoint;
    return `${APP_CONFIG.apiBaseUrl.replace(/\/$/, '')}${endpoint}`;
  }

  async function postPrediction(payload) {
    // AbortController giúp giao diện không treo nếu ML backend chưa chạy.
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), APP_CONFIG.requestTimeoutMs);

    try {
      const response = await fetch(buildApiUrl(APP_CONFIG.predictEndpoint), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      const rawText = await response.text();
      let data = {};
      if (rawText) {
        try {
          data = JSON.parse(rawText);
        } catch (parseError) {
          throw new Error('Backend trả về dữ liệu không đúng định dạng JSON.');
        }
      }

      if (!response.ok) {
        throw new Error(data.message || data.detail || `Yêu cầu thất bại với mã ${response.status}.`);
      }

      return data;
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Hết thời gian chờ phản hồi từ backend.');
      }
      throw error;
    } finally {
      window.clearTimeout(timeoutId);
    }
  }

  function normalizeResponse(data, payload) {
    const score20 = pickNumber(data, ['predicted_score_20', 'predicted_score', 'predictedScore', 'score']);
    if (score20 === null) {
      throw new Error('Không tìm thấy trường điểm dự đoán trong phản hồi từ backend.');
    }

    const normalizedScore20 = Math.max(0, Math.min(20, score20));
    const score10 = pickNumber(data, ['predicted_score_10', 'predictedScore10']) ?? (normalizedScore20 / 2);
    const label = buildDefaultLabel(normalizedScore20);

    return {
      predicted20: normalizedScore20.toFixed(1),
      predicted10: Number(score10).toFixed(1),
      scenario: data.scenario || payload.scenario,
      modelScenario: data.model_scenario || payload.scenario,
      label,
      description: buildDefaultDescription(normalizedScore20),
      advice: data.message || buildDefaultAdvice(payload, normalizedScore20)
    };
  }

  function pickNumber(source, keys) {
    for (const key of keys) {
      const value = source?.[key];
      if (typeof value === 'number' && Number.isFinite(value)) return value;
      if (typeof value === 'string' && value.trim() !== '' && !Number.isNaN(Number(value))) return Number(value);
    }
    return null;
  }

  function buildDefaultLabel(score20) {
    if (score20 >= 16) return 'Rất khả quan';
    if (score20 >= 12) return 'Khả quan';
    return 'Cần cải thiện';
  }

  function buildDefaultDescription(score20) {
    if (score20 >= 16) return 'Kết quả dự đoán cho thấy học sinh đang có nền tảng học tập tốt và khả năng đạt điểm cuối kỳ cao.';
    if (score20 >= 12) return 'Kết quả dự đoán ở mức ổn định, vẫn còn dư địa cải thiện nếu duy trì học tập đều đặn.';
    return 'Kết quả dự đoán chưa cao, cần theo dõi sát tiến độ học tập và tăng cường ôn tập.';
  }

  function buildDefaultAdvice(payload, score20) {
    if (payload.scenario === 'reference') {
      return 'Kịch bản reference dùng thêm G1/G2 nên phù hợp khi đã có điểm quá trình.';
    }
    if (payload.scenario === 'early_warning') {
      return 'Kịch bản cảnh báo sớm dùng thêm môn học, mong muốn học tiếp và thời gian đi học.';
    }
    if (score20 >= 12) return 'Nên duy trì nhịp học và theo dõi số buổi vắng để cải thiện kết quả.';
    return 'Cần tăng thời gian tự học và theo dõi sát tiến độ học tập.';
  }

  function setUiState(type, message) {
    if (result.formStateBadge) {
      result.formStateBadge.textContent = type === 'loading' ? 'Đang gửi' : type === 'success' ? 'Hoàn tất' : type === 'error' ? 'Lỗi' : 'Sẵn sàng';
    }
    if (result.requestStatusBadge) {
      result.requestStatusBadge.textContent = type === 'loading' ? 'Đang xử lý' : type === 'success' ? 'Thành công' : type === 'error' ? 'Thất bại' : 'Chưa gửi';
    }
    if (result.connectionBadge) {
      result.connectionBadge.textContent = message;
    }
  }

  function updateResult(payload, normalized) {
    result.resultPanel.classList.remove('empty-state');
    result.predictedScore.textContent = normalized.predicted20;
    result.predictedScore10.textContent = normalized.predicted10;
    result.scoreStatus.textContent = normalized.label;
    result.scoreDesc.textContent = normalized.description;
    result.feedbackText.textContent = normalized.advice;

    result.summaryStudent.textContent = payload.student_name;
    result.summaryClass.textContent = payload.class_name;
    result.summaryScenario.textContent = SCENARIOS[payload.scenario].label;
    result.summaryStudyTime.textContent = `${payload.studytime} - ${studyTimeLabels[payload.studytime]}`;
    result.summaryAbsences.textContent = String(payload.absences);
    result.summaryFailures.textContent = String(payload.failures);
    result.summarySchoolsup.textContent = payload.schoolsup === 1 ? 'Có' : 'Không';
    result.summaryFamsup.textContent = payload.famsup === 1 ? 'Có' : 'Không';
    result.summaryInternet.textContent = payload.internet === 1 ? 'Có' : 'Không';
    result.summarySubject.textContent = payload.subject ? subjectLabels[payload.subject] : '--';
    result.summaryHigher.textContent = payload.higher === undefined ? '--' : payload.higher === 1 ? 'Có' : 'Không';
    result.summaryTraveltime.textContent = payload.traveltime ? String(payload.traveltime) : '--';
    result.summaryGrades.textContent = payload.scenario === 'reference' ? `${payload.G1} / ${payload.G2}` : '--';
    result.summaryRequestedAt.textContent = new Date().toLocaleString('vi-VN');
  }

  function appendHistory(payload, normalized) {
    const emptyRow = historyBody.querySelector('.empty-row');
    if (emptyRow) emptyRow.remove();

    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${escapeHtml(new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }))}</td>
      <td>${escapeHtml(payload.student_name)}</td>
      <td>${escapeHtml(payload.class_name)}</td>
      <td>${escapeHtml(SCENARIOS[normalized.scenario]?.label || normalized.scenario)}</td>
      <td>${payload.studytime}</td>
      <td>${payload.schoolsup === 1 ? 'Có' : 'Không'}</td>
      <td>${payload.famsup === 1 ? 'Có' : 'Không'}</td>
      <td>${payload.internet === 1 ? 'Có' : 'Không'}</td>
      <td>${normalized.predicted20}</td>
    `;
    historyBody.prepend(row);
  }

  async function loadHistoryFromDatabase() {
    if (!historyBody) return;
    try {
      const response = await fetch('/Predict/History?take=10');
      if (!response.ok) throw new Error(`Không tải được lịch sử, mã lỗi ${response.status}`);
      renderHistoryFromDatabase(await response.json());
    } catch (error) {
      console.error(error);
    }
  }

  function renderHistoryFromDatabase(histories) {
    historyBody.innerHTML = '';
    if (!histories || histories.length === 0) {
      historyBody.innerHTML = '<tr class="empty-row"><td colspan="9">Chưa có lần dự đoán nào.</td></tr>';
      return;
    }

    histories.forEach((item) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${escapeHtml(item.created_at)}</td>
        <td>${escapeHtml(item.student_name || '--')}</td>
        <td>${escapeHtml(item.class_name || '--')}</td>
        <td>${escapeHtml(SCENARIOS[item.scenario]?.label || item.scenario || '--')}</td>
        <td>${escapeHtml(item.studytime)}</td>
        <td>${item.schoolsup === 1 ? 'Có' : 'Không'}</td>
        <td>${item.famsup === 1 ? 'Có' : 'Không'}</td>
        <td>${item.internet === 1 ? 'Có' : 'Không'}</td>
        <td>${Number(item.predicted_score).toFixed(2)}</td>
      `;
      historyBody.appendChild(row);
    });
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!validateForm()) {
      setUiState('error', 'Biểu mẫu còn lỗi. Vui lòng kiểm tra lại các trường dữ liệu.');
      return;
    }

    const payload = buildPredictionPayload();
    submitBtn.disabled = true;
    setUiState('loading', 'Đang gửi dữ liệu đến backend và chờ kết quả dự đoán...');

    try {
      const data = await postPrediction(payload);
      const normalized = normalizeResponse(data, payload);
      updateResult(payload, normalized);
      appendHistory(payload, normalized);
      await loadHistoryFromDatabase();
      setUiState('success', 'Nhận kết quả dự đoán thành công.');
      document.getElementById('result-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
      console.error(error);
      setUiState('error', error.message || 'Không thể hoàn tất yêu cầu dự đoán.');
    } finally {
      submitBtn.disabled = false;
    }
  }

  function handleReset() {
    window.setTimeout(() => {
      Object.keys(fields).forEach((key) => showError(key, ''));
      initScenarioUi();
      result.resultPanel.classList.add('empty-state');
      [
        result.predictedScore,
        result.predictedScore10,
        result.summaryStudent,
        result.summaryClass,
        result.summaryScenario,
        result.summaryStudyTime,
        result.summaryAbsences,
        result.summarySchoolsup,
        result.summaryFamsup,
        result.summaryInternet,
        result.summarySubject,
        result.summaryHigher,
        result.summaryTraveltime,
        result.summaryGrades,
        result.summaryFailures,
        result.summaryRequestedAt
      ].forEach((item) => {
        if (item) item.textContent = '--';
      });
      result.scoreStatus.textContent = 'Chưa có dữ liệu';
      result.scoreDesc.textContent = 'Gửi biểu mẫu để xem kết quả từ backend.';
      result.feedbackText.textContent = 'Hệ thống sẽ hiển thị nhận xét sau khi nhận phản hồi thành công từ dịch vụ dự đoán.';
      setUiState('idle', 'Sẵn sàng gửi yêu cầu.');
    }, 0);
  }
});
