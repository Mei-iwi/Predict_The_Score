using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Nhận dữ liệu từ giao diện web và giữ validation khớp với FastAPI.
public class PredictionInputModel
{
    [JsonPropertyName("scenario")]
    public string Scenario { get; set; } = "web_minimal";

    [JsonPropertyName("student_name")]
    public string? StudentName { get; set; }
    [JsonPropertyName("class_name")]
    public string? ClassName { get; set; }


    [JsonPropertyName("studytime")]
    [Required(ErrorMessage = "Vui lòng chọn mức thời gian tự học")]
    [Range(1, 4, ErrorMessage = "Studytime phải từ 1 đến 4")]
    public int Studytime { get; set; }


    [JsonPropertyName("failures")]
    [Required(ErrorMessage = "Vui lòng nhập số lần chưa đạt")]
    [Range(0, 4, ErrorMessage = "Failures phải từ 0 đến 4")]
    public int Failures { get; set; }


    [JsonPropertyName("absences")]
    [Required(ErrorMessage = "Vui lòng nhập số buổi vắng")]
    [Range(0, 93, ErrorMessage = "Absences phải từ 0 đến 93")]
    public int Absences { get; set; }

    [JsonPropertyName("schoolsup")]
    [Required(ErrorMessage = "Vui lòng chọn hỗ trợ từ nhà trường")]
    [Range(0, 1, ErrorMessage = "Schoolsup chỉ nhận 0 hoặc 1")]
    public int Schoolsup { get; set; }


    [JsonPropertyName("famsup")]
    [Required(ErrorMessage = "Vui lòng chọn hỗ trợ từ gia đình")]
    [Range(0, 1, ErrorMessage = "Famsup chỉ nhận 0 hoặc 1")]
    public int Famsup { get; set; }


    [JsonPropertyName("internet")]
    [Required(ErrorMessage = "Vui lòng chọn tình trạng Internet")]
    [Range(0, 1, ErrorMessage = "Internet chỉ nhận 0 hoặc 1")]
    public int Internet { get; set; }

    [JsonPropertyName("subject")]
    public string? Subject { get; set; }

    [JsonPropertyName("higher")]
    [Range(0, 1, ErrorMessage = "Higher chỉ nhận 0 hoặc 1")]
    public int? Higher { get; set; }

    [JsonPropertyName("traveltime")]
    [Range(1, 4, ErrorMessage = "Traveltime phải từ 1 đến 4")]
    public int? Traveltime { get; set; }

    [JsonPropertyName("G1")]
    [Range(0, 20, ErrorMessage = "G1 phải từ 0 đến 20")]
    public int? G1 { get; set; }

    [JsonPropertyName("G2")]
    [Range(0, 20, ErrorMessage = "G2 phải từ 0 đến 20")]
    public int? G2 { get; set; }

    [JsonPropertyName("note")]
    public string? Note { get; set; }
}
