package sample

import kafkaCom.Consumer

object Main {
  def main(args: Array[String]) = {
    println("Hello, world")
    val consumer = new Consumer()
    consumer.loadKafka("weather")
    consumer.writeData()
    println("Bye, world")


  }
}
