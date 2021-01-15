package com.example.smartgrove;

import android.provider.AlarmClock;
import android.provider.MediaStore;

import java.util.ArrayList;
import java.util.HashMap;


public class Almacen {

    // Guardamos en un hashmap para evitar repetidos
    // No pueden haber dos muestras con misma fecha
    HashMap<String,Muestra> almacen;

    public Almacen(){
        this.almacen=new HashMap<String, Muestra>();
    }

    public Almacen(HashMap<String, Muestra> otroAlmacen) {
        this.almacen = otroAlmacen;

    }

    // Añade la muestra al almacen
    public void addMuestra(Muestra muestra){
        this.almacen.put(muestra.getFecha().toString(),muestra);
    }

    // Elimina una mustra por su clave "fecha"
    public void removeMuestra(String fecha){
        this.almacen.remove(fecha);
    }

    // Borra el almacen completamente
    public void borrarAlmacen(){
        this.almacen.clear();
    }

    // Devuelve una lista con todas las muestras en el almacen
    public ArrayList<Muestra> getMuestras(){
        ArrayList<Muestra> array=new ArrayList<Muestra>();
        for(String fecha:almacen.keySet()){
            array.add(almacen.get(fecha));
        }
        return array;
    }

}
