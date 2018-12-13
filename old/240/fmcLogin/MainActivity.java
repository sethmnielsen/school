package edu.byu.cs.woodfiel.widgetdemo2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private Button searchButton;
    private EditText searchField;
    private Spinner spinner;
    private TextView helloWorld;
    private EditText editText;
    private EditText editText3;
    private Button theButton;
    private Switch bottomSwitch;


    private static final String keepYourHandsOffString ="Keep your hands off!";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Process Search
        searchField = (EditText)findViewById(R.id.searchText);
        searchButton = (Button)findViewById(R.id.search_button);
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String content = searchField.getText().toString();
                if (content.length() == 0) {
                    Toast.makeText(getBaseContext(), "The search field must contain at least 1 character.", Toast.LENGTH_LONG).show();
                } else {
                    Toast.makeText(getBaseContext(), "Search field = '" + content + "'", Toast.LENGTH_SHORT).show();
                }
            }
        });

        //Process Spinner
        final String[] spinnerColors = getResources().getStringArray((R.array.colors));
        spinner = (Spinner)findViewById(R.id.spinner);
        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if(position == 0) {
                    Toast.makeText(getBaseContext(), "You must select a color!", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getBaseContext(), "You selected the color " + spinnerColors[position], Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                //Must be orverridden but we don't use it.
            }
        });

        //Process Clicking on TextView
        helloWorld = (TextView)findViewById(R.id.textView);
        helloWorld.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getBaseContext(), "You just clicked on a TextField", Toast.LENGTH_SHORT).show();
            }
        });

        //Process Editing EditText View
        editText = (EditText)findViewById(R.id.editText);
        editText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String content = editText.getText().toString();
                Toast.makeText(getBaseContext(), "TextField = '" + content + "'", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        //Process The Button
        theButton = (Button)findViewById(R.id.button);
        theButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getBaseContext(), "You Hit THE button.", Toast.LENGTH_SHORT).show();
            }
        });

        //Process Editing EditText View
        editText3 = (EditText)findViewById(R.id.editText3);
        editText3.addTextChangedListener(new TextWatcher() {
            private int counter = 0;

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(counter == 0) {
                    Toast.makeText(getBaseContext(), "I TOLD you to keep your hands off!", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void afterTextChanged(Editable s) {
                String currentValue = editText3.getText().toString();
                if(currentValue.equals(keepYourHandsOffString)) {
                    counter = 0;
                } else {
                    editText3.setText(keepYourHandsOffString, TextView.BufferType.EDITABLE);
                    counter++;
                }
            }
        });

        //Handle Switch
        bottomSwitch = (Switch)findViewById(R.id.switchView);
        bottomSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(/*bottomSwitch.isChecked()*/isChecked) {
                    Toast.makeText(getBaseContext(), "The switch is now ON", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getBaseContext(), "The switch is now OFF", Toast.LENGTH_SHORT).show();
                }
            }
        });


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.search_filter_set, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        Intent intent;
        switch(item.getItemId()) {
            case R.id.searchMenuItem:
                intent = new Intent(getBaseContext(), RecyclerActivity.class);
                startActivity(intent);
                break;
            case R.id.searchMenuFilter:
                intent = new Intent(getBaseContext(), ExpandableListActivity.class);
                startActivity(intent);
            default:
        }
        return true;
    }
}
