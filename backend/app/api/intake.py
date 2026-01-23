"""
Intake API endpoints for AI-guided section recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.schemas.intake import (
    DiscoveryQuestion,
    DiscoveryQuestionnaire,
    IntakeRecommendationResponse,
    SubmitIntakeRequest,
)
from app.schemas.user import CurrentUserResponse
from app.services.intake_service import generate_recommendations

router = APIRouter()


@router.get("/questions", response_model=DiscoveryQuestionnaire)
async def get_discovery_questions(request: Request) -> DiscoveryQuestionnaire:
    """Get the discovery questionnaire for intake"""

    questions = [
        DiscoveryQuestion(
            id="role",
            text="What best describes your role?",
            type="single_select",
            options=[
                {"value": "ciso", "label": "CISO / Head of Security"},
                {
                    "value": "security_manager",
                    "label": "Security Manager / Security Analyst",
                },
                {"value": "it_manager", "label": "IT Manager / Infrastructure Lead"},
                {"value": "cio_cto", "label": "CIO / CTO"},
                {"value": "founder", "label": "Founder / Business Owner"},
                {"value": "consultant", "label": "Consultant / Advisor"},
                {"value": "other", "label": "Other"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="org_size",
            text="Roughly how big is your organisation?",
            type="single_select",
            options=[
                {"value": "1-50", "label": "1–50"},
                {"value": "51-250", "label": "51–250"},
                {"value": "251-1000", "label": "251–1000"},
                {"value": "1000+", "label": "1000+"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="sector",
            text="Which sector fits you best?",
            type="single_select",
            options=[
                {
                    "value": "general_corporate",
                    "label": "General Corporate / Professional Services",
                },
                {"value": "finance", "label": "Finance / Banking / Insurance"},
                {"value": "healthcare", "label": "Healthcare / Life Sciences"},
                {"value": "government", "label": "Government / Public Sector"},
                {"value": "energy", "label": "Energy / Utilities"},
                {"value": "manufacturing", "label": "Manufacturing / Industrial"},
                {"value": "saas_tech", "label": "SaaS / Technology"},
                {"value": "other", "label": "Other / Not sure"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="environment",
            text="Where do most of your systems run today?",
            type="single_select",
            options=[
                {"value": "on_premises", "label": "Mostly on-premises"},
                {"value": "cloud", "label": "Mostly in the cloud"},
                {"value": "hybrid", "label": "Hybrid (mix of cloud + on-prem)"},
                {"value": "not_sure", "label": "Not sure"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="system_types",
            text="Which of these do you have today?",
            type="multi_select",
            options=[
                {
                    "value": "ot_ics",
                    "label": "OT/ICS / SCADA / Industrial control systems",
                },
                {
                    "value": "public_web_apps",
                    "label": "Public-facing web applications or APIs",
                },
                {
                    "value": "internal_custom_apps",
                    "label": "Internal custom applications (developed in-house)",
                },
                {
                    "value": "saas_tools",
                    "label": "Mainly SaaS tools (e.g. Microsoft 365, Google Workspace, CRM)",
                },
                {"value": "other", "label": "Other"},
                {"value": "not_sure", "label": "Not sure"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="cloud_providers",
            text="Which cloud platforms do you use?",
            type="multi_select",
            options=[
                {"value": "aws", "label": "AWS"},
                {"value": "azure", "label": "Azure"},
                {"value": "gcp", "label": "Google Cloud Platform (GCP)"},
                {"value": "other", "label": "Other"},
                {"value": "none", "label": "None"},
                {"value": "not_sure", "label": "Not sure"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="primary_goal",
            text="What's your primary reason for doing this assessment?",
            type="single_select",
            options=[
                {
                    "value": "overall_posture",
                    "label": "Understand our overall security posture",
                },
                {
                    "value": "audit_cert",
                    "label": "Prepare for an audit or certification (e.g. ISO 27001, SOC 2)",
                },
                {
                    "value": "cloud_identity",
                    "label": "Focus specifically on cloud and identity security",
                },
                {
                    "value": "supplier_gaps",
                    "label": "Understand gaps before engaging a supplier/partner",
                },
                {
                    "value": "benchmark",
                    "label": "Benchmark ourselves against best practices",
                },
                {"value": "other", "label": "Something else"},
            ],
            required=True,
        ),
        DiscoveryQuestion(
            id="time_preference",
            text="How much time do you want to spend today?",
            type="single_select",
            options=[
                {
                    "value": "quick",
                    "label": "Quick overview (approx. 10–15 minutes, only key sections)",
                },
                {
                    "value": "moderate",
                    "label": "Moderate depth (approx. 30–40 minutes, more coverage)",
                },
                {
                    "value": "deep",
                    "label": "Deep dive (I'm happy to go into detailed sections)",
                },
            ],
            required=True,
        ),
    ]

    return DiscoveryQuestionnaire(questions=questions)


@router.post("/recommend", response_model=IntakeRecommendationResponse)
async def submit_intake_and_recommend(
    request: Request,
    intake_request: SubmitIntakeRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse | None = Depends(get_current_user),
) -> IntakeRecommendationResponse:
    """
    Submit intake answers and get AI-powered section recommendations.
    Works for both authenticated and anonymous users.
    """
    try:
        user_id = current_user.id if current_user else None

        recommendations = generate_recommendations(
            answers=intake_request.answers,
            db=db,
            user_id=user_id,
        )

        return recommendations

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}",
        )
