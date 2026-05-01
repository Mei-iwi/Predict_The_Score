
using PredictTheScore.Web.Models.Prediction;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

builder.Services.AddScoped<IPredictionHistoryService, PredictionHistoryService>();

builder.Services.AddHttpClient<IMlApiClient, MlApiClient>((sp, client) =>
{
    var configuration = sp.GetRequiredService<IConfiguration>();

    var baseUrl = configuration["MlService:BaseUrl"] ?? "http://127.0.0.1:8000";

    var timeoutSeconds = configuration.GetValue<int?>("MlService:TimeoutSeconds") ?? 15;

    client.BaseAddress = new Uri(baseUrl);
    client.Timeout = TimeSpan.FromSeconds(timeoutSeconds);
});



var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
