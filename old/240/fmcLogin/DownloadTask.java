package edu.byu.cs240.asyncwebaccess;

import android.os.AsyncTask;
import java.net.URL;

public class DownloadTask extends AsyncTask<URL, Integer, Long> {

    public interface Context {
        void onProgressUpdate(int percent);
        void onDownloadComplete(long totalBytes);
    }

    private Context context;

    public DownloadTask(Context c) {
        context = c;
    }

    protected Long doInBackground(URL... urls) {

        HttpClient httpClient = new HttpClient();

        long totalSize = 0;

        for (int i = 0; i < urls.length; i++) {

            String urlContent = httpClient.getUrl(urls[i]);
            if (urlContent != null) {
                totalSize += urlContent.length();
            }

            int progress = 0;
            if (i == urls.length - 1) {
                progress = 100;
            }
            else {
                float cur = i + 1;
                float total = urls.length;
                progress = (int)((cur / total) * 100);
            }
            publishProgress(progress);
        }

        return totalSize;
    }

    protected void onProgressUpdate(Integer... progress) {
        int percent = progress[0];
        context.onProgressUpdate(percent);
    }

    protected void onPostExecute(Long result) {
        long totalBytes = result;
        context.onDownloadComplete(totalBytes);
    }
}
