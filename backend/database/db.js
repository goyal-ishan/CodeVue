const dns=require('dns');
dns.setServers(['1.1.1.1', '8.8.8.8']);


const mongoose=require('mongoose');

const connectToDb=async()=>{
    try{
       await mongoose.connect(process.env.MONGOURI);
       console.log('MongoDB connected successfully');
    }catch(e)
    {
        console.log('mongoDB connection failed!',e);
    }
}