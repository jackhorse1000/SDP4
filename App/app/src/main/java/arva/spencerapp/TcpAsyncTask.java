package arva.spencerapp;

import android.os.AsyncTask;
import android.os.Handler;
import android.util.Log;

public class TcpAsyncTask extends AsyncTask<String, String, TCPClient> {

    private Handler mHandler;
    private static final String TAG = "TcpAsyncTask";
    private TCPClient tcpClient;


    public TcpAsyncTask(Handler mHandler){
        this.mHandler = mHandler;
    }

    @Override
    protected TCPClient doInBackground(String... strings) {
        Log.d(TAG, "In do in background");

        try{
            tcpClient = new TCPClient(mHandler,
                    new TCPClient.MessageCallback() {
                        @Override
                        public void callbackMessageReceiver(String message) {
                            publishProgress(message); // todo callback for message recieved
                        }
                    });

        }catch (NullPointerException e){
            Log.d(TAG, "Caught null pointer exception");
            e.printStackTrace();
        }
        tcpClient.run();
        return null;
    }

    /**
     * Overriden method from AsyncTask class. Here we're checking if server answered properly.
     * @param values If "restart" message came, the client is stopped and computer should be restarted.
     *               Otherwise "wrong" message is sent and 'Error' message is shown in UI.
     */
    @Override
    protected void onProgressUpdate(String... values) {
        super.onProgressUpdate(values);
        Log.d(TAG, "In progress update, values: " + values.toString());
        // todo check response from server
        // todo Update UI of progress
        // todo Update UI of progress

//        if(values[0].equals("")){
//            tcpClient.stopClient();

//        }else{
//            tcpClient.sendMessage("wrong");
//
//            tcpClient.stopClient(); // stop client they got it wrong
//        }
    }

    @Override
    protected void onPostExecute(TCPClient result){
        super.onPostExecute(result);
        Log.d(TAG, "In on post execute");
        if(result != null && result.isRunning()){
            result.stopClient();
        }
        // todo Update UI client has been stopped
    }


}
