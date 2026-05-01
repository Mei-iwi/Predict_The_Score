namespace PredictTheScore.Web.Models.Prediction;

public interface IMlApiClient
{
    Task<PredictionResponseDto> PredictAsync(PredictionRequestDto request, CancellationToken cancellationToken = default);
}