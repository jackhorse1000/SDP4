package arva.spencerapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class DemoActivity extends AppCompatActivity {

    private Button liftFrontBtn, liftBackBtn, lowerBackBtn, lowerFrontBtn,
        forwardBtn, backBtn, leftBtn, rightBtn, stopAllBtn, lowerBothBtn, liftBothBtn;

    private TextView statusTxt, connectionTxt;

    private TCPClient tcpClient;
    private int sensorInputCount = 0;
    private String[] sensorDataArray = {"sensor Front distance = 13cm", "sensor Front touch = 1", "sensor Front touch = 0", "sensor Front distance = 10cm", "sensor Front distance = 12.5cm",
            "sensor Back touch = 1", "sensor Back touch = 0", "sensor Front lifting = 1", "sensor Front lifting = 0", "sensor Front lifting = 1"};
    private ArrayAdapter arrayAdapter;

    private final String TAG = "DemoActivity";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_demo);

        setListeners();


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
        System.out.println("64 sensorlist activity starts");




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

        lowerBothBtn = findViewById(R.id.lower_both_btn);
        lowerBothBtn.setOnClickListener(v -> {
            String sendText = lowerBothBtn.getText().toString();
            lowerBothBtn.setText(lowerBothBtn.getText().equals("lower both") ? "stop lower both" : "lower both");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        liftBothBtn = findViewById(R.id.lift_both_btn);
        liftBothBtn.setOnClickListener(v -> {
            String sendText = liftBothBtn.getText().toString();
            liftBothBtn.setText(liftBothBtn.getText().equals("lift both") ? "stop lift both" : "lift both");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        stopAllBtn = findViewById(R.id.stop_all_btn);
        stopAllBtn.setOnClickListener(v -> TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("stop all")));

        liftFrontBtn = findViewById(R.id.lift_front_btn);
        liftFrontBtn.setOnClickListener(v -> {
            String sendText = liftFrontBtn.getText().toString();
            liftFrontBtn.setText(liftFrontBtn.getText().equals("lift front") ? "stop lift front" : "lift front");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        liftBackBtn = findViewById(R.id.lift_back_btn);
        liftBackBtn.setOnClickListener(v -> {
            String sendText = liftBackBtn.getText().toString();
            liftBackBtn.setText(liftBackBtn.getText().equals("lift back") ? "stop lift back" : "lift back");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        lowerFrontBtn = findViewById(R.id.lower_front_btn);
        lowerFrontBtn.setOnClickListener(v -> {
            String sendText = lowerFrontBtn.getText().toString();
            lowerFrontBtn.setText(lowerFrontBtn.getText().equals("lower front") ? "stop lower front" : "lower front");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        lowerBackBtn = findViewById(R.id.lower_back_btn);
        lowerBackBtn.setOnClickListener(v -> {
            String sendText = lowerBackBtn.getText().toString();
            lowerBackBtn.setText(lowerBackBtn.getText().equals("lower back") ? "stop lower back" : "lower back");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        backBtn = findViewById(R.id.backward_btn);
        backBtn.setOnClickListener(v -> {
            String sendText = backBtn.getText().toString();
            backBtn.setText(backBtn.getText().equals("backward") ? "stop backward" : "backward");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        forwardBtn = findViewById(R.id.forward_btn);
        forwardBtn.setOnClickListener(v -> {
            String sendText = forwardBtn.getText().toString();
            forwardBtn.setText(forwardBtn.getText().equals("forward") ? "stop forward" : "forward");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        leftBtn = findViewById(R.id.left_btn);
        leftBtn.setOnClickListener(v -> {
            String sendText = leftBtn.getText().toString();
            leftBtn.setText(leftBtn.getText().equals("turn left") ? "stop turn left" : "turn left");
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        rightBtn = findViewById(R.id.right_btn);
        rightBtn.setOnClickListener(v -> {
            String sendText = rightBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
            rightBtn.setText(rightBtn.getText().equals("turn right") ? "stop turn right" : "turn right");
        });
    }

}
