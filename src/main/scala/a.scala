// run with sbt ~compile run

// code creates new sub to topic called: example
// count how much a word is shown on the topic

import java.util.Properties
import java.util.concurrent.TimeUnit
import org.apache.kafka.streams.kstream.Materialized
import org.apache.kafka.streams.scala.ImplicitConversions._
import org.apache.kafka.streams.scala._
import org.apache.kafka.streams.scala.kstream._
import org.apache.kafka.streams.{KafkaStreams, StreamsConfig}

object WordCountApplication extends App {
  import Serdes._

  val random = new scala.util.Random()
  val randomString = random.alphanumeric.take(10).mkString

  val props: Properties = {
    val p = new Properties()
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, randomString)
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092")
    p
  }

  val builder: StreamsBuilder = new StreamsBuilder
  val textLines: KStream[String, String] = builder.stream[String, String]("example")
  val wordCounts: KTable[String, Long] = textLines
    .flatMapValues(textLine => textLine.toLowerCase.split("\\W+"))
    .groupBy((_, word) => word)
    .count()(Materialized.as("counts-store"))
  
  val wordCountsAsKStream: KStream[String, Long] = wordCounts.toStream

  def printWordCount(word: String, count: Long): Unit = {
    println(s"Word: $word, Count: $count")
  }

  wordCountsAsKStream.foreach(printWordCount)

  val streams: KafkaStreams = new KafkaStreams(builder.build(), props)
  streams.start()

  sys.ShutdownHookThread {
    streams.close(1, TimeUnit.SECONDS)
    println("closed stream")
  }
}