package arva.spencerapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    private Button connectRobotBtn;
    private Button demoBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connectRobotBtn = (Button) findViewById(R.id.connect_btn);

        connectRobotBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Try and connect to robot, then go to Navigation Activity
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
