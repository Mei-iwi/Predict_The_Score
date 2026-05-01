using Microsoft.AspNetCore.Mvc;
using PredictTheScore.Web.Models.Prediction;

namespace PredictTheScore.Web.Controllers;

[ApiController]
[Route("[controller]")]
public class PredictController : Controller
{
    private readonly IMlApiClient _mlApiClient;
    private readonly ILogger<PredictController> _logger;

    public PredictController(IMlApiClient mlApiClient, ILogger<PredictController> logger)
    {
        _mlApiClient = mlApiClient;
        _logger = logger;
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
}