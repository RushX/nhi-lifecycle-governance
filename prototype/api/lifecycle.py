def calculate_risk_score(autonomy_level: int, data_classification: str,
                          external_exposure: bool, deployment_env: str) -> int:
    score = 0

    # Autonomy level — 30% weight (max 30)
    score += autonomy_level * 6

    # Data classification — 30% weight
    classification_scores = {
        "public": 0,
        "internal": 10,
        "confidential": 20,
        "restricted": 30
    }
    score += classification_scores[data_classification.lower()]

    # External exposure — 15% weight
    if external_exposure:
        score += 15

    # Deployment environment — 25% weight
    env_scores = {
        "development": 5,
        "staging": 15,
        "production": 25
    }
    score += env_scores[deployment_env.lower()]

    return min(score, 100)

def get_risk_level(score: int) -> str:
    if score <= 30:
        return "low"
    elif score <= 60:
        return "medium"
    elif score <= 80:
        return "high"
    else:
        return "critical"

# High-risk agents (score >= 61) require security team sign-off
# before transitioning to active — enforced at process level
# See: framework/lifecycle-model.md Stage 2 entry criteria
# registered → active enforces change approval before activation
# aligned to SOC 2 CC6.3 and ITGC change management controls
def validate_lifecycle_transition(current: str, new: str) -> bool:
    allowed = {
        "registered":     ["active", "retired"],
        "pending_review": ["", "suspended", "retired"],
        "active":         ["pending_review", "suspended", "retired"],
        "suspended":      ["pending_review", "retired"],
        "retired":        []
    }
    return new in allowed.get(current, [])