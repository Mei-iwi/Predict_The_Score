using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Chỉ chứa dữ liệu gửi sang fastapi
public class PredictionRequestDto
{
    [JsonPropertyName("studytime")]
    public int Studytime { get; set; }
    [JsonPropertyName("failures")]
    public int Failures { get; set; }
    [JsonPropertyName("absences")]
    public int Absences { get; set; }
    [JsonPropertyName("schoolsup")]
    public int Schoolsup { get; set; }
    [JsonPropertyName("famsup")]
    public int Famsup { get; set; }
    [JsonPropertyName("internet")]
    public int Internet { get; set; }
}