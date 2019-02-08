package arva.spencerapp;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class NavigationActivity extends AppCompatActivity {
    private final String TAG = "NavActivity";

    private TCPClient tcpClient;

    private Button connectSpencerBtn, forwardBtn, backwardBtn, leftBtn, rightBtn,
        upstairsBtn, downStairsBtn;

    private TextView statusTxt, connectionTxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        setListeners();

        connectToSpencer();
    }

    private void connectToSpencer() {
        Handler mainHandler = new Handler(getMainLooper());

        tcpClient = new TCPClient(new TCPClient.MessageCallback() {
            @Override
            public void connectionStateChanged(TCPClient.ConnectionState state) {
                mainHandler.post(() -> connectionTxt.setText(state.toString()));
                String connection_state = state.toString();
                if (connection_state.equals("CLOSED"))
                    mainHandler.post(()-> connectSpencerBtn.setClickable(true));
                else
                    mainHandler.post(()-> connectSpencerBtn.setClickable(false));
                Log.d(TAG, "Connection state change: " + state);
            }

            @Override
            public void messageReceived(String message) {
                mainHandler.post(() -> {
                    if (message.startsWith("sensor")) {
//                        updateArray(message); // todo fix
                    } else {
                        statusTxt.setText(message);
                    }
                });
                Log.d(TAG, "messaged received: " + message);
            }
        });

        TCPClient.EXECUTOR.submit(tcpClient::run);
    }


    private void setListeners() {
        statusTxt = findViewById(R.id.status_txt);
        connectionTxt = findViewById(R.id.connection_status_txt);

        connectSpencerBtn = findViewById(R.id.connect_spencer_btn);
        connectSpencerBtn.setOnClickListener(v -> connectToSpencer());

        forwardBtn = findViewById(R.id.forward_btn);
        forwardBtn.setOnClickListener(v -> {
            String sendText = forwardBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        backwardBtn = findViewById(R.id.backward_btn);
        backwardBtn.setOnClickListener(v -> {
            String sendText = backwardBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        leftBtn = findViewById(R.id.turn_left_btn);
        leftBtn.setOnClickListener(v -> {
            String sendText = leftBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        rightBtn = findViewById(R.id.turn_right_btn);
        rightBtn.setOnClickListener(v -> {
            String sendText = rightBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        upstairsBtn = findViewById(R.id.upstairs_btn);
        upstairsBtn.setOnClickListener(v -> {
            String sendText = upstairsBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        downStairsBtn = findViewById(R.id.downstairs_btn);
        downStairsBtn.setOnClickListener(v -> {
            String sendText = downStairsBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });
    }
}
