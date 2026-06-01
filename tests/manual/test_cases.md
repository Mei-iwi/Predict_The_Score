# Manual Test Cases

## 1. Valid input
- Start FastAPI and the ASP.NET Core web app.
- Enter a student name, class name, and valid values:
  - studytime: 2
  - failures: 0
  - absences: 4
  - schoolsup: 1
  - famsup: 1
  - internet: 1
- Submit the form.
- Expected result: the page shows a prediction on the 20-point scale and the 10-point scale.

## 2. Invalid studytime
- Enter studytime outside the allowed range, for example 9.
- Submit the form.
- Expected result: validation prevents the request or the backend returns a clear 422 validation error.

## 3. Backend not running
- Stop the FastAPI backend.
- Keep the web app running and submit valid input.
- Expected result: the web page shows a friendly message that the ML backend is not running or cannot be reached.

## 4. History is saved after prediction
- Start the database, FastAPI backend, and web app.
- Submit a valid prediction.
- Refresh the page or reload history.
- Expected result: the latest prediction appears in the history table with student name, class name, input values, scores, model name, and created time.

## 5. Score conversion
- Submit a valid prediction.
- Compare the two displayed scores.
- Expected result: the 10-point score equals the 20-point score divided by 2, rounded to two decimal places.

## 6. Advanced mode visibility
- Open the web app.
- Expected result: default form shows only the 6 `web_minimal` fields.
- Click "Nâng cấp mô hình dự đoán".
- Expected result: scenario selector appears.

## 7. early_warning scenario
- Select `early_warning`.
- Expected result: the form shows `subject`, `higher`, and `traveltime`.
- Submit valid input if `model_early_warning.joblib` exists.
- Expected result: prediction returns selected scenario, or a clear message says the model artifact must be trained.

## 8. reference scenario
- Select `reference`.
- Expected result: the form shows `subject`, `higher`, `traveltime`, `G1`, and `G2`.
- Submit valid input if `model_reference.joblib` exists.
- Expected result: prediction returns selected scenario, or a clear message says the model artifact must be trained.

## 9. Switch back to web_minimal
- Select `web_minimal` or reset the form.
- Expected result: advanced fields are hidden and quick prediction still works.
