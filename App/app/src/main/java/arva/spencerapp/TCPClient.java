package arva.spencerapp;

import android.os.Handler;
import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class TCPClient {
    private final String IP = "palmon";
    private final int PORT = 1050;

    private static final String TAG = "TCPClient";
    private final Handler mHandler;
    private String incomingMessage;
    BufferedReader in;
    PrintWriter out;
    private MessageCallback listener = null ; // todo need to create this
    private boolean mRun = false;

    public TCPClient(Handler mHandler, MessageCallback listener) {
        this.listener         = listener;
        this.mHandler         = mHandler;
    }

    /**
     * Public method for sending the message via OutputStream object.
     * @param message Message passed as an argument and sent via OutputStream object.
     */
    public void sendMessage(String message){
        if (out != null && !out.checkError()) {
            out.println(message);
            out.flush();
            Log.d(TAG, "Sent Message: " + message);

        }
    }

    /**
     * Public method for stopping the TCPClient object ( and finalizing it after that ) from AsyncTask
     */
    public void stopClient(){
        Log.d(TAG, "Client stopped!");
        mRun = false;
    }

    void run() {

        mRun = true;

        try {
            Log.d(TAG, "Connecting...");


            // todo update UI showing connecting

//            InetAddress serverAddress = InetAddress.getByName(IP);

            /**
             * Here the socket is created with hardcoded port.
             * Also the port is given in IpGetter class.
             */
            Socket socket = new Socket(IP, PORT);

            try {

                // Create PrintWriter object for sending messages to server.
                out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

                //Create BufferedReader object for receiving messages from server.
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                Log.d(TAG, "In/Out created");

                //Sending message with command specified by AsyncTask
//                this.sendMessage(command); // todo send a test command

                // todo update UI
//                mHandler.sendEmptyMessageDelayed(MainActivity.SENDING,2000);

                //Listen for the incoming messages while mRun = true
                while (mRun) {
                    incomingMessage = in.readLine();
                    Log.d(TAG, "Waiting to recieve a message");
                    break;
//                    if (incomingMessage != null && listener != null) {
//
//                        /**
//                         * Incoming message is passed to MessageCallback object.
//                         * Next it is retrieved by AsyncTask and passed to onPublishProgress method.
//                         *
//                         */
//                        listener.callbackMessageReceiver(incomingMessage);
//                    }
//                    incomingMessage = null;
                }

                Log.d(TAG, "Received Message: " +incomingMessage);

            } catch (Exception e) {

                Log.d(TAG, "Error ", e);
                // todo update UI there has been an error
            } finally {

                out.flush();
                out.close();
                in.close();
                socket.close();
                // todo update UI socket has been closed
                Log.d(TAG, "Socket Closed");
            }

        } catch (Exception e) {

            Log.d(TAG, "Error", e);
            // todo update UI there has been an error
        }

    }

    /**
     * Method for checking if TCPClient is running.
     * @return true if is running, false if is not running
     */
    public boolean isRunning() {
        return mRun;
    }

    /**
     * Callback Interface for sending received messages to 'onPublishProgress' method in AsyncTask.
     *
     */
    public interface MessageCallback {
        /**
         * Method overriden in AsyncTask 'doInBackground' method while creating the TCPClient object.
         * @param message Received message from server app.
         */
        public void callbackMessageReceiver(String message);
    }
}
