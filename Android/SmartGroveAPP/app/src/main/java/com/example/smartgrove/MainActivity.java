package com.example.smartgrove;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
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
import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    String urlGoogle = "https://script.googleusercontent.com/macros/echo?user_content_key=hfautCUoMpL7vTfTZKvbL3tP2Kbnt12m-G4bYscxlI_V81lEcHYLi440z9Gwv0fP65Xs_1Honef3-N-r-I47Skg6RWzFXbZ4m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBFiRF860KCpoZ4E0XPSsTar_QXW9Bz817n-n-h8NY7IYJnhzk8SktW1HxiHj3sYOiannw6BiFb7&lib=MaI25Xl4VUYQKa9FPNAK_RnOWC6KqnnsA";
    TextView recibido;
    Button descargar;
    RequestQueue requestQueue;

    Almacen almacen;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        almacen = new Almacen();

        recibido = (TextView) findViewById(R.id.recibido);
        descargar = (Button) findViewById(R.id.descargar);
        requestQueue = Volley.newRequestQueue(this);
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
                                JSONObject jsonObject = new JSONObject(response.get(i).toString());
                                String fecha = jsonObject.getString("Fecha");
                                int temperatura = Integer.parseInt(jsonObject.getString("Temperatura"));
                                int humedad = Integer.parseInt(jsonObject.getString("Humedad"));
                                Muestra muestra = new Muestra(fecha,temperatura,humedad);
                                almacen.addMuestra(muestra);

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                        muestraDatos();
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                }
        );
        requestQueue.add(jsonArrayRequest);
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

    public void onClickDescargarDatos(View view){
        jsonArrayRequest();
    }

}