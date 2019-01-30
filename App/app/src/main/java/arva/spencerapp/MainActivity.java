package arva.spencerapp;

import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private Button connectBluetoothRobotBtn;
    private Button connectWifiRobotBtn;
    private Button demoBtn;
    private final static int REQUEST_ENABLE_BT = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        createListeners();

    }

    public void createListeners(){

        connectBluetoothRobotBtn = (Button) findViewById(R.id.connect_bluetooth_btn);

        connectBluetoothRobotBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Try and connect to robot, then go to Navigation Activity
                BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
                if (mBluetoothAdapter == null) {
                    // Device doesn't support Bluetooth
                    Toast.makeText(getApplicationContext(), "Phone does not support bluetooth", Toast.LENGTH_LONG);
                    return;
                }
                if (!mBluetoothAdapter.isEnabled()) {
                    Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                    startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
                }
                goToNavigationActivity();
            }
        });

        demoBtn = (Button) findViewById(R.id.demo_btn);
        demoBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                goToDemoActivity();
            }
        });
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
