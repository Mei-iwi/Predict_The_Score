const APP_CONFIG = {
  apiBaseUrl: '',
  predictEndpoint: '/Predict/Submit',
  requestTimeoutMs: 15000
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
  const fields = {
    studentName: {
      input: document.getElementById('studentName'),
      error: document.getElementById('studentNameError'),
      validate: (value) => value.trim() ? '' : 'Vui lòng nhập họ và tên học sinh.'
    },
    className: {
      input: document.getElementById('className'),
      error: document.getElementById('classNameError'),
      validate: (value) => value.trim() ? '' : 'Vui lòng nhập lớp.'
    },
    studyTime: {
      input: document.getElementById('studyTime'),
      error: document.getElementById('studyTimeError'),
      validate: (value) => value ? '' : 'Vui lòng chọn mức thời gian tự học.'
    },
    absences: {
      input: document.getElementById('absences'),
      error: document.getElementById('absencesError'),
      validate: (value) => validateIntegerRange(value, 0, 100, 'Số buổi vắng học')
    },
    failures: {
      input: document.getElementById('failures'),
      error: document.getElementById('failuresError'),
      validate: (value) => validateIntegerRange(value, 0, 10, 'Số lần chưa đạt')
    },
    schoolsup: {
      input: document.getElementById('schoolsup'),
      error: document.getElementById('schoolsupError'),
      validate: (value) => value !== '' ? '' : 'Vui lòng chọn hỗ trợ từ nhà trường.'
    },
    famsup: {
      input: document.getElementById('famsup'),
      error: document.getElementById('famsupError'),
      validate: (value) => value !== '' ? '' : 'Vui lòng chọn hỗ trợ từ gia đình.'
    },
    internet: {
      input: document.getElementById('internet'),
      error: document.getElementById('internetError'),
      validate: (value) => value !== '' ? '' : 'Vui lòng chọn tình trạng Internet.'
    }
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
    summaryStudyTime: document.getElementById('summaryStudyTime'),
    summaryAbsences: document.getElementById('summaryAbsences'),
    summarySchoolsup: document.getElementById('summarySchoolsup'),
    summaryFamsup: document.getElementById('summaryFamsup'),
    summaryInternet: document.getElementById('summaryInternet'),
    summaryFailures: document.getElementById('summaryFailures'),
    summaryRequestedAt: document.getElementById('summaryRequestedAt'),
    requestStatusBadge: document.getElementById('requestStatusBadge'),
    formStatus: document.getElementById('formStatus'),
    formStateBadge: document.getElementById('formStateBadge'),
    connectionBadge: document.getElementById('connectionBadge'),
    apiEndpointLabel: document.getElementById('apiEndpointLabel'),
    apiEndpointText: document.getElementById('apiEndpointText'),
    payloadPreview: document.getElementById('payloadPreview')
  };

  const studyTimeLabels = {
    1: 'Dưới 2 giờ/tuần',
    2: 'Từ 2 đến 5 giờ/tuần',
    3: 'Từ 5 đến 10 giờ/tuần',
    4: 'Trên 10 giờ/tuần'
  };

  initializeConfig();

  form.addEventListener('submit', handleSubmit);
  resetBtn.addEventListener('click', handleReset);

  function initializeConfig() {
    const fullEndpoint = buildApiUrl(APP_CONFIG.predictEndpoint);

    if (result.apiEndpointLabel) {
      result.apiEndpointLabel.textContent = 'Dự đoán khả năng';
    }

    if (result.apiEndpointText) {
      result.apiEndpointText.textContent = fullEndpoint;
    }
  }

  function validateIntegerRange(value, min, max, label) {
    if (value === '') return `Vui lòng nhập ${label.toLowerCase()}.`;
    const numeric = Number(value);
    if (!Number.isInteger(numeric)) return `${label} phải là số nguyên.`;
    if (numeric < min || numeric > max) return `${label} phải trong khoảng ${min} đến ${max}.`;
    return '';
  }
  function showError(fieldKey, message) {
    const field = fields[fieldKey];

    if (!field || !field.input || !field.error) {
      return;
    }

    field.error.textContent = message;
    field.input.classList.toggle('input-error', Boolean(message));
    field.input.setAttribute('aria-invalid', Boolean(message));
  }

  function validateForm() {
    let valid = true;

    Object.keys(fields).forEach((key) => {
      const message = fields[key].validate(fields[key].input.value);
      showError(key, message);
      if (message) valid = false;
    });

    return valid;
  }

  function getPayload() {
    return {
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
  }
  function renderPayload(payload) {
    if (!result.payloadPreview) return;

    result.payloadPreview.textContent = JSON.stringify({
      studytime: payload.studytime,
      absences: payload.absences,
      failures: payload.failures,
      schoolsup: payload.schoolsup,
      famsup: payload.famsup,
      internet: payload.internet
    }, null, 2);
  }

  function buildApiUrl(endpoint) {
    if (!APP_CONFIG.apiBaseUrl) return endpoint;
    return `${APP_CONFIG.apiBaseUrl.replace(/\/$/, '')}${endpoint}`;
  }

  async function postPrediction(payload) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), APP_CONFIG.requestTimeoutMs);

    try {
      const response = await fetch(buildApiUrl(APP_CONFIG.predictEndpoint), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
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
        const message = data.message || data.detail || `Yêu cầu thất bại với mã ${response.status}.`;
        throw new Error(message);
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
    const score20 = pickNumber(data, [
      'predicted_score',
      'predictedScore',
      'prediction',
      'score',
      'g3_prediction',
      'predicted_g3',
      'predicted_score_20'
    ]);

    if (score20 === null) {
      throw new Error('Không tìm thấy trường điểm dự đoán trong phản hồi từ backend.');
    }

    const normalizedScore20 = Math.max(0, Math.min(20, score20));
    const score10 = pickNumber(data, ['predicted_score_10', 'predictedScore10']) ?? (normalizedScore20 / 2);
    const label = pickString(data, ['label', 'status', 'level']) ?? buildDefaultLabel(normalizedScore20);
    const description = pickString(data, ['description', 'desc', 'summary']) ?? buildDefaultDescription(normalizedScore20);
    const advice = pickString(data, ['advice', 'recommendation', 'message', 'feedback']) ?? buildDefaultAdvice(payload, normalizedScore20);

    return {
      predicted20: normalizedScore20.toFixed(1),
      predicted10: Number(score10).toFixed(1),
      label,
      description,
      advice
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

  function pickString(source, keys) {
    for (const key of keys) {
      const value = source?.[key];
      if (typeof value === 'string' && value.trim()) return value.trim();
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
    if (score20 >= 16) {
      return 'Tiếp tục duy trì nhịp học hiện tại, đồng thời tập trung luyện các chuyên đề trọng tâm trước kỳ kiểm tra cuối.';
    }

    if (score20 >= 12) {
      return payload.absences > 5
        ? 'Nên giảm số buổi vắng học và bổ sung thêm thời gian tự học để cải thiện kết quả cuối kỳ.'
        : 'Nên tăng cường luyện tập theo từng chuyên đề và củng cố các phần kiến thức còn yếu.';
    }

    return 'Cần xây dựng lại kế hoạch học tập, ưu tiên ôn lại kiến thức nền tảng và theo dõi sát điểm quá trình trong các tuần tới.';
  }

  function setUiState(type, message) {
    if (result.formStatus) {
      result.formStatus.textContent = message;
      result.formStatus.className = `status-banner ${type}`;
    }

    if (result.formStateBadge) {
      result.formStateBadge.textContent =
        type === 'loading' ? 'Đang gửi' :
          type === 'success' ? 'Hoàn tất' :
            type === 'error' ? 'Lỗi' :
              'Sẵn sàng';
    }

    if (result.requestStatusBadge) {
      result.requestStatusBadge.textContent =
        type === 'loading' ? 'Đang xử lý' :
          type === 'success' ? 'Thành công' :
            type === 'error' ? 'Thất bại' :
              'Chưa gửi';
    }

    if (result.connectionBadge) {
      result.connectionBadge.textContent =
        type === 'loading' ? 'Đang chờ phản hồi từ backend' :
          type === 'success' ? 'Kết nối thành công' :
            type === 'error' ? 'Kết nối lỗi' :
              'Sẵn sàng gửi yêu cầu';
    }
  }

  function updateResult(payload, normalized) {
    result.resultPanel.classList.remove('empty-state');
    result.predictedScore.textContent = normalized.predicted20;
    result.predictedScore10.textContent = normalized.predicted10;
    result.scoreStatus.textContent = normalized.label;
    result.scoreDesc.textContent = normalized.description;
    result.feedbackText.textContent = normalized.advice;

    result.summarySchoolsup.textContent = payload.schoolsup === 1 ? 'Có' : 'Không';
    result.summaryFamsup.textContent = payload.famsup === 1 ? 'Có' : 'Không';
    result.summaryInternet.textContent = payload.internet === 1 ? 'Có' : 'Không';

    result.summaryStudent.textContent = payload.student_name;
    result.summaryClass.textContent = payload.class_name;
    result.summaryStudyTime.textContent = `${payload.studytime} • ${studyTimeLabels[payload.studytime]}`;
    result.summaryAbsences.textContent = String(payload.absences);
    // result.summaryG1.textContent = String(payload.G1);
    // result.summaryG2.textContent = String(payload.G2);
    result.summaryFailures.textContent = String(payload.failures);
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
      <td>${payload.studytime}</td>
      <td>${payload.schoolsup === 1 ? 'Có' : 'Không'}</td>
      <td>${payload.famsup === 1 ? 'Có' : 'Không'}</td>
      <td>${payload.internet === 1 ? 'Có' : 'Không'}</td>
      <td>${normalized.predicted20}</td>
    `;
    historyBody.prepend(row);

    while (historyBody.children.length > 6) {
      historyBody.removeChild(historyBody.lastElementChild);
    }
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

    const payload = getPayload();
    renderPayload(payload);
    submitBtn.disabled = true;
    setUiState('loading', 'Đang gửi dữ liệu đến backend và chờ kết quả dự đoán...');

    try {
      const data = await postPrediction(payload);
      console.log('Response from /Predict/Submit:', data);
      const normalized = normalizeResponse(data, payload);
      updateResult(payload, normalized);
      appendHistory(payload, normalized);
      setUiState('success', 'Nhận kết quả dự đoán thành công.');
      document.getElementById('result-section')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
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
      result.resultPanel.classList.add('empty-state');
      result.predictedScore.textContent = '--';
      result.predictedScore10.textContent = '--';
      result.scoreStatus.textContent = 'Chưa có dữ liệu';
      result.scoreDesc.textContent = 'Gửi biểu mẫu để xem kết quả từ backend.';
      result.feedbackText.textContent = 'Hệ thống sẽ hiển thị nhận xét sau khi nhận phản hồi thành công từ dịch vụ dự đoán.';
      result.summaryStudent.textContent = '--';
      result.summaryClass.textContent = '--';
      result.summaryStudyTime.textContent = '--';
      result.summaryAbsences.textContent = '--';
      result.summarySchoolsup.textContent = '--';
      result.summaryFamsup.textContent = '--';
      result.summaryInternet.textContent = '--';
      result.summaryFailures.textContent = '--';
      result.summaryRequestedAt.textContent = '--';
      if (result.payloadPreview) {
        result.payloadPreview.textContent = JSON.stringify({
          studytime: null,
          absences: null,
          failures: null,
          schoolsup: null,
          famsup: null,
          internet: null
        }, null, 2);
      }
      setUiState('idle', 'Sẵn sàng gửi yêu cầu.');
    }, 0);
  }
});
