# Database Schema Note

The project uses MySQL and raw SQL through `MySqlConnector`. Entity Framework is not used.

## Table: PredictionHistory

The `PredictionHistory` table stores each prediction made from the web app.

Important columns:

- `StudentName`: student name entered on the form.
- `ClassName`: class name entered on the form.
- `StudyTime`, `Failures`, `Absences`, `SchoolSup`, `FamSup`, `Internet`: model input values.
- `Note`: optional note from the form.
- `PredictedScore`: predicted G3 score on the 20-point scale.
- `PredictedScore10`: predicted score converted to the 10-point scale.
- `ModelName`: model or scenario returned by FastAPI.
- `Scenario`: selected prediction scenario, for example `web_minimal`, `early_warning`, or `reference`.
- `CreatedAt`: time the prediction was saved.

Create the table with:

```bash
mysql -u <user> -p < database/schema/001_init.sql
```

If the table already existed before `PredictedScore10` was added, run:

```bash
mysql -u <user> -p < database/migrations/002_add_predicted_score_10.sql
```

If the table already existed before `Scenario` was added, run:

```bash
mysql -u <user> -p < database/migrations/003_add_scenario.sql
```

The web app reads the connection string from `ConnectionStrings:DefaultConnection` in `appsettings.json` or environment configuration.
