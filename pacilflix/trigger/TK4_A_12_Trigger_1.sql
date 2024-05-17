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