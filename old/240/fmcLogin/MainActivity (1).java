package edu.byu.cs240.asyncwebaccess;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity implements DownloadTask.Context {

    private ProgressBar progressBar;
    private TextView totalSizeTextView;
    private Button downloadButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        progressBar = (ProgressBar)findViewById(R.id.progressBar);

        totalSizeTextView = (TextView)findViewById(R.id.totalSizeTextView);

        downloadButton = (Button)findViewById(R.id.downloadButton);
        downloadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                downloadButtonClicked();
            }
        });

        resetViews();
    }

    private void resetViews() {
        progressBar.setProgress(0);
        totalSizeTextView.setText("Total Size:");
    }

    private void downloadButtonClicked() {
        try {
            resetViews();

            DownloadTask task = new DownloadTask(this);

            task.execute(new URL("https://home.byu.edu/home/"),
                    new URL("https://www.whitehouse.gov/"),
                    new URL("http://www.oracle.com/index.html"));
        }
        catch (MalformedURLException e) {
            Log.e("MainActivity", e.getMessage(), e);
        }
    }

    @Override
    public void onProgressUpdate(int percent) {
        progressBar.setProgress(percent);
    }

    @Override
    public void onDownloadComplete(long totalBytes) {
        totalSizeTextView.setText("Total Size: " + totalBytes);
    }

}
