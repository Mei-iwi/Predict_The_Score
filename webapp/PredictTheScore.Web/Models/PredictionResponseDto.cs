using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Nhận kết quả từ fastapi
public class PredictionResponseDto
{
    [JsonPropertyName("predicted_score")]
    public double PredictedScore { get; set; }

    [JsonPropertyName("predicted_score_10")]
    public double PredictedScore10 { get; set; }

    [JsonPropertyName("model_name")]
    public string ModelName { get; set; } = string.Empty;

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;
}
