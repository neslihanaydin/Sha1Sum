package com.example.neslihan.summyphone;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.drawable.AnimationDrawable;
import android.nfc.Tag;
import android.os.Build;
import android.os.CountDownTimer;
import android.os.Environment;
import android.os.ParcelFileDescriptor;
import android.support.annotation.NonNull;
import android.support.annotation.RequiresApi;
import android.support.constraint.ConstraintLayout;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.hardware.usb.UsbManager;
import android.hardware.usb.UsbAccessory;
import android.widget.Toast;

import java.io.File;
import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class MainActivity extends AppCompatActivity {


    Button button ;
    ConstraintLayout myLayout;
    Button popUpButton ;
    final String FILENAME = "sumMyPhone.txt";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        myLayout = findViewById(R.id.myLayout);
        popUpButton = findViewById(R.id.btnBilgiPopUp);


    }
    void timer(){

        new CountDownTimer(3200,800){
            @Override
            public void onTick(long l) {

            }

            @Override
            public void onFinish() {
                Intent intent = new Intent(getApplicationContext(),Main2Activity.class);
                startActivity(intent);
                finish();
            }
        }.start();
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    void ozetAlmaBaslat(View view){
        if( checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
            requestPermissions(new String[] {Manifest.permission.WRITE_EXTERNAL_STORAGE}, 2);
        }else{

            File textFile = new File(Environment.getExternalStorageDirectory(), "sumMyPhone.txt");
            try {
                Calendar calendar = Calendar.getInstance();
                SimpleDateFormat mdformat = new SimpleDateFormat("yyyy / MM / dd ");
                String strDate = ""+mdformat.format(calendar.getTime());
                FileOutputStream fos = new FileOutputStream(textFile);
                fos.write((strDate).getBytes());
                fos.close();
               // Toast.makeText(this," ",Toast.LENGTH_SHORT).show();
                timer();


            }catch (IOException e){
                e.printStackTrace();
            }

        }

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {

        if(requestCode == 2){
            if(grantResults.length >0 && grantResults[0]==PackageManager.PERMISSION_GRANTED){
                File textFile = new File(Environment.getExternalStorageDirectory(), "sumMyPhone.txt");
                try {
                    Calendar calendar = Calendar.getInstance();
                    SimpleDateFormat mdformat = new SimpleDateFormat("yyyy / MM / dd ");
                    String strDate = ""+mdformat.format(calendar.getTime());
                    FileOutputStream fos = new FileOutputStream(textFile);
                    fos.write((strDate).getBytes());
                    fos.close();
                   // Toast.makeText(this," ",Toast.LENGTH_SHORT).show();
                    timer();
                }catch (IOException e){
                    e.printStackTrace();
                }
            }
        }

        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    void bilgiGosterPopUp(View view){

        Intent intent = new Intent(getApplicationContext(),BilgiPopUpActivity.class);
        startActivity(intent);

    }




}
