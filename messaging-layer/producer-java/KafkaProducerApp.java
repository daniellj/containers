import org.apache.kafka.clients.producer.*;
import java.text.*;
import java.util.*;

public class KafkaProducerApp {

    public static void main(String[] args){

        /* instantiate a java.util.Properties class to store input parameters */
        Properties props = new Properties();

        /* hostname where brokers are running: kafka */
        /* obrigatory parameters to start Kafka Producer */
        props.put("bootstrap.servers", "127.0.0.1:9092, 127.0.0.1:9093, 127.0.0.1:9094");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        /* optional parameters to start Kafka Producer */
        props.put("acks", "1");
        props.put("buffer.memory", 33554432);
        props.put("compression.type", "none");
        props.put("retries", 0);
        props.put("batch.size", 16384);
        props.put("client.id", "");
        props.put("linger.ms", 0);
        props.put("max.block.ms", 60000);
        props.put("max.request.size", 1048576);
        props.put("partitioner.class", "org.apache.kafka.clients.producer.internals.DefaultPartitioner");
        props.put("request.timeout.ms", 30000);
        props.put("max.in.flight.requests.per.connection", 5);
        props.put("retry.backoff.ms", 5);

        /* instantiate the Kafka Producer class (org.apache.kafka.clients.producer.Producer.KafkaProducer constructor), passing the input serialized parameters stored in 'props' */
        KafkaProducer<String, String> myProducer = new KafkaProducer<String, String>(props);

        /* instantiate the java.text.DateFormat class (SimpleDateFormat constructor) */
        DateFormat dtFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss:SSS");
        String topic = "topic01";

        /* number of messages to send */
        int numberOfRecords = 2000;

        /* sleep time to waiting before to send the next message */
        long sleepTimer = 0;

        try {
            for (int i = 0; i < numberOfRecords; i++)
                myProducer.send(new ProducerRecord<String, String>(topic, String.format("Mensagem de Teste: %s  enviada em %s", Integer.toString(i), dtFormat.format(new Date()))));
                Thread.sleep(sleepTimer);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            //myProducer.close();
        }
    }
}