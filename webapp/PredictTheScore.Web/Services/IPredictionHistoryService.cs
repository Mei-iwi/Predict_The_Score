using PredictTheScore.Web.Models.Prediction;

namespace PredictTheScore.Web.Models.Prediction;

public interface IPredictionHistoryService
{
    Task SaveAsync(
        PredictionInputModel input,
        PredictionRequestDto mlRequest,
        PredictionResponseDto result,
        CancellationToken cancellationToken = default
    );

    Task<IReadOnlyList<PredictionHistory>> GetLatestAsync(
        int take = 20,
        CancellationToken cancellationToken = default
    );
}