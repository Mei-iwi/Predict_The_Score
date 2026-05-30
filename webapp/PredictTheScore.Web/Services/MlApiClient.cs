namespace PredictTheScore.Web.Models.Prediction;

public class MlApiClient : IMlApiClient
{
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _configuration;
    private readonly ILogger<MlApiClient> _logger;

    public MlApiClient(HttpClient httpClient, IConfiguration configuration, ILogger<MlApiClient> logger)
    {
        _httpClient = httpClient;
        _configuration = configuration;
        _logger = logger;
    }

    public async Task<PredictionResponseDto> PredictAsync(PredictionRequestDto request, CancellationToken cancellationToken = default)
    {
        var endpoint = _configuration["MlService:PredictEndpoint"] ?? "/predict";

        try
        {
            var response = await _httpClient.PostAsJsonAsync(endpoint, request, cancellationToken);
            var rawBody = await response.Content.ReadAsStringAsync(cancellationToken);

            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning("ML API returned error, StatusCode={StatusCode}, Body={Body}", response.StatusCode, rawBody);
                throw new InvalidOperationException($"ML API loi voi ma trang thai {(int)response.StatusCode}");
            }

            var result = await response.Content.ReadFromJsonAsync<PredictionResponseDto>(cancellationToken: cancellationToken);
            if (result == null)
            {
                throw new InvalidOperationException("ML API tra ve du lieu rong");
            }

            return result;
        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(ex, "Timeout when calling ML API");
            throw new InvalidOperationException("Qua thoi gian cho phan hoi tu ML API");
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Cannot connect to ML API");
            throw new InvalidOperationException("Khong ket noi duoc backend ML");
        }
    }
}
