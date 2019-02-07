package arva.spencerapp;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class NavigationActivity extends AppCompatActivity implements Handler.Callback {
    private final String TAG = "NavActivity";

    private TCPClient tcpClient;

    private Button connectSpencerBtn;

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
    }

    @Override
    public boolean handleMessage(Message msg) {
        // TODO: handle message here
        Log.d(TAG, "Message received");
        return false;
    }
}
