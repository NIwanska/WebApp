-- Active: 1718634278776@@127.0.0.1@5432@app_db@public
DROP PROCEDURE IF EXISTS product_reports;


CREATE OR REPLACE PROCEDURE product_reports (
    p_product_id INTEGER,
    p_month VARCHAR,
    p_year INTEGER,
    p_count INTEGER,
    p_total DOUBLE PRECISION
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    v_count INTEGER;
    v_total INTEGER;
BEGIN

    -- INSERT INTO product_monthly_reports (id, product_item_id, month, year, count, total)
    --     VALUES (DEFAULT, p_product_id, p_month, p_year, p_count, p_total);

    SELECT id, count, total
    INTO v_id, v_count, v_total
    FROM product_monthly_reports
    WHERE product_item_id = p_product_id AND month = p_month AND year = p_year
    ORDER BY year, month DESC
    LIMIT 1;

    IF v_id IS NULL THEN
        INSERT INTO product_monthly_reports (id, product_item_id, month, year, count, total)
        VALUES (DEFAULT, p_product_id, p_month, p_year, p_count, p_total);
    ELSE
        UPDATE product_monthly_reports
        SET count = v_count+p_count, total=v_total+p_total
        WHERE id = v_id;
    END IF;
END;
$$;
