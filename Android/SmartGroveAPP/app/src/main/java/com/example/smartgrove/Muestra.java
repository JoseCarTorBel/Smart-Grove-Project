package com.example.smartgrove;

public class Muestra {

    private String fecha;
    private int temperatura;
    private int humedad;

    public Muestra(String fecha, int temperatura, int humedad) {
        this.fecha = fecha;
        this.temperatura = temperatura;
        this.humedad = humedad;
    }

    public String getFecha() {
        return fecha;
    }

    public void setFecha(String fecha) {
        this.fecha = fecha;
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
