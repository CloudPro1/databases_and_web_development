CREATE DEFINER=`root`@`localhost` PROCEDURE `driver_salary_report`(r_month int, r_year int)
BEGIN
	
	DECLARE done INT DEFAULT 0;
    DECLARE cursor_dr_id INT;
    DECLARE cursor_workhours_sum INT;
    DECLARE cursor_dr_name VARCHAR(45);
    
	DECLARE sr_cursor CURSOR FOR 
		SELECT s.dr_id, SUM(TIMESTAMPDIFF(HOUR, work_start, work_finish)) as workhours_sum, d.name
		FROM schedule s JOIN drivers d ON s.dr_id = d.dr_id
		WHERE YEAR(s.date_of_workday)=r_year AND MONTH(s.date_of_workday)=r_month
        GROUP BY s.dr_id, d.name
        ORDER BY d.name ASC;
    
	DECLARE continue HANDLER FOR NOT FOUND SET done = 1;
    
	IF NOT EXISTS (
		SELECT 1 FROM salary_report 
		WHERE sr_year=r_year AND sr_month=r_month  
	) THEN
		OPEN sr_cursor;
		FETCH sr_cursor INTO cursor_dr_id, cursor_workhours_sum, cursor_dr_name;
		WHILE done=0 DO
			INSERT INTO salary_report
			VALUES (NULL, cursor_dr_name, cursor_dr_id, r_year, r_month, cursor_workhours_sum);
			FETCH sr_cursor INTO cursor_dr_id, cursor_workhours_sum, cursor_dr_name;
		END WHILE;
		CLOSE sr_cursor;
		SELECT 'Отчёт успешно создан' AS message;
    ELSE
        SELECT "Такой отчёт уже существует" AS err_message;
END IF;
END
