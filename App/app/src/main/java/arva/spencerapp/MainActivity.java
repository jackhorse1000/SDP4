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

 //        connectToSpencer();

   //        if(is_connected){
                goToNavigationActivity();
     //     }
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




}
