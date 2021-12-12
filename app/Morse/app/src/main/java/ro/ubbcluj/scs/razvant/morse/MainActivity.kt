package ro.ubbcluj.scs.razvant.morse

import android.os.Bundle
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.hivemq.client.mqtt.MqttClient
import com.hivemq.client.mqtt.mqtt3.Mqtt3AsyncClient
import com.hivemq.client.mqtt.mqtt3.message.connect.connack.Mqtt3ConnAck
import com.hivemq.client.mqtt.mqtt3.message.publish.Mqtt3Publish
import java.nio.charset.StandardCharsets
import kotlinx.android.synthetic.main.activity_main.*
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    private  lateinit var client:Mqtt3AsyncClient;
    @RequiresApi(Build.VERSION_CODES.N)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        client = MqttClient.builder()
                .useMqttVersion3()
                .identifier("app")
                .serverHost("d751b986666147cc9c2407d44621abe7.s1.eu.hivemq.cloud")
                .serverPort(8883)
                .sslWithDefaultConfig()
                .buildAsync()


        client.connectWith()
                .simpleAuth()
                .username("timboiu.razvan@at")
                .password("5CeqjvM#G+".toByteArray())
                .applySimpleAuth()
                .send()

        setupActivity()
    }


    @RequiresApi(Build.VERSION_CODES.N)
    private fun setupActivity() {
        sendMessage.setOnClickListener {
            client.publishWith()
                    .topic("morse")
                    .payload(messageTxt.text.toString().toByteArray())
                    .send()
        }
    }
}