namespace PredictTheScore.Web.Models.Prediction;

public interface IMlApiClient
{
    Task<PredictionReponseDto> PredictAsync(PredictionRequestDto request, CancellationToken cancellationToken = default);
}