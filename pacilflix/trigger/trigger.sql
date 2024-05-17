/*trigger cek username duplicate*/
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

/*trigger timestamp terunduh kurang dari 1 hari*/
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

/*trigger ulasan tidak bisa dibuat lebih dari satu kali oleh user yang sama*/
CREATE OR REPLACE FUNCTION cek_ulasan_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM ULASAN WHERE id_tayangan = NEW.id_tayangan AND username = NEW.username) THEN
        RAISE EXCEPTION 'Anda sudah memberikan ulasan untuk tayangan ini sebelumnya.';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_cek_ulasan_duplicate
BEFORE INSERT ON ULASAN
FOR EACH ROW
EXECUTE FUNCTION cek_ulasan_duplicate();