package edu.byu.cs240.asyncwebaccess;

import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpClient {

    public String getUrl(URL url) {
        try {
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.connect();

            if (connection.getResponseCode() == HttpURLConnection.HTTP_OK) {
                // Get response body input stream
                InputStream responseBody = connection.getInputStream();

                // Read response body bytes
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                byte[] buffer = new byte[1024];
                int length = 0;
                while ((length = responseBody.read(buffer)) != -1) {
                    baos.write(buffer, 0, length);
                }

                // Convert response body bytes to a string
                String responseBodyData = baos.toString();
                return responseBodyData;
            }
        }
        catch (Exception e) {
            Log.e("HttpClient", e.getMessage(), e);
        }

        return null;
     }
}
