package edu.byu.cs.woodfiel.widgetdemo2;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseExpandableListAdapter;
import android.widget.ExpandableListAdapter;
import android.widget.ExpandableListView;
import android.widget.Toast;

public class ExpandableListActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_expandable_list);

        ExpandableListAdapter listAdapter = new ListAdapter(getBaseContext());
        ExpandableListView listView = (ExpandableListView) findViewById(R.id.expandable_view);
        listView.setAdapter(listAdapter);
        //listView.expandGroup(0);
        //listView.expandGroup(1);

        listView.setOnChildClickListener(new ExpandableListView.OnChildClickListener() {

            /**
             * Callback method to be invoked when a child in this expandable list has
             * been clicked.
             *
             * @param parent        The ExpandableListView where the click happened
             * @param v             The view within the expandable list/ListView that was clicked
             * @param groupPosition The group position that contains the child that
             *                      was clicked
             * @param childPosition The child position within the group
             * @param id            The row id of the child that was clicked
             * @return True if the click was handled
             */
            @Override
            public boolean onChildClick(ExpandableListView parent, View v, int groupPosition, int childPosition, long id) {
                String headerName = (String) parent.getExpandableListAdapter().getGroup(groupPosition);
                String childString = (String) parent.getExpandableListAdapter().getChild(groupPosition, childPosition);
                String suffix = "th";
                int index = childPosition + 1;
                switch(index) {
                    case 1:
                        suffix = "st";
                        break;
                    case 2:
                        suffix = "nd";
                        break;
                    case 3:
                        suffix = "rd";
                        break;
                    default:
                        suffix = "th";
                }
                Toast.makeText(getBaseContext(), "The " + index + suffix + " child in the " + headerName + " group = " + childString, Toast.LENGTH_LONG).show();

                return true;
            }
        });
    }
}
