CREATE OR REPLACE FUNCTION check_username_terdaftar() 
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pengguna WHERE username = NEW.username
    ) THEN
        RAISE EXCEPTION 'Username sudah terdaftar di sistem.';
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER before_pengguna_daftar
BEFORE INSERT ON pengguna
FOR EACH ROW
EXECUTE FUNCTION check_username_terdaftar();

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
