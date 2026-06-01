using Microsoft.AspNetCore.Mvc;
using PredictTheScore.Web.Models.Prediction;

namespace PredictTheScore.Web.Controllers;

[ApiController]
[Route("[controller]")]
public class PredictController : Controller
{
    private readonly IMlApiClient _mlApiClient;
    private readonly ILogger<PredictController> _logger;
    private readonly IPredictionHistoryService _historyService;

    public PredictController(IMlApiClient mlApiClient, ILogger<PredictController> logger, IPredictionHistoryService historyService)
    {
        _mlApiClient = mlApiClient;
        _logger = logger;
        _historyService = historyService;
    }
    [HttpPost("Submit")]
    public async Task<IActionResult> Submit([FromBody] PredictionInputModel input, CancellationToken cancellationToken)
    {
        // MVC nhận dữ liệu từ form web, kiểm tra validation rồi chỉ gửi 6 field model cần sang FastAPI.
        if (!ModelState.IsValid)
        {
            return ValidationProblem(ModelState);
        }

        var mlRequest = new PredictionRequestDto
        {
            Studytime = input.Studytime,
            Failures = input.Failures,
            Absences = input.Absences,
            Schoolsup = input.Schoolsup,
            Famsup = input.Famsup,
            Internet = input.Internet
        };

        try
        {
            var prediction = await _mlApiClient.PredictAsync(mlRequest, cancellationToken);
            // Backend ML đã trả thang 10; dòng fallback giữ UI ổn nếu backend cũ chưa có field này.
            var predictedScore10 = prediction.PredictedScore10 > 0
                ? prediction.PredictedScore10
                : Math.Round(prediction.PredictedScore / 2, 2);
            await _historyService.SaveAsync(input, mlRequest, prediction, cancellationToken);

            return Ok(new
            {
                predicted_score = prediction.PredictedScore,
                predicted_score_10 = predictedScore10,
                model_name = prediction.ModelName,
                student_name = input.StudentName,
                class_name = input.ClassName,
                message = string.IsNullOrWhiteSpace(prediction.Message)
                    ? "Dự đoán thành công"
                    : prediction.Message
            });
        }
        catch (InvalidOperationException ex)
        {
            _logger.LogWarning(ex, "Prediction failed");
            return StatusCode(StatusCodes.Status502BadGateway, new
            {
                message = "Không kết nối được ML backend. Hãy kiểm tra FastAPI đang chạy đúng địa chỉ."
            });
        }


    }
    [HttpGet("History")]
    public async Task<IActionResult> History(
       [FromQuery] int take = 10,
       CancellationToken cancellationToken = default)
    {
        // History được dùng để giao diện tải lại các lần dự đoán gần nhất từ MySQL.
        var histories = await _historyService.GetLatestAsync(take, cancellationToken);

        var result = histories.Select(x => new
        {
            id = x.Id,
            student_name = x.StudentName,
            class_name = x.ClassName,
            studytime = x.StudyTime,
            failures = x.Failures,
            absences = x.Absences,
            schoolsup = x.SchoolSup,
            famsup = x.FamSup,
            internet = x.Internet,
            note = x.Note,
            predicted_score = x.PredictedScore,
            predicted_score_10 = x.PredictedScore10,
            model_name = x.ModelName,
            created_at = x.CreatedAt.ToString("dd/MM/yyyy HH:mm:ss")
        });

        return Ok(result);
    }

}
