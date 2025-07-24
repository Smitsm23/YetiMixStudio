using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

[ApiController]
[Route("api/[controller]")]
public class RecipeController : ControllerBase
{
    private readonly IHttpClientFactory _clientFactory;
    private readonly IConfiguration _configuration;

    public RecipeController(IHttpClientFactory clientFactory, IConfiguration configuration)
    {
        _clientFactory = clientFactory;
        _configuration = configuration;
    }

    [HttpPost("generate")]
    public async Task<IActionResult> GenerateRecipe([FromBody] RecipeRequest request)
    {
        if (request == null || string.IsNullOrEmpty(request.TargetHex) || request.AvailablePaints.Count == 0)
        {
            return BadRequest("Invalid request data.");
        }

        var pythonServiceUrl = _configuration["PythonService:Url"];
        if (string.IsNullOrEmpty(pythonServiceUrl))
        {
            return StatusCode(500, "Python service URL is not configured.");
        }

        var client = _clientFactory.CreateClient();

        try
        {
            // IMPORTANT: Serialize to snake_case for the Python service
            var options = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower };
            var jsonPayload = JsonSerializer.Serialize(request, options);
            var content = new StringContent(jsonPayload, System.Text.Encoding.UTF8, "application/json");

            var response = await client.PostAsync($"{pythonServiceUrl}/generate-recipe", content);

            if (response.IsSuccessStatusCode)
            {
                var jsonResponse = await response.Content.ReadAsStringAsync();
                // IMPORTANT: Deserialize from snake_case from the Python service
                var recipes = JsonSerializer.Deserialize<List<RecipeResponse>>(jsonResponse, options);
                return Ok(recipes); // This will be serialized to camelCase for the frontend by default
            }

            return StatusCode((int)response.StatusCode, "Error fetching recipe from color service.");
        }
        catch (HttpRequestException e)
        {
            return StatusCode(503, $"Service unavailable: {e.Message}");
        }
    }
}