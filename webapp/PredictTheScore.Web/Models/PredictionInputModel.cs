using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace PredictTheScore.Web.Models.Prediction;

// Nhận dữ liệu từ giao diện web
public class PredictionInputModel
{
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
    [Range(0, 10, ErrorMessage = "Failures phải từ 0 đến 10")]
    public int Failures { get; set; }


    [JsonPropertyName("absences")]
    [Required(ErrorMessage = "Vui lòng nhập số buổi vắng")]
    [Range(0, 100, ErrorMessage = "Absences phải từ 0 đến 100")]
    public int Absences { get; set; }

    [JsonPropertyName("schoolsup")]
    [Required(ErrorMessage = "Vui lòng chọn hỗ trợ từ nhà trường")]
    [Range(0, 1, ErrorMessage = "Schoolsup chỉ nhận o hoặc 1")]
    public int Schoolsup { get; set; }


    [JsonPropertyName("famsup")]
    [Required(ErrorMessage = "Vui lòng chọn hỗ trợ từ gia đình")]
    [Range(0, 1, ErrorMessage = "Famsup chỉ nhận 0 hoặc 1")]
    public int Famsup { get; set; }


    [JsonPropertyName("internet")]
    [Required(ErrorMessage = "Vui lòng chọn tình trạng Internet")]
    [Range(0, 100, ErrorMessage = "Internet chỉ nhật 0 hoặc 1")]
    public int Internet { get; set; }


    [JsonPropertyName("note")]
    public string? Note { get; set; }
}