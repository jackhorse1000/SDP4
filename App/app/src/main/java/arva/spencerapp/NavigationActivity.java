package arva.spencerapp;

import android.content.Context;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class NavigationActivity extends AppCompatActivity implements Handler.Callback{

    private final String TAG = "NavActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        new TcpAsyncTask(new Handler(this)).execute("");
    }


    @Override
    public boolean handleMessage(Message msg) {
        // todo handle message here
        Log.d(TAG, "Message recieved");
        return false;
    }
}
