package arva.spencerapp;

import android.bluetooth.BluetoothAdapter;
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

public class MainActivity extends AppCompatActivity {

    private final static int REQUEST_ENABLE_BT = 1;
    private Button connectBluetoothRobotBtn;
    private Button connectWifiRobotBtn;
    private Button demoBtn;

    private TCPClient tcpClient;
    private TextView statusTxt, connectionTxt;
    private final String TAG = "MainActivity";
    private boolean is_connected = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

      
        createListeners();
    }

    public void createListeners() {

        connectWifiRobotBtn = findViewById(R.id.connect_wifi_btn);
        connectWifiRobotBtn.setOnClickListener(v -> {
            // Try and connect to robot, then go to Navigation Activity
            TCPClient.EXECUTOR.submit(() -> {
                new TCPClient(new TCPClient.MessageCallback() {
                    @Override
                    public void connectionStateChanged(TCPClient.ConnectionState state) {
                    }

                    @Override
                    public void messageReceived(String message) {
                    }
                }).run();
            });

 //          connectToSpencer();

 //           if(is_connected){
                goToNavigationActivity();
 //            }
        });

        demoBtn = findViewById(R.id.demo_btn);
        demoBtn.setOnClickListener(v -> goToDemoActivity());
    }

    private void goToNavigationActivity() {
        Intent navigationIntent = new Intent(MainActivity.this, NavigationActivity.class);
        startActivity(navigationIntent);
    }

    private void goToDemoActivity() {
        Intent demoIntent = new Intent(MainActivity.this, DemoActivity.class);
        startActivity(demoIntent);
    }

/*  private void connectToSpencer() {
        Handler mainHandler = new Handler(getMainLooper());

        tcpClient = new TCPClient(new TCPClient.MessageCallback() {
            @Override
            public void connectionStateChanged(TCPClient.ConnectionState state) {
                if(state ==null){
                    showDialog();
                }
                mainHandler.post(() -> connectionTxt.setText(state.toString()));
                String connection_state = state.toString();


                if (connection_state.equals("CLOSED")){
                    mainHandler.post(()-> connectWifiRobotBtn.setClickable(true));
                }


                else if(state == TCPClient.ConnectionState.CONNECTED){
                    is_connected = true;

                    mainHandler.post(()-> connectWifiRobotBtn.setClickable(false));
                    Log.d(TAG, "Connection state change: " + state);
                }
                else{
                    mainHandler.post(()-> connectWifiRobotBtn.setClickable(false));
                    Log.d(TAG, "Connection state change: " + state);
                }

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
    }*/

    private void showDialog(){
        AlertDialog.Builder builder=new AlertDialog.Builder(this);

        builder.setTitle("温馨提示");
        builder.setMessage("天冷多加衣！");
        builder.setPositiveButton("我知道了",
            new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialogInterface, int i) {

                }
            });
        AlertDialog dialog=builder.create();
        dialog.show();

    }

}
