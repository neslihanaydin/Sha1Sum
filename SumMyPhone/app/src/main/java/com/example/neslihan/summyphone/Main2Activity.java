package com.example.neslihan.summyphone;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.drawable.AnimationDrawable;
import android.os.Build;
import android.os.CountDownTimer;
import android.os.Environment;
import android.support.annotation.NonNull;
import android.support.annotation.RequiresApi;
import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Calendar;

public class Main2Activity extends AppCompatActivity {
    AnimationDrawable animationDrawable;
    TextView textView ;
    TextView txtDosyaVerileri;
    ImageView imageView;
    final String FILENAME = "sumMyPhoneLog.txt";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        ImageView loading = findViewById(R.id.imageView);
        textView = findViewById(R.id.textView);
        imageView = findViewById(R.id.imageView);
        txtDosyaVerileri = findViewById(R.id.txtDosyaVerileri);
        animationDrawable = (AnimationDrawable) loading.getDrawable();
        animationDrawable.start();
        txtDosyaVerileri.setMovementMethod(new ScrollingMovementMethod());
        timer();

    }

    void timer(){

        new CountDownTimer(3600000,20000){
            @RequiresApi(api = Build.VERSION_CODES.M)
            @Override
            public void onTick(long l) {
                kontrolEt();
                if(txtDosyaVerileri.getText().length()>2){
                    animationDrawable.stop();
                    imageView.setImageResource(R.drawable.frame_tick);
                    textView.setText("Özet alma işlemi gerçekleşti. Logların kopyasını aşağıda görebilirsiniz.");
                    onFinish();
                }
            }

            @Override
            public void onFinish() {
                if (txtDosyaVerileri.getText().length()==0){
                    timer();
                }

            }
        }.start();
    }

    @RequiresApi(api = Build.VERSION_CODES.M)
    void kontrolEt(){
        if(checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
            requestPermissions(new String[] {Manifest.permission.READ_EXTERNAL_STORAGE},3);
        }else {
            StringBuilder sb = new StringBuilder();
            try{
                File textFile = new File(Environment.getExternalStorageDirectory(),FILENAME);
                FileInputStream fis = new FileInputStream(textFile);
                if(fis != null){
                    InputStreamReader isr = new InputStreamReader(fis);
                    BufferedReader buff = new BufferedReader(isr);

                    String line = null;
                    while ((line = buff.readLine()) != null){
                        sb.append(line+"\n");
                    }
                    fis.close();
                }
                txtDosyaVerileri.setText(sb);
            }catch (IOException e){
                e.printStackTrace();
            }

        }

    }
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {

        if(requestCode == 3){
            if(grantResults.length >0 && grantResults[0]==PackageManager.PERMISSION_GRANTED){
                StringBuilder sb = new StringBuilder();
                try{
                    File textFile = new File(Environment.getExternalStorageDirectory(),FILENAME);
                    FileInputStream fis = new FileInputStream(textFile);
                    if(fis != null){
                        InputStreamReader isr = new InputStreamReader(fis);
                        BufferedReader buff = new BufferedReader(isr);

                        String line = null;
                        while ((line = buff.readLine()) != null){
                            sb.append(line+"\n");
                        }
                        fis.close();
                    }
                    txtDosyaVerileri.setText(sb);
                }catch (IOException e){
                    e.printStackTrace();
                }
            }
        }

        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }



}
