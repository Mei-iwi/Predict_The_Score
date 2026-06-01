using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Nhận kết quả từ FastAPI, gồm điểm thang 20 và thang 10.
public class PredictionResponseDto
{
    [JsonPropertyName("predicted_score")]
    public double PredictedScore { get; set; }

    [JsonPropertyName("predicted_score_20")]
    public double PredictedScore20 { get; set; }

    [JsonPropertyName("predicted_score_10")]
    public double PredictedScore10 { get; set; }

    [JsonPropertyName("model_name")]
    public string ModelName { get; set; } = string.Empty;

    [JsonPropertyName("scenario")]
    public string Scenario { get; set; } = "web_minimal";

    [JsonPropertyName("model_scenario")]
    public string ModelScenario { get; set; } = "web_minimal";

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;
}
