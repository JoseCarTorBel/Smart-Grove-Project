package com.example.smartgrove;

import android.graphics;
import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    String urlGoogle = "https://script.googleusercontent.com/macros/echo?user_content_key=hfautCUoMpL7vTfTZKvbL3tP2Kbnt12m-G4bYscxlI_V81lEcHYLi440z9Gwv0fP65Xs_1Honef3-N-r-I47Skg6RWzFXbZ4m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBFiRF860KCpoZ4E0XPSsTar_QXW9Bz817n-n-h8NY7IYJnhzk8SktW1HxiHj3sYOiannw6BiFb7&lib=MaI25Xl4VUYQKa9FPNAK_RnOWC6KqnnsA";
    TextView recibido;
    Button descargar;
    RequestQueue requestQueue;

    Almacen almacen;

    EditText inicioFecha;
    EditText finFecha;

    ProgressBar barraProgreso;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        almacen = new Almacen();

        recibido = (TextView) findViewById(R.id.recibido);
        descargar = (Button) findViewById(R.id.descargar);
        requestQueue = Volley.newRequestQueue(this);

        inicioFecha = (EditText) findViewById(R.id.inicioFecha);
        finFecha = (EditText) findViewById(R.id.finFecha);

        barraProgreso = (ProgressBar) findViewById(R.id.progressBar);
        barraProgreso.setProgress(0);

        inicioFecha.setText("22/12/2020");
        finFecha.setText("22/12/2021");
    }

    public void onClickFechaInicio(View view){
        showDatePickerDialogInicio();
    }

    public void onClickFechaFin(View view){
        showDatePickerDialogFin();
    }

    private void showDatePickerDialogInicio() {
        DatePickerFragment newFragment = DatePickerFragment.newInstance(new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int year, int month, int day) {
                // +1 because January is zero
                final String selectedDate = day + "/" + (month+1) + "/" + year;
                inicioFecha.setText(selectedDate);
            }
        });



        newFragment.show(this.getSupportFragmentManager(), "datePicker");
    }

    private void showDatePickerDialogFin() {
        DatePickerFragment newFragment = DatePickerFragment.newInstance(new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int year, int month, int day) {
                final String selectedDate = day + "/" + (month+1) + "/" + year;
                finFecha.setText(selectedDate);
            }
        });

        newFragment.show(this.getSupportFragmentManager(), "datePicker");
    }

    private void stringRequest(){
        StringRequest request = new StringRequest(
                Request.Method.GET,
                urlGoogle,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        recibido.setText(response);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                }

        );
        requestQueue.add(request);
    }

    private void jsonArrayRequest(){
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                urlGoogle,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        int size = response.length();
                        for(int i=0;i<size;i++){
                            try {
                                barraProgreso.setProgress(barraProgreso.getProgress()+70);
                                JSONObject jsonObject = new JSONObject(response.get(i).toString());
                                String fecha = jsonObject.getString("Fecha");
                                int temperatura = Integer.parseInt(jsonObject.getString("Temperatura"));
                                int humedad = Integer.parseInt(jsonObject.getString("Humedad"));
                                Muestra muestra = new Muestra(fecha,temperatura,humedad);
                                almacen.addMuestra(muestra);

                            } catch (JSONException | ParseException e) {
                                e.printStackTrace();
                            }
                        }
                        //muestraDatos();
                        SimpleDateFormat formatter=new SimpleDateFormat("dd/MM/yyyy");
                        Date inicio = null;
                        Date fin = null;
                        try {
                             inicio = formatter.parse(inicioFecha.getText().toString());
                             fin = formatter.parse(finFecha.getText().toString());
                        } catch (ParseException e) {
                            e.printStackTrace();
                            return;
                        }
                        ArrayList<Muestra> lista = getDatosIntervalo(inicio,fin);
                        //TODO AQUI LLAMAR METODO HACER LA GRAFICA
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                }
        );
        barraProgreso.setProgress(20);
        requestQueue.add(jsonArrayRequest);
        barraProgreso.setProgress(30);
    }


    public void muestraDatos(){


        recibido.setText("");
        for(Muestra muestra:almacen.getMuestras()){
            recibido.append(muestra.getFecha()+"\n");
            recibido.append(muestra.getTemperatura()+"\n");
            recibido.append(muestra.getHumedad()+"\n");
            recibido.append("------------------------------\n");
        }
    }

    public ArrayList<Muestra> getDatosIntervalo(Date fechaIni, Date fechaFin){
        recibido.setText("");
       ArrayList<Muestra> lista = new ArrayList<Muestra>();
        for(Muestra muestra:almacen.getMuestras()){
            if(muestra.getFecha().before(fechaFin) && muestra.getFecha().after(fechaIni)) {
                recibido.append(muestra.getFecha() + "\n");
                recibido.append(muestra.getTemperatura() + "\n");
                recibido.append(muestra.getHumedad() + "\n");
                recibido.append("------------------------------\n");
                lista.add(muestra);
            }
        }
        return lista;
    }

    public void onClickDescargarDatos(View view){
        barraProgreso.setProgress(10);
        jsonArrayRequest();
    }



    private void creaGraficas(){

    }

}