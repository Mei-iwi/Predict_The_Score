
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


    public async Task<PredictionReponseDto> PredictAsync(PredictionRequestDto request, CancellationToken cancellationToken = default)
    {
        var endpoint = _configuration["MlService:PredictEndpoint"] ?? "/predict";
        try
        {
            var respone = await _httpClient.PostAsJsonAsync(endpoint, request, cancellationToken);

            var rawBody = await respone.Content.ReadAsStringAsync(cancellationToken);

            if (!respone.IsSuccessStatusCode)
            {
                _logger.LogWarning("ML API returned error, StatusCode={StatusCode}, Body={Body}", respone.StatusCode, rawBody);
                throw new InvalidOperationException($"ML API lỗi với mã trạng thái {(int)respone.StatusCode}");
            }
            var result = await respone.Content.ReadFromJsonAsync<PredictionReponseDto>(cancellationToken: cancellationToken);
            if (result == null)
            {
                throw new InvalidOperationException("ML API trả về dữ liệu rống");
            }
            return result;

        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(ex, "Timeout when calling ML api");
            throw new InvalidOperationException("Quá thời gian chờ phản hồi từ ML API");
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Cannot connect to ML API");
            throw new InvalidOperationException("Không kết nối được backend ML");
        }
    }
}