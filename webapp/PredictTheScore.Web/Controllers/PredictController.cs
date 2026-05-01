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
            await _historyService.SaveAsync(input, mlRequest, prediction, cancellationToken);

            return Ok(new
            {
                predicted_score = prediction.PredictedScore,
                predicted_score_10 = Math.Round(prediction.PredictedScore / 2, 2),
                model_name = prediction.ModelName,
                student_name = input.StudentName,
                class_name = input.ClassName,
                message = "Dự đoán thành công"
            });
        }
        catch (InvalidOperationException ex)
        {
            _logger.LogWarning(ex, "Prediction failed");
            return StatusCode(StatusCodes.Status502BadGateway, new
            {
                message = ex.Message
            });
        }


    }
    [HttpGet("History")]
    public async Task<IActionResult> History(
       [FromQuery] int take = 10,
       CancellationToken cancellationToken = default)
    {
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
            predicted_score_10 = Math.Round((double)x.PredictedScore / 2, 2),
            model_name = x.ModelName,
            created_at = x.CreatedAt.ToString("dd/MM/yyyy HH:mm:ss")
        });

        return Ok(result);
    }

}