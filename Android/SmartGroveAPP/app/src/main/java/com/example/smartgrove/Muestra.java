package com.example.smartgrove;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Muestra {

    // Usamos el formateador para obtener la fecha
    SimpleDateFormat formatter=new SimpleDateFormat("yyyy-MM-dd");
    private Date fecha;
    private int temperatura;
    private int humedad;

    public Muestra(String fecha, int temperatura, int humedad) throws ParseException {
        this.fecha = formatter.parse(fecha);
        this.temperatura = temperatura;
        this.humedad = humedad;
    }

    public Date getFecha() {
        return fecha;
    }

    public void setFecha(String fecha) throws ParseException {
        formatter.parse(fecha);
    }

    public int getTemperatura() {
        return temperatura;
    }

    public void setTemperatura(int temperatura) {
        this.temperatura = temperatura;
    }

    public int getHumedad() {
        return humedad;
    }

    public void setHumedad(int humedad) {
        this.humedad = humedad;
    }


}
