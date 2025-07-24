using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Caching.Memory; // Add this using statement

[ApiController]
[Route("api/[controller]")]
public class PaintsController : ControllerBase
{
    private readonly IHttpClientFactory _clientFactory;
    private readonly IConfiguration _configuration;
    private readonly ILogger<PaintsController> _logger;
    private readonly IMemoryCache _memoryCache; // Add the cache

    // Update the constructor to accept the cache
    public PaintsController(IHttpClientFactory clientFactory, IConfiguration configuration, ILogger<PaintsController> logger, IMemoryCache memoryCache)
    {
        _clientFactory = clientFactory;
        _configuration = configuration;
        _logger = logger;
        _memoryCache = memoryCache;
    }

    [HttpGet]
    public async Task<IActionResult> GetAllPaints()
    {
        _logger.LogInformation("--- GetAllPaints endpoint was hit! ---");

        const string cacheKey = "AllPaintsList";

        // Try to get paints from cache, checking if the result is actually not null
        if (_memoryCache.TryGetValue(cacheKey, out List<Paint>? paints) && paints != null)
        {
            _logger.LogInformation($"Serving {paints.Count} paints from cache.");
            return Ok(paints);
        }

        _logger.LogInformation("No cache found. Fetching from Supabase...");

        var supabaseUrl = _configuration["Supabase:Url"];
        var supabaseKey = _configuration["Supabase:ApiKey"];

        if (string.IsNullOrEmpty(supabaseUrl) || string.IsNullOrEmpty(supabaseKey))
        {
            _logger.LogError("Supabase configuration is missing.");
            return StatusCode(500, "Supabase configuration is missing.");
        }

        try
        {
            var requestUrl = $"{supabaseUrl}/rest/v1/paints?select=*&is_deleted=eq.false&limit=7000";
            var client = _clientFactory.CreateClient();
            client.DefaultRequestHeaders.Add("apikey", supabaseKey);
            client.DefaultRequestHeaders.Add("Authorization", $"Bearer {supabaseKey}");
            
            var response = await client.GetAsync(requestUrl);

            if (response.IsSuccessStatusCode)
            {
                var jsonResponse = await response.Content.ReadAsStringAsync();
                var options = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower };
                var fetchedPaints = JsonSerializer.Deserialize<List<Paint>>(jsonResponse, options);

                // THIS IS THE KEY FIX: Check for a null result after deserializing
                if (fetchedPaints == null)
                {
                    _logger.LogError("Failed to deserialize paints from Supabase; response was likely empty or invalid.");
                    return StatusCode(500, "Could not process response from data source.");
                }

                _logger.LogInformation($"Successfully fetched {fetchedPaints.Count} paints.");

                var cacheEntryOptions = new MemoryCacheEntryOptions()
                    .SetAbsoluteExpiration(TimeSpan.FromHours(24));

                _memoryCache.Set(cacheKey, fetchedPaints, cacheEntryOptions);

                return Ok(fetchedPaints);
            }
            
            _logger.LogError($"Error fetching from Supabase. Status: {response.StatusCode}");
            return StatusCode((int)response.StatusCode, "Error fetching paints from Supabase.");
        }
        catch (HttpRequestException e)
        {
            _logger.LogError(e, "Error contacting Supabase.");
            return StatusCode(503, $"Service unavailable: {e.Message}");
        }
    }
}