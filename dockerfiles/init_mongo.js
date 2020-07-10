db.createUser(
    {
        user: "mysensors",
        pwd: "pwd",
        roles:[
            {
                role: "readWrite",
                db: "mysensors_db"
            }
        ]
    }
)