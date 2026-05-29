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
