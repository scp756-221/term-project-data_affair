package proj756

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object Utility {
  /*
    Utility to get an Int from an environment variable.
    Return defInt if the environment var does not exist
    or cannot be converted to a string.
  */
  def envVarToInt(ev: String, defInt: Int): Int = {
    try {
      sys.env(ev).toInt
    } catch {
      case e: Exception => defInt
    }
  }

  /*
    Utility to get an environment variable.
    Return defStr if the environment var does not exist.
  */
  def envVar(ev: String, defStr: String): String = {
    sys.env.getOrElse(ev, defStr)
  }
}

object RMusic {

  val feeder = csv("music.csv").eager.random

  val rmusic = forever("i") {
    feed(feeder)
    .exec(http("RMusic ${i}")
      .get("/api/v1/music/${UUID}"))
      .pause(1)
  }

}

object RUser {

  val feeder = csv("users.csv").eager.circular

  val ruser = forever("i") {
    feed(feeder)
    .exec(http("RUser ${i}")
      .get("/api/v1/user/${UUID}"))
    .pause(1)
  }

}

object PurchaseCoverage {
  val feeder = csv("purchases.csv").eager.circular
  val rpurchases = {
    feed(feeder)
    .exec(http("Write purchase")
      .post("/api/v1/purchase")
      .header("Content-Type" , "application/json")
      .body(StringBody(string = """{
        "user_id": "${user_id}",
        "music_id": "${music_id}",
        "purchase_amount": "${purchase_amount}"}
        """ ))
      .check(status.is(200))
      .check(jsonPath("$..purchase_id").ofType[String].saveAs("purchase_id")))
    .pause(1)
    .exec(http("Read purchase")
      .get("/api/v1/purchase/${purchase_id}")
      .check(status.is(200))
      .check(jsonPath("$..user_id").is("${user_id}")))
    .pause(1)
    .exec(http("Update purchase")
      .put("/api/v1/purchase")
      .header("Content-Type", "application/json")
      .body(StringBody(string = """
          "purchase_id": "${purchase_id}",
          "user_id": "${user_id}",
          "music_id": "${music_id}",
          "purchase_amount": "100"}
      """))
      .check(status.is(200)))
    .pause(1)
    .exec(http("Get Purchase by user")
      .get("/api/v1/purchase/byuser/${user_id}")
      .check(status.is(200)))
    .pause(1)
    .exec(http("Delete purchase")
      .delete("/api/v1/purchase/${purchase_id}")
      .check(status.is(200)))
    .pause(1)
  }
}

object UserFlowLoad {
  val feeder = csv("load.csv").eager.circular
  val ruserflow = {
    feed(feeder)
    .exec(http("Write Music")
      .post("/api/v1/music")
      .header("Content-Type" , "application/json")
      .body(StringBody(string = """{
          "Artist": "${Artist}",
          "SongTitle": "${SongTitle}"
        }""" ))
      .check(status.is(200))
      .check(jsonPath("$..music_id").ofType[String].saveAs("music_id")))
    .pause(1)
    .exec(http("Write User")
      .post("/api/v1/user")
      .header("Content-Type" , "application/json")
      .body(StringBody(string = """{
          "fname": "${fname}",
          "lname": "${lname}",
          "email": "${email}"
        }""" ))
      .check(status.is(200))
      .check(jsonPath("$..user_id").ofType[String].saveAs("user_id")))
    .pause(1)
    .exec(http("Read music")
      .get("/api/v1/music/${music_id}")
      .check(status.is(200))
      .check(jsonPath("$..SongTitle").is("${SongTitle}")))
    .pause(1)
    .exec(http("User Login to Purchase")
      .put("/api/v1/user/login")
      .header("Content-Type", "application/json")
      .body(StringBody(string = """{
          "uid": "${user_id}"
      }"""))
      .check(status.is(200)))
    .pause(1)
    .exec(http("Read user")
      .get("/api/v1/user/${user_id}")
      .check(status.is(200))
      .check(jsonPath("$..email").is("${email}")))
    .pause(1)
    .exec(http("Write purchase")
      .post("/api/v1/purchase")
      .header("Content-Type" , "application/json")
      .body(StringBody(string = """{
          "user_id": "${user_id}",
          "music_id": "${music_id}",
          "purchase_amount": "${purchase_amount}"}
        """ ))
      .check(status.is(200))
      .check(jsonPath("$..purchase_id").ofType[String].saveAs("purchase_id")))
    .pause(1)
    .exec(http("Read purchase")
      .get("/api/v1/purchase/${purchase_id}")
      .check(status.is(200))
      .check(jsonPath("$..user_id").is("${user_id}")))
    .pause(1)
    .exec(http("Get purchase by user")
      .get("/api/v1/purchase/byuser/${user_id}")
      .check(status.is(200)))
    .pause(1)
  }
}

/*
  After one S1 read, pause a random time between 1 and 60 s
*/
object RUserVarying {
  val feeder = csv("users.csv").eager.circular

  val ruser = forever("i") {
    feed(feeder)
    .exec(http("RUserVarying ${i}")
      .get("/api/v1/user/${UUID}"))
    .pause(1, 60)
  }
}

/*
  After one S2 read, pause a random time between 1 and 60 s
*/

object RMusicVarying {
  val feeder = csv("music.csv").eager.circular

  val rmusic = forever("i") {
    feed(feeder)
    .exec(http("RMusicVarying ${i}")
      .get("/api/v1/music/${UUID}"))
    .pause(1, 60)
  }
}

/*
  Failed attempt to interleave reads from User and Music tables.
  The Gatling EDSL only honours the second (Music) read,
  ignoring the first read of User. [Shrug-emoji] 
 */
object RBoth {

  val u_feeder = csv("users.csv").eager.circular
  val m_feeder = csv("music.csv").eager.random

  val rboth = forever("i") {
    feed(u_feeder)
    .exec(http("RUser ${i}")
      .get("/api/v1/user/${UUID}"))
    .pause(1);

    feed(m_feeder)
    .exec(http("RMusic ${i}")
      .get("/api/v1/music/${UUID}"))
      .pause(1)
  }

}

// Get Cluster IP from CLUSTER_IP environment variable or default to 127.0.0.1 (Minikube)
class ReadTablesSim extends Simulation {
  val httpProtocol = http
    .baseUrl("http://" + Utility.envVar("CLUSTER_IP", "127.0.0.1") + "/")
    .acceptHeader("application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    .authorizationHeader("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZGJmYmMxYzAtMDc4My00ZWQ3LTlkNzgtMDhhYTRhMGNkYTAyIiwidGltZSI6MTYwNzM2NTU0NC42NzIwNTIxfQ.zL4i58j62q8mGUo5a0SQ7MHfukBUel8yl8jGT5XmBPo")
    .acceptLanguageHeader("en-US,en;q=0.5")
}

class PurchaseCoverageClosedSim extends ReadTablesSim {
  val scnPurchase = scenario("Purchases Coverage")
      .exec(PurchaseCoverage.rpurchases)
    
  setUp(
    scnPurchase.inject(constantConcurrentUsers(Utility.envVarToInt("USERS", 1)).during(15.minutes))
  ).protocols(httpProtocol)
}

class PurchaseCoverageOpenSim extends ReadTablesSim {
  val scnPurchase = scenario("Purchases Coverage")
      .exec(PurchaseCoverage.rpurchases)
    
  setUp(
    scnPurchase.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class UserRampFlowClosedSim extends ReadTablesSim {
  val scnUserFlow = scenario("User Flow")
      .exec(UserFlowLoad.ruserflow)
  val users = Utility.envVarToInt("USERS", 1)
  setUp(
    scnUserFlow.inject(rampConcurrentUsers(1).to(users).during(10 * users))
  ).protocols(httpProtocol)
}

class UserConcurrentFlowClosedSim extends ReadTablesSim {
  val scnUserFlow = scenario("User Flow")
      .exec(UserFlowLoad.ruserflow)
  val users = Utility.envVarToInt("USERS", 1)
  setUp(
    scnUserFlow.inject(constantConcurrentUsers(users).during(15.minutes))
  ).protocols(httpProtocol)
}

class UserFlowOpenSim extends ReadTablesSim {
  val scnUserFlow = scenario("User Flow")
      .exec(UserFlowLoad.ruserflow)
    
  setUp(
    scnUserFlow.inject(constantUsersPerSec(Utility.envVarToInt("USERS", 1)).during(15.minutes))
  ).protocols(httpProtocol)
}

class ReadUserSim extends ReadTablesSim {
  val scnReadUser = scenario("ReadUser")
      .exec(RUser.ruser)

  setUp(
    scnReadUser.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

class ReadMusicSim extends ReadTablesSim {
  val scnReadMusic = scenario("ReadMusic")
    .exec(RMusic.rmusic)

  setUp(
    scnReadMusic.inject(atOnceUsers(Utility.envVarToInt("USERS", 1)))
  ).protocols(httpProtocol)
}

/*
  Read both services concurrently at varying rates.
  Ramp up new users one / 10 s until requested USERS
  is reached for each service.
*/
class ReadBothVaryingSim extends ReadTablesSim {
  val scnReadMV = scenario("ReadMusicVarying")
    .exec(RMusicVarying.rmusic)

  val scnReadUV = scenario("ReadUserVarying")
    .exec(RUserVarying.ruser)

  val users = Utility.envVarToInt("USERS", 10)

  setUp(
    // Add one user per 10 s up to specified value
    scnReadMV.inject(rampConcurrentUsers(1).to(users).during(10*users)),
    scnReadUV.inject(rampConcurrentUsers(1).to(users).during(10*users))
  ).protocols(httpProtocol)
}

/*
  This doesn't work---it just reads the Music table.
  We left it in here as possible inspiration for other work
  (or a warning that this approach will fail).
 */
/*
class ReadBothSim extends ReadTablesSim {
  val scnReadBoth = scenario("ReadBoth")
    .exec(RBoth.rboth)

  setUp(
    scnReadBoth.inject(atOnceUsers(1))
  ).protocols(httpProtocol)
}
*/
