-- Example SQL for healthcare data practice

-- Patient summary with lab counts
SELECT p.PatientID, p.Age, p.DiagnosisName,
       COUNT(l.LabTestName) AS lab_count,
       AVG(l.TestResultValue) AS avg_result
FROM patients p
LEFT JOIN labs l ON p.PatientID = l.PatientID
GROUP BY p.PatientID, p.Age, p.DiagnosisName;

-- Data quality check query
SELECT HospitalSite,
       COUNT(*) AS total_patients,
       SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS missing_age,
       SUM(CASE WHEN DischargeDate < AdmissionDate THEN 1 ELSE 0 END) AS invalid_dates
FROM patients
GROUP BY HospitalSite;
