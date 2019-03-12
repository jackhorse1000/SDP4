package arva.spencerapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.util.Log;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

public class SensorListActivity extends AppCompatActivity {

    private ArrayAdapter<String> arrayAdapter;
    private String[] sensorDataArray = {"sensor Front distance = 13cm", "sensor Front touch = 1", "sensor Front touch = 0", "sensor Front distance = 10cm", "sensor Front distance = 12.5cm",
        "sensor Back touch = 1", "sensor Back touch = 0", "sensor Front lifting = 1", "sensor Front lifting = 0", "sensor Front lifting = 1"};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.v("18","meg");
        setContentView(R.layout.activity_sensor_list);
        Log.v("20","meg");
        arrayAdapter = new ArrayAdapter<String>(this, R.layout.sensor_list_item, sensorDataArray);
        Log.v("22","meg");
        ListView listView = (ListView) findViewById(R.id.sensor_list_view);
        Log.v("24","meg");
        listView.setAdapter(arrayAdapter);
        Log.v("26","meg");
    }

}
