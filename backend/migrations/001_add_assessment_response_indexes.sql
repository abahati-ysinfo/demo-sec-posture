
CREATE INDEX IF NOT EXISTS idx_assessment_responses_assessment_question 
ON assessment_responses(assessment_id, question_id);

CREATE INDEX IF NOT EXISTS idx_assessment_responses_assessment_id 
ON assessment_responses(assessment_id);

CREATE INDEX IF NOT EXISTS idx_assessment_responses_updated_at 
ON assessment_responses(updated_at);

SELECT 
    tablename, 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'assessment_responses' 
ORDER BY indexname;
