package arva.spencerapp;

import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

public class NavigationActivity extends AppCompatActivity {
    private final String TAG = "NavActivity";

    private TCPClient tcpClient;

    private Button connectSpencerBtn, forwardBtn, backwardBtn, leftBtn, rightBtn,
        upstairsBtn, downStairsBtn, stopAllBtn;

    private TextView statusTxt, connectionTxt;

    AlertDialog alert11;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        setListeners();

        AlertDialog.Builder builder1 = new AlertDialog.Builder(this);
        builder1.setMessage("Spencer has been disconnected");
        builder1.setCancelable(false);

        builder1.setPositiveButton(
            "Reconnect",
            new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    connectToSpencer();
                    dialog.cancel();
                }
            });

        builder1.setNegativeButton(
            "go back",
            new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                    kickOut();
                    dialog.cancel();
                }
            });


        alert11 = builder1.create();

        alert11.setCanceledOnTouchOutside(false);

        connectToSpencer();
    }

    private void connectToSpencer() {
        Handler mainHandler = new Handler(getMainLooper());

        tcpClient = new TCPClient(new TCPClient.MessageCallback() {
            @Override
            public void connectionStateChanged(TCPClient.ConnectionState state) {
                mainHandler.post(() -> connectionTxt.setText(state.toString()));
                String connection_state = state.toString();
                if (connection_state.equals("CLOSED")){
                    Log.d(TAG, "43 messaged received: " + connection_state);
                    mainHandler.post(() -> alert11.show());
                } else{
                    Log.d(TAG, "46 messaged received: " + connection_state);
                    // kickOut();
                }
                Log.d(TAG, "49 messaged received: " + connection_state);
                Log.d(TAG, "Connection state change: " + state);
            }

            @Override
            public void messageReceived(String message) {
                mainHandler.post(() -> {
                    if (message.startsWith("sensor")) {
//                        updateArray(message); // todo fix
                    } else {
                        statusTxt.setText(message);
                        Log.d(TAG, "56 messaged received: " + message);
                        if(  message.equals(TCPClient.ConnectionState.CLOSED) ){
                            Log.d(TAG, "62 messaged received: " + message);

                            alert11.show();
                        }
                    }
                });
                Log.d(TAG, "67 messaged received: " + message);
            }
        });

        TCPClient.EXECUTOR.submit(tcpClient::run);
    }

    private void kickOut() {
        Intent navigationIntent = new Intent( NavigationActivity.this, MainActivity.class);
        navigationIntent.putExtra("reason","kickedBack");
        startActivity(navigationIntent);
        finish();
    }

    private void setListeners() {
        statusTxt = findViewById(R.id.status_txt);
        connectionTxt = findViewById(R.id.connection_status_txt);

        stopAllBtn = findViewById(R.id.stop_all_btn);
        stopAllBtn.setOnClickListener(v -> {
            String sendText = stopAllBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage(sendText));
        });

        forwardBtn = findViewById(R.id.forward_btn);
        forwardBtn.setOnClickListener(v -> {
            String sendText = forwardBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("forward"));
        });

        backwardBtn = findViewById(R.id.backward_btn);
        backwardBtn.setOnClickListener(v -> {
            String sendText = backwardBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("backward"));
        });

        leftBtn = findViewById(R.id.turn_left_btn);
        leftBtn.setOnClickListener(v -> {
            String sendText = leftBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("turn_left"));
        });

        rightBtn = findViewById(R.id.turn_right_btn);
        rightBtn.setOnClickListener(v -> {
            String sendText = rightBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("turn_right"));
        });

        upstairsBtn = findViewById(R.id.upstairs_btn);
        upstairsBtn.setOnClickListener(v -> {
            String sendText = upstairsBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("climb"));
        });

        downStairsBtn = findViewById(R.id.downstairs_btn);
        downStairsBtn.setOnClickListener(v -> {
            String sendText = downStairsBtn.getText().toString();
            TCPClient.EXECUTOR.submit(() -> tcpClient.sendMessage("downstairs"));
        });
    }


}
