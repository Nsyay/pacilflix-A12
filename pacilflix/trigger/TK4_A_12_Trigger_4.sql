CREATE OR REPLACE FUNCTION cek_paket()
RETURNS TRIGGER AS $$
DECLARE
    paket_aktif RECORD;
BEGIN
    SELECT * INTO paket_aktif
    FROM TRANSACTION
    WHERE username = NEW.username AND end_date_time >= CURRENT_DATE
    ORDER BY end_date_time DESC
    LIMIT 1;

    IF paket_aktif IS NOT NULL THEN
        UPDATE TRANSACTION
        SET end_date_time = NEW.end_date_time,
            nama_paket = NEW.nama_paket,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = NEW.timestamp_pembayaran
        WHERE username = NEW.username AND start_date_time = paket_aktif.start_date_time;
        RETURN NULL;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER aktivasi_paket
BEFORE INSERT ON TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION cek_paket();
