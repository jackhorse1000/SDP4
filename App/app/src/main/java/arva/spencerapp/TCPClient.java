package arva.spencerapp;

import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Objects;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class TCPClient {
    private static final String TAG = TCPClient.class.getName();

    public static final ExecutorService EXECUTOR = Executors.newCachedThreadPool();

    private static final String IP = "192.168.105.153";
    private static final int PORT = 1050;

    private BufferedWriter out;
    private final MessageCallback listener;
    private boolean running = false;

    public TCPClient(MessageCallback listener) {
        Objects.requireNonNull(listener, "listener cannot be null");
        this.listener = listener;
    }

    /**
     * Public method for sending the message via OutputStream object.
     *
     * @param message Message passed as an argument and sent via OutputStream object.
     */
    public void sendMessage(String message) {
        if (out != null) {
            try {
                out.write(message + "\n");
                out.flush();
            } catch (IOException e) {
                Log.e(TAG, "Unable to send message", e);
            }

            Log.d(TAG, "Sent Message: " + message);
        } else {
            Log.e(TAG, "Not connected. Unable to send message");
        }
    }

    /**
     * Public method for stopping the TCPClient object ( and finalizing it after that ) from AsyncTask
     */
    public void stopClient() {
        Log.d(TAG, "Stopping client");
        running = false;
    }

    void run() {
        running = true;
        Log.d(TAG, "Connecting");
        listener.connectionStateChanged(ConnectionState.CONNECTING);

        // Connect the socket, and input/output streams
        try (Socket socket = new Socket(IP, PORT);
             BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8));
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8))
        ) {
            this.out = out;

            Log.d(TAG, "Connected");
            listener.connectionStateChanged(ConnectionState.CONNECTED);

            //Listen for the incoming messages while mRun = true
            while (running) {
                Log.d(TAG, "Waiting to receive a message");
                String message = in.readLine();
                if (message == null) break;
                Log.d(TAG, "Received " + message);
                listener.messageReceived(message);
            }
        } catch (Exception e) {
            Log.e(TAG, "Error", e);
        } finally {
            Log.d(TAG, "Closed");
            listener.connectionStateChanged(ConnectionState.CLOSED);

            this.running = false;
            this.out = null;
        }
    }

    /**
     * Method for checking if TCPClient is running.
     *
     * @return true if is running, false if is not running
     */
    public boolean isRunning() {
        return running;
    }

    public enum ConnectionState {
        CONNECTING,
        CONNECTED,
        CLOSED
    }

    /**
     * Callback Interface for sending received messages to 'onPublishProgress' method in AsyncTask.
     */
    public interface MessageCallback {
        /**
         * Fired when the connection state is changed
         *
         * @param state The current connection state.
         */
        void connectionStateChanged(ConnectionState state);

        /**
         * Method overriden in AsyncTask 'doInBackground' method while creating the TCPClient object.
         *
         * @param message Received message from server app.
         */
        void messageReceived(String message);
    }
}
