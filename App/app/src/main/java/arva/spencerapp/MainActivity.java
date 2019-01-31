package arva.spencerapp;

import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private final static int REQUEST_ENABLE_BT = 1;
    private Button connectBluetoothRobotBtn;
    private Button connectWifiRobotBtn;
    private Button demoBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connectBluetoothRobotBtn = findViewById(R.id.connect_bluetooth_btn);
        createListeners();
    }

    public void createListeners() {

        connectBluetoothRobotBtn = findViewById(R.id.connect_bluetooth_btn);
        connectBluetoothRobotBtn.setOnClickListener(v -> {
            // Try and connect to robot, then go to Navigation Activity
            BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

            if (mBluetoothAdapter == null) {
                // Device doesn't support Bluetooth
                Toast.makeText(getApplicationContext(), "Phone does not support bluetooth", Toast.LENGTH_LONG).show();
                return;
            }

            if (!mBluetoothAdapter.isEnabled()) {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }

            goToNavigationActivity();
        });

        connectWifiRobotBtn = findViewById(R.id.connect_wifi_btn);
        connectWifiRobotBtn.setOnClickListener(v -> {
            // Try and connect to robot, then go to Navigation Activity
            TCPClient.EXECUTOR.submit(() -> {
                new TCPClient(null).run();
            });

            goToNavigationActivity();
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
