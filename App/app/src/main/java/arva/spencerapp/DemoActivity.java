package arva.spencerapp;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class DemoActivity extends AppCompatActivity {

    private Button liftFrontBtn, liftBackBtn, lowerBackBtn, lowerFrontBtn,
        forwardBtn, backBtn, leftBtn, rightBtn;

    private TextView statusTxt, connectionTxt;

    private TCPClient tcpClient;

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
                mainHandler.post(() -> {
                    connectionTxt.setText(state.toString());
                });
                Log.d(TAG, "Connection state change: " + state);
            }

            @Override
            public void messageReceived(String message) {
                mainHandler.post(() -> {
                    statusTxt.setText(message);
                });
                Log.d(TAG, "messaged received: " + message);
            }
        });

        TCPClient.EXECUTOR.submit(tcpClient::run);
    }

    private void setListeners() {
        statusTxt = findViewById(R.id.status_txt);
        connectionTxt = findViewById(R.id.connection_status_txt);

        liftFrontBtn = findViewById(R.id.lift_front_btn);
        liftFrontBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(liftFrontBtn.getText().equals("lift front"))
                    liftFrontBtn.setText("Stop lift front");
                else
                    liftFrontBtn.setText("lift front");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("lift front");
                });
            }
        });

        liftBackBtn = findViewById(R.id.lift_back_btn);
        liftBackBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(liftBackBtn.getText().equals("lift back"))
                    liftBackBtn.setText("Stop lift back");
                else
                    liftBackBtn.setText("lift back");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("lift back");
                });
            }
        });

        lowerFrontBtn = findViewById(R.id.lower_front_btn);
        lowerFrontBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(lowerFrontBtn.getText().equals("lower front"))
                    lowerFrontBtn.setText("Stop lower front");
                else
                    lowerFrontBtn.setText("lower front");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("lower front");
                });
            }
        });

        lowerBackBtn = findViewById(R.id.lower_back_btn);
        lowerBackBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(lowerBackBtn.getText().equals("lower back"))
                    lowerBackBtn.setText("Stop lower back");
                else
                    lowerBackBtn.setText("lower back");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("lower back");
                });
            }
        });

        backBtn = findViewById(R.id.backward_btn);
        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(backBtn.getText().equals("backward"))
                    backBtn.setText("Stop backward");
                else
                    backBtn.setText("backward");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("back");
                });
            }
        });

        forwardBtn = findViewById(R.id.forward_btn);
        forwardBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(forwardBtn.getText().equals("forward"))
                    forwardBtn.setText("stop forward");
                else
                    forwardBtn.setText("forward");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("forward");
                });
            }
        });

        leftBtn = findViewById(R.id.left_btn);
        leftBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(leftBtn.getText().equals("turn left"))
                    leftBtn.setText("stop turn left");
                else
                    leftBtn.setText("turn left");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("left");
                });
            }
        });

        rightBtn = findViewById(R.id.right_btn);
        rightBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(rightBtn.getText().equals("turn right"))
                    rightBtn.setText("stop turn right");
                else
                    rightBtn.setText("turn right");
                TCPClient.EXECUTOR.submit(()->{
                    tcpClient.sendMessage("right");
                });
            }
        });
    }

}
