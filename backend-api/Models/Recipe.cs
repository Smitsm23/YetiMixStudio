using System.Collections.Generic;

// Request sent to the Python microservice (will be serialized to snake_case).
public record RecipeRequest(
    string TargetHex,
    List<Paint> AvailablePaints
);

// Response received from the Python microservice (will be deserialized from snake_case).
public record RecipeResponse(
    Dictionary<string, int> Recipe,
    double Accuracy,
    string MixedHex
);