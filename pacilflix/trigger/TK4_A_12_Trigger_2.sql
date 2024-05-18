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