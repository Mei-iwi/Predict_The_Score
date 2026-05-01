using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Nhận kết quả từ fastapi
public class PredictionResponseDto
{
    [JsonPropertyName("predicted_score")]
    public double PredictedScore { get; set; }

    [JsonPropertyName("model_name")]
    public string ModelName { get; set; } = string.Empty;
}