using System.Text.Json;

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
            // Gọi FastAPI bằng JSON để giữ contract giống Swagger của backend ML.
            var response = await _httpClient.PostAsJsonAsync(endpoint, request, cancellationToken);
            var rawBody = await response.Content.ReadAsStringAsync(cancellationToken);

            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning("ML API returned error, StatusCode={StatusCode}, Body={Body}", response.StatusCode, rawBody);
                throw new InvalidOperationException(ParseErrorMessage(rawBody, (int)response.StatusCode));
            }

            var result = await response.Content.ReadFromJsonAsync<PredictionResponseDto>(cancellationToken: cancellationToken);
            if (result == null)
            {
                throw new InvalidOperationException("ML API trả về dữ liệu rỗng");
            }

            return result;
        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(ex, "Timeout when calling ML API");
            throw new InvalidOperationException("Quá thời gian chờ phản hồi từ ML API");
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Cannot connect to ML API");
            throw new InvalidOperationException("Không kết nối được backend ML");
        }
    }

    private static string ParseErrorMessage(string rawBody, int statusCode)
    {
        if (!string.IsNullOrWhiteSpace(rawBody))
        {
            try
            {
                using var doc = JsonDocument.Parse(rawBody);
                if (doc.RootElement.TryGetProperty("detail", out var detail))
                {
                    return detail.ValueKind == JsonValueKind.String
                        ? detail.GetString() ?? $"ML API lỗi với mã trạng thái {statusCode}"
                        : detail.ToString();
                }
            }
            catch (JsonException)
            {
                return rawBody;
            }
        }

        return $"ML API lỗi với mã trạng thái {statusCode}";
    }
}
