namespace PredictTheScore.Web.Models.Prediction;

public class PredictionHistory
{
    public long Id { get; set; }

    public string? StudentName { get; set; }

    public string? ClassName { get; set; }

    public int StudyTime { get; set; }

    public int Failures { get; set; }

    public int Absences { get; set; }

    public int SchoolSup { get; set; }

    public int FamSup { get; set; }

    public int Internet { get; set; }

    public string? Note { get; set; }

    public decimal PredictedScore { get; set; }

    public string ModelName { get; set; } = string.Empty;

    public DateTime CreatedAt { get; set; }
}