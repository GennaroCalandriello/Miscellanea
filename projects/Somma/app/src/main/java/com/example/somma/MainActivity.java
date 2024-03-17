package com.example.somma;
import android.widget.Button;
import android.widget.TextView;
import android.widget.EditText;
import java.util.Calendar;



import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Sets the content view to your XML layout

        // Passo 1: Ottieni la Data Corrente
        Calendar calendario = Calendar.getInstance();
        int anno = calendario.get(Calendar.YEAR);
        int mese = calendario.get(Calendar.MONTH);
        int giorno = calendario.get(Calendar.DAY_OF_MONTH);

        // Formatta la data (es: "12/03/2024")
        String dataOdierna = giorno + "/" + (mese + 1) + "/" + anno; // Aggiungi 1 al mese

        // Initialize UI elements
        EditText number1 = (EditText) findViewById(R.id.number1); // Find the first EditText
        //EditText number1 = "num1";
        EditText number2 = (EditText) findViewById(R.id.number2); // Find the second EditText
        Button calculateButton = (Button) findViewById(R.id.calc); // Find the Button
        TextView resultView = (TextView) findViewById(R.id.res); // Find the TextView

        EditText editTextDate = findViewById(R.id.data1);
        editTextDate.setText(dataOdierna);

        // Set OnClickListener for the button
        calculateButton.setOnClickListener(v -> {
            // Retrieve input numbers
            // Note: Add try-catch for NumberFormatException to handle invalid input
            try {
                double num1 = Double.parseDouble(number1.getText().toString()); // Convert input to number
                double num2 = Double.parseDouble(number2.getText().toString()); // Convert input to number

                // Calculate sum
                double sum = num1 + num2;

                // Display result
                resultView.setText(String.valueOf(sum));
            } catch (NumberFormatException e) {
                resultView.setText("");
            }
        });
    }
}