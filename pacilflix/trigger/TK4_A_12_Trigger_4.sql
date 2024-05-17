CREATE OR REPLACE FUNCTION check_timestamp_terunduh() RETURNS TRIGGER AS
$$
    BEGIN
        IF OLD.timestamp > CURRENT_TIMESTAMP - INTERVAL '1 day' THEN
        RAISE EXCEPTION 'Tayangan minimal harus berada di daftar unduhan selama 1 hari agar bisa dihapus.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_delete_tayangan_terunduh
BEFORE DELETE ON TAYANGAN_TERUNDUH
FOR EACH ROW
EXECUTE FUNCTION check_timestamp_terunduh();