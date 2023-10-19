const mongoose = require('mongoose')

const connectDb = async()=>{
    try{
        const connect = await mongoose.connect(process.env.CONNECTION_STRING)
        console.log(
            "DB COnnected : ",
        connect.connection.host,
        connect.connection.name)
    }
    catch{
        console.log(err)
        process.exit(1)
    }
}

module.exports =  connectDb