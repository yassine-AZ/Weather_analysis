package kafkaCom

import org.apache.spark.sql
import org.apache.spark.sql.{Encoders, SparkSession}
import org.apache.spark.sql.functions.{col, from_json}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._

class Consumer() {

  var df: sql.DataFrame = _

  val schema = new StructType()
    .add("city", StringType, false)
    .add("temperature", FloatType, false)
    .add("humidity", FloatType, false)
    .add("currentTime", TimestampType, false)
    .add("lon", DoubleType, false)
    .add("lat", DoubleType, false)


  val spark = SparkSession
    .builder
    .appName("sparkConsumer")
    .config("spark.master", "local")
    .getOrCreate()

  spark.sparkContext.setLogLevel("ERROR")
  import spark.implicits._
  def loadKafka(topic:String): Unit ={
    df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("auto.offset.reset", "latest")
      .option("value.deserializer", "StringDeserializer")
      .option("subscribe", topic)
      .load()
      .select(from_json(col("value").cast("string"), schema).alias("parsed_value"))
      .select(col("parsed_value.*"))

      df.printSchema()

  }

  def writeData(): Unit ={
    //val initial = df.selectExpr("CAST(value AS STRING)").toDF("value")



    df.writeStream
      .format("csv")
      .trigger(Trigger.ProcessingTime("60 seconds"))
      .option("timestampFormat", "yyyy-MM-dd hh:mm:ss.SSSSSSS")
      .option("checkpointLocation", "hdfs://localhost:9000/weatherProject/checkpoint")
      .option("path", "hdfs://localhost:9000/weatherProject/data")
      .outputMode("append")
      .start()
      .awaitTermination()
  }

}
