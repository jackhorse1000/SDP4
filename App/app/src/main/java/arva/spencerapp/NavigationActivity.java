package arva.spencerapp;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

public class NavigationActivity extends AppCompatActivity implements Handler.Callback {
    private final String TAG = "NavActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        new TcpAsyncTask(new Handler(this)).execute("");
    }


    @Override
    public boolean handleMessage(Message msg) {
        // TODO: handle message here
        Log.d(TAG, "Message received");
        return false;
    }
}
