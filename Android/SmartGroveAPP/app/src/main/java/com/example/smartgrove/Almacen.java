package com.example.smartgrove;

import android.provider.AlarmClock;
import android.provider.MediaStore;

import java.util.ArrayList;
import java.util.HashMap;

public class Almacen {

    HashMap<String,Muestra> almacen;

    public Almacen(){
        this.almacen=new HashMap<String, Muestra>();
    }

    public Almacen(HashMap<String, Muestra> otroAlmacen) {
        this.almacen = otroAlmacen;

    }

    public void addMuestra(Muestra muestra){
        this.almacen.put(muestra.getFecha(),muestra);
    }

    public void removeMuestra(String fecha){
        this.almacen.remove(fecha);
    }

    public void borrarAlmacen(){
        this.almacen.clear();
    }

    public ArrayList<Muestra> getMuestras(){
        ArrayList<Muestra> array=new ArrayList<Muestra>();
        for(String fecha:almacen.keySet()){
            array.add(almacen.get(fecha));
        }
        return array;
    }


    //TODO metodos que te dem muestra en un intervalo de fechas
    //TODO en MUESTRA convertir fecha (string) a datatime





}
