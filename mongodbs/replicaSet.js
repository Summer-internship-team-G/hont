config = {
    _id: "replication",
    members: [
      { _id: 0, host: "mongodb:27017" },
      { _id: 1, host: "mongo2:27017" },
      { _id: 2, host: "mongo3:27017" }
    ],
  }
  
  rs.initiate(config)
  
  rs.conf()