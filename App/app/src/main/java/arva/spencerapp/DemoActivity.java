package arva.spencerapp;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class DemoActivity extends AppCompatActivity {

    private Button liftFrontBtn, liftBackBtn, lowerBackBtn, lowerFrontBtn,
        forwardBtn, backBtn, leftBtn, rightBtn;

    private TextView statusTxt, connectionTxt;

    private TCPClient tcpClient;
    private int sensorInputCount = 0;
    private String[] sensorDataArray = {"", "", "", "", "", "", "", "", "", ""};
    private ArrayAdapter arrayAdapter;

    private final String TAG = "DemoActivity";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_demo);

        setListeners();

        arrayAdapter = new ArrayAdapter<>(this, R.layout.sensor_list_item, sensorDataArray);

        ListView listView = findViewById(R.id.sensor_list_view);
        listView.setAdapter(arrayAdapter);

        Handler mainHandler = new Handler(getMainLooper());

        tcpClient = new TCPClient(new TCPClient.MessageCallback() {
            @Override
            public void connectionStateChanged(TCPClient.ConnectionState state) {
                mainHandler.post(() -> connectionTxt.setText(state.toString()));
                Log.d(TAG, "Connection state change: " + state);
            }

            @Override
            public void messageReceived(String message) {
                mainHandler.post(() -> {
                    if (message.startsWith("sensor")) {
                        updateArray(message);
                    } else {
                        statusTxt.setText(message);
                    }
                });
                Log.d(TAG, "messaged received: " + message);
            }
        });

        TCPClient.EXECUTOR.submit(tcpClient::run);
    }

    private void updateArray(String str) {

        if (sensorInputCount + 1 <= sensorDataArray.length) {
            sensorDataArray[sensorInputCount] = str;
            sensorInputCount++;
        } else {
            String temp = sensorDataArray[sensorDataArray.length-1];
            sensorDataArray[sensorDataArray.length-1] = str;
            for (int i = sensorDataArray.length-2; i >= 1  ; i--) {
                String temp_ = sensorDataArray[i];
                sensorDataArray[i] = temp;
                temp = temp_;

            }
            sensorDataArray[0] = temp;
        }
        arrayAdapter.notifyDataSetChanged();
    }

    private void setListeners() {
        statusTxt = findViewById(R.id.status_txt);
        connectionTxt = findViewById(R.id.connection_status_txt);

        liftFrontBtn = findViewById(R.id.lift_front_btn);
        liftFrontBtn.setOnClickListener(v -> {
            liftFrontBtn.setText(liftFrontBtn.getText().equals("lift front") ? "Stop lift front" : "lift front");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("lift front"));
        });

        liftBackBtn = findViewById(R.id.lift_back_btn);
        liftBackBtn.setOnClickListener(v -> {
            liftBackBtn.setText(liftBackBtn.getText().equals("lift back") ? "Stop lift back" : "lift back");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("lift back"));
        });

        lowerFrontBtn = findViewById(R.id.lower_front_btn);
        lowerFrontBtn.setOnClickListener(v -> {
            lowerFrontBtn.setText(lowerFrontBtn.getText().equals("lower front") ? "Stop lower front" : "lower front");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("lower front"));
        });

        lowerBackBtn = findViewById(R.id.lower_back_btn);
        lowerBackBtn.setOnClickListener(v -> {
            lowerBackBtn.setText(lowerBackBtn.getText().equals("lower back") ? "Stop lower back" : "lower back");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("lower back"));
        });

        backBtn = findViewById(R.id.backward_btn);
        backBtn.setOnClickListener(v -> {
            backBtn.setText(backBtn.getText().equals("backward") ? "Stop backward" : "backward");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("back"));
        });

        forwardBtn = findViewById(R.id.forward_btn);
        forwardBtn.setOnClickListener(v -> {
            forwardBtn.setText(forwardBtn.getText().equals("forward") ? "stop forward" : "forward");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("forward"));
        });

        leftBtn = findViewById(R.id.left_btn);
        leftBtn.setOnClickListener(v -> {
            leftBtn.setText(leftBtn.getText().equals("turn left") ? "stop turn left" : "turn left");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("left"));
        });

        rightBtn = findViewById(R.id.right_btn);
        rightBtn.setOnClickListener(v -> {
            rightBtn.setText(rightBtn.getText().equals("turn right") ? "stop turn right" : "turn right");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("right"));
        });
    }

}
