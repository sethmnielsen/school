package edu.byu.cs.woodfiel.widgetdemo2;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class RecyclerActivity extends AppCompatActivity {
    private RecyclerView mRecyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager mLayoutManager;

    private Button addLineButton;
    private int lineCounter;

    private List<String> lines;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler);


        lineCounter = 3;

        addLineButton = (Button)findViewById(R.id.addLine);
        addLineButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getBaseContext(), "Adding a Line", Toast.LENGTH_SHORT).show();
                ((MyAdapter)mAdapter).addLine("Line " + lineCounter++);
            }
        });

        mRecyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);

        //mRecyclerView.setHasFixedSize(true);

        mLayoutManager = new LinearLayoutManager(this);
        ((LinearLayoutManager)mLayoutManager).setOrientation(LinearLayoutManager.VERTICAL);
        mRecyclerView.setLayoutManager(mLayoutManager);

        lines = new ArrayList<>();
        lines.add("First Line");
        lines.add("Second Line");

        mAdapter = new MyAdapter(lines);
        mRecyclerView.setAdapter(mAdapter);
    }
}
