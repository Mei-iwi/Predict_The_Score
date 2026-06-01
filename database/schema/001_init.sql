CREATE TABLE IF NOT EXISTS PredictionHistory (
    -- Lưu lịch sử dự đoán để frontend có thể hiển thị lại các lần nhập gần nhất.
    Id BIGINT PRIMARY KEY AUTO_INCREMENT,
    StudentName VARCHAR(150) NULL,
    ClassName VARCHAR(50) NULL,
    StudyTime INT NOT NULL,
    Failures INT NOT NULL,
    Absences INT NOT NULL,
    SchoolSup TINYINT NOT NULL,
    FamSup TINYINT NOT NULL,
    Internet TINYINT NOT NULL,
    Scenario VARCHAR(50) NULL,
    Note TEXT NULL,
    PredictedScore DECIMAL(5,2) NOT NULL,
    PredictedScore10 DECIMAL(5,2) NOT NULL,
    ModelName VARCHAR(100) NOT NULL,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
