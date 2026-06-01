using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Chứa field gửi sang FastAPI; field nâng cao chỉ có giá trị khi scenario cần.
public class PredictionRequestDto
{
    [JsonPropertyName("scenario")]
    public string Scenario { get; set; } = "web_minimal";

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

    [JsonPropertyName("subject")]
    public string? Subject { get; set; }

    [JsonPropertyName("higher")]
    public int? Higher { get; set; }

    [JsonPropertyName("traveltime")]
    public int? Traveltime { get; set; }

    [JsonPropertyName("G1")]
    public int? G1 { get; set; }

    [JsonPropertyName("G2")]
    public int? G2 { get; set; }
}
