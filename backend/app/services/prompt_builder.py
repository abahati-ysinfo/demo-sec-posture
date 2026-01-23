"""Prompt builder service for AI report generation"""

from typing import Any

from app.core.config import settings
from app.services.pii_redactor import PIIRedactor


def build_section_prompt_v2(
    section: Any,
    section_responses: list[dict[str, Any]],
    curated_context: str = "",
    redact_pii: bool | None = None,
) -> tuple[str, int]:
    """Build JSON-mode prompt for section analysis with optional PII redaction

    Returns:
        tuple[str, int]: (prompt, redaction_count)
    """
    if redact_pii is None:
        redact_pii = settings.PII_REDACTION_ENABLED

    redaction_count = 0
    if redact_pii:
        redactor = PIIRedactor(enabled=True)
        section_responses, redaction_count = redactor.redact_responses(
            section_responses
        )

    signals = []
    for i, resp in enumerate(section_responses, 1):
        answer_str = str(resp["answer"])
        signal_parts = [f"Q{i}: {answer_str} (weight:{resp['weight']})"]

        if settings.INCLUDE_ENHANCED_CONTEXT_IN_AI and resp.get("context"):
            context_str = str(resp["context"])
            if len(context_str) > settings.MAX_CONTEXT_CHARS:
                context_str = context_str[: settings.MAX_CONTEXT_CHARS - 3] + "..."
            signal_parts.append(f"  Context: {context_str}")

        if settings.INCLUDE_COMMENTS_IN_AI and resp.get("comment"):
            comment_str = str(resp["comment"])
            if len(comment_str) > settings.MAX_COMMENT_CHARS:
                comment_str = comment_str[: settings.MAX_COMMENT_CHARS - 3] + "..."
            signal_parts.append(f"  User comment: {comment_str}")

        signals.append("\n".join(signal_parts))

    prompt = f"""Analyze this cybersecurity assessment section and provide comprehensive, structured insights.

Section: {section.title}
Description: {section.description}

Signals:
{chr(10).join(signals)}

{curated_context}

Provide your analysis as JSON matching this schema:
{{
  "risk_level": "Low|Medium|Medium-High|High|Critical",
  "risk_explanation": "Detailed explanation (80-100 words)",
  "strengths": ["strength1", "strength2", "strength3"],
  "gaps": [
    {{
      "gap": "description (60-70 words)",
      "linked_signals": ["Q1", "Q7"],
      "severity": "Low|Medium|High|Critical"
    }}
  ],
  "recommendations": [
    {{
      "action": "specific action (15-25 words)",
      "rationale": "why this matters (80 words)",
      "linked_signals": ["Q3"],
      "effort": "Low|Medium|High",
      "impact": "Low|Medium|High|Critical",
      "timeline": "30-day|60-day|90-day",
      "references": ["NIST CSF PR.AC-1"]
    }}
  ],
  "benchmarks": [
    {{
      "control": "Multi-Factor Authentication",
      "status": "Implemented|Partial|Missing|Not Applicable",
      "framework": "NIST|ISO|OWASP|CIS",
      "reference": "NIST CSF PR.AC-7"
    }}
  ],
  "confidence_score": 0.85
}}

WORD COUNT REQUIREMENTS (TOTAL: 600-1000 WORDS):
- risk_explanation: 80-100 words - Provide a comprehensive analysis of the current security posture, specific risks identified, and their potential business impact
- strengths: 3-5 items, each 20-30 words - Highlight specific positive security practices with context
- gaps: 3-5 items, each gap description 60-70 words (max 900 characters) - Identify specific security weaknesses with detailed explanations and context
- recommendations: 3-5 items, each rationale 80 words - Provide actionable guidance with detailed justification, impact analysis, and implementation considerations

IMPORTANT: Each gap description must not exceed 900 characters to ensure proper validation. Keep descriptions comprehensive but concise.

NOTE: The example below demonstrates the expected level of detail and word counts. Follow this example closely for structure and comprehensiveness.

STRICT REQUIREMENTS:
1. Every gap MUST reference at least one signal (Q1, Q2, etc.) that supports it
2. Every recommendation MUST reference the signals it addresses
3. Use exact signal IDs from the list above (Q1-Q{len(section_responses)})
4. Severity levels must match: Critical (score <40%), High (40-60%), Medium (60-80%), Low (>80%)
5. Effort estimates: Low (<1 week), Medium (1-4 weeks), High (>1 month)
6. Timeline: 30-day for Critical/High, 60-day for Medium, 90-day for Low
7. Benchmark status must be based on signals: Missing if answer=No, Partial if answer=Partial, Implemented if answer=Yes
8. If any gap has severity "Critical", risk_level MUST be "High" or "Critical"

COMPREHENSIVE EXAMPLE:
{{
  "risk_level": "Medium-High",
  "risk_explanation": "The organization demonstrates foundational access control practices with password complexity requirements and role-based permissions. However, critical gaps exist in multi-factor authentication deployment and privileged access management. The reliance on password-only authentication for administrative accounts creates significant vulnerability to credential-based attacks, which represent over 80% of security breaches. Without MFA, a single compromised password grants full system access. The absence of regular access reviews compounds this risk, as dormant accounts with elevated privileges remain active indefinitely, violating least-privilege principles and regulatory requirements.",
  "strengths": [
    "Password complexity requirements are enforced across all user accounts, requiring minimum 12 characters with mixed case, numbers, and special characters, reducing brute-force attack susceptibility",
    "Role-based access control (RBAC) framework is implemented for application-level permissions, ensuring users only access resources necessary for their job functions",
    "Annual security awareness training is provided to all employees, covering phishing recognition, password hygiene, and social engineering tactics"
  ],
  "gaps": [
    {{
      "gap": "Multi-factor authentication is not implemented for administrative accounts, leaving critical systems vulnerable to credential theft and unauthorized access despite strong password policies. This gap is particularly concerning given the organization's handling of sensitive customer data and regulatory compliance requirements under frameworks like SOC 2 and ISO 27001. The current password-only approach fails to protect against phishing, credential stuffing, and password reuse attacks that commonly target administrative accounts. Industry data shows that MFA prevents 99.9% of account compromise attempts.",
      "linked_signals": ["Q7", "Q12"],
      "severity": "High"
    }},
    {{
      "gap": "No automated user access review process exists, resulting in accumulation of orphaned accounts and excessive permissions that violate least-privilege principles. Without regular quarterly reviews, access rights granted for temporary projects or role changes remain indefinitely, creating unnecessary attack surface. This lack of governance increases insider threat risk and fails to meet compliance requirements for access certification under SOC 2, ISO 27001, and industry regulations. Manual reviews are infrequent and error-prone, leading to audit findings.",
      "linked_signals": ["Q15", "Q18"],
      "severity": "Medium"
    }},
    {{
      "gap": "Privileged access management solution is absent, preventing secure storage and rotation of administrative credentials and lacking session recording for audit purposes. Administrative passwords are stored in shared spreadsheets or password managers without proper controls, rarely rotated, and lack accountability through session monitoring. This creates persistent attack vectors where compromised credentials remain valid indefinitely. The absence of just-in-time access provisioning means administrators maintain standing privileges rather than temporary elevation, violating zero-trust principles and compliance frameworks.",
      "linked_signals": ["Q9", "Q14"],
      "severity": "High"
    }}
  ],
  "recommendations": [
    {{
      "action": "Deploy multi-factor authentication for all administrative and privileged accounts using hardware tokens or authenticator apps",
      "rationale": "Current password-only authentication (Q7: No, Q12: No) exposes critical systems to credential-based attacks that represent the leading cause of security breaches. MFA reduces account compromise risk by 99.9% according to Microsoft research and is required by SOC 2, ISO 27001, and most cyber insurance policies. Implementation should prioritize administrative accounts first to protect the most sensitive access, then expand to all users within 90 days. Hardware tokens provide phishing-resistant authentication superior to SMS-based methods. This control directly addresses the High-severity gap in authentication controls.",
      "linked_signals": ["Q7", "Q12"],
      "effort": "Medium",
      "impact": "Critical",
      "timeline": "30-day",
      "references": ["NIST CSF PR.AC-7", "ISO 27001 A.9.4.2", "CIS Control 6.3"]
    }},
    {{
      "action": "Implement quarterly access reviews with automated workflows for approval and deprovisioning of unnecessary permissions",
      "rationale": "Without regular reviews (Q15: No, Q18: Partial), access rights accumulate over time leading to excessive privileges and compliance violations. Automated quarterly reviews ensure timely removal of access for terminated employees and role changes, addressing current audit findings. This process should include manager attestation, automated notifications, and integration with HR systems for termination workflows. The implementation reduces insider threat risk by limiting the attack surface available to compromised accounts and ensures compliance with access certification requirements. Regular reviews also identify privilege creep where users accumulate permissions beyond their current role.",
      "linked_signals": ["Q15", "Q18"],
      "effort": "Medium",
      "impact": "High",
      "timeline": "60-day",
      "references": ["NIST CSF PR.AC-4", "ISO 27001 A.9.2.5", "SOC 2 CC6.2"]
    }},
    {{
      "action": "Deploy privileged access management (PAM) solution to secure, rotate, and monitor all administrative credentials and sessions",
      "rationale": "Lack of PAM (Q9: No, Q14: No) means administrative passwords are stored insecurely and rarely rotated, creating persistent attack vectors that remain exploitable indefinitely. PAM solutions provide secure vaults for credential storage, automatic password rotation on configurable schedules, session recording for forensic analysis, and just-in-time access provisioning that eliminates standing privileges. This is critical for compliance with PCI-DSS, HIPAA, and SOX requirements for organizations handling sensitive data. Modern PAM platforms also provide privileged session monitoring, keystroke logging, and automated threat detection for suspicious administrative activities.",
      "linked_signals": ["Q9", "Q14"],
      "effort": "High",
      "impact": "High",
      "timeline": "60-day",
      "references": ["NIST CSF PR.AC-6", "ISO 27001 A.9.4.3", "CIS Control 5.4"]
    }}
  ],
  "benchmarks": [
    {{
      "control": "Multi-Factor Authentication",
      "status": "Missing",
      "framework": "NIST",
      "reference": "NIST CSF PR.AC-7"
    }},
    {{
      "control": "Access Review Process",
      "status": "Partial",
      "framework": "ISO",
      "reference": "ISO 27001 A.9.2.5"
    }},
    {{
      "control": "Privileged Access Management",
      "status": "Missing",
      "framework": "CIS",
      "reference": "CIS Control 5.4"
    }}
  ],
  "confidence_score": 0.85
}}

Provide detailed, actionable insights that help the organization understand their security posture and prioritize improvements. Be specific and reference industry standards.
"""
    return prompt, redaction_count
