package arva.spencerapp;

import android.app.Dialog;
import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

public class MainActivity extends AppCompatActivity {

    private final static int REQUEST_ENABLE_BT = 1;
    private Button connectBluetoothRobotBtn;
    private Button connectWifiRobotBtn;
    private Button technicalMenu;

    private TCPClient tcpClient;
    private TextView statusTxt, connectionTxt;
    private final String TAG = "MainActivity";
    private boolean is_connected = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        connectionTxt = findViewById(R.id.connection_status_txt);
        String str = "c";
        Intent intent = getIntent();
        if(intent != null){
             str = intent.getStringExtra("reason");
        }

        if( str != null  && str.equals("kickedBack")){
            Log.d(TAG, "42 "+str );
            Context context = getApplicationContext();
            CharSequence text = "disconnected, please reconnect again!";
            int duration = Toast.LENGTH_SHORT;

            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
        createListeners();

        Log.d(TAG, "36 "+str );
    }



    public void createListeners() {
        technicalMenu = findViewById(R.id.technical_btn);
        technicalMenu.setOnClickListener(v -> {
            goTotechnicalMenuActivity();
        });
        Handler mainHandler = new Handler(getMainLooper());
        connectWifiRobotBtn = findViewById(R.id.connect_wifi_btn);
        connectWifiRobotBtn.setOnClickListener(v -> {
            // Try and connect to robot, then go to Navigation Activity
            TCPClient.EXECUTOR.submit(() -> {
                new TCPClient(new TCPClient.MessageCallback() {
                    @Override
                    public void connectionStateChanged(TCPClient.ConnectionState state) {
                        mainHandler.post(() -> connectionTxt.setText(state.toString()));
                        String connection_state = state.toString();
                        if (connection_state.equals("CONNECTED")){
                        //    goToNavigationActivity();
                        //    mainHandler.post(()-> connectWifiRobotBtn.setClickable(true));
                        }
                        else
                        //    mainHandler.post(()-> connectWifiRobotBtn.setClickable(false));
                        Log.d(TAG, "Connection state change: " + state);
                    }

                    @Override
                    public void messageReceived(String message) {
                        mainHandler.post(() -> {
                            if (message.startsWith("sensor")) {
//                        updateArray(message); // todo fix
                            } else {
    //                            statusTxt.setText(message);
                            }
                        });
                        Log.d(TAG, "messaged received: " + message);
                    }
                }).run();
            });
            Log.d(TAG, "70 messaged received: " );
            goToNavigationActivity();
            Log.d(TAG, "72 messaged received: " );
        });


    }

    private void goTotechnicalMenuActivity() {
        Intent navigationIntent = new Intent(MainActivity.this, UserGuideActivity.class);
        startActivity(navigationIntent);
    }

    private void goToNavigationActivity() {
        Intent navigationIntent = new Intent(MainActivity.this, NavigationActivity.class);
        startActivity(navigationIntent);
    }

    private void goToDemoActivity() {
        Intent demoIntent = new Intent(MainActivity.this, DemoActivity.class);
        startActivity(demoIntent);
    }




}
