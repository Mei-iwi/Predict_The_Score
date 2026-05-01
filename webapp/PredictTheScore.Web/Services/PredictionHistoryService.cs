using MySqlConnector;
using PredictTheScore.Web.Models.Prediction;

namespace PredictTheScore.Web.Models.Prediction;

public class PredictionHistoryService : IPredictionHistoryService
{
    private readonly IConfiguration _configuration;

    public PredictionHistoryService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public async Task SaveAsync(
     PredictionInputModel input,
     PredictionRequestDto mlRequest,
     PredictionResponseDto result,
     CancellationToken cancellationToken = default)
    {
        var connectionString = _configuration.GetConnectionString("DefaultConnection");

        if (string.IsNullOrWhiteSpace(connectionString))
        {
            throw new InvalidOperationException("Thiếu ConnectionStrings:DefaultConnection trong appsettings.json");
        }

        await using var conn = new MySqlConnection(connectionString);
        await conn.OpenAsync(cancellationToken);

        const string sql = """
        INSERT INTO PredictionHistory
        (
            StudentName,
            ClassName,
            StudyTime,
            Failures,
            Absences,
            SchoolSup,
            FamSup,
            Internet,
            Note,
            PredictedScore,
            ModelName
        )
        VALUES
        (
            @StudentName,
            @ClassName,
            @StudyTime,
            @Failures,
            @Absences,
            @SchoolSup,
            @FamSup,
            @Internet,
            @Note,
            @PredictedScore,
            @ModelName
        );
        """;

        await using var cmd = new MySqlCommand(sql, conn);

        cmd.Parameters.AddWithValue("@StudentName", input.StudentName ?? string.Empty);
        cmd.Parameters.AddWithValue("@ClassName", input.ClassName ?? string.Empty);
        cmd.Parameters.AddWithValue("@StudyTime", mlRequest.Studytime);
        cmd.Parameters.AddWithValue("@Failures", mlRequest.Failures);
        cmd.Parameters.AddWithValue("@Absences", mlRequest.Absences);
        cmd.Parameters.AddWithValue("@SchoolSup", mlRequest.Schoolsup);
        cmd.Parameters.AddWithValue("@FamSup", mlRequest.Famsup);
        cmd.Parameters.AddWithValue("@Internet", mlRequest.Internet);
        cmd.Parameters.AddWithValue("@Note", input.Note ?? string.Empty);
        cmd.Parameters.AddWithValue("@PredictedScore", result.PredictedScore);
        cmd.Parameters.AddWithValue("@ModelName", result.ModelName);

        await cmd.ExecuteNonQueryAsync(cancellationToken);
    }

    public async Task<IReadOnlyList<PredictionHistory>> GetLatestAsync(
        int take = 20,
        CancellationToken cancellationToken = default)
    {
        var connectionString = _configuration.GetConnectionString("DefaultConnection");

        if (string.IsNullOrWhiteSpace(connectionString))
        {
            throw new InvalidOperationException("Thiếu ConnectionStrings:DefaultConnection trong appsettings.json");
        }

        var histories = new List<PredictionHistory>();

        await using var conn = new MySqlConnection(connectionString);
        await conn.OpenAsync(cancellationToken);

        const string sql = """
    SELECT
        Id,
        StudentName,
        ClassName,
        StudyTime,
        Failures,
        Absences,
        SchoolSup,
        FamSup,
        Internet,
        Note,
        PredictedScore,
        ModelName,
        CreatedAt
    FROM PredictionHistory
    ORDER BY CreatedAt DESC
    LIMIT @Take;
    """;

        await using var cmd = new MySqlCommand(sql, conn);
        cmd.Parameters.AddWithValue("@Take", take);

        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);

        while (await reader.ReadAsync(cancellationToken))
        {
            histories.Add(new PredictionHistory
            {
                Id = reader.GetInt64(reader.GetOrdinal("Id")),
                StudentName = reader.IsDBNull(reader.GetOrdinal("StudentName"))
    ? null
    : reader.GetString(reader.GetOrdinal("StudentName")),

                ClassName = reader.IsDBNull(reader.GetOrdinal("ClassName"))
    ? null
    : reader.GetString(reader.GetOrdinal("ClassName")),

                Note = reader.IsDBNull(reader.GetOrdinal("Note"))
    ? null
    : reader.GetString(reader.GetOrdinal("Note")),
                StudyTime = reader.GetInt32(reader.GetOrdinal("StudyTime")),
                Failures = reader.GetInt32(reader.GetOrdinal("Failures")),
                Absences = reader.GetInt32(reader.GetOrdinal("Absences")),
                SchoolSup = reader.GetInt32(reader.GetOrdinal("SchoolSup")),
                FamSup = reader.GetInt32(reader.GetOrdinal("FamSup")),
                Internet = reader.GetInt32(reader.GetOrdinal("Internet")),
                PredictedScore = reader.GetDecimal(reader.GetOrdinal("PredictedScore")),
                ModelName = reader.GetString(reader.GetOrdinal("ModelName")),
                CreatedAt = reader.GetDateTime(reader.GetOrdinal("CreatedAt"))
            });
        }

        return histories;
    }
}