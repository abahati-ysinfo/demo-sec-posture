# Security Posture Assessment - Complete Question Database

*Comprehensive documentation of all assessment questions with detailed option explanations*

## Overview

- **Total Sections:** 19
- **Total Subsections:** 63
- **Total Questions:** 409
- **Documentation Level:** Enhanced with detailed option explanations, market benchmarks, and actionable recommendations

## Table of Contents

- [Section 1: Governance & Strategy](#section-1-governance-and-strategy)
  - [1.1: Security Vision & Objectives](#subsection-11-security-vision-and-objectives)
  - [1.2: Policies & Standards Lifecycle](#subsection-12-policies-and-standards-lifecycle)
  - [1.3: Budget & Resource Allocation](#subsection-13-budget-and-resource-allocation)
  - [1.4: Metrics / KPIs / Board Reporting](#subsection-14-metrics-/-kpis-/-board-reporting)
- [Section 4: Identity & Access Management (IAM)](#section-4-identity-and-access-management-(iam))
  - [4.1: Directory Architecture (AD/AAD/IDaaS)](#subsection-41-directory-architecture-(ad/aad/idaas))
  - [4.2: Access Control & Authorization](#subsection-42-access-control-and-authorization)
  - [4.3: User Lifecycle Management](#subsection-43-user-lifecycle-management)
  - [4.4: Multi-Factor Authentication](#subsection-44-multi-factor-authentication)
- [Section 2: Risk Management](#section-2-risk-management)
  - [2.1: Risk Assessment & Analysis](#subsection-21-risk-assessment-and-analysis)
  - [2.2: Risk Treatment & Mitigation](#subsection-22-risk-treatment-and-mitigation)
  - [2.3: Business Impact Analysis](#subsection-23-business-impact-analysis)
- [Section 3: Asset Management](#section-3-asset-management)
  - [3.1: Asset Inventory & Classification](#subsection-31-asset-inventory-and-classification)
  - [3.2: Asset Lifecycle Management](#subsection-32-asset-lifecycle-management)
  - [3.3: Data Classification & Handling](#subsection-33-data-classification-and-handling)
- [Section 5: Network Security](#section-5-network-security)
  - [5.1: Network Architecture & Segmentation](#subsection-51-network-architecture-and-segmentation)
  - [5.2: Firewall & Perimeter Security](#subsection-52-firewall-and-perimeter-security)
  - [5.3: Network Monitoring & Detection](#subsection-53-network-monitoring-and-detection)
  - [5.4: Remote Access & VPN](#subsection-54-remote-access-and-vpn)
- [Section 6: Endpoint Security](#section-6-endpoint-security)
  - [6.1: Endpoint Protection & Management](#subsection-61-endpoint-protection-and-management)
  - [6.2: Mobile Device Security](#subsection-62-mobile-device-security)
  - [6.3: Endpoint Configuration Management](#subsection-63-endpoint-configuration-management)
- [Section 7: Data Protection & Privacy](#section-7-data-protection-and-privacy)
  - [7.1: Data Encryption & Protection](#subsection-71-data-encryption-and-protection)
  - [7.2: Privacy & Compliance](#subsection-72-privacy-and-compliance)
  - [7.3: Data Backup & Recovery](#subsection-73-data-backup-and-recovery)
  - [7.4: Data Governance & Subject Rights](#subsection-74-data-governance-and-subject-rights)
- [Section 8: Application Security](#section-8-application-security)
  - [8.1: Secure Development Lifecycle](#subsection-81-secure-development-lifecycle)
  - [8.2: Web Application Security](#subsection-82-web-application-security)
  - [8.3: API Security](#subsection-83-api-security)
  - [8.4: DevSecOps & CI/CD Security](#subsection-84-devsecops-and-ci/cd-security)
- [Section 9: Cloud & Container Security](#section-9-cloud-and-container-security)
  - [9.1: Cloud Infrastructure Security](#subsection-91-cloud-infrastructure-security)
  - [9.2: Cloud Identity & Access Management](#subsection-92-cloud-identity-and-access-management)
  - [9.3: Container & Serverless Security](#subsection-93-container-and-serverless-security)
- [Section 10: Incident Response & Resilience](#section-10-incident-response-and-resilience)
  - [10.1: Incident Response Planning](#subsection-101-incident-response-planning)
  - [10.2: Incident Detection & Response](#subsection-102-incident-detection-and-response)
  - [10.3: Incident Recovery & Lessons Learned](#subsection-103-incident-recovery-and-lessons-learned)
- [Section 11: Business Continuity](#section-11-business-continuity)
  - [11.1: Business Continuity Planning](#subsection-111-business-continuity-planning)
  - [11.2: Disaster Recovery](#subsection-112-disaster-recovery)
  - [11.3: Crisis Management](#subsection-113-crisis-management)
  - [11.4: Recovery Operations](#subsection-114-recovery-operations)
- [Section 12: Vendor Management](#section-12-vendor-management)
  - [12.1: Vendor Risk Assessment](#subsection-121-vendor-risk-assessment)
  - [12.2: Contract Management](#subsection-122-contract-management)
  - [12.3: Vendor Monitoring & Oversight](#subsection-123-vendor-monitoring-and-oversight)
  - [12.4: Supply Chain Security](#subsection-124-supply-chain-security)
- [Section 13: Security Awareness & Training](#section-13-security-awareness-and-training)
  - [13.1: Security Awareness Program](#subsection-131-security-awareness-program)
  - [13.2: Phishing & Social Engineering](#subsection-132-phishing-and-social-engineering)
  - [13.3: Role-Based Training](#subsection-133-role-based-training)
  - [13.4: Training Management & Compliance](#subsection-134-training-management-and-compliance)
- [Section 14: Physical Security](#section-14-physical-security)
  - [14.1: Facility Security](#subsection-141-facility-security)
  - [14.2: Environmental Controls](#subsection-142-environmental-controls)
  - [14.3: Equipment Security](#subsection-143-equipment-security)
- [Section 15: Monitoring & Detection](#section-15-monitoring-and-detection)
  - [15.1: Security Monitoring](#subsection-151-security-monitoring)
  - [15.2: Threat Detection](#subsection-152-threat-detection)
  - [15.3: Log Management](#subsection-153-log-management)
- [Section 16: Vulnerability Management](#section-16-vulnerability-management)
  - [16.1: Vulnerability Assessment](#subsection-161-vulnerability-assessment)
  - [16.2: Vulnerability Management Process](#subsection-162-vulnerability-management-process)
  - [16.3: Patch Management](#subsection-163-patch-management)
- [Section 17: Compliance & Audit](#section-17-compliance-and-audit)
  - [17.1: Regulatory Compliance](#subsection-171-regulatory-compliance)
  - [17.2: Internal Audits](#subsection-172-internal-audits)
  - [17.3: External Audits & Certifications](#subsection-173-external-audits-and-certifications)
- [Section 18: OT/ICS & IoT Security](#section-18-ot/ics-and-iot-security)
  - [18.1: Operational Technology Security](#subsection-181-operational-technology-security)
  - [18.2: IoT Device Security](#subsection-182-iot-device-security)
- [Section 19: AI/ML & Machine Learning Security](#section-19-ai/ml-and-machine-learning-security)
  - [19.1: Model Security & Governance](#subsection-191-model-security-and-governance)
  - [19.2: ML Pipeline Security](#subsection-192-ml-pipeline-security)

---

## Section 1: Governance & Strategy

**Suggested Respondents:** CISO, CIO, Risk Officer

### Subsection 1.1: Security Vision & Objectives

#### Question 1.1.1

**Question:** Does your organization have a formally documented cybersecurity strategy?

**Type:** multiple_choice

**Weight:** 5

**Scale:** governance

**Explanation:** A documented cybersecurity strategy provides clear direction and alignment with business objectives.

**Answer Options:**

**Option documented_approved_maintained: Documented, approved, and maintained**
*Basic Description:* Current, approved strategy with regular updates

**📋 What This Option Means:**
- **Definition:** Organization has a written cybersecurity strategy that has been formally approved by leadership and is actively maintained with regular updates.
- **Why It Matters:** Demonstrates mature governance with clear strategic direction, leadership buy-in, and commitment to keeping strategy current with evolving threats and business needs.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 40% of organizations have fully documented and maintained strategies
- **Industry Benchmark:** Best practice for enterprise organizations and regulated industries
- **Compliance Frameworks:** Meets ISO 27001, NIST CSF, and SOC 2 requirements for strategic planning

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Ensure strategy is reviewed at least annually and communicated effectively across the organization.
- **Path to Improvement:** Focus on measuring strategy effectiveness and demonstrating ROI to stakeholders.

**Option documented_but_stale: Documented but not approved or maintained**
*Basic Description:* Written strategy but outdated or not formally approved

**📋 What This Option Means:**
- **Definition:** A cybersecurity strategy document exists but lacks formal leadership approval or has not been updated recently, making it potentially outdated or misaligned with current business objectives.
- **Why It Matters:** Indicates strategy development effort but lack of governance maturity. Strategy may not reflect current priorities or have necessary leadership support for implementation.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 25% of organizations have documented but unmaintained strategies
- **Industry Benchmark:** Common in growing organizations transitioning to mature security programs
- **Compliance Frameworks:** Partially meets requirements but may not satisfy audit expectations for currency

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Prioritize getting formal leadership approval and establishing a regular review cycle (at least annually).
- **Path to Improvement:** Update strategy to reflect current business objectives and threat landscape, then seek formal approval.

**Option informal_understanding: Informal understanding (not documented)**
*Basic Description:* Strategy exists in practice but not written down

**📋 What This Option Means:**
- **Definition:** Security direction and priorities are understood by the security team but not formally documented, relying on tribal knowledge and informal communication.
- **Why It Matters:** Creates risk of inconsistent interpretation, lack of accountability, and difficulty onboarding new team members. Strategy cannot be effectively communicated to stakeholders or measured for effectiveness.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 20% of organizations operate with informal strategies
- **Industry Benchmark:** Common in small organizations but considered immature for mid-size and enterprise
- **Compliance Frameworks:** Does not meet most regulatory requirements for documented security programs

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Document current informal strategy as a first step. Engage leadership to formalize and approve the documented strategy.
- **Path to Improvement:** Create a concise strategy document (5-10 pages) covering objectives, scope, governance, and key initiatives.

**Option no_strategy: No strategy in place**
*Basic Description:* No cybersecurity strategy exists

**📋 What This Option Means:**
- **Definition:** Organization has no defined cybersecurity strategy, either formal or informal, resulting in reactive security posture without clear direction or priorities.
- **Why It Matters:** Represents significant governance gap and risk. Security investments and activities lack strategic alignment, making it difficult to prioritize resources or demonstrate value to leadership.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 10% of organizations have no defined strategy
- **Industry Benchmark:** Considered a critical security governance failure
- **Compliance Frameworks:** Fails most regulatory requirements and industry standards

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Developing a cybersecurity strategy should be immediate priority. Start with a simple one-page strategic plan covering key objectives, scope, and governance.
- **Path to Improvement:** Engage executive leadership to define security vision and objectives aligned with business goals.

**Option not_sure: Not sure**
*Basic Description:* Unclear if strategy exists or its status

**📋 What This Option Means:**
- **Definition:** Respondent is uncertain whether a cybersecurity strategy exists or what its current status is, indicating lack of visibility or communication about strategic security direction.
- **Why It Matters:** Suggests communication gap or lack of engagement with security governance. Even if strategy exists, it's not effectively communicated to stakeholders.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 5% of respondents are unsure about strategy existence
- **Industry Benchmark:** Indicates need for improved security governance communication
- **Compliance Frameworks:** Uncertainty about strategy existence is a red flag for auditors

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Investigate with security leadership whether strategy exists. If it does, improve communication and accessibility. If not, prioritize strategy development.
- **Path to Improvement:** Establish clear communication channels for security governance and strategic direction.


#### Question 1.1.2

**Question:** How often is your cybersecurity strategy reviewed and updated?

**Type:** multiple_choice

**Scale:** frequency_review

**Explanation:** Regular strategy reviews ensure alignment with evolving threats and business changes.

**Answer Options:**

**Option quarterly: Quarterly**
*Basic Description:* Every three months review cycle

**📋 What This Option Means:**
- **Definition:** Cybersecurity strategy is formally reviewed and updated every three months, providing frequent alignment checks with business objectives and rapid response to threat landscape changes.
- **Why It Matters:** Quarterly reviews demonstrate mature governance and proactive risk management. Enables rapid adaptation to emerging threats and business changes.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 10% of organizations review quarterly
- **Industry Benchmark:** Best practice for high-risk industries and rapidly evolving organizations
- **Compliance Frameworks:** Exceeds most regulatory requirements, aligns with agile security governance models

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Ensure reviews remain substantive and don't become administrative overhead. Focus on actionable insights and strategic adjustments.
- **Path to Improvement:** Maintain this cadence and focus on measuring strategy effectiveness through KPIs.

**Option annually: Annually**
*Basic Description:* Once per year review cycle

**📋 What This Option Means:**
- **Definition:** Cybersecurity strategy is formally reviewed and updated once every 12 months, typically aligned with annual business planning cycles.
- **Why It Matters:** Annual reviews ensure strategy remains aligned with evolving business objectives and threat landscape. However, may miss rapid changes in threat environment or business priorities.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 65% of organizations review annually
- **Industry Benchmark:** Standard for stable, low-risk industries
- **Compliance Frameworks:** ISO 27001 requires annual management review, NIST CSF suggests regular strategy updates

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Consider supplementing with quarterly threat landscape reviews and ad-hoc reviews after major business changes or security incidents.
- **Path to Improvement:** Move to bi-annual or quarterly reviews for more dynamic threat response, especially in high-risk industries.

**Option only_after_changes: Only after major changes/incidents**
*Basic Description:* Event-driven reviews only

**📋 What This Option Means:**
- **Definition:** Cybersecurity strategy reviews are triggered only by specific events such as security incidents, major business changes, regulatory updates, or significant threat landscape shifts.
- **Why It Matters:** Event-driven reviews can be highly relevant and timely, but may result in inconsistent review frequency and potential gaps during quiet periods. Risk of reactive rather than proactive strategy management.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 15% of organizations use purely event-driven reviews
- **Industry Benchmark:** Common in resource-constrained organizations but not considered best practice
- **Compliance Frameworks:** May not meet regulatory requirements for regular reviews, could satisfy requirements if events trigger sufficient review frequency

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Establish clear criteria for what events trigger reviews and ensure minimum annual review regardless of events. Document review triggers and maintain review schedule visibility.
- **Path to Improvement:** Transition to scheduled reviews (at least annually) supplemented by event-driven reviews for major changes.

**Option only_after_major_changes: No formal review schedule**
*Basic Description:* No regular review process

**📋 What This Option Means:**
- **Definition:** The organization does not have a formal process for reviewing and updating its cybersecurity strategy, meaning the strategy remains static after initial creation or reviews happen inconsistently without defined triggers.
- **Why It Matters:** Lack of strategy reviews creates significant risk of strategy becoming outdated, misaligned with business objectives, and ineffective against evolving threats. This is a critical governance gap.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** Less than 10% of organizations have no review process
- **Industry Benchmark:** Considered a significant security governance failure
- **Compliance Frameworks:** Fails most regulatory requirements, does not meet ISO 27001, SOX, or other major frameworks

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Immediately establish at minimum an annual strategy review process. Assign clear ownership, define review scope, and document review outcomes. This is a high-priority remediation item.
- **Path to Improvement:** Start with annual reviews and evolve to bi-annual or quarterly based on organizational risk profile and industry requirements.


#### Question 1.1.3

**Question:** Are cybersecurity objectives aligned with business objectives?

**Type:** multiple_choice

**Explanation:** Alignment ensures cybersecurity investments support business goals and priorities.

**Answer Options:**

**Option fully_aligned: Fully aligned**
*Basic Description:* Complete integration with business goals

**Option partially_aligned: Partially aligned**
*Basic Description:* Some alignment but gaps exist

**Option not_aligned: Not aligned**
*Basic Description:* Security operates independently

**Option unknown: Unknown**
*Basic Description:* Alignment status unclear


#### Question 1.1.4

**Question:** Who is accountable for cybersecurity strategy execution?

**Type:** multiple_choice

**Explanation:** Clear accountability ensures cybersecurity strategy has executive ownership and support.

**Answer Options:**

**Option ciso: CISO**
*Basic Description:* Chief Information Security Officer

**📋 What This Option Means:**
- **Definition:** The Chief Information Security Officer has primary accountability for cybersecurity strategy execution, including resource allocation, program oversight, and performance measurement.
- **Why It Matters:** CISO accountability ensures dedicated security leadership with appropriate expertise and authority. Provides clear escalation path and executive-level security advocacy.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 78% of large organizations assign CISO accountability
- **Industry Benchmark:** Standard practice for organizations with dedicated security teams
- **Compliance Frameworks:** Aligns with NIST CSF governance requirements, Supports SOX internal control frameworks

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Ensure CISO has sufficient authority, budget, and board access to execute strategy effectively. Define clear success metrics and reporting relationships.
- **Path to Improvement:** Consider dual accountability with business executives for strategic alignment while maintaining CISO operational accountability.

**Option cio: CIO**
*Basic Description:* Chief Information Officer

**📋 What This Option Means:**
- **Definition:** The Chief Information Officer has primary accountability for cybersecurity strategy execution, typically as part of broader IT governance responsibilities.
- **Why It Matters:** CIO accountability can provide good IT integration but may lack dedicated security focus. Risk of security being subordinated to IT operational priorities.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 35% of mid-size organizations assign CIO accountability
- **Industry Benchmark:** Common in organizations without dedicated CISO role
- **Compliance Frameworks:** May meet basic governance requirements, Could create conflicts between IT efficiency and security priorities

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Ensure CIO has adequate security expertise or dedicated security leadership reporting to them. Define clear security performance metrics separate from IT operational metrics.
- **Path to Improvement:** Consider establishing dedicated CISO role as organization grows, or appointing Deputy CISO under CIO leadership.

**Option ceo: CEO**
*Basic Description:* Chief Executive Officer

**📋 What This Option Means:**
- **Definition:** The Chief Executive Officer has direct accountability for cybersecurity strategy execution, demonstrating highest level of organizational commitment to security.
- **Why It Matters:** CEO accountability ensures maximum organizational priority and resource allocation for security. However, may lack technical expertise and day-to-day operational focus needed for effective execution.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 12% of organizations assign direct CEO accountability
- **Industry Benchmark:** More common in small organizations or highly regulated industries
- **Compliance Frameworks:** Demonstrates strong tone at the top, May exceed regulatory expectations for executive accountability

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Ensure CEO has strong security advisory support and delegates operational execution to qualified security professionals. Maintain CEO strategic oversight while building dedicated security capabilities.
- **Path to Improvement:** Transition to dedicated CISO accountability as organization scales, while maintaining CEO strategic oversight and support.

**Option board: Board**
*Basic Description:* Board of Directors oversight

**📋 What This Option Means:**
- **Definition:** The Board of Directors maintains direct oversight and accountability for cybersecurity strategy execution, typically through a dedicated committee or full board governance.
- **Why It Matters:** Board accountability demonstrates highest governance commitment but may lack operational effectiveness due to meeting frequency and technical expertise limitations.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 8% of organizations assign direct board accountability
- **Industry Benchmark:** Rare except in highly regulated industries or after major incidents
- **Compliance Frameworks:** Exceeds most governance requirements, May indicate response to regulatory pressure or incident

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Establish clear delegation to executive leadership for day-to-day execution while maintaining board strategic oversight. Ensure board has adequate security expertise or advisory support.
- **Path to Improvement:** Transition to executive accountability (CEO/CISO) with regular board reporting and oversight rather than direct board execution responsibility.

**Option shared_between_multiple_executives: Shared between multiple executives**
*Basic Description:* Distributed accountability across leadership team

**📋 What This Option Means:**
- **Definition:** Cybersecurity strategy execution accountability is formally distributed across multiple executives (e.g., CISO for technical execution, CFO for budget, CIO for IT integration), with defined roles and coordination mechanisms.
- **Why It Matters:** Shared accountability can leverage diverse expertise and ensure cross-functional alignment, but requires strong coordination and clear role definition to avoid gaps or conflicts.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 18% of organizations use formal shared accountability models
- **Industry Benchmark:** Increasingly common in matrix organizations and complex enterprises
- **Compliance Frameworks:** Can meet requirements if clearly documented with defined roles and coordination

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Document accountability matrix clearly, establish coordination mechanisms (steering committee, regular sync meetings), and define escalation paths for conflicts. Ensure one executive has tie-breaking authority.
- **Path to Improvement:** Formalize shared accountability with written RACI matrix and regular governance reviews to ensure effective coordination.

**Option no: No clear owner / Unclear**
*Basic Description:* Accountability not clearly defined

**📋 What This Option Means:**
- **Definition:** There is no clearly defined executive accountability for cybersecurity strategy execution, or accountability is ambiguous with multiple potential owners but no formal assignment.
- **Why It Matters:** Lack of clear accountability is a critical governance failure. Creates risk of strategy not being executed, resources not being allocated, and no one taking ownership of security outcomes.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 5% of organizations lack clear accountability (often after leadership transitions)
- **Industry Benchmark:** Considered a critical security governance gap
- **Compliance Frameworks:** Fails most regulatory requirements, major audit finding

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Immediately prioritize establishing clear accountability. Engage executive leadership to assign primary accountability (typically CISO, CIO, or CEO) with documented authority and responsibilities.
- **Path to Improvement:** This is a high-priority remediation item. Establish clear accountability within 30 days and document in security governance charter.

**Option other: Other**
*Basic Description:* Different role or structure

**📋 What This Option Means:**
- **Definition:** Cybersecurity strategy execution accountability is assigned to a different role not listed above (such as COO, CRO, General Counsel) or uses an alternative governance structure.
- **Why It Matters:** Alternative accountability structures may work in specific organizational contexts but should be clearly defined and appropriate for the organization's risk profile.

**📊 Market Context & Benchmarks:**
- **Industry Adoption Rate:** 7% of organizations use alternative accountability models
- **Industry Benchmark:** Varies by industry and organizational structure
- **Compliance Frameworks:** May meet requirements if clearly defined and appropriate for risk profile

**🎯 Recommendations & Next Steps:**
- **If You Select This Option:** Clearly document accountability structure, define roles and responsibilities, and ensure the assigned executive has appropriate authority and expertise (or access to security expertise).
- **Path to Improvement:** Evaluate whether alternative structure is optimal or if transitioning to standard CISO/CIO accountability would improve effectiveness.


#### Question 1.1.5

**Question:** What is your organization's risk appetite for cybersecurity?

**Type:** multiple_choice

**Explanation:** Risk appetite defines how much cybersecurity risk the organization is willing to accept.

**Answer Options:**

**Option very_low: Very low**
*Basic Description:* Minimal risk tolerance, maximum security

**Option low: Low**
*Basic Description:* Conservative approach to risk

**Option medium: Medium**
*Basic Description:* Balanced risk and business needs

**Option high: High**
*Basic Description:* Accept higher risk for agility

**Option very_high: Very high**
*Basic Description:* Maximum risk tolerance


#### Question 1.1.6

**Question:** Are cybersecurity metrics regularly reported to executive leadership?

**Type:** yes_no

**Explanation:** Regular reporting ensures leadership visibility into cybersecurity posture and performance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.1.7

**Question:** How mature is your cybersecurity governance framework?

**Type:** multiple_choice

**Explanation:** Maturity levels indicate the sophistication and effectiveness of governance processes.

**Answer Options:**

**Option ad_hoc: Ad-hoc**
*Basic Description:* Informal, reactive processes

**Option defined: Defined**
*Basic Description:* Documented processes and procedures

**Option managed: Managed**
*Basic Description:* Measured and controlled processes

**Option optimized: Optimized**
*Basic Description:* Continuously improving processes



### Subsection 1.2: Policies & Standards Lifecycle

#### Question 1.2.1

**Question:** How many cybersecurity policies does your organization maintain?

**Type:** multiple_choice

**Explanation:** Policy count indicates coverage breadth - too few may miss areas, too many may be unmanageable.

**Answer Options:**

**Option 0_5: 0-5**
*Basic Description:* Minimal policy coverage

**Option 6_15: 6-15**
*Basic Description:* Basic policy framework

**Option 16_30: 16-30**
*Basic Description:* Comprehensive policy set

**Option 30: 30+**
*Basic Description:* Extensive policy library


#### Question 1.2.2

**Question:** How frequently are security policies reviewed?

**Type:** multiple_choice

**Scale:** frequency_review

**Explanation:** Regular reviews ensure policies remain current with threats, regulations, and business changes.

**Answer Options:**

**Option quarterly: Quarterly**
*Basic Description:* Every three months review cycle

**Option annually: Annually**
*Basic Description:* Once per year review

**Option only_after_changes: Only after major changes/incidents**
*Basic Description:* Event-driven reviews only

**Option only_after_major_changes: No formal review schedule**
*Basic Description:* No regular review process


#### Question 1.2.3

**Question:** What is the average age of your current security policies?

**Type:** multiple_choice

**Explanation:** Older policies may not address current threats or reflect modern security practices.

**Answer Options:**

**Option 1_year: <1 year**
*Basic Description:* Recently created or updated

**Option 1_2_years: 1-2 years**
*Basic Description:* Moderately current policies

**Option 2_3_years: 2-3 years**
*Basic Description:* Aging policies needing review

**Option 3_years: 3+ years**
*Basic Description:* Outdated policies requiring updates

**Option unknown: Unknown**
*Basic Description:* Policy age not tracked or unclear


#### Question 1.2.4

**Question:** Do you have a formal policy approval process?

**Type:** yes_no

**Explanation:** Formal approval ensures policies have proper authority and stakeholder buy-in.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.2.5

**Question:** Are policies regularly communicated to all employees?

**Type:** yes_no

**Explanation:** Communication ensures employees understand their security responsibilities and requirements.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.2.6

**Question:** How do you track policy compliance?

**Type:** multiple_choice

**Scale:** implementation

**Explanation:** Compliance tracking ensures policies are being followed and identifies gaps.

**Answer Options:**

**Option fully_implemented: Automated tools**
*Basic Description:* Software-based compliance monitoring

**Option partially_implemented: Manual tracking**
*Basic Description:* Human-driven compliance checks

**Option planned: Combination of automated + manual**
*Basic Description:* Hybrid approach using both methods

**Option not_implemented: No tracking**
*Basic Description:* No compliance monitoring in place

**Option not_sure: Not sure**
*Basic Description:* Tracking method unclear


#### Question 1.2.7

**Question:** Do you maintain policy exception processes?

**Type:** yes_no

**Explanation:** Exception processes allow controlled deviations while maintaining security oversight.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 1.3: Budget & Resource Allocation

#### Question 1.3.1

**Question:** What percentage of IT budget is allocated to cybersecurity?

**Type:** multiple_choice

**Scale:** coverage

**Explanation:** Industry benchmarks suggest 10-15% of IT budget should be allocated to cybersecurity.

**Answer Options:**

**Option 76_100: 15.0%+**
*Basic Description:* Above average investment

**Option 51_75: 10.0-14.9%**
*Basic Description:* Industry standard allocation

**Option 26_50: 5.0-9.9%**
*Basic Description:* Basic security investment

**Option 0_25: 0-4.9%**
*Basic Description:* Below industry minimum

**Option not_sure: Not sure**
*Basic Description:* Budget allocation not tracked or unclear


#### Question 1.3.2

**Question:** How has your cybersecurity budget changed in the last year?

**Type:** multiple_choice

**Explanation:** Budget trends indicate organizational commitment to cybersecurity improvement.

**Answer Options:**

**Option increased_significantly: Increased significantly**
*Basic Description:* Major budget growth (>20%)

**Option increased_slightly: Increased slightly**
*Basic Description:* Modest budget growth (<20%)

**Option remained_same: Remained same**
*Basic Description:* No budget change

**Option decreased: Decreased**
*Basic Description:* Budget reduction


#### Question 1.3.3

**Question:** Do you have dedicated cybersecurity staff?

**Type:** yes_no

**Explanation:** Dedicated staff ensures focused expertise and accountability for security functions.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.3.4

**Question:** How many FTE cybersecurity professionals do you employ?

**Type:** multiple_choice

**Explanation:** Staffing levels should align with organization size, complexity, and risk profile.

**Answer Options:**

**Option 0: 0**
*Basic Description:* No dedicated security staff

**Option 1_5: 1-5**
*Basic Description:* Small security team

**Option 6_15: 6-15**
*Basic Description:* Medium security team

**Option 16_30: 16-30**
*Basic Description:* Large security team

**Option 30: 30+**
*Basic Description:* Enterprise security organization


#### Question 1.3.5

**Question:** Do you use external cybersecurity services?

**Type:** yes_no

**Explanation:** External services can supplement internal capabilities and provide specialized expertise.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.3.6

**Question:** How do you justify cybersecurity investments?

**Type:** multiple_choice

**Explanation:** Risk-based justification ensures investments address the most critical security needs.

**Answer Options:**

**Option risk_based: Risk-based**
*Basic Description:* Investments based on risk analysis

**Option compliance_driven: Compliance-driven**
*Basic Description:* Investments for regulatory compliance

**Option industry_benchmarks: Industry benchmarks**
*Basic Description:* Investments based on peer comparison

**Option ad_hoc: Ad-hoc**
*Basic Description:* No systematic justification process



### Subsection 1.4: Metrics / KPIs / Board Reporting

#### Question 1.4.1

**Question:** Do you have established cybersecurity KPIs?

**Type:** multiple_choice

**Scale:** implementation

**Explanation:** KPIs provide measurable indicators of cybersecurity program effectiveness.

**Answer Options:**

**Option fully_implemented: Yes, formal KPIs with regular tracking**
*Basic Description:* Documented KPIs with consistent measurement

**Option partially_implemented: Yes, informal metrics tracked**
*Basic Description:* Some metrics tracked but not formalized

**Option planned: No KPIs established**
*Basic Description:* No formal or informal KPI tracking


#### Question 1.4.2

**Question:** How often do you report cybersecurity metrics to the board?

**Type:** multiple_choice

**Explanation:** Regular board reporting ensures governance oversight and strategic alignment.

**Answer Options:**

**Option monthly: Monthly**
*Basic Description:* Every month board reporting

**Option quarterly: Quarterly**
*Basic Description:* Every three months reporting

**Option annually: Annually**
*Basic Description:* Once per year reporting

**Option never: Never**
*Basic Description:* No board reporting


#### Question 1.4.3

**Question:** Which metrics do you track?

**Type:** multiple_select

**Explanation:** Comprehensive metrics provide visibility into different aspects of security posture.

**Answer Options:**
**Option security_incidents_count: Security incidents count**
*Basic Description:* Number of security incidents per period

**Option mean_time_to_detect_mttd: Mean time to detect (MTTD)**
*Basic Description:* Average time to detect security incidents

**Option mean_time_to_respond_mttr: Mean time to respond (MTTR)**
*Basic Description:* Average time to respond to incidents

**Option vulnerability_remediation_time: Vulnerability remediation time**
*Basic Description:* Time taken to remediate vulnerabilities

**Option patch_compliance_rate: Patch compliance rate**
*Basic Description:* Percentage of systems with current patches

**Option user_awareness_training_completion: User awareness training completion**
*Basic Description:* Training completion rates

**Option security_audit_findings: Security audit findings**
*Basic Description:* Number and severity of audit findings

**Option risk_assessment_scores: Risk assessment scores**
*Basic Description:* Overall risk posture scores



#### Question 1.4.4

**Question:** Do you benchmark your security posture against industry peers?

**Type:** yes_no

**Explanation:** Benchmarking helps identify gaps and improvement opportunities relative to industry standards.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.4.5

**Question:** How do you measure cybersecurity program effectiveness?

**Type:** multiple_choice

**Explanation:** Effectiveness measurement demonstrates program value and identifies improvement areas.

**Answer Options:**

**Option quantitative_metrics: Quantitative metrics**
*Basic Description:* Numerical data and measurements

**Option qualitative_assessments: Qualitative assessments**
*Basic Description:* Subjective evaluations and reviews

**Option both: Both**
*Basic Description:* Combined quantitative and qualitative

**Option not_measured: Not measured**
*Basic Description:* No effectiveness measurement


#### Question 1.4.6

**Question:** Do you maintain security Key Performance Indicators (KPIs)?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Security KPIs provide measurable insights into security program effectiveness.

**Answer Options:**
**Option incident_response_time: Incident response time**
*Basic Description:* Time to detect and respond to incidents

**Option vulnerability_remediation_rate: Vulnerability remediation rate**
*Basic Description:* Speed of vulnerability patching

**Option security_awareness_metrics: Security awareness metrics**
*Basic Description:* Training completion and phishing test results

**Option compliance_status: Compliance status**
*Basic Description:* Adherence to regulatory requirements

**Option access_control_effectiveness: Access control effectiveness**
*Basic Description:* Proper access provisioning and reviews

**Option security_tool_coverage: Security tool coverage**
*Basic Description:* Percentage of assets protected

**Option no: No KPIs maintained**
*Basic Description:* KPIs not currently tracked



#### Question 1.4.7

**Question:** Do you have defined security Objectives and Key Results (OKRs)?

**Type:** yes_no

**Weight:** 1

**Explanation:** Security OKRs align security initiatives with business objectives and drive measurable outcomes.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 1.4.8

**Question:** How do you measure security program maturity?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Maturity measurement guides security program improvement and investment decisions.

**Answer Options:**
**Option maturity_model_framework: Maturity model framework**
*Basic Description:* Using CMMI, NIST CSF, or similar

**Option capability_assessments: Capability assessments**
*Basic Description:* Regular capability evaluations

**Option benchmark_comparisons: Benchmark comparisons**
*Basic Description:* Comparing against industry standards

**Option audit_results: Audit results**
*Basic Description:* Based on internal/external audit findings

**Option self_assessment: Self-assessment**
*Basic Description:* Internal maturity evaluations

**Option not_measured: Not measured**
*Basic Description:* Maturity not currently assessed



#### Question 1.4.9

**Question:** Which security metrics are reported to the board?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Board-level security metrics ensure executive visibility into security program performance.

**Answer Options:**
**Option incident_statistics: Incident statistics**
*Basic Description:* Number and severity of security incidents

**Option risk_posture: Risk posture**
*Basic Description:* Overall organizational risk levels

**Option compliance_status: Compliance status**
*Basic Description:* Regulatory compliance metrics

**Option security_investments: Security investments**
*Basic Description:* Budget and resource allocation

**Option program_maturity: Program maturity**
*Basic Description:* Security program maturity scores

**Option vulnerability_metrics: Vulnerability metrics**
*Basic Description:* Critical vulnerability counts and trends

**Option third_party_risk: Third-party risk**
*Basic Description:* Vendor security risk metrics

**Option no: No board reporting**
*Basic Description:* Security metrics not reported to board




---

## Section 4: Identity & Access Management (IAM)


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown
**Suggested Respondents:** Directory/IAM Architect

### Subsection 4.1: Directory Architecture (AD/AAD/IDaaS)

#### Question 4.1.1

**Question:** What is your primary identity provider?

**Type:** multiple_choice

**Explanation:** Identity providers centralize authentication and user management across systems.

**Answer Options:**

**Option active_directory: Active Directory**
*Basic Description:* Microsoft on-premises directory

**Option azure_ad: Azure AD**
*Basic Description:* Microsoft cloud identity service

**Option okta: Okta**
*Basic Description:* Third-party identity provider

**Option auth0: Auth0**
*Basic Description:* Developer-focused identity platform

**Option google_workspace: Google Workspace**
*Basic Description:* Google cloud identity service

**Option other: Other**
*Basic Description:* Different identity provider

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.1.2

**Question:** How many separate identity stores do you maintain?

**Type:** multiple_choice

**Explanation:** Multiple identity stores increase complexity and security risks - consolidation is preferred.

**Answer Options:**

**Option 1: 1**
*Basic Description:* Single identity store

**Option 2_3: 2-3**
*Basic Description:* Few identity stores

**Option 4_5: 4-5**
*Basic Description:* Multiple identity stores

**Option 6: 6+**
*Basic Description:* Many identity stores

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.1.3

**Question:** Do you have identity federation implemented?

**Type:** yes_no

**Explanation:** Federation allows secure sharing of identity information across different systems and organizations.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.1.4

**Question:** What percentage of applications use centralized authentication?

**Type:** multiple_choice

**Explanation:** Centralized authentication improves security and user experience while reducing management overhead.

**Answer Options:**

**Option 0_25: 0-25%**
*Basic Description:* Minimal centralized authentication

**Option 26_50: 26-50%**
*Basic Description:* Some centralized authentication

**Option 51_75: 51-75%**
*Basic Description:* Most applications centralized

**Option 76_100: 76-100%**
*Basic Description:* Nearly all applications centralized

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.1.5

**Question:** Do you have a single sign-on (SSO) solution?

**Type:** yes_no

**Explanation:** SSO improves user experience and security by reducing password fatigue and enabling centralized access control.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.1.6

**Question:** How do you synchronize identities across systems?

**Type:** multiple_choice

**Explanation:** Automated synchronization ensures consistency and reduces administrative overhead and errors.

**Answer Options:**

**Option automated: Automated**
*Basic Description:* System-driven synchronization

**Option manual: Manual**
*Basic Description:* Human-driven synchronization

**Option not_synchronized: Not synchronized**
*Basic Description:* No identity synchronization

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.1.7

**Question:** Do you have directory service redundancy?

**Type:** yes_no

**Explanation:** Directory redundancy ensures authentication availability during outages.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.1.8

**Question:** How do you monitor directory service health?

**Type:** multiple_select

**Explanation:** Directory monitoring ensures reliable identity services and detects security issues.

**Answer Options:**
**Option automated_monitoring_tools: Automated monitoring tools**
*Basic Description:* Using SIEM, monitoring platforms, or similar

**Option manual_reviews: Manual reviews**
*Basic Description:* Regular manual checks and reviews

**Option combination_approach: Combination approach**
*Basic Description:* Mix of automated and manual monitoring

**Option third_party_service: Third-party service**
*Basic Description:* Outsourced monitoring

**Option not_monitored: Not monitored**
*Basic Description:* Not currently monitored



**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 4.2: Access Control & Authorization

#### Question 4.2.1

**Question:** What access control model do you use?

**Type:** multiple_choice

**Explanation:** Access control models define how permissions are granted and managed.

**Answer Options:**

**Option role_based_rbac: Role-based (RBAC)**
*Basic Description:* Permissions based on user roles

**Option attribute_based_abac: Attribute-based (ABAC)**
*Basic Description:* Permissions based on attributes

**Option discretionary_dac: Discretionary (DAC)**
*Basic Description:* Owner-controlled permissions

**Option mandatory_mac: Mandatory (MAC)**
*Basic Description:* System-enforced permissions

**Option mixed_approach: Mixed approach**
*Basic Description:* Combination of access models

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.2.2

**Question:** Do you implement least privilege access?

**Type:** yes_no

**Explanation:** Least privilege reduces security risk by granting minimal necessary access.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.2.3

**Question:** How do you manage privileged accounts?

**Type:** multiple_select

**Explanation:** Privileged account management protects high-risk administrative access.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.2.4

**Question:** Do you use dynamic authorization?

**Type:** yes_no

**Explanation:** Dynamic authorization adapts access decisions based on context and risk.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.2.5

**Question:** How do you handle emergency access?

**Type:** multiple_select

**Explanation:** Emergency access procedures balance security with operational needs during crises.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.2.6

**Question:** Do you implement segregation of duties?

**Type:** yes_no

**Explanation:** Segregation of duties prevents single individuals from having excessive control.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 4.3: User Lifecycle Management

#### Question 4.3.1

**Question:** Do you have automated user provisioning?

**Type:** yes_no

**Explanation:** Automated provisioning ensures consistent and timely account creation.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.3.2

**Question:** How do you handle user onboarding?

**Type:** multiple_select

**Explanation:** Structured onboarding ensures users receive appropriate access from day one.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.3.3

**Question:** Do you conduct regular access reviews?

**Type:** multiple_choice

**Explanation:** Regular access reviews identify and remove unnecessary permissions.

**Answer Options:**

**Option monthly: Monthly**
*Basic Description:* Every month review cycle

**Option quarterly: Quarterly**
*Basic Description:* Every three months review

**Option annually: Annually**
*Basic Description:* Once per year review

**Option as_needed: As needed**
*Basic Description:* Event-driven reviews only

**Option never: Never**
*Basic Description:* No formal reviews

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.3.4

**Question:** How do you handle user role changes?

**Type:** multiple_select

**Explanation:** Role change processes ensure access remains appropriate as responsibilities change.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.3.5

**Question:** Do you have automated user deprovisioning?

**Type:** yes_no

**Explanation:** Automated deprovisioning ensures timely access removal when users leave.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.3.6

**Question:** How quickly do you disable accounts for terminated users?

**Type:** multiple_choice

**Explanation:** Rapid account disabling prevents unauthorized access by former employees.

**Answer Options:**

**Option immediately: Immediately**
*Basic Description:* Instant account disabling

**Option within_1_hour: Within 1 hour**
*Basic Description:* Disabled within one hour

**Option within_24_hours: Within 24 hours**
*Basic Description:* Disabled within one day

**Option within_1_week: Within 1 week**
*Basic Description:* Disabled within one week

**Option no: No defined timeframe**
*Basic Description:* No specific timeline

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.3.7

**Question:** Do you track orphaned accounts?

**Type:** yes_no

**Explanation:** Orphaned account tracking identifies accounts that should be disabled or removed.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 4.4: Multi-Factor Authentication

#### Question 4.4.1

**Question:** Do you require multi-factor authentication (MFA)?

**Type:** yes_no

**Explanation:** MFA significantly reduces the risk of account compromise from stolen credentials.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.4.2

**Question:** What MFA methods do you support?

**Type:** multiple_select

**Explanation:** Multiple MFA methods provide flexibility while maintaining security.

**Answer Options:**
**Option sms_text_message: SMS/Text message**
*Basic Description:* One-time codes via SMS

**Option authenticator_app: Authenticator app**
*Basic Description:* TOTP-based authenticator apps

**Option hardware_token: Hardware token**
*Basic Description:* Physical security keys like YubiKey

**Option biometric: Biometric**
*Basic Description:* Fingerprint or facial recognition

**Option push_notification: Push notification**
*Basic Description:* Mobile app push approvals

**Option not_implemented: Not implemented**
*Basic Description:* MFA not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.4.3

**Question:** What percentage of users have MFA enabled?

**Type:** multiple_choice

**Explanation:** High MFA adoption rates improve overall security posture.

**Answer Options:**

**Option 0_25: 0-25%**
*Basic Description:* Minimal MFA adoption

**Option 26_50: 26-50%**
*Basic Description:* Some MFA adoption

**Option 51_75: 51-75%**
*Basic Description:* Most users have MFA

**Option 76_100: 76-100%**
*Basic Description:* Nearly all users have MFA

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 4.4.4

**Question:** Do you have conditional access policies?

**Type:** yes_no

**Explanation:** Conditional access adapts authentication requirements based on risk factors.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 4.4.5

**Question:** How do you handle MFA bypass requests?

**Type:** multiple_choice

**Scale:** governance

**Explanation:** MFA bypass procedures should balance security with operational needs.

**Answer Options:**
**Option documented_approved_maintained: Formal documented approval process with logging**
*Basic Description:* Documented procedure with audit trail

**Option documented_but_stale: Temporary time-bound bypass with justification**
*Basic Description:* Limited duration with business justification required

**Option informal_understanding: Manual ad-hoc approval (no logging)**
*Basic Description:* Case-by-case approval without formal tracking

**Option no_strategy: Not allowed (no bypasses permitted)**
*Basic Description:* MFA cannot be bypassed under any circumstances

**Option not_currently_managed: Not currently managed**
*Basic Description:* No formal process for handling bypass requests




---

## Section 2: Risk Management

**Suggested Respondents:** Enterprise Risk Manager, Compliance Lead

### Subsection 2.1: Risk Assessment & Analysis

#### Question 2.1.1

**Question:** How frequently does your organization conduct cybersecurity risk assessments?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular risk assessments help identify and prioritize cybersecurity threats and vulnerabilities.

**Answer Options:**

**Option quarterly:** Monthly

**Option annually:** Quarterly

**Option only_after_changes:** Annually

**Option only_after_major_changes:** Bi-annually

**Option as_needed:** As needed

**Option no_formal_review:** Never


#### Question 2.1.2

**Question:** Do you have a formal risk management framework in place?

**Type:** yes_no

**Explanation:** A formal framework provides structure and consistency for risk management activities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.1.3

**Question:** What methodology do you use for risk assessment?

**Type:** multiple_choice

**Explanation:** Standardized methodologies ensure comprehensive and consistent risk assessments.

**Answer Options:**

**Option nist: NIST**
*Basic Description:* NIST Risk Management Framework

**Option iso_27001: ISO 27001**
*Basic Description:* ISO 27001 risk management

**Option fair: FAIR**
*Basic Description:* Factor Analysis of Information Risk

**Option custom: Custom**
*Basic Description:* Organization-specific methodology

**Option none: None**
*Basic Description:* No formal methodology


#### Question 2.1.4

**Question:** Do you maintain a risk register or inventory?

**Type:** yes_no

**Explanation:** A risk register provides centralized tracking and management of identified risks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.1.5

**Question:** How do you prioritize cybersecurity risks?

**Type:** multiple_choice

**Explanation:** Risk prioritization ensures resources are allocated to the most critical threats first.

**Answer Options:**

**Option impact_x_likelihood: Impact x Likelihood**
*Basic Description:* Risk matrix approach

**Option business_criticality: Business criticality**
*Basic Description:* Based on business importance

**Option regulatory_requirements: Regulatory requirements**
*Basic Description:* Compliance-driven prioritization

**Option ad_hoc: Ad-hoc**
*Basic Description:* No systematic approach

**Option not_prioritized: Not prioritized**
*Basic Description:* No risk prioritization


#### Question 2.1.6

**Question:** Do you conduct threat modeling exercises?

**Type:** yes_no

**Explanation:** Threat modeling helps identify potential attack vectors and security weaknesses.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.1.7

**Question:** How often do you update your risk assessments?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular updates ensure risk assessments reflect current threat landscape and business changes.

**Answer Options:**

**Option quarterly: Continuously**
*Basic Description:* Ongoing risk assessment updates

**Option annually: Quarterly**
*Basic Description:* Every three months updates

**Option only_after_changes: Annually**
*Basic Description:* Once per year updates

**Option only_after_major_changes: When incidents occur**
*Basic Description:* Event-driven updates only

**Option as_needed: Never**
*Basic Description:* No risk assessment updates



### Subsection 2.2: Risk Treatment & Mitigation

#### Question 2.2.1

**Question:** What risk treatment strategies does your organization employ?

**Type:** multiple_select

**Explanation:** Multiple treatment strategies provide flexibility in addressing different types of risks.

**Answer Options:**
**Option avoid: Avoid**
*Basic Description:* Eliminate the risk entirely by discontinuing the activity or changing approach

**Option mitigate: Mitigate**
*Basic Description:* Reduce likelihood or impact through security controls and safeguards

**Option transfer: Transfer**
*Basic Description:* Shift risk to third parties via insurance, contracts, or outsourcing

**Option accept: Accept**
*Basic Description:* Acknowledge and monitor risk within organizational tolerance levels

**Option monitor: Monitor**
*Basic Description:* Track risk over time for future action or reassessment

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 2.2.2

**Question:** Do you have defined risk tolerance levels?

**Type:** yes_no

**Explanation:** Risk tolerance levels guide decision-making about which risks to accept or mitigate.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.2.3

**Question:** How do you track risk mitigation progress?

**Type:** multiple_choice

**Explanation:** Progress tracking ensures risk mitigation efforts are effective and timely.

**Answer Options:**

**Option automated_tools: Automated tools**
*Basic Description:* Software-based progress tracking

**Option manual_tracking: Manual tracking**
*Basic Description:* Human-driven progress monitoring

**Option periodic_reviews: Periodic reviews**
*Basic Description:* Regular review meetings

**Option not_tracked: Not tracked**
*Basic Description:* No progress tracking


#### Question 2.2.4

**Question:** Do you have cybersecurity insurance?

**Type:** yes_no

**Explanation:** Cybersecurity insurance provides financial protection against cyber incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.2.5

**Question:** What is your organization's risk appetite statement?

**Type:** multiple_choice

**Explanation:** A clear risk appetite statement guides consistent risk decision-making across the organization.

**Answer Options:**

**Option formally_documented: Formally documented**
*Basic Description:* Written risk appetite statement

**Option informally_understood: Informally understood**
*Basic Description:* Unwritten but understood

**Option under_development: Under development**
*Basic Description:* Currently being created

**Option not_defined: Not defined**
*Basic Description:* No risk appetite defined


#### Question 2.2.6

**Question:** How do you communicate risks to stakeholders?

**Type:** multiple_choice

**Explanation:** Effective risk communication ensures stakeholders can make informed decisions.

**Answer Options:**

**Option regular_reports: Regular reports**
*Basic Description:* Scheduled risk reporting

**Option dashboard_metrics: Dashboard/metrics**
*Basic Description:* Visual risk dashboards

**Option ad_hoc_briefings: Ad-hoc briefings**
*Basic Description:* As-needed risk communication

**Option not_communicated: Not communicated**
*Basic Description:* No risk communication



### Subsection 2.3: Business Impact Analysis

#### Question 2.3.1

**Question:** Have you conducted a business impact analysis (BIA)?

**Type:** yes_no

**Explanation:** BIA identifies critical business processes and their dependencies for risk prioritization.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.3.2

**Question:** How do you classify business processes by criticality?

**Type:** multiple_choice

**Explanation:** Process classification helps prioritize protection efforts and resource allocation.

**Answer Options:**

**Option critical_high_medium_low: Critical/High/Medium/Low**
*Basic Description:* Four-tier criticality levels

**Option tier_1_2_3: Tier 1/2/3**
*Basic Description:* Three-tier classification system

**Option custom_classification: Custom classification**
*Basic Description:* Organization-specific classification

**Option not_classified: Not classified**
*Basic Description:* No process classification


#### Question 2.3.3

**Question:** Do you have defined Recovery Time Objectives (RTO)?

**Type:** yes_no

**Explanation:** RTOs define acceptable downtime for business processes and guide recovery planning.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.3.4

**Question:** Do you have defined Recovery Point Objectives (RPO)?

**Type:** yes_no

**Explanation:** RPOs define acceptable data loss and guide backup and recovery strategies.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 2.3.5

**Question:** How often do you update your business impact analysis?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular updates ensure BIA reflects current business operations and dependencies.

**Answer Options:**

**Option quarterly: Annually**
*Basic Description:* Once per year updates

**Option annually: Bi-annually**
*Basic Description:* Twice per year updates

**Option only_after_changes: When business changes**
*Basic Description:* Event-driven updates only

**Option only_after_major_changes: Never updated**
*Basic Description:* No BIA updates


#### Question 2.3.6

**Question:** Do you quantify financial impact of potential cyber incidents?

**Type:** yes_no

**Explanation:** Financial quantification helps justify security investments and insurance decisions.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



---

## Section 3: Asset Management

**Suggested Respondents:** ITAM Lead, Infrastructure Manager

### Subsection 3.1: Asset Inventory & Classification

#### Question 3.1.1

**Question:** Do you maintain a comprehensive IT asset inventory?

**Type:** yes_no

**Explanation:** Asset inventory is fundamental for security management and risk assessment.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.1.2

**Question:** What percentage of your IT assets are inventoried?

**Type:** multiple_choice

**Explanation:** High inventory coverage is essential for effective security management.

**Answer Options:**

**Option 90_100:** 90-100%

**Option 75_89:** 75-89%

**Option 50_74:** 50-74%

**Option 25_49:** 25-49%

**Option 0_24:** 0-24%


#### Question 3.1.3

**Question:** How do you discover and track new assets?

**Type:** multiple_choice

**Explanation:** Automated discovery helps maintain accurate and up-to-date asset inventories.

**Answer Options:**

**Option automated_discovery:** Automated discovery

**Option manual_registration:** Manual registration

**Option network_scanning:** Network scanning

**Option combination:** Combination

**Option no:** No process


#### Question 3.1.4

**Question:** Do you classify assets by criticality or sensitivity?

**Type:** yes_no

**Explanation:** Asset classification enables risk-based security controls and resource allocation.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.1.5

**Question:** What asset types do you track?

**Type:** multiple_select

**Explanation:** Comprehensive asset tracking covers all technology components that could pose security risks.

**Answer Options:**
**Option endpoints: Endpoints**
*Basic Description:* Laptops, desktops, and workstations

**Option servers: Servers**
*Basic Description:* Physical and virtual servers

**Option mobile_devices: Mobile devices**
*Basic Description:* Smartphones, tablets, and mobile endpoints

**Option network_devices: Network devices**
*Basic Description:* Switches, routers, firewalls, and network infrastructure

**Option applications_and_services: Applications and services**
*Basic Description:* Software applications and business services

**Option databases_and_storage: Databases and storage**
*Basic Description:* Database systems and storage infrastructure

**Option cloud_resources: Cloud resources**
*Basic Description:* IaaS, PaaS, and SaaS cloud assets

**Option ot_ics_iot_devices: OT/ICS/IoT devices**
*Basic Description:* Operational technology, industrial control systems, and IoT devices

**Option backup_media: Backup media**
*Basic Description:* Backup tapes, drives, and archive storage

**Option third_party_saas_applications: Third-party/SaaS applications**
*Basic Description:* External SaaS applications and third-party services

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 3.1.6

**Question:** How often do you update your asset inventory?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Frequent updates ensure inventory accuracy in dynamic IT environments.

**Answer Options:**

**Option quarterly:** Real-time

**Option annually:** Daily

**Option only_after_changes:** Weekly

**Option only_after_major_changes:** Monthly

**Option as_needed:** Quarterly

**Option no_formal_review:** Annually


#### Question 3.1.7

**Question:** Do you track asset ownership and accountability?

**Type:** yes_no

**Explanation:** Clear ownership ensures accountability for asset security and maintenance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 3.2: Asset Lifecycle Management

#### Question 3.2.1

**Question:** Do you have formal asset lifecycle management processes?

**Type:** yes_no

**Explanation:** Lifecycle management ensures security controls are maintained throughout asset lifespan.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.2.2

**Question:** How do you handle asset procurement security requirements?

**Type:** multiple_choice

**Explanation:** Security requirements during procurement prevent introduction of vulnerable assets.

**Answer Options:**

**Option security_review_required: Security review required**
*Basic Description:* Mandatory security review process

**Option standard_security_specs: Standard security specs**
*Basic Description:* Predefined security specifications

**Option vendor_security_assessment: Vendor security assessment**
*Basic Description:* Vendor security evaluation

**Option no: No requirements**
*Basic Description:* No security requirements


#### Question 3.2.3

**Question:** Do you have secure asset disposal procedures?

**Type:** yes_no

**Explanation:** Secure disposal prevents data breaches and ensures compliance with data protection regulations.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.2.4

**Question:** How do you handle end-of-life assets?

**Type:** multiple_choice

**Explanation:** Proper end-of-life handling prevents data exposure and ensures regulatory compliance.

**Answer Options:**

**Option data_wiping:** Data wiping

**Option physical_destruction:** Physical destruction

**Option certified_disposal:** Certified disposal

**Option return_to_vendor:** Return to vendor

**Option no:** No formal process


#### Question 3.2.5

**Question:** Do you track asset warranty and support status?

**Type:** yes_no

**Explanation:** Tracking support status helps identify assets that may lack security updates.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.2.6

**Question:** How do you manage asset configuration changes?

**Type:** multiple_choice

**Explanation:** Configuration management prevents unauthorized changes that could introduce vulnerabilities.

**Answer Options:**

**Option change_management_process: Change management process**
*Basic Description:* Formal change control procedures

**Option automated_configuration: Automated configuration**
*Basic Description:* System-driven configuration management

**Option manual_tracking: Manual tracking**
*Basic Description:* Human-driven change tracking

**Option no: No formal process**
*Basic Description:* No configuration management



### Subsection 3.3: Data Classification & Handling

#### Question 3.3.1

**Question:** Do you have a data classification scheme?

**Type:** yes_no

**Explanation:** Data classification enables appropriate protection controls based on sensitivity.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.3.2

**Question:** What data classification levels do you use?

**Type:** multiple_choice

**Explanation:** Clear classification levels help users understand appropriate handling requirements.

**Answer Options:**

**Option public_internal_confidential_restricted: Public/Internal/Confidential/Restricted**
*Basic Description:* Four-tier data classification

**Option high_medium_low: High/Medium/Low**
*Basic Description:* Three-tier classification system

**Option custom_scheme: Custom scheme**
*Basic Description:* Organization-specific classification

**Option no: No classification**
*Basic Description:* No data classification


#### Question 3.3.3

**Question:** Do you label data according to its classification?

**Type:** yes_no

**Explanation:** Data labeling helps users identify and apply appropriate protection measures.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.3.4

**Question:** How do you enforce data handling requirements?

**Type:** multiple_choice

**Explanation:** Enforcement mechanisms ensure data classification translates to actual protection.

**Answer Options:**

**Option technical_controls:** Technical controls

**Option policy_enforcement:** Policy enforcement

**Option training:** Training

**Option combination:** Combination

**Option not_enforced:** Not enforced


#### Question 3.3.5

**Question:** Do you track data location and movement?

**Type:** yes_no

**Explanation:** Data tracking helps ensure compliance with regulations and internal policies.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 3.3.6

**Question:** How do you handle data retention and disposal?

**Type:** multiple_choice

**Explanation:** Proper retention and disposal reduce data exposure risks and ensure compliance.

**Answer Options:**

**Option automated_policies: Automated policies**
*Basic Description:* System-driven retention and disposal

**Option manual_processes: Manual processes**
*Basic Description:* Human-driven data management

**Option legal_hold_procedures: Legal hold procedures**
*Basic Description:* Legal compliance procedures

**Option no: No formal process**
*Basic Description:* No retention/disposal process



---

## Section 5: Network Security

**Suggested Respondents:** Network Security Engineer

### Subsection 5.1: Network Architecture & Segmentation

#### Question 5.1.1

**Question:** Do you implement network segmentation?

**Type:** yes_no

**Explanation:** Network segmentation limits the spread of attacks and reduces blast radius.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.1.2

**Question:** What type of network segmentation do you use?

**Type:** multiple_select

**Explanation:** Multiple segmentation techniques provide defense in depth.

**Answer Options:**
**Option physical_segmentation: Physical segmentation**
*Basic Description:* Separate physical networks

**Option virtual_segmentation_vlans: Virtual segmentation (VLANs)**
*Basic Description:* Virtual LANs

**Option software_defined_networking_sdn: Software-defined networking (SDN)**
*Basic Description:* SDN-based segmentation

**Option micro_segmentation: Micro-segmentation**
*Basic Description:* Granular workload-level segmentation

**Option no: No segmentation**
*Basic Description:* No network segmentation implemented



#### Question 5.1.3

**Question:** Do you have a DMZ (demilitarized zone)?

**Type:** yes_no

**Explanation:** DMZ provides additional protection for public-facing services.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.1.4

**Question:** How do you control network access between segments?

**Type:** multiple_choice

**Explanation:** Access controls between segments prevent lateral movement of attackers.

**Answer Options:**

**Option firewalls: Firewalls**
*Basic Description:* Firewall-based access control

**Option access_control_lists: Access control lists**
*Basic Description:* ACL-based access control

**Option zero_trust_model: Zero trust model**
*Basic Description:* Zero trust network architecture

**Option no: No controls**
*Basic Description:* No network access controls


#### Question 5.1.5

**Question:** Do you implement zero trust network principles?

**Type:** multiple_choice

**Explanation:** Zero trust assumes no implicit trust and verifies every transaction.

**Answer Options:**

**Option fully_implemented: Fully implemented**
*Basic Description:* Complete zero trust implementation

**Option partially_implemented: Partially implemented**
*Basic Description:* Some zero trust principles

**Option planning: Planning**
*Basic Description:* Zero trust implementation planned

**Option not_implemented: Not implemented**
*Basic Description:* No zero trust implementation


#### Question 5.1.6

**Question:** How do you secure wireless networks?

**Type:** multiple_select

**Scale:** implementation

**Explanation:** Wireless security prevents unauthorized network access and data interception.

**Answer Options:**
**Option fully_implemented: WPA2-Enterprise or WPA3 encryption**
*Basic Description:* Modern encryption standards with enterprise authentication

**Option partially_implemented: WPA2-Personal (pre-shared key)**
*Basic Description:* Basic password-based encryption

**Option planned: Guest network isolation (separate SSID)**
*Basic Description:* Segregated network for visitors

**Option not_implemented: 802.1X authentication**
*Basic Description:* Certificate or credential-based access control

**Option network_access_control_nac: Network access control (NAC)**
*Basic Description:* Device posture checking before network access

**Option wireless_intrusion_detection_prevention: Wireless intrusion detection/prevention**
*Basic Description:* Monitoring for rogue access points and attacks

**Option no: No specific wireless security controls**
*Basic Description:* Basic or no wireless security measures



#### Question 5.1.7

**Question:** Do you have network documentation and diagrams?

**Type:** yes_no

**Explanation:** Network documentation is essential for security planning and incident response.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 5.2: Firewall & Perimeter Security

#### Question 5.2.1

**Question:** What types of firewalls do you deploy?

**Type:** multiple_select

**Explanation:** Multiple firewall types provide layered protection at different network levels.

**Answer Options:**
**Option next_generation_firewall_ngfw: Next-generation firewall (NGFW)**
*Basic Description:* Advanced firewall with IPS/IDS

**Option traditional_firewall: Traditional firewall**
*Basic Description:* Standard packet filtering firewall

**Option web_application_firewall_waf: Web application firewall (WAF)**
*Basic Description:* Application-layer firewall

**Option cloud_firewall: Cloud firewall**
*Basic Description:* Cloud-native firewall service

**Option not_deployed: Not deployed**
*Basic Description:* No firewall deployed



#### Question 5.2.2

**Question:** How often do you review firewall rules?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular rule reviews prevent rule creep and maintain security effectiveness.

**Answer Options:**

**Option quarterly: Weekly**
*Basic Description:* Every week review cycle

**Option annually: Monthly**
*Basic Description:* Every month review cycle

**Option only_after_changes: Quarterly**
*Basic Description:* Every three months review

**Option only_after_major_changes: Annually**
*Basic Description:* Once per year review

**Option as_needed: As needed**
*Basic Description:* Event-driven reviews only

**Option no_formal_review: Never**
*Basic Description:* No formal reviews


#### Question 5.2.3

**Question:** Do you implement default deny policies?

**Type:** yes_no

**Explanation:** Default deny ensures only explicitly allowed traffic is permitted.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.2.4

**Question:** Do you have intrusion detection/prevention systems (IDS/IPS)?

**Type:** multiple_choice

**Explanation:** IDS/IPS systems detect and prevent malicious network activity.

**Answer Options:**

**Option both_ids_and_ips:** Both IDS and IPS

**Option ids_only:** IDS only

**Option ips_only:** IPS only

**Option neither:** Neither


#### Question 5.2.5

**Question:** How do you handle firewall change management?

**Type:** multiple_choice

**Explanation:** Change management prevents unauthorized modifications and maintains security.

**Answer Options:**

**Option formal_change_process:** Formal change process

**Option automated_deployment:** Automated deployment

**Option manual_changes:** Manual changes

**Option no:** No process


#### Question 5.2.6

**Question:** Do you monitor firewall logs?

**Type:** yes_no

**Explanation:** Log monitoring helps detect attacks and troubleshoot connectivity issues.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.2.7

**Question:** Do you perform firewall penetration testing?

**Type:** multiple_choice

**Explanation:** Penetration testing validates firewall effectiveness against real-world attacks.

**Answer Options:**

**Option annually:** Annually

**Option bi_annually:** Bi-annually

**Option after_major_changes:** After major changes

**Option never:** Never



### Subsection 5.3: Network Monitoring & Detection

#### Question 5.3.1

**Question:** Do you have network traffic monitoring capabilities?

**Type:** yes_no

**Explanation:** Traffic monitoring helps detect anomalies and potential security incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.3.2

**Question:** What network monitoring tools do you use?

**Type:** multiple_select

**Explanation:** Multiple monitoring tools provide comprehensive visibility into network activity.

**Answer Options:**
**Option commercial_solution: Commercial solution**
*Basic Description:* Vendor-provided commercial product

**Option open_source_solution: Open-source solution**
*Basic Description:* Open-source tools and platforms

**Option custom_built_solution: Custom-built solution**
*Basic Description:* Internally developed solution

**Option managed_service: Managed service**
*Basic Description:* Third-party managed service

**Option not_deployed: Not deployed**
*Basic Description:* Not currently deployed



#### Question 5.3.3

**Question:** Do you monitor for lateral movement?

**Type:** yes_no

**Explanation:** Lateral movement detection helps identify compromised systems spreading through the network.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.3.4

**Question:** How do you detect network anomalies?

**Type:** multiple_choice

**Explanation:** Anomaly detection helps identify previously unknown threats and attack patterns.

**Answer Options:**

**Option machine_learning:** Machine learning

**Option signature_based:** Signature-based

**Option behavioral_analysis:** Behavioral analysis

**Option manual_review:** Manual review

**Option no:** No detection


#### Question 5.3.5

**Question:** Do you have network forensics capabilities?

**Type:** yes_no

**Explanation:** Network forensics enables investigation of security incidents and attack reconstruction.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.3.6

**Question:** How long do you retain network logs?

**Type:** multiple_choice

**Explanation:** Log retention enables historical analysis and compliance with regulatory requirements.

**Answer Options:**

**Option 30_days:** 30 days

**Option 90_days:** 90 days

**Option 6_months:** 6 months

**Option 1_year:** 1 year

**Option 1_year_5:** > 1 year

**Option not_retained:** Not retained



### Subsection 5.4: Remote Access & VPN

#### Question 5.4.1

**Question:** What remote access solutions do you provide?

**Type:** multiple_select

**Explanation:** Secure remote access is essential for modern distributed workforces.

**Answer Options:**
**Option commercial_solution: Commercial solution**
*Basic Description:* Vendor-provided commercial product

**Option open_source_solution: Open-source solution**
*Basic Description:* Open-source tools and platforms

**Option custom_built_solution: Custom-built solution**
*Basic Description:* Internally developed solution

**Option managed_service: Managed service**
*Basic Description:* Third-party managed service

**Option not_deployed: Not deployed**
*Basic Description:* Not currently deployed



#### Question 5.4.2

**Question:** Do you require multi-factor authentication for remote access?

**Type:** yes_no

**Explanation:** MFA significantly reduces the risk of unauthorized remote access.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 5.4.3

**Question:** What VPN protocols do you support?

**Type:** multiple_select

**Explanation:** Modern VPN protocols provide better security and performance than legacy options.

**Answer Options:**
**Option ipsec_ikev2: IPsec/IKEv2**
*Basic Description:* Industry-standard IPsec with IKEv2 key exchange

**Option ssl_tls_vpn_e_g_openvpn: SSL/TLS VPN (e.g., OpenVPN)**
*Basic Description:* SSL/TLS-based VPN protocols like OpenVPN

**Option wireguard: WireGuard**
*Basic Description:* Modern, lightweight VPN protocol with strong cryptography

**Option l2tp_ipsec: L2TP/IPsec**
*Basic Description:* Layer 2 Tunneling Protocol with IPsec encryption

**Option sstp: SSTP**
*Basic Description:* Secure Socket Tunneling Protocol (Microsoft)

**Option none_not_applicable: None/Not applicable**
*Basic Description:* No VPN or not applicable to our organization



#### Question 5.4.4

**Question:** Do you implement split tunneling policies?

**Type:** multiple_choice

**Explanation:** Split tunneling policies balance security with performance and user experience.

**Answer Options:**

**Option prohibited:** Prohibited

**Option allowed_with_restrictions:** Allowed with restrictions

**Option fully_allowed:** Fully allowed

**Option not_configured:** Not configured


#### Question 5.4.5

**Question:** How do you monitor remote access sessions?

**Type:** multiple_choice

**Explanation:** Remote access monitoring helps detect unauthorized usage and security incidents.

**Answer Options:**

**Option real_time_monitoring:** Real-time monitoring

**Option log_analysis:** Log analysis

**Option periodic_reviews:** Periodic reviews

**Option not_monitored:** Not monitored


#### Question 5.4.6

**Question:** Do you have device compliance requirements for remote access?

**Type:** yes_no

**Explanation:** Device compliance ensures remote devices meet security standards before network access.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



---

## Section 6: Endpoint Security

**Suggested Respondents:** Endpoint Engineering Lead

### Subsection 6.1: Endpoint Protection & Management

#### Question 6.1.1

**Question:** What endpoint protection solutions do you deploy?

**Type:** multiple_select

**Explanation:** Multiple endpoint protection layers provide comprehensive defense against various threats.

**Answer Options:**
**Option commercial_solution: Commercial solution**
*Basic Description:* Vendor-provided commercial product

**Option open_source_solution: Open-source solution**
*Basic Description:* Open-source tools and platforms

**Option custom_built_solution: Custom-built solution**
*Basic Description:* Internally developed solution

**Option managed_service: Managed service**
*Basic Description:* Third-party managed service

**Option not_deployed: Not deployed**
*Basic Description:* Not currently deployed



#### Question 6.1.2

**Question:** Do you have centralized endpoint management?

**Type:** yes_no

**Explanation:** Centralized management enables consistent policy enforcement and monitoring across all endpoints.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.1.3

**Question:** How do you manage endpoint configurations?

**Type:** multiple_choice

**Explanation:** Automated configuration management ensures consistent security settings across endpoints.

**Answer Options:**

**Option group_policy: Group Policy**
*Basic Description:* Microsoft Active Directory centralized configuration management

**Option mdm_emm: MDM/EMM**
*Basic Description:* Mobile Device Management/Enterprise Mobility Management

**Option configuration_management_tools: Configuration management tools**
*Basic Description:* Automated tools like Ansible, Puppet, Chef

**Option manual_configuration:** Manual configuration

**Option no:** No management


#### Question 6.1.4

**Question:** Do you implement application whitelisting/allowlisting?

**Type:** yes_no

**Explanation:** Application control prevents execution of unauthorized or malicious software.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.1.5

**Question:** How often do you update endpoint protection signatures?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Frequent signature updates ensure protection against the latest threats.

**Answer Options:**

**Option quarterly:** Real-time

**Option annually:** Hourly

**Option only_after_changes:** Daily

**Option only_after_major_changes:** Weekly

**Option as_needed:** Manual updates


#### Question 6.1.6

**Question:** Do you monitor endpoint security events?

**Type:** yes_no

**Explanation:** Event monitoring enables rapid detection and response to security incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.1.7

**Question:** What percentage of endpoints have security agents installed?

**Type:** multiple_choice

**Explanation:** High coverage ensures comprehensive endpoint protection across the organization.

**Answer Options:**

**Option 90_100:** 90-100%

**Option 75_89:** 75-89%

**Option 50_74:** 50-74%

**Option 25_49:** 25-49%

**Option 0_24:** 0-24%



### Subsection 6.2: Mobile Device Security

#### Question 6.2.1

**Question:** Do you have a mobile device management (MDM) solution?

**Type:** yes_no

**Explanation:** MDM solutions provide centralized management and security for mobile devices.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.2.2

**Question:** What mobile device policies do you enforce?

**Type:** multiple_select

**Explanation:** Mobile policies protect corporate data on personal and company devices.

**Answer Options:**
**Option screen_lock_passcode_enforcement: Screen lock/passcode enforcement**
*Basic Description:* Require device passcode or biometric authentication

**Option full_device_encryption: Full-device encryption**
*Basic Description:* Mandate encryption for all mobile devices

**Option mdm_enrollment: MDM enrollment**
*Basic Description:* Require Mobile Device Management enrollment

**Option os_version_enforcement: OS version enforcement**
*Basic Description:* Enforce minimum operating system versions

**Option app_allow_deny_lists: App allow/deny lists**
*Basic Description:* Control which applications can be installed

**Option jailbreak_root_detection: Jailbreak/root detection**
*Basic Description:* Detect and block compromised devices

**Option remote_wipe_capability: Remote wipe capability**
*Basic Description:* Ability to remotely erase device data

**Option conditional_access_policies: Conditional access policies**
*Basic Description:* Context-based access controls for mobile devices

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 6.2.3

**Question:** How do you handle BYOD (Bring Your Own Device)?

**Type:** multiple_choice

**Explanation:** BYOD policies balance user convenience with security requirements.

**Answer Options:**

**Option full_mdm_enrollment:** Full MDM enrollment

**Option app_wrapping_containerization:** App wrapping/containerization

**Option vpn_only_access:** VPN-only access

**Option not_allowed:** Not allowed

**Option no:** No controls


#### Question 6.2.4

**Question:** Do you separate personal and corporate data on mobile devices?

**Type:** yes_no

**Explanation:** Data separation protects corporate information while preserving user privacy.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.2.5

**Question:** How do you manage mobile app installations?

**Type:** multiple_choice

**Explanation:** App management prevents installation of malicious or unauthorized applications.

**Answer Options:**

**Option app_store_restrictions:** App store restrictions

**Option corporate_app_catalog:** Corporate app catalog

**Option sideloading_blocked:** Sideloading blocked

**Option no:** No restrictions


#### Question 6.2.6

**Question:** Do you monitor mobile device compliance?

**Type:** yes_no

**Explanation:** Compliance monitoring ensures devices meet security requirements before accessing corporate resources.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 6.3: Endpoint Configuration Management

#### Question 6.3.1

**Question:** Do you have standardized endpoint configurations?

**Type:** yes_no

**Weight:** 3

**Explanation:** Standardized configurations reduce security risks and improve management efficiency.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.3.2

**Question:** How do you enforce endpoint configuration compliance?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Configuration enforcement ensures endpoints maintain security standards.

**Answer Options:**

**Option group_policy: Group Policy**
*Basic Description:* Microsoft Active Directory centralized configuration management

**Option configuration_management_tools: Configuration management tools**
*Basic Description:* Automated tools like Ansible, Puppet, Chef

**Option manual_checks:** Manual checks

**Option no:** No enforcement


#### Question 6.3.3

**Question:** Do you monitor endpoint configuration drift?

**Type:** yes_no

**Weight:** 3

**Explanation:** Configuration drift monitoring helps maintain security baselines over time.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 6.3.4

**Question:** How often do you review endpoint security configurations?

**Type:** multiple_choice

**Weight:** 1


**Scale:** frequency_review
**Explanation:** Regular configuration reviews ensure ongoing security effectiveness.

**Answer Options:**

**Option quarterly:** Weekly

**Option annually:** Monthly

**Option only_after_changes:** Quarterly

**Option only_after_major_changes:** Annually

**Option as_needed:** As needed

**Option no_formal_review:** Never



---

## Section 7: Data Protection & Privacy

**Suggested Respondents:** DLP Owner, Data Protection Officer

### Subsection 7.1: Data Encryption & Protection

#### Question 7.1.1

**Question:** Do you encrypt data at rest?

**Type:** yes_no

**Explanation:** Data encryption at rest protects against unauthorized access to stored information.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.1.2

**Question:** Do you encrypt data in transit?

**Type:** yes_no

**Explanation:** Data encryption in transit protects against interception during transmission.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.1.3

**Question:** What encryption standards do you use?

**Type:** multiple_select

**Explanation:** Strong encryption standards provide robust protection for sensitive data.

**Answer Options:**
**Option aes_256: AES-256**
*Basic Description:* Advanced Encryption Standard 256-bit

**Option aes_128: AES-128**
*Basic Description:* Advanced Encryption Standard 128-bit

**Option rsa: RSA**
*Basic Description:* RSA encryption

**Option other: Other encryption**
*Basic Description:* Other encryption methods

**Option not_encrypted: Not encrypted**
*Basic Description:* Data not encrypted



#### Question 7.1.4

**Question:** How do you manage encryption keys?

**Type:** multiple_choice

**Explanation:** Proper key management is essential for maintaining encryption security.

**Answer Options:**

**Option hardware_security_module_hsm:** Hardware Security Module (HSM)

**Option key_management_service_kms:** Key Management Service (KMS)

**Option software_based:** Software-based

**Option manual_management:** Manual management

**Option no:** No key management


#### Question 7.1.5

**Question:** Do you implement data loss prevention (DLP) controls?

**Type:** yes_no

**Explanation:** DLP controls prevent unauthorized data exfiltration and ensure compliance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.1.6

**Question:** How do you protect data on mobile devices?

**Type:** multiple_select

**Explanation:** Mobile data protection prevents loss of sensitive information on portable devices.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures



#### Question 7.1.7

**Question:** Do you use database encryption?

**Type:** multiple_choice

**Explanation:** Database encryption protects sensitive information stored in database systems.

**Answer Options:**

**Option transparent_data_encryption_tde:** Transparent Data Encryption (TDE)

**Option column_level_encryption:** Column-level encryption

**Option application_level_encryption:** Application-level encryption

**Option no:** No database encryption



### Subsection 7.2: Privacy & Compliance

#### Question 7.2.1

**Question:** Which privacy regulations apply to your organization?

**Type:** multiple_select

**Explanation:** Understanding applicable regulations is essential for compliance planning.

**Answer Options:**
**Option gdpr: GDPR**
*Basic Description:* General Data Protection Regulation (European Union)

**Option ccpa_cpra: CCPA/CPRA**
*Basic Description:* California Consumer Privacy Act / California Privacy Rights Act

**Option hipaa: HIPAA**
*Basic Description:* Health Insurance Portability and Accountability Act

**Option glba: GLBA**
*Basic Description:* Gramm-Leach-Bliley Act (financial services)

**Option sox: SOX**
*Basic Description:* Sarbanes-Oxley Act (financial reporting)

**Option pci_dss: PCI DSS**
*Basic Description:* Payment Card Industry Data Security Standard

**Option pipeda: PIPEDA**
*Basic Description:* Personal Information Protection and Electronic Documents Act (Canada)

**Option lgpd: LGPD**
*Basic Description:* Lei Geral de Proteção de Dados (Brazil)

**Option none_not_applicable: None/Not applicable**
*Basic Description:* No specific privacy regulations apply



#### Question 7.2.2

**Question:** Do you have a privacy policy?

**Type:** yes_no

**Explanation:** Privacy policies inform users about data collection and processing practices.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.2.3

**Question:** Do you conduct privacy impact assessments (PIAs)?

**Type:** yes_no

**Explanation:** PIAs help identify and mitigate privacy risks in new projects and systems.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.2.4

**Question:** How do you handle data subject requests?

**Type:** multiple_choice

**Explanation:** Efficient handling of data subject requests ensures compliance with privacy regulations.

**Answer Options:**

**Option automated_system:** Automated system

**Option manual_process:** Manual process

**Option third_party_service:** Third-party service

**Option no:** No formal process


#### Question 7.2.5

**Question:** Do you have a Data Protection Officer (DPO)?

**Type:** yes_no

**Explanation:** DPOs provide expertise and oversight for privacy compliance programs.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.2.6

**Question:** How do you obtain consent for data processing?

**Type:** multiple_choice

**Explanation:** Proper consent mechanisms ensure lawful processing of personal data.

**Answer Options:**

**Option explicit_consent:** Explicit consent

**Option opt_in:** Opt-in

**Option opt_out:** Opt-out

**Option implied_consent:** Implied consent

**Option no:** No consent mechanism



### Subsection 7.3: Data Backup & Recovery

#### Question 7.3.1

**Question:** Do you have a data backup strategy?

**Type:** yes_no

**Explanation:** Backup strategies ensure data availability and business continuity.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.3.2

**Question:** How frequently do you backup critical data?

**Type:** multiple_choice

**Explanation:** Frequent backups minimize data loss in case of incidents.

**Answer Options:**

**Option real_time:** Real-time

**Option hourly:** Hourly

**Option daily:** Daily

**Option weekly:** Weekly

**Option monthly:** Monthly


#### Question 7.3.3

**Question:** Where do you store backup data?

**Type:** multiple_select

**Scale:** coverage

**Explanation:** Multiple backup locations protect against site-specific disasters.

**Answer Options:**
**Option 76_100: Primary site only**
*Basic Description:* Backups stored at main facility

**Option 51_75: Secondary on-premises site**
*Basic Description:* Separate physical location (same organization)

**Option 26_50: Cloud storage (single region)**
*Basic Description:* Cloud provider in one geographic region

**Option 0_25: Cloud storage (multi-region)**
*Basic Description:* Replicated across multiple geographic regions

**Option offline_off_site_media: Offline / off-site media**
*Basic Description:* Tape or removable media stored off-site

**Option mix_of_the_above: Mix of the above**
*Basic Description:* Combination of multiple storage locations

**Option not_sure: Not sure / No defined strategy**
*Basic Description:* Backup location not clearly defined



#### Question 7.3.4

**Question:** Do you test backup restoration procedures?

**Type:** multiple_choice

**Explanation:** Regular testing ensures backups can be successfully restored when needed.

**Answer Options:**

**Option monthly:** Monthly

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option never:** Never


#### Question 7.3.5

**Question:** Are your backups encrypted?

**Type:** yes_no

**Explanation:** Backup encryption protects data confidentiality during storage and transmission.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 7.3.6

**Question:** What is your target Recovery Point Objective (RPO)?

**Type:** multiple_choice

**Explanation:** RPO defines acceptable data loss and guides backup frequency decisions.

**Answer Options:**

**Option 1_hour:** < 1 hour

**Option 1_4_hours:** 1-4 hours

**Option 4_24_hours:** 4-24 hours

**Option 24_hours:** > 24 hours

**Option not_defined:** Not defined



### Subsection 7.4: Data Governance & Subject Rights

#### Question 7.4.1

**Question:** Do you have data discovery and lineage capabilities?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Data discovery and lineage support compliance and risk management.

**Answer Options:**

**Option automated_discovery:** Automated discovery

**Option manual_mapping:** Manual mapping

**Option partial_capabilities:** Partial capabilities

**Option no:** No capabilities


#### Question 7.4.2

**Question:** How do you handle data subject access requests (DSAR)?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Efficient DSAR handling ensures compliance with privacy regulations.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 7.4.3

**Question:** Do you conduct Data Protection Impact Assessments (DPIA)?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** DPIAs identify and mitigate privacy risks in data processing activities.

**Answer Options:**

**Option for_all_high_risk_processing:** For all high-risk processing

**Option for_new_systems_only:** For new systems only

**Option occasionally:** Occasionally

**Option never:** Never


#### Question 7.4.4

**Question:** How do you manage cross-border data transfers?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Proper transfer mechanisms ensure lawful international data transfers.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 7.4.5

**Question:** Do you maintain consent management capabilities?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Consent management ensures lawful processing and user control over personal data.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization




---

## Section 8: Application Security


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown
**Suggested Respondents:** DevSecOps Lead, Application Security Architect

### Subsection 8.1: Secure Development Lifecycle

#### Question 8.1.1

**Question:** Do you have a secure software development lifecycle (SDLC)?

**Type:** yes_no

**Explanation:** Secure SDLC integrates security practices throughout the development process.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.1.2

**Question:** Do you conduct security code reviews?

**Type:** multiple_choice

**Explanation:** Code reviews help identify security vulnerabilities before deployment.

**Answer Options:**

**Option always:** Always

**Option for_critical_applications:** For critical applications

**Option occasionally:** Occasionally

**Option never:** Never

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.1.3

**Question:** What static application security testing (SAST) tools do you use?

**Type:** multiple_select

**Explanation:** SAST tools automatically identify security vulnerabilities in source code.

**Answer Options:**
**Option commercial_sast_tool: Commercial SAST tool**
*Basic Description:* Vendor SAST solution

**Option open_source_sast_tool: Open-source SAST tool**
*Basic Description:* Open-source static analysis

**Option ide_integrated_analysis: IDE-integrated analysis**
*Basic Description:* Built into development environment

**Option manual_code_review: Manual code review**
*Basic Description:* Manual security code review

**Option not_performed: Not performed**
*Basic Description:* SAST not performed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.1.4

**Question:** Do you perform dynamic application security testing (DAST)?

**Type:** yes_no

**Explanation:** DAST identifies vulnerabilities in running applications through external testing.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.1.5

**Question:** Do you use interactive application security testing (IAST)?

**Type:** yes_no

**Explanation:** IAST combines SAST and DAST approaches for comprehensive testing.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.1.6

**Question:** How do you manage third-party libraries and dependencies?

**Type:** multiple_choice

**Explanation:** Dependency management prevents introduction of vulnerable third-party components.

**Answer Options:**

**Option automated_scanning:** Automated scanning

**Option manual_review:** Manual review

**Option dependency_management_tools:** Dependency management tools

**Option no:** No management

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.1.7

**Question:** Do you have secure coding standards?

**Type:** yes_no

**Explanation:** Coding standards provide guidelines for writing secure code.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 8.2: Web Application Security

#### Question 8.2.1

**Question:** Do you protect against OWASP Top 10 vulnerabilities?

**Type:** yes_no

**Explanation:** OWASP Top 10 represents the most critical web application security risks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.2.2

**Question:** Do you implement input validation and sanitization?

**Type:** yes_no

**Explanation:** Input validation prevents injection attacks and data corruption.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.2.3

**Question:** How do you handle authentication in web applications?

**Type:** multiple_select

**Scale:** implementation

**Explanation:** Proper authentication mechanisms protect against unauthorized access.

**Answer Options:**
**Option fully_implemented: Centralized SSO (SAML/OIDC/OAuth) for all apps**
*Basic Description:* Single sign-on across all applications

**Option partially_implemented: Centralized SSO for some apps, local auth for others**
*Basic Description:* Mixed authentication approach

**Option planned: Local username/password per application**
*Basic Description:* Each app manages its own authentication

**Option not_implemented: Social login (Google/Microsoft/etc.) only**
*Basic Description:* Third-party identity providers

**Option mixed_approach_legacy_systems: Mixed approach / legacy systems**
*Basic Description:* Combination of multiple authentication methods

**Option not_sure: Not sure / Not defined**
*Basic Description:* Authentication approach unclear



#### Question 8.2.4

**Question:** Do you implement proper session management?

**Type:** yes_no

**Explanation:** Session management prevents session hijacking and fixation attacks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.2.5

**Question:** Do you use Content Security Policy (CSP)?

**Type:** yes_no

**Explanation:** CSP helps prevent cross-site scripting (XSS) attacks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.2.6

**Question:** How do you protect against cross-site request forgery (CSRF)?

**Type:** multiple_choice

**Explanation:** CSRF protection prevents unauthorized actions on behalf of authenticated users.

**Answer Options:**

**Option csrf_tokens:** CSRF tokens

**Option samesite_cookies:** SameSite cookies

**Option referrer_validation:** Referrer validation

**Option no:** No protection


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 8.3: API Security

#### Question 8.3.1

**Question:** How do you secure your APIs?

**Type:** multiple_select

**Explanation:** API security prevents unauthorized access and abuse of application interfaces.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.3.2

**Question:** Do you implement API rate limiting?

**Type:** yes_no

**Explanation:** Rate limiting prevents API abuse and denial of service attacks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.3.3

**Question:** Do you log and monitor API usage?

**Type:** yes_no

**Explanation:** API monitoring helps detect suspicious activity and security incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.3.4

**Question:** How do you handle API versioning?

**Type:** multiple_choice

**Explanation:** Proper API versioning ensures backward compatibility and security updates.

**Answer Options:**

**Option url_versioning:** URL versioning

**Option header_versioning:** Header versioning

**Option parameter_versioning:** Parameter versioning

**Option no:** No versioning

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.3.5

**Question:** Do you validate API inputs and outputs?

**Type:** yes_no

**Explanation:** Input/output validation prevents injection attacks and data leakage.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 8.3.6

**Question:** Do you use API gateways?

**Type:** yes_no

**Explanation:** API gateways provide centralized security, monitoring, and management.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 8.4: DevSecOps & CI/CD Security

#### Question 8.4.1

**Question:** Do you integrate security testing in your CI/CD pipeline?

**Type:** multiple_choice

**Weight:** 5

**Explanation:** Automated security testing in CI/CD enables early detection of vulnerabilities.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.4.2

**Question:** Do you implement merge gate policies for security?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Merge gates prevent vulnerable code from reaching production.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.4.3

**Question:** How do you scan for secrets in code repositories?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Secret scanning prevents credential exposure in source code.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.4.4

**Question:** Do you perform Infrastructure as Code (IaC) security scanning?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** IaC scanning identifies misconfigurations before deployment.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.4.5

**Question:** How do you handle security findings in CI/CD?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Structured handling ensures security findings are addressed promptly.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.4.6

**Question:** Do you enforce SBOM generation and attestation in your release pipeline?

**Type:** multiple_choice

**Weight:** 5

**Explanation:** SBOM enforcement provides supply chain transparency and enables vulnerability tracking.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 8.4.7

**Question:** Do you implement mandatory Infrastructure as Code (IaC) policy enforcement?

**Type:** multiple_choice

**Weight:** 5

**Explanation:** Mandatory IaC policies prevent misconfigurations and enforce security standards.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization




---

## Section 9: Cloud & Container Security


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown
**Suggested Respondents:** Cloud Security Architect

### Subsection 9.1: Cloud Infrastructure Security

#### Question 9.1.1

**Question:** Which cloud service models do you use?

**Type:** multiple_select

**Explanation:** Different service models require different security approaches and responsibilities.

**Answer Options:**
**Option iaas: IaaS**
*Basic Description:* Infrastructure as a Service (virtual machines, storage, networks)

**Option paas: PaaS**
*Basic Description:* Platform as a Service (application platforms, databases)

**Option saas: SaaS**
*Basic Description:* Software as a Service (cloud applications)

**Option faas_serverless: FaaS/Serverless**
*Basic Description:* Function as a Service or serverless computing

**Option private_cloud: Private cloud**
*Basic Description:* Dedicated private cloud infrastructure

**Option hybrid_multi_cloud: Hybrid/Multi-cloud**
*Basic Description:* Combination of multiple cloud environments

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.1.2

**Question:** Do you have a cloud security strategy?

**Type:** yes_no

**Explanation:** A cloud security strategy ensures consistent protection across cloud environments.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 9.1.3

**Question:** How do you secure cloud configurations?

**Type:** multiple_select

**Explanation:** Secure configurations prevent common cloud misconfigurations and vulnerabilities.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.1.4

**Question:** Do you implement network security in the cloud?

**Type:** multiple_choice

**Explanation:** Cloud network security controls protect against unauthorized access and attacks.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.1.5

**Question:** How do you monitor cloud security?

**Type:** multiple_select

**Explanation:** Cloud security monitoring provides visibility into threats and compliance issues.

**Answer Options:**
**Option automated_monitoring_tools: Automated monitoring tools**
*Basic Description:* Using SIEM, monitoring platforms, or similar

**Option manual_reviews: Manual reviews**
*Basic Description:* Regular manual checks and reviews

**Option combination_approach: Combination approach**
*Basic Description:* Mix of automated and manual monitoring

**Option third_party_service: Third-party service**
*Basic Description:* Outsourced monitoring

**Option not_monitored: Not monitored**
*Basic Description:* Not currently monitored


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.1.6

**Question:** Do you encrypt data in cloud storage?

**Type:** yes_no

**Explanation:** Cloud data encryption protects against unauthorized access to stored information.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 9.1.7

**Question:** How do you manage cloud costs and security trade-offs?

**Type:** multiple_choice

**Explanation:** Balancing cost and security ensures adequate protection within budget constraints.

**Answer Options:**

**Option security_first_approach:** Security-first approach

**Option cost_optimized_with_security:** Cost-optimized with security

**Option balanced_approach:** Balanced approach

**Option cost_first_approach:** Cost-first approach


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 9.2: Cloud Identity & Access Management

#### Question 9.2.1

**Question:** How do you manage cloud identities?

**Type:** multiple_select

**Explanation:** Proper cloud identity management ensures secure access to cloud resources.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.2.2

**Question:** Do you implement least privilege in cloud environments?

**Type:** yes_no

**Explanation:** Least privilege reduces the risk of unauthorized access and privilege escalation.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 9.2.3

**Question:** How do you secure cloud API access?

**Type:** multiple_select

**Explanation:** API security prevents unauthorized access to cloud management interfaces.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.2.4

**Question:** Do you rotate cloud access credentials?

**Type:** multiple_choice

**Explanation:** Credential rotation reduces the risk of compromised access keys.

**Answer Options:**

**Option automatically:** Automatically

**Option regularly:** Regularly

**Option occasionally:** Occasionally

**Option never:** Never


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown

#### Question 9.2.5

**Question:** How do you manage privileged access to cloud resources?

**Type:** multiple_choice

**Explanation:** Privileged access management prevents unauthorized administrative actions.

**Answer Options:**

**Option pam_solution:** PAM solution

**Option break_glass_procedures:** Break-glass procedures

**Option shared_accounts:** Shared accounts

**Option no:** No special controls


#### Question 9.2.6

**Question:** Do you monitor cloud access and activities?

**Type:** yes_no

**Explanation:** Activity monitoring helps detect unauthorized access and suspicious behavior.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 9.3: Container & Serverless Security

#### Question 9.3.1

**Question:** Do you use containers in your cloud environment?

**Type:** yes_no

**Explanation:** Container usage requires specific security considerations and controls.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 9.3.2

**Question:** How do you secure container images?

**Type:** multiple_select

**Explanation:** Container image security prevents deployment of vulnerable or malicious containers.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.3.3

**Question:** Do you implement container runtime security?

**Type:** multiple_choice

**Explanation:** Runtime security protects containers during execution from various threats.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.3.4

**Question:** How do you secure serverless functions?

**Type:** multiple_select

**Explanation:** Serverless security addresses unique risks in function-as-a-service environments.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 9.3.5

**Question:** Do you scan for vulnerabilities in cloud workloads?

**Type:** yes_no

**Explanation:** Vulnerability scanning identifies security weaknesses in cloud-deployed applications.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 9.3.6

**Question:** How do you manage secrets in cloud environments?

**Type:** multiple_choice

**Explanation:** Proper secret management prevents exposure of sensitive credentials and keys.

**Answer Options:**

**Option cloud_secret_managers:** Cloud secret managers

**Option environment_variables:** Environment variables

**Option configuration_files:** Configuration files

**Option hardcoded:** Hardcoded

**Option external_vault:** External vault



---

## Section 10: Incident Response & Resilience


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown
**Suggested Respondents:** CISO, Incident Response Manager

### Subsection 10.1: Incident Response Planning

#### Question 10.1.1

**Question:** Do you have a formal incident response plan?

**Type:** yes_no

**Explanation:** A formal incident response plan ensures coordinated and effective response to security incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.1.2

**Question:** How often do you update your incident response plan?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular updates ensure the plan remains current with threats and organizational changes.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option only_after_changes:** After incidents

**Option only_after_major_changes:** As needed

**Option as_needed:** Never updated

**Option no_formal_review: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.1.3

**Question:** Do you have an incident response team (IRT)?

**Type:** yes_no

**Explanation:** A dedicated incident response team provides specialized expertise for handling security incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.1.4

**Question:** What roles are defined in your incident response team?

**Type:** multiple_select

**Explanation:** Clear roles ensure effective coordination and decision-making during incidents.

**Answer Options:**
**Option incident_commander_lead: Incident Commander/Lead**
*Basic Description:* Overall incident response coordinator and decision maker

**Option communications_lead: Communications Lead**
*Basic Description:* Internal and external communications coordinator

**Option forensics_investigation_lead: Forensics/Investigation Lead**
*Basic Description:* Digital forensics and investigation specialist

**Option it_operations: IT Operations**
*Basic Description:* Technical operations and system recovery

**Option security_engineering: Security Engineering**
*Basic Description:* Security tools and threat analysis

**Option legal_privacy_officer: Legal/Privacy Officer**
*Basic Description:* Legal compliance and privacy considerations

**Option human_resources: Human Resources**
*Basic Description:* Employee-related incident handling

**Option public_relations_communications: Public Relations/Communications**
*Basic Description:* External media and stakeholder communications

**Option external_ir_provider_consultant: External IR Provider/Consultant**
*Basic Description:* Third-party incident response support

**Option business_unit_representatives: Business Unit Representatives**
*Basic Description:* Business stakeholders and process owners

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.1.5

**Question:** Do you conduct incident response training?

**Type:** multiple_choice

**Explanation:** Training ensures team members are prepared to execute the incident response plan effectively.

**Answer Options:**

**Option regularly:** Regularly

**Option annually:** Annually

**Option occasionally:** Occasionally

**Option never:** Never


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown

#### Question 10.1.6

**Question:** Do you perform incident response exercises or tabletops?

**Type:** multiple_choice

**Explanation:** Exercises test the incident response plan and identify areas for improvement.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option occasionally:** Occasionally

**Option never:** Never


#### Question 10.1.7

**Question:** Do you have predefined incident severity levels?

**Type:** yes_no

**Explanation:** Severity levels help prioritize response efforts and determine escalation procedures.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 10.2: Incident Detection & Response

#### Question 10.2.1

**Question:** How do you detect security incidents?

**Type:** multiple_select

**Explanation:** Multiple detection methods improve the likelihood of identifying security incidents quickly.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.2.2

**Question:** What is your target time for incident detection?

**Type:** multiple_choice

**Explanation:** Rapid detection minimizes the impact and spread of security incidents.

**Answer Options:**

**Option 1_hour:** < 1 hour

**Option 1_4_hours:** 1-4 hours

**Option 4_24_hours:** 4-24 hours

**Option 24_hours:** > 24 hours

**Option no:** No target

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.2.3

**Question:** Do you have 24/7 incident response capabilities?

**Type:** yes_no

**Explanation:** Round-the-clock capabilities ensure incidents can be addressed regardless of when they occur.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.2.4

**Question:** How do you contain security incidents?

**Type:** multiple_select

**Explanation:** Containment prevents incidents from spreading and causing additional damage.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.2.5

**Question:** Do you have incident escalation procedures?

**Type:** yes_no

**Explanation:** Escalation procedures ensure appropriate stakeholders are notified based on incident severity.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.2.6

**Question:** How do you communicate during incidents?

**Type:** multiple_select

**Explanation:** Effective communication keeps stakeholders informed and coordinates response efforts.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 10.3: Incident Recovery & Lessons Learned

#### Question 10.3.1

**Question:** Do you have incident recovery procedures?

**Type:** yes_no

**Explanation:** Recovery procedures ensure systems and operations are restored safely after incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.3.2

**Question:** How do you validate system integrity after incidents?

**Type:** multiple_choice

**Explanation:** Integrity validation ensures systems are clean before returning to normal operations.

**Answer Options:**

**Option automated_scanning:** Automated scanning

**Option manual_verification:** Manual verification

**Option third_party_assessment:** Third-party assessment

**Option no:** No validation

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.3.3

**Question:** Do you conduct post-incident reviews?

**Type:** yes_no

**Explanation:** Post-incident reviews identify lessons learned and opportunities for improvement.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.3.4

**Question:** Do you document incident details and response actions?

**Type:** yes_no

**Explanation:** Documentation provides valuable information for future incidents and compliance requirements.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 10.3.5

**Question:** How do you track incident metrics?

**Type:** multiple_select

**Explanation:** Metrics help measure incident response effectiveness and identify improvement areas.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 10.3.6

**Question:** Do you update security controls based on incident findings?

**Type:** yes_no

**Explanation:** Control updates help prevent similar incidents from occurring in the future.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



---

## Section 11: Business Continuity

**Suggested Respondents:** BCP Coordinator, Risk Manager

### Subsection 11.1: Business Continuity Planning

#### Question 11.1.1

**Question:** Do you have a business continuity plan (BCP)?

**Type:** yes_no

**Explanation:** A BCP ensures critical business functions can continue during and after disruptions.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.1.2

**Question:** How often do you update your business continuity plan?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular updates ensure the plan remains current with business changes and lessons learned.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option only_after_changes:** After incidents

**Option only_after_major_changes:** As needed

**Option as_needed:** Never updated


#### Question 11.1.3

**Question:** Do you conduct business impact assessments (BIA)?

**Type:** yes_no

**Explanation:** BIAs identify critical business processes and their recovery requirements.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.1.4

**Question:** What is your target Recovery Time Objective (RTO) for critical systems?

**Type:** multiple_choice

**Explanation:** RTO defines acceptable downtime and guides recovery planning decisions.

**Answer Options:**

**Option 1_hour:** < 1 hour

**Option 1_4_hours:** 1-4 hours

**Option 4_24_hours:** 4-24 hours

**Option 24_hours:** > 24 hours

**Option not_defined:** Not defined


#### Question 11.1.5

**Question:** Do you have alternate work locations identified?

**Type:** yes_no

**Explanation:** Alternate locations ensure business operations can continue if primary facilities are unavailable.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.1.6

**Question:** Do you test your business continuity plan?

**Type:** multiple_choice

**Explanation:** Regular testing validates the plan's effectiveness and identifies improvement areas.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option occasionally:** Occasionally

**Option never:** Never



### Subsection 11.2: Disaster Recovery

#### Question 11.2.1

**Question:** Do you have a disaster recovery plan (DRP)?

**Type:** yes_no

**Explanation:** A DRP provides procedures for recovering IT systems and data after disasters.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.2.2

**Question:** Where do you maintain disaster recovery capabilities?

**Type:** multiple_select

**Explanation:** Multiple recovery options provide flexibility and resilience against different disaster scenarios.

**Answer Options:**
**Option on_premises_data_center: On-premises data center**
*Basic Description:* Secondary on-premises facility

**Option co_location_facility: Co-location facility**
*Basic Description:* Third-party colocation data center

**Option cloud_provider_iaas: Cloud provider (IaaS)**
*Basic Description:* Cloud-based disaster recovery infrastructure

**Option managed_dr_service: Managed DR service**
*Basic Description:* Third-party managed disaster recovery service

**Option hot_site: Hot site**
*Basic Description:* Fully operational backup site ready for immediate use

**Option warm_site: Warm site**
*Basic Description:* Partially equipped site requiring some setup time

**Option cold_site: Cold site**
*Basic Description:* Basic facility requiring significant setup

**Option none_not_applicable: None/Not applicable**
*Basic Description:* No dedicated DR capabilities



#### Question 11.2.3

**Question:** How do you replicate critical data for disaster recovery?

**Type:** multiple_choice

**Explanation:** Data replication ensures critical information is available for recovery operations.

**Answer Options:**

**Option real_time_replication:** Real-time replication

**Option near_real_time:** Near real-time

**Option scheduled_backups:** Scheduled backups

**Option manual_copying:** Manual copying

**Option no:** No replication


#### Question 11.2.4

**Question:** Do you conduct disaster recovery exercises?

**Type:** multiple_choice

**Explanation:** DR exercises validate recovery procedures and team readiness.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option occasionally:** Occasionally

**Option never:** Never


#### Question 11.2.5

**Question:** How do you communicate during disaster recovery?

**Type:** multiple_select

**Explanation:** Effective communication keeps stakeholders informed during recovery operations.

**Answer Options:**
**Option out_of_band_messaging: Out-of-band messaging**
*Basic Description:* SMS, phone tree, or alternate communication channels

**Option emergency_notification_system: Emergency notification system**
*Basic Description:* Dedicated mass notification platform

**Option dedicated_dr_communication_platform: Dedicated DR communication platform**
*Basic Description:* Separate Slack/Teams tenant or communication tool

**Option satellite_backup_phone_system: Satellite/backup phone system**
*Basic Description:* Backup telephony infrastructure

**Option alternate_email_system: Alternate email system**
*Basic Description:* Secondary email system independent of primary

**Option predefined_conference_bridges: Predefined conference bridges**
*Basic Description:* Pre-configured conference call lines

**Option physical_rally_points: Physical rally points**
*Basic Description:* Designated physical meeting locations

**Option not_implemented: Not implemented**
*Basic Description:* No dedicated DR communication plan




### Subsection 11.3: Crisis Management

#### Question 11.3.1

**Question:** Do you have a crisis management team?

**Type:** yes_no

**Explanation:** A crisis management team provides leadership and coordination during major disruptions.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.3.2

**Question:** Do you have crisis communication procedures?

**Type:** yes_no

**Explanation:** Communication procedures ensure consistent and timely information sharing during crises.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.3.3

**Question:** How do you coordinate with external stakeholders during crises?

**Type:** multiple_select

**Explanation:** External coordination ensures comprehensive crisis response and stakeholder management.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 11.3.4

**Question:** Do you conduct crisis management training?

**Type:** multiple_choice

**Explanation:** Training ensures team members are prepared to manage crises effectively.

**Answer Options:**

**Option regularly:** Regularly

**Option annually:** Annually

**Option occasionally:** Occasionally

**Option never:** Never


#### Question 11.3.5

**Question:** How do you manage crisis decision-making authority?

**Type:** multiple_select

**Explanation:** Clear decision-making authority enables rapid crisis response.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 11.3.6

**Question:** Do you have crisis resource allocation procedures?

**Type:** yes_no

**Explanation:** Resource allocation procedures ensure critical needs are met during crises.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 11.4: Recovery Operations

#### Question 11.4.1

**Question:** Do you have documented recovery procedures?

**Type:** yes_no

**Explanation:** Recovery procedures provide step-by-step guidance for restoring operations.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.4.2

**Question:** How do you prioritize recovery activities?

**Type:** multiple_select

**Explanation:** Recovery prioritization ensures critical functions are restored first.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 11.4.3

**Question:** Do you have recovery time objectives (RTO) defined?

**Type:** yes_no

**Explanation:** RTOs establish target timeframes for restoring business functions.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.4.4

**Question:** Do you have recovery point objectives (RPO) defined?

**Type:** yes_no

**Explanation:** RPOs define acceptable data loss limits during recovery.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 11.4.5

**Question:** How do you coordinate recovery activities?

**Type:** multiple_select

**Explanation:** Coordinated recovery ensures efficient restoration of operations.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 11.4.6

**Question:** Do you conduct post-incident reviews?

**Type:** yes_no

**Explanation:** Post-incident reviews identify lessons learned and improvement opportunities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



---

## Section 12: Vendor Management

**Suggested Respondents:** Vendor Risk Manager, Procurement

### Subsection 12.1: Vendor Risk Assessment

#### Question 12.1.1

**Question:** Do you conduct security assessments of vendors?

**Type:** yes_no

**Explanation:** Vendor security assessments help identify and mitigate third-party risks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 12.1.2

**Question:** What criteria do you use for vendor security evaluation?

**Type:** multiple_select

**Explanation:** Multiple evaluation criteria provide comprehensive vendor risk assessment.

**Answer Options:**
**Option security_questionnaire_assessment: Security questionnaire/assessment**
*Basic Description:* Standardized security questionnaire or assessment

**Option soc_2_type_ii_or_iso_27001_certification: SOC 2 Type II or ISO 27001 certification**
*Basic Description:* Third-party security certifications and attestations

**Option penetration_test_reports: Penetration test reports**
*Basic Description:* Recent penetration testing results

**Option data_processing_agreement_dpa: Data Processing Agreement (DPA)**
*Basic Description:* Data processing and privacy agreements

**Option breach_notification_history: Breach notification history**
*Basic Description:* Historical security incident and breach record

**Option subprocessor_management: Subprocessor management**
*Basic Description:* Vendor's third-party and subprocessor controls

**Option regulatory_compliance_attestations: Regulatory compliance attestations**
*Basic Description:* Compliance with relevant regulations (HIPAA, PCI DSS, etc.)

**Option contractual_slas_and_guarantees: Contractual SLAs and guarantees**
*Basic Description:* Service level agreements and security guarantees

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 12.1.3

**Question:** How do you classify vendor risk levels?

**Type:** multiple_choice

**Explanation:** Risk classification helps prioritize vendor management efforts and controls.

**Answer Options:**

**Option high_medium_low:** High/Medium/Low

**Option critical_important_standard:** Critical/Important/Standard

**Option tiered_approach:** Tiered approach

**Option no:** No classification


#### Question 12.1.4

**Question:** Do you require security certifications from vendors?

**Type:** multiple_choice

**Explanation:** Security certifications provide assurance of vendor security practices.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 12.1.5

**Question:** How often do you reassess vendor security?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular reassessment ensures ongoing vendor security compliance.

**Answer Options:**

**Option quarterly:** Annually

**Option annually:** Bi-annually

**Option only_after_changes:** Contract renewal

**Option only_after_major_changes:** As needed

**Option as_needed:** Never


#### Question 12.1.6

**Question:** Do you maintain a vendor risk register?

**Type:** yes_no

**Explanation:** A risk register provides centralized tracking of vendor security risks.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 12.1.7

**Question:** How do you handle high-risk vendors?

**Type:** multiple_select

**Explanation:** High-risk vendors require additional security measures and oversight.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed




### Subsection 12.2: Contract Management

#### Question 12.2.1

**Question:** Do you include security requirements in vendor contracts?

**Type:** yes_no

**Explanation:** Contractual security requirements establish legal obligations for vendor security.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 12.2.2

**Question:** What security clauses do you include in contracts?

**Type:** multiple_select

**Explanation:** Comprehensive security clauses protect organizational interests and data.

**Answer Options:**
**Option option_1: Option 1**
*Basic Description:* First option

**Option option_2: Option 2**
*Basic Description:* Second option

**Option option_3: Option 3**
*Basic Description:* Third option

**Option option_4: Option 4**
*Basic Description:* Fourth option

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 12.2.3

**Question:** Do you require vendor insurance coverage?

**Type:** multiple_choice

**Explanation:** Insurance coverage provides financial protection against vendor-related incidents.

**Answer Options:**

**Option cyber_liability:** Cyber liability

**Option professional_liability:** Professional liability

**Option general_liability:** General liability

**Option all_of_the_above:** All of the above

**Option none_required:** None required


#### Question 12.2.4

**Question:** How do you handle data processing agreements?

**Type:** multiple_choice

**Explanation:** Data processing agreements ensure compliance with privacy regulations.

**Answer Options:**

**Option standard_dpa:** Standard DPA

**Option custom_agreements:** Custom agreements

**Option vendor_templates:** Vendor templates

**Option no:** No formal agreements


#### Question 12.2.5

**Question:** Do you include right-to-audit clauses?

**Type:** yes_no

**Explanation:** Audit rights enable verification of vendor security compliance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 12.2.6

**Question:** How do you handle contract termination security requirements?

**Type:** multiple_select

**Explanation:** Termination requirements ensure secure end-of-relationship procedures.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed




### Subsection 12.3: Vendor Monitoring & Oversight

#### Question 12.3.1

**Question:** How do you monitor vendor security performance?

**Type:** multiple_select

**Explanation:** Ongoing monitoring ensures vendors maintain security standards.

**Answer Options:**
**Option automated_monitoring_tools: Automated monitoring tools**
*Basic Description:* Using SIEM, monitoring platforms, or similar

**Option manual_reviews: Manual reviews**
*Basic Description:* Regular manual checks and reviews

**Option combination_approach: Combination approach**
*Basic Description:* Mix of automated and manual monitoring

**Option third_party_service: Third-party service**
*Basic Description:* Outsourced monitoring

**Option not_monitored: Not monitored**
*Basic Description:* Not currently monitored



#### Question 12.3.2

**Question:** Do you require incident notification from vendors?

**Type:** yes_no

**Explanation:** Incident notification enables rapid response to vendor security events.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 12.3.3

**Question:** What is your required timeframe for vendor incident notification?

**Type:** multiple_choice

**Explanation:** Timely notification enables effective incident response and risk mitigation.

**Answer Options:**

**Option immediately:** Immediately

**Option 24_hours:** 24 hours

**Option 72_hours:** 72 hours

**Option 1_week:** 1 week

**Option no:** No requirement


#### Question 12.3.4

**Question:** Do you conduct vendor security audits?

**Type:** multiple_choice

**Explanation:** Security audits verify vendor compliance with security requirements.

**Answer Options:**

**Option regularly:** Regularly

**Option risk_based:** Risk-based

**Option contract_driven:** Contract-driven

**Option never:** Never


#### Question 12.3.5

**Question:** How do you handle vendor security incidents?

**Type:** multiple_select

**Explanation:** Structured incident handling ensures effective response to vendor security events.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 12.3.6

**Question:** Do you maintain vendor contact information for security issues?

**Type:** yes_no

**Explanation:** Current contact information enables rapid communication during security incidents.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 12.4: Supply Chain Security

#### Question 12.4.1

**Question:** Do you maintain Software Bill of Materials (SBOM) for your applications?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** SBOM provides visibility into software components and dependencies.

**Answer Options:**

**Option comprehensive_sbom:** Comprehensive SBOM

**Option partial_sbom:** Partial SBOM

**Option planning_to_implement:** Planning to implement

**Option no:** No SBOM


#### Question 12.4.2

**Question:** How do you verify software integrity?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Software integrity verification prevents tampering and ensures authenticity.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 12.4.3

**Question:** Do you assess open source component risks?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Open source risk assessment identifies potential security and compliance issues.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 12.4.4

**Question:** How do you handle SaaS application security?

**Type:** multiple_select

**Weight:** 3

**Explanation:** SaaS security assessment ensures third-party services meet security standards.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 12.4.5

**Question:** Do you monitor supply chain security threats?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Supply chain monitoring enables rapid response to emerging threats.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization




---

## Section 13: Security Awareness & Training

**Suggested Respondents:** Security Awareness Lead, HR Learning & Development

### Subsection 13.1: Security Awareness Program

#### Question 13.1.1

**Question:** Do you have a formal security awareness program?

**Type:** yes_no

**Explanation:** A formal program ensures consistent and comprehensive security awareness across the organization.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.1.2

**Question:** How often do you conduct security awareness training?

**Type:** multiple_choice

**Explanation:** Regular training keeps security awareness current with evolving threats.

**Answer Options:**

**Option monthly: Monthly**
*Basic Description:* Every month review cycle

**Option quarterly: Quarterly**
*Basic Description:* Every three months review

**Option annually: Annually**
*Basic Description:* Once per year review

**Option as_needed: As needed**
*Basic Description:* Event-driven reviews only

**Option never: Never**
*Basic Description:* No formal reviews


#### Question 13.1.3

**Question:** What topics are covered in your security awareness training?

**Type:** multiple_select

**Explanation:** Comprehensive topics ensure broad security awareness coverage.

**Answer Options:**
**Option phishing_and_social_engineering: Phishing and social engineering**
*Basic Description:* Recognizing and responding to phishing attacks

**Option password_security_and_mfa: Password security and MFA**
*Basic Description:* Strong passwords and multi-factor authentication

**Option data_handling_and_classification: Data handling and classification**
*Basic Description:* Proper handling of sensitive data

**Option device_and_endpoint_security: Device and endpoint security**
*Basic Description:* Securing laptops, mobile devices, and endpoints

**Option incident_reporting_procedures: Incident reporting procedures**
*Basic Description:* How to report security incidents

**Option acceptable_use_policies: Acceptable use policies**
*Basic Description:* Acceptable use of company resources

**Option remote_work_security: Remote work security**
*Basic Description:* Security practices for remote work

**Option third_party_and_supply_chain_risk: Third-party and supply chain risk**
*Basic Description:* Vendor and third-party security awareness

**Option secure_coding_practices: Secure coding practices**
*Basic Description:* Security best practices for developers

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 13.1.4

**Question:** How do you deliver security awareness training?

**Type:** multiple_select

**Explanation:** Multiple delivery methods accommodate different learning preferences and reinforce messages.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 13.1.5

**Question:** Do you track security awareness training completion?

**Type:** yes_no

**Explanation:** Tracking ensures all employees receive required security awareness training.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.1.6

**Question:** What is your target completion rate for security training?

**Type:** multiple_choice

**Explanation:** High completion rates ensure comprehensive security awareness across the organization.

**Answer Options:**

**Option 100:** 100%

**Option 95_99:** 95-99%

**Option 90_94:** 90-94%

**Option 80_89:** 80-89%

**Option no:** No target


#### Question 13.1.7

**Question:** Do you customize training content for different roles?

**Type:** yes_no

**Explanation:** Customized training addresses specific organizational risks and improves relevance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.1.8

**Question:** How often do you conduct phishing simulations?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Regular phishing simulations test and improve user awareness of social engineering attacks.

**Answer Options:**

**Option monthly:** Monthly

**Option quarterly:** Quarterly

**Option bi_annually:** Bi-annually

**Option annually:** Annually

**Option never:** Never


#### Question 13.1.9

**Question:** Do you conduct executive tabletop exercises?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Executive tabletop exercises prepare leadership for security incident response.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option bi_annually:** Bi-annually

**Option as_needed:** As needed

**Option never:** Never


#### Question 13.1.10

**Question:** How do you measure security culture maturity?

**Type:** multiple_select

**Weight:** 1

**Explanation:** Security culture measurement identifies areas for improvement in human security factors.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented




### Subsection 13.2: Phishing & Social Engineering

#### Question 13.2.1

**Question:** Do you conduct phishing simulation exercises?

**Type:** yes_no

**Explanation:** Phishing simulations test and improve employee ability to identify malicious emails.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.2.2

**Question:** How often do you run phishing simulations?

**Type:** multiple_choice

**Explanation:** Regular simulations maintain awareness and improve detection capabilities.

**Answer Options:**

**Option monthly:** Monthly

**Option quarterly:** Quarterly

**Option bi_annually:** Bi-annually

**Option annually:** Annually

**Option never:** Never


#### Question 13.2.3

**Question:** How do you handle employees who fail phishing tests?

**Type:** multiple_select

**Explanation:** Appropriate responses help improve individual security awareness without being punitive.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 13.2.4

**Question:** Do you provide social engineering awareness training?

**Type:** yes_no

**Explanation:** Social engineering training helps employees recognize and respond to manipulation attempts.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.2.5

**Question:** What is your current phishing simulation click rate?

**Type:** multiple_choice

**Explanation:** Low click rates indicate effective security awareness and training programs.

**Answer Options:**

**Option 0_4_9:** 0-4.9%

**Option 5_0_9_9:** 5.0-9.9%

**Option 10_20:** 10-20%

**Option 20:** >20%

**Option not_measured:** Not measured



### Subsection 13.3: Role-Based Training

#### Question 13.3.1

**Question:** Do you provide role-specific security training?

**Type:** yes_no

**Explanation:** Role-specific training addresses unique security responsibilities and risks for different positions.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.3.2

**Question:** What roles receive specialized security training?

**Type:** multiple_select

**Explanation:** Different roles face different security risks and require tailored training.

**Answer Options:**
**Option all_employees: All employees**
*Basic Description:* General security awareness for all staff

**Option privileged_it_administrators: Privileged IT administrators**
*Basic Description:* System and network administrators with elevated access

**Option developers_and_engineers: Developers and engineers**
*Basic Description:* Software developers and engineering teams

**Option executive_leadership: Executive leadership**
*Basic Description:* C-level executives and senior management

**Option contractors_and_temporary_staff: Contractors and temporary staff**
*Basic Description:* Non-employee workers with system access

**Option third_party_vendors: Third-party vendors**
*Basic Description:* External vendors with access to systems or data

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 13.3.3

**Question:** Do you provide security training for new employees?

**Type:** yes_no

**Explanation:** New employee training ensures security awareness from the start of employment.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.3.4

**Question:** How do you measure training effectiveness?

**Type:** multiple_select

**Explanation:** Effectiveness measurement helps improve training programs and demonstrate value.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 13.3.5

**Question:** Do you provide security training for contractors and vendors?

**Type:** yes_no

**Explanation:** Third-party training ensures consistent security practices across all personnel.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.3.6

**Question:** How do you handle security training for remote workers?

**Type:** multiple_select

**Explanation:** Remote workers face unique security challenges requiring tailored training approaches.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed




### Subsection 13.4: Training Management & Compliance

#### Question 13.4.1

**Question:** Do you maintain training records and certificates?

**Type:** yes_no

**Explanation:** Training records provide compliance evidence and track individual progress.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.4.2

**Question:** How do you handle training compliance requirements?

**Type:** multiple_select

**Explanation:** Compliance requirements drive training content and frequency decisions.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 13.4.3

**Question:** Do you have training renewal or refresher requirements?

**Type:** multiple_choice

**Explanation:** Regular refresher training maintains current security awareness.

**Answer Options:**

**Option annual:** Annual

**Option bi_annual:** Bi-annual

**Option based_on_role_changes:** Based on role changes

**Option as_needed:** As needed

**Option no:** No renewals


#### Question 13.4.4

**Question:** How do you budget for security training?

**Type:** multiple_choice

**Explanation:** Dedicated budgeting ensures consistent investment in security awareness.

**Answer Options:**

**Option dedicated_budget:** Dedicated budget

**Option part_of_it_budget:** Part of IT budget

**Option hr_budget:** HR budget

**Option ad_hoc_funding:** Ad-hoc funding

**Option no:** No specific budget


#### Question 13.4.5

**Question:** Do you use external training providers?

**Type:** multiple_choice

**Explanation:** External providers can offer specialized expertise and current threat intelligence.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 13.4.6

**Question:** How do you customize training for different audiences?

**Type:** multiple_select

**Explanation:** Customized training improves relevance and effectiveness for different user groups.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 13.4.7

**Question:** Do you integrate security training with onboarding?

**Type:** yes_no

**Explanation:** Onboarding integration ensures new employees receive security training from day one.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 13.4.8

**Question:** How do you communicate training requirements to employees?

**Type:** multiple_select

**Explanation:** Clear communication ensures employees understand training expectations and deadlines.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented




---

## Section 14: Physical Security

**Suggested Respondents:** Facilities Manager, Corporate Security

### Subsection 14.1: Facility Security

#### Question 14.1.1

**Question:** Do you have physical access controls for your facilities?

**Type:** yes_no

**Explanation:** Physical access controls prevent unauthorized entry to facilities and sensitive areas.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.1.2

**Question:** What types of physical access controls do you use?

**Type:** multiple_select

**Explanation:** Multiple access control methods provide layered physical security protection.

**Answer Options:**
**Option biometric: Biometric**
*Basic Description:* Fingerprint, facial recognition, etc.

**Option card_badge_access: Card/badge access**
*Basic Description:* RFID or magnetic stripe cards

**Option pin_password: PIN/password**
*Basic Description:* Numeric or alphanumeric codes

**Option multi_factor: Multi-factor**
*Basic Description:* Combination of multiple methods

**Option security_personnel: Security personnel**
*Basic Description:* Manned security checkpoints

**Option no: No formal controls**
*Basic Description:* No formal access control system



#### Question 14.1.3

**Question:** Do you have surveillance systems in place?

**Type:** multiple_select

**Explanation:** Surveillance systems provide detection and deterrence for physical security threats.

**Answer Options:**
**Option 24_7_monitoring: 24/7 monitoring**
*Basic Description:* Continuous surveillance monitoring

**Option recording_only: Recording only**
*Basic Description:* Cameras record but not actively monitored

**Option motion_activated: Motion-activated**
*Basic Description:* Cameras activate on motion detection

**Option limited_coverage: Limited coverage**
*Basic Description:* Partial surveillance coverage

**Option no: No surveillance**
*Basic Description:* No surveillance system



#### Question 14.1.4

**Question:** How do you manage visitor access?

**Type:** multiple_select

**Explanation:** Visitor management ensures unauthorized individuals cannot access sensitive areas.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 14.1.5

**Question:** Do you have secure areas for sensitive equipment?

**Type:** yes_no

**Explanation:** Secure areas protect critical infrastructure and sensitive equipment from unauthorized access.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.1.6

**Question:** How often do you review physical access logs?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular log reviews help detect unauthorized access attempts and security incidents.

**Answer Options:**

**Option quarterly:** Daily

**Option annually:** Weekly

**Option only_after_changes:** Monthly

**Option only_after_major_changes:** As needed

**Option as_needed:** Never



### Subsection 14.2: Environmental Controls

#### Question 14.2.1

**Question:** Do you have environmental monitoring systems?

**Type:** multiple_choice

**Explanation:** Environmental monitoring protects equipment and data from environmental threats.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 14.2.2

**Question:** Do you have backup power systems?

**Type:** multiple_choice

**Explanation:** Backup power ensures continued operations during power outages.

**Answer Options:**

**Option ups_systems:** UPS systems

**Option generators:** Generators

**Option battery_backup:** Battery backup

**Option multiple_power_sources:** Multiple power sources

**Option none:** None


#### Question 14.2.3

**Question:** How do you protect against fire hazards?

**Type:** multiple_select

**Explanation:** Fire protection systems prevent damage to equipment and data from fire incidents.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures



#### Question 14.2.4

**Question:** Do you have climate control systems?

**Type:** yes_no

**Explanation:** Climate control maintains optimal environmental conditions for equipment operation.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 14.3: Equipment Security

#### Question 14.3.1

**Question:** How do you secure workstations and laptops?

**Type:** multiple_select

**Explanation:** Equipment security prevents theft and unauthorized access to devices.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures



#### Question 14.3.2

**Question:** Do you have policies for equipment disposal?

**Type:** yes_no

**Explanation:** Secure disposal policies ensure sensitive data is properly destroyed when equipment is retired.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.3.3

**Question:** How do you handle mobile device security?

**Type:** multiple_select

**Explanation:** Mobile device security protects against data loss and unauthorized access.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 14.3.4

**Question:** Do you maintain an asset inventory?

**Type:** yes_no

**Explanation:** Asset inventory helps track and manage physical security of equipment and devices.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.3.5

**Question:** How do you secure server rooms and data centers?

**Type:** multiple_select

**Explanation:** Server room security protects critical infrastructure from physical threats.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures



#### Question 14.3.6

**Question:** Do you have equipment maintenance security procedures?

**Type:** yes_no

**Explanation:** Maintenance security procedures ensure equipment servicing doesn't compromise security.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.3.7

**Question:** How do you handle equipment loans and temporary access?

**Type:** multiple_select

**Explanation:** Equipment loan procedures prevent unauthorized use and ensure accountability.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 14.3.8

**Question:** Do you conduct physical security audits?

**Type:** multiple_choice

**Explanation:** Regular audits identify physical security gaps and improvement opportunities.

**Answer Options:**

**Option annually:** Annually

**Option bi_annually:** Bi-annually

**Option as_needed:** As needed

**Option never:** Never


#### Question 14.3.9

**Question:** How do you secure network equipment and cables?

**Type:** multiple_select

**Explanation:** Network infrastructure security prevents unauthorized access and tampering.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures



#### Question 14.3.10

**Question:** Do you have procedures for emergency equipment access?

**Type:** yes_no

**Explanation:** Emergency procedures ensure critical equipment remains accessible during crises.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.3.11

**Question:** How do you protect against electromagnetic interference?

**Type:** multiple_select

**Explanation:** EMI protection ensures equipment operates reliably and data remains secure.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures



#### Question 14.3.12

**Question:** Do you have clean desk and clear screen policies?

**Type:** yes_no

**Explanation:** Clean desk policies prevent unauthorized access to sensitive information.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.3.13

**Question:** How do you secure backup media and storage?

**Type:** multiple_select

**Explanation:** Backup media security ensures data recovery capabilities are protected.

**Answer Options:**
**Option daily: Daily**
*Basic Description:* Daily backup schedule

**Option weekly: Weekly**
*Basic Description:* Weekly backup schedule

**Option monthly: Monthly**
*Basic Description:* Monthly backup schedule

**Option real_time_continuous: Real-time/Continuous**
*Basic Description:* Continuous data protection

**Option no: No regular backups**
*Basic Description:* Backups not performed regularly



#### Question 14.3.14

**Question:** Do you have physical security incident response procedures?

**Type:** yes_no

**Explanation:** Physical incident procedures ensure appropriate response to security breaches.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 14.3.15

**Question:** How do you manage physical security during construction or renovation?

**Type:** multiple_select

**Explanation:** Construction security prevents unauthorized access during facility changes.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 14.3.16

**Question:** Do you conduct physical penetration testing?

**Type:** multiple_choice

**Explanation:** Physical penetration testing validates the effectiveness of physical security controls.

**Answer Options:**

**Option annually:** Annually

**Option bi_annually:** Bi-annually

**Option as_needed:** As needed

**Option never:** Never



---

## Section 15: Monitoring & Detection


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown
**Suggested Respondents:** SOC Lead, Security Analyst

### Subsection 15.1: Security Monitoring

#### Question 15.1.1

**Question:** Do you have a Security Operations Center (SOC)?

**Type:** yes_no

**Explanation:** A SOC provides centralized security monitoring and incident response capabilities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 15.1.2

**Question:** What security monitoring tools do you use?

**Type:** multiple_select

**Explanation:** Multiple monitoring tools provide comprehensive visibility into security events.

**Answer Options:**
**Option commercial_solution: Commercial solution**
*Basic Description:* Vendor-provided commercial product

**Option open_source_solution: Open-source solution**
*Basic Description:* Open-source tools and platforms

**Option custom_built_solution: Custom-built solution**
*Basic Description:* Internally developed solution

**Option managed_service: Managed service**
*Basic Description:* Third-party managed service

**Option not_deployed: Not deployed**
*Basic Description:* Not currently deployed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.1.3

**Question:** Do you have 24/7 security monitoring?

**Type:** yes_no

**Explanation:** Continuous monitoring ensures threats are detected regardless of when they occur.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 15.1.4

**Question:** How do you correlate security events?

**Type:** multiple_choice

**Explanation:** Event correlation helps identify complex attack patterns and reduce false positives.

**Answer Options:**

**Option automated_correlation:** Automated correlation

**Option manual_analysis:** Manual analysis

**Option hybrid_approach:** Hybrid approach

**Option no:** No correlation

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.1.5

**Question:** What is your mean time to detect (MTTD) security incidents?

**Type:** multiple_choice

**Explanation:** Faster detection reduces the impact and spread of security incidents.

**Answer Options:**

**Option 1_hour:** < 1 hour

**Option 1_4_hours:** 1-4 hours

**Option 4_24_hours:** 4-24 hours

**Option 24_hours:** > 24 hours

**Option not_measured:** Not measured

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.1.6

**Question:** Do you monitor user behavior for anomalies?

**Type:** yes_no

**Explanation:** User behavior analytics help detect insider threats and compromised accounts.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 15.1.7

**Question:** How do you handle security alerts?

**Type:** multiple_select

**Explanation:** Effective alert handling ensures timely response to genuine security threats.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 15.2: Threat Detection

#### Question 15.2.1

**Question:** Do you use threat intelligence feeds?

**Type:** yes_no

**Explanation:** Threat intelligence helps identify known threats and attack patterns.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 15.2.2

**Question:** What types of threat detection do you implement?

**Type:** multiple_select

**Explanation:** Multiple detection methods improve coverage against different types of threats.

**Answer Options:**
**Option type_a: Type A**
*Basic Description:* Primary implementation type

**Option type_b: Type B**
*Basic Description:* Secondary implementation type

**Option type_c: Type C**
*Basic Description:* Alternative implementation type

**Option hybrid: Hybrid**
*Basic Description:* Combination of multiple types

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.2.3

**Question:** Do you conduct proactive threat hunting?

**Type:** multiple_choice

**Explanation:** Threat hunting proactively identifies threats that may have evaded automated detection.

**Answer Options:**

**Option regularly:** Regularly

**Option occasionally:** Occasionally

**Option after_incidents:** After incidents

**Option never:** Never


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown

#### Question 15.2.4

**Question:** How do you detect advanced persistent threats (APTs)?

**Type:** multiple_select

**Explanation:** APT detection requires sophisticated monitoring and analysis capabilities.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.2.5

**Question:** Do you monitor for insider threats?

**Type:** yes_no

**Explanation:** Insider threat monitoring helps detect malicious or negligent employee activities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 15.2.6

**Question:** How do you validate threat detection effectiveness?

**Type:** multiple_select

**Explanation:** Validation ensures detection capabilities are working effectively against real threats.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 15.3: Log Management

#### Question 15.3.1

**Question:** Do you have centralized log management?

**Type:** yes_no

**Explanation:** Centralized logging provides comprehensive visibility and easier analysis of security events.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 15.3.2

**Question:** What types of logs do you collect?

**Type:** multiple_select

**Explanation:** Comprehensive log collection provides better visibility into security events.

**Answer Options:**
**Option type_a: Type A**
*Basic Description:* Primary implementation type

**Option type_b: Type B**
*Basic Description:* Secondary implementation type

**Option type_c: Type C**
*Basic Description:* Alternative implementation type

**Option hybrid: Hybrid**
*Basic Description:* Combination of multiple types

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.3.3

**Question:** How long do you retain security logs?

**Type:** multiple_choice

**Explanation:** Adequate log retention supports incident investigation and compliance requirements.

**Answer Options:**

**Option 30_days:** 30 days

**Option 90_days:** 90 days

**Option 6_months:** 6 months

**Option 1_year:** 1 year

**Option 1_year_5:** > 1 year

**Option varies_by_log_type:** Varies by log type

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.3.4

**Question:** Do you protect log integrity?

**Type:** multiple_choice

**Explanation:** Log integrity protection ensures logs cannot be tampered with by attackers.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.3.5

**Question:** How do you analyze security logs?

**Type:** multiple_select

**Explanation:** Effective log analysis helps identify security incidents and trends.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 15.3.6

**Question:** Do you have log monitoring alerts?

**Type:** yes_no

**Explanation:** Log monitoring alerts provide real-time notification of security events.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



---

## Section 16: Vulnerability Management

**Suggested Respondents:** Vulnerability Management Lead, Patch Coordinator

### Subsection 16.1: Vulnerability Assessment

#### Question 16.1.1

**Question:** Do you conduct regular vulnerability assessments?

**Type:** yes_no

**Explanation:** Regular vulnerability assessments help identify security weaknesses before they can be exploited.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.1.2

**Question:** How often do you perform vulnerability scans?

**Type:** multiple_choice


**Scale:** frequency_monitoring
**Explanation:** Frequent scanning ensures vulnerabilities are identified quickly as they emerge.

**Answer Options:**

**Option continuously:** Daily

**Option daily:** Weekly

**Option weekly:** Monthly

**Option monthly:** Quarterly

**Option quarterly:** Annually

**Option only_when_issues:** Never

**Option not_monitored: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.1.3

**Question:** What types of vulnerability assessments do you perform?

**Type:** multiple_select

**Explanation:** Comprehensive assessments cover all potential attack vectors and system types.

**Answer Options:**
**Option type_a: Type A**
*Basic Description:* Primary implementation type

**Option type_b: Type B**
*Basic Description:* Secondary implementation type

**Option type_c: Type C**
*Basic Description:* Alternative implementation type

**Option hybrid: Hybrid**
*Basic Description:* Combination of multiple types

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.1.4

**Question:** Do you use automated vulnerability scanning tools?

**Type:** yes_no

**Explanation:** Automated tools provide consistent and scalable vulnerability detection capabilities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.1.5

**Question:** Do you conduct manual penetration testing?

**Type:** multiple_choice

**Explanation:** Manual testing identifies complex vulnerabilities that automated tools might miss.

**Answer Options:**

**Option regularly:** Regularly

**Option annually:** Annually

**Option occasionally:** Occasionally

**Option never:** Never

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.1.6

**Question:** How do you validate vulnerability scan results?

**Type:** multiple_select

**Explanation:** Validation ensures scan results are accurate and actionable.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.1.7

**Question:** Do you scan for vulnerabilities in third-party components?

**Type:** yes_no

**Explanation:** Third-party component scanning identifies vulnerabilities in dependencies and libraries.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 16.2: Vulnerability Management Process

#### Question 16.2.1

**Question:** Do you have a formal vulnerability management process?

**Type:** yes_no

**Explanation:** A formal process ensures consistent and effective vulnerability handling.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.2.2

**Question:** How do you prioritize vulnerabilities for remediation?

**Type:** multiple_select

**Explanation:** Effective prioritization ensures critical vulnerabilities are addressed first.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.2.3

**Question:** What are your target remediation timeframes?

**Type:** multiple_choice

**Explanation:** Defined timeframes ensure timely vulnerability remediation based on risk levels.

**Answer Options:**

**Option critical_24h_high_7d_medium_30d:** Critical: 24h, High: 7d, Medium: 30d

**Option critical_72h_high_14d_medium_60d:** Critical: 72h, High: 14d, Medium: 60d

**Option critical_7d_high_30d_medium_90d:** Critical: 7d, High: 30d, Medium: 90d

**Option no:** No defined timeframes


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown

#### Question 16.2.4

**Question:** How do you track vulnerability remediation progress?

**Type:** multiple_select

**Explanation:** Progress tracking ensures vulnerabilities are remediated within target timeframes.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.2.5

**Question:** Do you have a vulnerability disclosure process?

**Type:** yes_no

**Explanation:** A disclosure process provides a channel for external researchers to report vulnerabilities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.2.6

**Question:** How do you handle zero-day vulnerabilities?

**Type:** multiple_select

**Explanation:** Zero-day handling requires rapid response and alternative protection measures.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


### Subsection 16.3: Patch Management

#### Question 16.3.1

**Question:** Do you have a formal patch management process?

**Type:** yes_no

**Weight:** 5

**Explanation:** Formal patch management ensures systematic and timely application of security updates.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.3.2

**Question:** How do you prioritize security patches?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Patch prioritization ensures critical vulnerabilities are addressed first.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.3.3

**Question:** What is your target timeframe for critical patches?

**Type:** multiple_choice

**Weight:** 5

**Explanation:** Rapid patching of critical vulnerabilities reduces exposure to attacks.

**Answer Options:**

**Option within_24_hours:** Within 24 hours

**Option within_72_hours:** Within 72 hours

**Option within_1_week:** Within 1 week

**Option within_1_month:** Within 1 month

**Option no:** No defined timeline

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.3.4

**Question:** How do you test patches before deployment?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Patch testing prevents deployment issues while maintaining security.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.3.5

**Question:** Do you have automated patch deployment capabilities?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Automation enables faster and more consistent patch deployment.

**Answer Options:**

**Option fully_automated:** Fully automated

**Option semi_automated:** Semi-automated

**Option manual_only:** Manual only

**Option varies_by_system_type:** Varies by system type

**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.3.6

**Question:** How do you track patch deployment status?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Deployment tracking ensures patches are successfully applied across all systems.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.3.7

**Question:** How do you handle patch rollback procedures?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Rollback procedures enable quick recovery from problematic patches.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_sure: Not sure**
*Basic Description:* Unclear or unknown


#### Question 16.3.8

**Question:** Do you have an emergency patching process?

**Type:** yes_no

**Weight:** 5

**Explanation:** Emergency processes enable rapid response to zero-day vulnerabilities and active exploits.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.3.9

**Question:** Do you maintain patch compliance reporting?

**Type:** yes_no

**Weight:** 1

**Explanation:** Compliance reporting provides visibility into patch status across the environment.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 16.3.10

**Question:** How do you handle end-of-life systems that cannot be patched?

**Type:** multiple_select

**Weight:** 3

**Explanation:** End-of-life systems require alternative security measures when patching is not possible.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed




---

## Section 17: Compliance & Audit

**Suggested Respondents:** Compliance Lead, Internal Audit

### Subsection 17.1: Regulatory Compliance

#### Question 17.1.1

**Question:** Which regulatory frameworks apply to your organization?

**Type:** multiple_select

**Explanation:** Understanding applicable regulations is essential for compliance planning and implementation.

**Answer Options:**
**Option gdpr: GDPR**
*Basic Description:* General Data Protection Regulation

**Option hipaa: HIPAA**
*Basic Description:* Health Insurance Portability and Accountability Act

**Option pci_dss: PCI DSS**
*Basic Description:* Payment Card Industry Data Security Standard

**Option soc_2: SOC 2**
*Basic Description:* Service Organization Control 2

**Option iso_27001: ISO 27001**
*Basic Description:* International Organization for Standardization 27001

**Option nist_csf: NIST CSF**
*Basic Description:* NIST Cybersecurity Framework

**Option not_applicable: Not applicable**
*Basic Description:* No specific compliance requirements



#### Question 17.1.2

**Question:** Do you have a compliance management program?

**Type:** yes_no

**Explanation:** A formal compliance program ensures systematic adherence to regulatory requirements.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 17.1.3

**Question:** How do you track compliance status?

**Type:** multiple_select

**Explanation:** Effective tracking ensures ongoing compliance and identifies gaps before they become violations.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 17.1.4

**Question:** Do you conduct regular compliance assessments?

**Type:** multiple_choice

**Explanation:** Regular assessments help maintain compliance and identify areas for improvement.

**Answer Options:**

**Option monthly:** Monthly

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option bi_annually:** Bi-annually

**Option as_required:** As required

**Option never:** Never


#### Question 17.1.5

**Question:** How do you handle compliance violations?

**Type:** multiple_select

**Explanation:** Structured violation handling ensures proper response and prevents recurrence.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 17.1.6

**Question:** Do you maintain compliance documentation?

**Type:** yes_no

**Explanation:** Proper documentation demonstrates compliance efforts and supports audit activities.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 17.1.7

**Question:** How do you stay updated on regulatory changes?

**Type:** multiple_select

**Explanation:** Staying current with regulatory changes ensures ongoing compliance as requirements evolve.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented




### Subsection 17.2: Internal Audits

#### Question 17.2.1

**Question:** Do you conduct internal security audits?

**Type:** yes_no

**Explanation:** Internal audits provide independent assessment of security controls and compliance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 17.2.2

**Question:** How often do you perform internal security audits?

**Type:** multiple_choice


**Scale:** frequency_review
**Explanation:** Regular internal audits help identify issues before external audits or incidents occur.

**Answer Options:**

**Option quarterly:** Quarterly

**Option annually:** Annually

**Option only_after_changes:** Bi-annually

**Option only_after_major_changes:** As needed

**Option as_needed:** Never


#### Question 17.2.3

**Question:** What areas do your internal audits cover?

**Type:** multiple_select

**Explanation:** Comprehensive audit coverage ensures all critical security areas are evaluated.

**Answer Options:**
**Option option_1: Option 1**
*Basic Description:* First option

**Option option_2: Option 2**
*Basic Description:* Second option

**Option option_3: Option 3**
*Basic Description:* Third option

**Option option_4: Option 4**
*Basic Description:* Fourth option

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 17.2.4

**Question:** Who conducts your internal security audits?

**Type:** multiple_choice

**Explanation:** Independent audit teams provide objective assessment of security controls.

**Answer Options:**

**Option internal_audit_team:** Internal audit team

**Option it_security_team:** IT security team

**Option external_consultants:** External consultants

**Option mixed_approach:** Mixed approach

**Option no:** No audits conducted


#### Question 17.2.5

**Question:** How do you track audit findings and remediation?

**Type:** multiple_select

**Explanation:** Systematic tracking ensures audit findings are properly addressed and resolved.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 17.2.6

**Question:** Do you have audit finding escalation procedures?

**Type:** yes_no

**Explanation:** Escalation procedures ensure critical findings receive appropriate management attention.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 17.3: External Audits & Certifications

#### Question 17.3.1

**Question:** Do you undergo external security audits?

**Type:** yes_no

**Explanation:** External audits provide independent validation of security controls and compliance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 17.3.2

**Question:** What types of external audits do you participate in?

**Type:** multiple_select

**Explanation:** Different audit types serve various compliance and business requirements.

**Answer Options:**
**Option type_a: Type A**
*Basic Description:* Primary implementation type

**Option type_b: Type B**
*Basic Description:* Secondary implementation type

**Option type_c: Type C**
*Basic Description:* Alternative implementation type

**Option hybrid: Hybrid**
*Basic Description:* Combination of multiple types

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 17.3.3

**Question:** How do you prepare for external audits?

**Type:** multiple_select

**Explanation:** Proper preparation increases audit success and reduces findings.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented



#### Question 17.3.4

**Question:** Do you maintain security certifications?

**Type:** multiple_choice

**Explanation:** Security certifications demonstrate commitment to security best practices.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 17.3.5

**Question:** How do you manage audit evidence collection?

**Type:** multiple_select

**Explanation:** Efficient evidence collection streamlines audit processes and reduces burden.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed



#### Question 17.3.6

**Question:** Do you conduct management reviews of audit results?

**Type:** yes_no

**Explanation:** Management review ensures audit findings receive appropriate attention and resources for remediation.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 17.3.7

**Question:** How do you communicate audit results to stakeholders?

**Type:** multiple_select

**Explanation:** Effective communication ensures stakeholders understand audit outcomes and required actions.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented




---

## Section 18: OT/ICS & IoT Security


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization
**Suggested Respondents:** OT Security Lead, Industrial Control Systems Engineer

### Subsection 18.1: Operational Technology Security

#### Question 18.1.1

**Question:** Do you have operational technology (OT) or industrial control systems (ICS)?

**Type:** yes_no

**Weight:** 1

**Explanation:** OT/ICS systems require specialized security approaches due to safety and availability requirements.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 18.1.2

**Question:** How do you segment OT networks from IT networks?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Network segmentation protects critical OT systems from IT-based attacks.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 18.1.3

**Question:** Do you conduct safety impact analysis for security changes?

**Type:** yes_no

**Weight:** 5

**Explanation:** Safety impact analysis ensures security measures don't compromise operational safety.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 18.1.4

**Question:** How do you handle OT system patching?

**Type:** multiple_select

**Weight:** 3

**Explanation:** OT patching requires careful coordination to maintain system availability and safety.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 18.1.5

**Question:** Do you monitor OT network traffic?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** OT network monitoring helps detect anomalies and potential security incidents.

**Answer Options:**

**Option continuous_monitoring:** Continuous monitoring

**Option periodic_monitoring:** Periodic monitoring

**Option passive_monitoring_only:** Passive monitoring only

**Option no:** No monitoring

**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 18.1.6

**Question:** Do you have OT-specific incident response procedures?

**Type:** yes_no

**Weight:** 3

**Explanation:** OT incident response requires specialized procedures considering safety and operational impact.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*



### Subsection 18.2: IoT Device Security

#### Question 18.2.1

**Question:** Do you have IoT devices in your environment?

**Type:** yes_no

**Weight:** 1

**Explanation:** IoT devices introduce unique security challenges requiring specialized management.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 18.2.2

**Question:** How do you secure IoT device communications?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Secure communications protect IoT data and prevent unauthorized access.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 18.2.3

**Question:** Do you maintain an inventory of IoT devices?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** IoT device inventory enables proper security management and risk assessment.

**Answer Options:**

**Option comprehensive_inventory:** Comprehensive inventory

**Option partial_inventory:** Partial inventory

**Option manual_tracking:** Manual tracking

**Option no:** No inventory

**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 18.2.4

**Question:** How do you manage IoT device firmware updates?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Regular firmware updates address security vulnerabilities in IoT devices.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option third_party_managed: Third-party managed**
*Basic Description:* Outsourced to service provider

**Option informal_process: Informal process**
*Basic Description:* Ad-hoc handling without formal procedures

**Option not_currently_managed: Not currently managed**
*Basic Description:* Not currently managed


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 18.2.5

**Question:** Do you monitor IoT device behavior?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** IoT monitoring helps detect compromised devices and unusual behavior.

**Answer Options:**

**Option continuous_monitoring:** Continuous monitoring

**Option periodic_monitoring:** Periodic monitoring

**Option anomaly_detection:** Anomaly detection

**Option no:** No monitoring



---

## Section 19: AI/ML & Machine Learning Security


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization
**Suggested Respondents:** AI/ML Security Lead, Data Science Lead

### Subsection 19.1: Model Security & Governance

#### Question 19.1.1

**Question:** Do you have AI/ML models in production?

**Type:** yes_no

**Weight:** 1

**Explanation:** AI/ML models in production require specialized security controls and governance.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*


#### Question 19.1.2

**Question:** Do you maintain a model registry with security controls?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Model registries provide centralized governance and security for ML artifacts.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 19.1.3

**Question:** How do you ensure model provenance and lineage?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Model provenance ensures traceability and helps identify security risks in the ML pipeline.

**Answer Options:**
**Option formal_documented_process: Formal documented process**
*Basic Description:* Documented procedures and workflows

**Option automated_system: Automated system**
*Basic Description:* Using automation tools or platforms

**Option manual_process: Manual process**
*Basic Description:* Manual handling and tracking

**Option not_currently_implemented: Not currently implemented**
*Basic Description:* Not currently implemented


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 19.1.4

**Question:** Do you conduct adversarial testing on ML models?

**Type:** multiple_choice

**Weight:** 5

**Explanation:** Adversarial testing identifies vulnerabilities to malicious inputs and model attacks.

**Answer Options:**

**Option regular_testing:** Regular testing

**Option occasional_testing:** Occasional testing

**Option only_for_critical_models:** Only for critical models

**Option no:** No testing

**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 19.1.5

**Question:** How do you protect against data poisoning attacks?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Data poisoning protection prevents malicious manipulation of training data.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 19.1.6

**Question:** Do you implement model explainability and bias detection?

**Type:** multiple_choice

**Weight:** 3

**Explanation:** Explainability and bias detection ensure responsible and secure AI deployment.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization




### Subsection 19.2: ML Pipeline Security

#### Question 19.2.1

**Question:** How do you secure your ML training pipeline?

**Type:** multiple_select

**Weight:** 5

**Explanation:** ML pipeline security prevents unauthorized access and resource abuse.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 19.2.2

**Question:** Do you protect feature stores and data privacy?

**Type:** multiple_choice

**Weight:** 5

**Explanation:** Feature store security protects sensitive data used in ML model training and inference.

**Answer Options:**
**Option fully_implemented: Fully implemented**
*Basic Description:* Fully implemented and operational

**Option partially_implemented: Partially implemented**
*Basic Description:* Partially implemented or in progress

**Option planned: Planned**
*Basic Description:* Planned but not yet implemented

**Option not_implemented: Not implemented**
*Basic Description:* Not currently implemented

**Option not_applicable: Not applicable**
*Basic Description:* Not applicable to our organization



#### Question 19.2.3

**Question:** How do you secure model inference endpoints?

**Type:** multiple_select

**Weight:** 5

**Explanation:** Inference endpoint security prevents abuse and protects model intellectual property.

**Answer Options:**
**Option encryption: Encryption**
*Basic Description:* Data encryption at rest and in transit

**Option access_controls: Access controls**
*Basic Description:* Role-based access control and authentication

**Option network_segmentation: Network segmentation**
*Basic Description:* Isolated network zones

**Option monitoring_and_logging: Monitoring and logging**
*Basic Description:* Continuous monitoring and audit logs

**Option security_policies: Security policies**
*Basic Description:* Documented security policies and procedures

**Option not_currently_secured: Not currently secured**
*Basic Description:* No specific security measures


**Option not_applicable: Not applicable**
*Basic Description:* Does not apply to our organization


#### Question 19.2.4

**Question:** Do you monitor for model drift and anomalies?

**Type:** multiple_select

**Weight:** 3

**Explanation:** Model monitoring detects degradation and potential security issues in production.

**Answer Options:**
**Option yes: Yes** - This security control/practice is implemented in your organization
**Option no: No** - This security control/practice is not currently implemented
*Note: If you select 'No', consider this an opportunity for security improvement.*

---
